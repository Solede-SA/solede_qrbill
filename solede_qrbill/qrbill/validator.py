# Copyright (c) 2024, Solede SA and contributors
# For license information, please see license.txt

import re
from frappe import _


def validate_swiss_iban(iban):
	"""
	Validate Swiss IBAN format and checksum
	
	Args:
		iban: IBAN string to validate
		
	Returns:
		bool: True if valid Swiss IBAN
	"""
	if not iban:
		return False
	
	# Remove spaces and convert to uppercase
	iban = iban.replace(" ", "").upper()
	
	# Check if it's a Swiss or Liechtenstein IBAN
	if not (iban.startswith("CH") or iban.startswith("LI")):
		return False
	
	# Check length (21 characters for CH/LI)
	if len(iban) != 21:
		return False
	
	# Validate IBAN checksum
	# Move first 4 chars to end
	rearranged = iban[4:] + iban[:4]
	
	# Convert letters to numbers (A=10, B=11, etc.)
	numeric_iban = ""
	for char in rearranged:
		if char.isdigit():
			numeric_iban += char
		else:
			numeric_iban += str(ord(char) - ord('A') + 10)
	
	# Check if mod 97 equals 1
	return int(numeric_iban) % 97 == 1


def is_qr_iban(iban):
	"""
	Check if IBAN is a QR-IBAN
	
	Args:
		iban: IBAN string to check
		
	Returns:
		bool: True if QR-IBAN
	"""
	if not iban:
		return False
	
	# Remove spaces
	iban_clean = iban.replace(" ", "").upper()
	
	# Check basic Swiss IBAN validity first
	if not validate_swiss_iban(iban):
		return False
	
	# QR-IBAN identification: positions 5-9 should be between 30000-31999
	if len(iban_clean) >= 9:
		qr_iban_identifier = iban_clean[4:9]
		try:
			identifier_num = int(qr_iban_identifier)
			return 30000 <= identifier_num <= 31999
		except ValueError:
			return False
	
	return False


def validate_qr_reference(reference):
	"""
	Validate QR reference (27 digits with valid check digit)
	
	Args:
		reference: QR reference string
		
	Returns:
		bool: True if valid QR reference
	"""
	if not reference:
		return False
	
	# Remove spaces
	reference = reference.replace(" ", "")
	
	# Check if it's exactly 27 digits
	if not re.match(r'^\d{27}$', reference):
		return False
	
	# Validate check digit (last digit)
	check_digit = calculate_mod10_recursive(reference[:-1])
	return reference[-1] == str(check_digit)


def calculate_mod10_recursive(ref):
	"""
	Calculate mod 10 recursive check digit
	
	Args:
		ref: Reference string without check digit
		
	Returns:
		int: Check digit (0-9)
	"""
	table = [0, 9, 4, 6, 8, 2, 7, 1, 3, 5]
	carry = 0
	
	for char in ref:
		carry = table[(carry + int(char)) % 10]
	
	return (10 - carry) % 10


def validate_amount(amount):
	"""
	Validate amount for QR-Bill
	
	Args:
		amount: Amount to validate
		
	Returns:
		bool: True if valid amount
	"""
	try:
		amount_float = float(amount)
		# Amount must be positive
		if amount_float <= 0:
			return False
		# Max 2 decimal places
		if round(amount_float, 2) != amount_float:
			return False
		# Max amount is 999999999.99
		if amount_float > 999999999.99:
			return False
		return True
	except (ValueError, TypeError):
		return False


def validate_swiss_address(address_doc):
	"""
	Validate if address is suitable for Swiss QR-Bill
	
	Args:
		address_doc: Address document
		
	Returns:
		tuple: (is_valid, error_message)
	"""
	errors = []
	
	# Check country
	if address_doc.country not in ["Switzerland", "Liechtenstein"]:
		errors.append(_("Country must be Switzerland or Liechtenstein"))
	
	# Check postal code (4 digits for Switzerland)
	if not address_doc.pincode:
		errors.append(_("Postal code is required"))
	elif not re.match(r'^\d{4}$', str(address_doc.pincode)):
		errors.append(_("Postal code must be 4 digits"))
	
	# Check city
	if not address_doc.city:
		errors.append(_("City is required"))
	
	# Check address line
	if not address_doc.address_line1:
		errors.append(_("Street address is required"))
	
	is_valid = len(errors) == 0
	error_message = ", ".join(errors) if errors else None
	
	return is_valid, error_message


def validate_text_length(text, max_length, field_name):
	"""
	Validate text length for QR-Bill fields
	
	Args:
		text: Text to validate
		max_length: Maximum allowed length
		field_name: Name of the field for error message
		
	Returns:
		tuple: (is_valid, error_message)
	"""
	if not text:
		return True, None
	
	if len(text) > max_length:
		return False, _("{0} exceeds maximum length of {1} characters").format(field_name, max_length)
	
	return True, None