# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-01-27

### Added

#### Swiss QR-Bill Generation
- Complete Swiss QR-Bill generator for ERPNext Sales Invoices
- Automatic QR-Bill generation compliant with Swiss Payment Standards
- QR-IBAN and Creditor Reference (SCOR) support
- Structured and unstructured reference handling

#### Sales Invoice Integration
- Seamless integration with ERPNext Sales Invoice DocType
- Automatic QR reference generation on submit
- Validation hooks for Swiss-specific requirements
- Custom fields for Swiss banking information (IBAN, QR-IBAN, BC Number)

#### QR Code Generation
- High-quality QR code generation with error correction
- Swiss Cross embedding in QR code center
- Compliant with Swiss Payment Standards 2.3
- Automatic encoding of payment information

#### Print Format Support
- Ready-to-use QR-Bill print format
- A4 and perforated payment slip layouts
- Customizable CSS styling
- Multi-language support (German, French, Italian, English)

#### Validation System
- IBAN format validation (Swiss and international)
- QR-IBAN specific validation
- Creditor Reference (SCOR) check digit verification
- Amount and currency validation
- Customer address completeness checks

### Features

- ✅ Automatic QR reference generation with SCOR algorithm
- ✅ Support for structured and unstructured messages
- ✅ Customer and company address parsing
- ✅ Multi-currency support (CHF, EUR)
- ✅ Automatic Swiss formatting (amounts, addresses)
- ✅ Print-ready QR-Bill with payment slip section
- ✅ Configurable via custom fields (no code changes needed)
- ✅ Compatible with Swiss banking systems
- ✅ Zero external dependencies

### Custom Fields

Added to Sales Invoice:
- `custom_qr_iban`: QR-IBAN for QR-Bill payments
- `custom_creditor_reference`: Structured reference number
- `custom_unstructured_message`: Additional payment information
- `custom_qr_reference`: Auto-generated QR reference number

Added to Company:
- `custom_bc_number`: Bank Clearing (BC) number
- `custom_company_iban`: Company IBAN for payments

Added to Customer:
- `custom_customer_iban`: Customer IBAN (if applicable)

### Developer Experience
- Modular architecture: generator, validator, utils, overrides
- Clean separation of concerns
- Well-documented code with docstrings
- Jinja template integration for print formats
- Hook-based validation and generation

### Compliance
- Compliant with Swiss Payment Standards 2.3
- ISO 11649 Creditor Reference (SCOR) implementation
- ISO 20022 payment message format
- Swiss QR Code specifications
- Swiss address format requirements

[1.0.0]: https://github.com/Solede-SA/solede_qrbill/releases/tag/v1.0.0
