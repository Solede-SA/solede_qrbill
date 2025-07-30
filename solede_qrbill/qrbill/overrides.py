# Copyright (c) 2024, Solede SA and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from .generator import is_qr_bill_applicable
from .utils import generate_qr_reference
from .validator import validate_swiss_iban
from .utils import validate_currency


def validate_swiss_qr_bill(doc, method):
	"""
	Validate Sales Invoice for Swiss QR-Bill requirements
	
	Args:
		doc: Sales Invoice document
		method: Event method name
	"""
	if not is_qr_bill_applicable(doc):
		return
	
	# Validate currency
	if not validate_currency(doc.currency):
		frappe.throw(_("QR-Bill only supports CHF or EUR currency"))
	
	# Validate bank account
	if doc.get("custom_qr_bank_account"):
		bank_account = frappe.get_doc("Bank Account", doc.custom_qr_bank_account)
		
		# Check if it's marked as QR-IBAN
		if not bank_account.get("custom_is_qr_iban"):
			frappe.throw(_("Selected bank account {0} is not configured as QR-IBAN").format(bank_account.name))
		
		# Validate IBAN
		iban = bank_account.iban or bank_account.bank_account_no
		if not validate_swiss_iban(iban):
			frappe.throw(_("Bank account {0} does not have a valid Swiss IBAN").format(bank_account.name))
	
	# Validate addresses
	if not doc.company_address:
		frappe.throw(_("Company address is required for QR-Bill"))
	
	if not doc.customer_address:
		frappe.throw(_("Customer address is required for QR-Bill"))
	
	# Check if addresses are Swiss
	company_country = frappe.db.get_value("Address", doc.company_address, "country")
	customer_country = frappe.db.get_value("Address", doc.customer_address, "country")
	
	if company_country != "Switzerland":
		frappe.throw(_("Company address must be in Switzerland for QR-Bill"))
	
	if customer_country != "Switzerland":
		frappe.throw(_("Customer address must be in Switzerland for QR-Bill"))


def generate_qr_reference_on_submit(doc, method):
	"""
	Generate QR reference when Sales Invoice is submitted
	
	Args:
		doc: Sales Invoice document
		method: Event method name
	"""
	if not is_qr_bill_applicable(doc):
		return
	
	# Generate reference if not already present
	if not doc.get("custom_qr_reference"):
		doc.custom_qr_reference = generate_qr_reference(doc.name)
		doc.db_set("custom_qr_reference", doc.custom_qr_reference)