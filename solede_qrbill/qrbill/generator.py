# Copyright (c) 2024, Solede SA and contributors
# For license information, please see license.txt

import io

import frappe
from frappe import _
from qrbill import QRBill

from .utils import generate_qr_reference, get_language_from_customer, qr_address
from .validator import is_qr_iban, validate_qr_reference, validate_swiss_iban


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

	try:
		return render_qr_bill_svg(qr_data)
	except Exception as e:
		frappe.log_error(
			f"Error generating QR-Bill for {sales_invoice_name}: {e!s}", "QR-Bill Generation Error"
		)
		frappe.throw(_("Error generating QR-Bill: {0}").format(str(e)))


def render_qr_bill_svg(qr_data):
	"""SVG del bollettino (210×106 mm) dai dati già preparati (conto, creditore, importo, valuta,
	debitore, riferimento, informazioni aggiuntive, lingua): la sola resa, senza documento, così chi
	genera una QR-fattura fuori da una Sales Invoice (es. BookFit per le istruzioni del bonifico)
	riusa questo punto."""
	out = io.StringIO()
	QRBill(**qr_data).as_svg(out)
	return out.getvalue()


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

	# Skip QR-Bill for credit notes (return invoices) - negative amounts not supported
	if doc.get("is_return"):
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

	# Prepare QR-Bill data (creditor and debtor: Swiss addresses, `is_qr_bill_applicable` guarantees it)
	qr_data = {
		"account": iban.replace(" ", ""),
		"creditor": qr_address(
			company.company_name, company_address.address_line1, company_address.pincode, company_address.city, "CH"
		),
		"amount": f"{doc.rounded_total or doc.grand_total:.2f}",
		"currency": doc.currency,
	}

	# The QRR reference is allowed only with a QR-IBAN (identifier 30000-31999); a normal IBAN
	# cannot carry it (SCOR or no reference)
	if is_qr_iban(iban) and doc.custom_qr_reference:
		qr_data["reference_number"] = doc.custom_qr_reference

	# Add debtor data if available (long names are wrapped by the library itself)
	if customer and customer_address:
		qr_data["debtor"] = qr_address(
			customer.customer_name,
			customer_address.address_line1,
			customer_address.pincode,
			customer_address.city,
			"CH",
		)

	# Add additional information if available
	if doc.get("custom_qr_additional_info"):
		qr_data["additional_information"] = doc.custom_qr_additional_info[:140]  # Max 140 chars

	# Add language preference from customer
	qr_data["language"] = get_language_from_customer(doc.customer)

	return qr_data
