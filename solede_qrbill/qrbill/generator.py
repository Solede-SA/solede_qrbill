# Copyright (c) 2024, Solede SA and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from qrbill import QRBill
from .validator import validate_swiss_iban, validate_qr_reference
from .utils import generate_qr_reference


@frappe.whitelist()
def generate_qr_bill_svg(sales_invoice_name):
	"""
	Generate QR-Bill SVG for a Sales Invoice
	
	Args:
		sales_invoice_name: Name of the Sales Invoice document
		
	Returns:
		str: SVG content of the QR-Bill or None if not applicable
	"""
	doc = frappe.get_doc("Sales Invoice", sales_invoice_name)
	
	# Check if QR-Bill is applicable
	if not is_qr_bill_applicable(doc):
		return None
	
	# Prepare data for QR-Bill
	qr_data = prepare_qr_bill_data(doc)
	
	# Generate QR-Bill
	try:
		bill = QRBill(**qr_data)
		
		# Generate SVG to a temporary file or string
		import tempfile
		import os
		
		# Create temporary file
		with tempfile.NamedTemporaryFile(mode='w', suffix='.svg', delete=False) as tmp_file:
			temp_path = tmp_file.name
		
		try:
			# Generate SVG to file
			bill.as_svg(temp_path)
			
			# Read SVG content
			with open(temp_path, 'r') as f:
				svg_content = f.read()
			
			return svg_content
		finally:
			# Clean up temporary file
			if os.path.exists(temp_path):
				os.remove(temp_path)
				
	except Exception as e:
		frappe.log_error(f"Error generating QR-Bill for {sales_invoice_name}: {str(e)}", "QR-Bill Generation Error")
		frappe.throw(_("Error generating QR-Bill: {0}").format(str(e)))


def is_qr_bill_applicable(doc):
	"""
	Check if QR-Bill should be generated for this document
	
	Args:
		doc: Sales Invoice document
		
	Returns:
		bool: True if QR-Bill should be generated
	"""
	if doc.doctype != "Sales Invoice":
		return False
	
	# Check if invoice has a QR bank account selected
	if not doc.get("custom_qr_bank_account"):
		return False
	
	# Check if the bank account is marked as QR-IBAN
	is_qr_iban = frappe.db.get_value("Bank Account", doc.custom_qr_bank_account, "custom_is_qr_iban")
	if not is_qr_iban:
		return False
	
	# Check if both company and customer addresses are Swiss
	if not doc.company_address or not doc.customer_address:
		return False
	
	company_country = frappe.db.get_value("Address", doc.company_address, "country")
	customer_country = frappe.db.get_value("Address", doc.customer_address, "country")
	
	return company_country == "Switzerland" and customer_country == "Switzerland"


def prepare_qr_bill_data(doc):
	"""
	Prepare data for QR-Bill generation
	
	Args:
		doc: Sales Invoice document
		
	Returns:
		dict: Data formatted for QRBill library
	"""
	company = frappe.get_doc("Company", doc.company)
	customer = frappe.get_doc("Customer", doc.customer)
	bank_account = frappe.get_doc("Bank Account", doc.custom_qr_bank_account)
	company_address = frappe.get_doc("Address", doc.company_address)
	customer_address = frappe.get_doc("Address", doc.customer_address)
	
	# Get IBAN from bank account
	# Use QR-IBAN if available, otherwise fallback to normal IBAN
	iban = bank_account.get("custom_qr_iban") or bank_account.iban or bank_account.bank_account_no
	
	# Validate IBAN
	if not validate_swiss_iban(iban):
		frappe.throw(_("Invalid Swiss IBAN for bank account {0}").format(bank_account.name))
	
	# Generate or get QR reference
	if not doc.get("custom_qr_reference"):
		doc.custom_qr_reference = generate_qr_reference(doc.name)
		doc.db_set("custom_qr_reference", doc.custom_qr_reference)
	
	# Validate reference
	if not validate_qr_reference(doc.custom_qr_reference):
		frappe.throw(_("Invalid QR reference"))
	
	# Prepare creditor data
	creditor_data = {
		"name": company.company_name[:70],  # Max 70 chars
		"pcode": str(company_address.pincode),
		"city": company_address.city,
		"country": "CH"
	}
	
	# Add street if available
	if company_address.address_line1:
		creditor_data["street"] = company_address.address_line1[:70]
	
	# Prepare QR-Bill data
	qr_data = {
		"account": iban.replace(" ", ""),
		"creditor": creditor_data,
		"amount": "{:.2f}".format(doc.grand_total),
		"currency": doc.currency
	}
	
	# Add reference only if we have a valid QR-IBAN
	# QR-IBAN identification: positions 5-9 should be between 30000-31999
	iban_clean = iban.replace(" ", "")
	if len(iban_clean) >= 9:
		qr_iban_identifier = iban_clean[4:9]
		try:
			identifier_num = int(qr_iban_identifier)
			# Check if it's a QR-IBAN (30000-31999 range)
			if 30000 <= identifier_num <= 31999:
				# It's a QR-IBAN, we can use QRR reference
				if doc.custom_qr_reference:
					qr_data["reference_number"] = doc.custom_qr_reference
			else:
				# It's a normal IBAN, we cannot use QRR reference
				# We could use SCOR reference or no reference
				pass
		except ValueError:
			# Not a valid number, treat as normal IBAN
			pass
	
	# Add debtor data if available
	if customer and customer_address:
		debtor_data = {
			"name": customer.customer_name[:70],  # Max 70 chars
			"pcode": str(customer_address.pincode),
			"city": customer_address.city,
			"country": "CH"
		}
		
		# Add street if available
		if customer_address.address_line1:
			debtor_data["street"] = customer_address.address_line1[:70]
		
		qr_data["debtor"] = debtor_data
	
	# Add additional information if available
	if doc.get("custom_qr_additional_info"):
		qr_data["additional_information"] = doc.custom_qr_additional_info[:140]  # Max 140 chars
	
	return qr_data