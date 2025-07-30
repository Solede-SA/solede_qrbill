# Copyright (c) 2024, Solede SA and contributors
# For license information, please see license.txt

import re
import frappe
from frappe import _
from .validator import calculate_mod10_recursive


def generate_qr_reference(invoice_number):
	"""
	Generate QR reference from invoice number
	
	Args:
		invoice_number: Sales Invoice name/number
		
	Returns:
		str: 27-digit QR reference with check digit
	"""
	# Extract only digits from invoice number
	digits_only = re.sub(r'[^0-9]', '', invoice_number)
	
	# If no digits, use a timestamp-based approach
	if not digits_only:
		import time
		digits_only = str(int(time.time() * 1000))[-10:]
	
	# Pad with zeros to make it 26 digits
	base_ref = digits_only.ljust(26, '0')[:26]
	
	# Calculate check digit
	check_digit = calculate_mod10_recursive(base_ref)
	
	# Return complete reference
	return f"{base_ref}{check_digit}"


def format_qr_reference(reference):
	"""
	Format QR reference with spaces for readability
	
	Args:
		reference: 27-digit reference
		
	Returns:
		str: Formatted reference (e.g., "21 00000 00003 13947 14300 09017")
	"""
	if not reference or len(reference) != 27:
		return reference
	
	# Format as: 2 5 5 5 5 5
	parts = [
		reference[0:2],
		reference[2:7],
		reference[7:12],
		reference[12:17],
		reference[17:22],
		reference[22:27]
	]
	
	return " ".join(parts)


def get_language_from_customer(customer_name):
	"""
	Get language preference from customer
	
	Args:
		customer_name: Customer document name
		
	Returns:
		str: Language code (de, fr, it, en)
	"""
	# Try to get language from customer
	language = frappe.db.get_value("Customer", customer_name, "language")
	
	if language:
		# Map Frappe language codes to QR-Bill language codes
		language_map = {
			"de": "de",
			"de-CH": "de",
			"fr": "fr",
			"fr-CH": "fr",
			"it": "it",
			"it-CH": "it",
			"en": "en",
			"en-US": "en",
			"en-GB": "en"
		}
		return language_map.get(language, "en")
	
	# Default to system language or English
	system_language = frappe.db.get_single_value("System Settings", "language")
	if system_language and system_language.startswith(("de", "fr", "it")):
		return system_language[:2]
	
	return "en"


def format_amount(amount):
	"""
	Format amount for QR-Bill (no thousand separators, 2 decimal places)
	
	Args:
		amount: Amount to format
		
	Returns:
		str: Formatted amount
	"""
	try:
		amount_float = float(amount)
		return "{:.2f}".format(amount_float)
	except (ValueError, TypeError):
		return "0.00"


def get_qr_bill_html(doc):
	"""
	Jinja filter to get QR-Bill HTML for a document
	
	Args:
		doc: Document (usually Sales Invoice)
		
	Returns:
		str: HTML containing the QR-Bill or empty string
	"""
	from .generator import generate_qr_bill_svg, is_qr_bill_applicable
	
	if not is_qr_bill_applicable(doc):
		return ""
	
	try:
		svg_content = generate_qr_bill_svg(doc.name)
		if not svg_content:
			return ""
		
		# Wrap SVG in HTML container with proper styling
		html = f"""
		<div class="qr-bill-container">
			<div class="qr-bill-scissors">
				<span style="position: absolute; top: -10px; left: -20px; font-size: 20px;">✂</span>
			</div>
			<div class="qr-bill-content">
				{svg_content}
			</div>
		</div>
		"""
		
		return html
		
	except Exception as e:
		frappe.log_error(f"Error generating QR-Bill HTML: {str(e)}", "QR-Bill Error")
		return ""


def validate_currency(currency):
	"""
	Validate if currency is supported for QR-Bill
	
	Args:
		currency: Currency code
		
	Returns:
		bool: True if supported
	"""
	return currency in ["CHF", "EUR"]


def clean_text_for_qr(text, max_length=70):
	"""
	Clean and truncate text for QR-Bill fields
	
	Args:
		text: Text to clean
		max_length: Maximum length (default 70)
		
	Returns:
		str: Cleaned and truncated text
	"""
	if not text:
		return ""
	
	# Remove special characters that might cause issues
	# Keep only alphanumeric, spaces, and basic punctuation
	cleaned = re.sub(r'[^\w\s\-.,/]', '', str(text))
	
	# Remove extra spaces
	cleaned = " ".join(cleaned.split())
	
	# Truncate to max length
	return cleaned[:max_length]