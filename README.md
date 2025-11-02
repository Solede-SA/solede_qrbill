# Solede QR-Bill

[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
[![Frappe](https://img.shields.io/badge/Frappe-v15+-blue.svg)](https://frappeframework.com)
[![ERPNext](https://img.shields.io/badge/ERPNext-v15+-green.svg)](https://erpnext.com)

Swiss QR-Bill generator for ERPNext Sales Invoices. Automatically generates compliant QR-Bills for Swiss companies and customers according to Swiss Payment Standards 2.3.

## 💡 Caratteristiche

- ✅ Complete Swiss QR-Bill generation for Sales Invoices
- ✅ Automatic QR reference generation with SCOR algorithm
- ✅ QR-IBAN and standard IBAN support
- ✅ Structured and unstructured message handling
- ✅ Swiss Cross embedding in QR code
- ✅ Print-ready payment slip format (A4 and perforated)
- ✅ Multi-language support (DE, FR, IT, EN)
- ✅ IBAN and QR-IBAN validation
- ✅ Multi-currency support (CHF, EUR)
- ✅ Zero external dependencies

## 📦 Installazione

```bash
# Ottieni l'app da GitHub
bench get-app https://github.com/Solede-SA/solede_qrbill.git

# Installa nel sito
bench --site [nome-sito] install-app solede_qrbill

# Applica modifiche
bench --site [nome-sito] migrate
```

**Requisiti**: Frappe v15+, ERPNext v15+, Python 3.10+

## 🔧 Configurazione

### 1. Setup Company

Vai in **Company** → Seleziona la tua azienda e compila:

- **IBAN**: IBAN aziendale per ricevere pagamenti
- **QR-IBAN**: QR-IBAN specifico (se disponibile)
- **BC Number**: Bank Clearing number (numero di clearing bancario)

### 2. Configura Sales Invoice

I campi QR-Bill sono disponibili automaticamente in Sales Invoice:

- **QR IBAN**: IBAN per questo specifico pagamento
- **Creditor Reference**: Riferimento strutturato (opzionale, auto-generato)
- **Unstructured Message**: Messaggio aggiuntivo per il cliente
- **QR Reference**: Auto-generato al submit della fattura

## 🚀 Utilizzo

### Generazione Automatica

1. Crea una **Sales Invoice** normalmente in ERPNext
2. Compila i dati standard (Customer, Items, etc.)
3. **Submit** la fattura
4. Il sistema genera automaticamente:
   - QR reference number (formato SCOR)
   - QR code con Swiss Cross
   - Payment slip pronto per la stampa

### Print Format

Il QR-Bill viene aggiunto automaticamente al print format della Sales Invoice:

1. Apri una Sales Invoice submitted
2. Clicca **Print**
3. Seleziona il print format con QR-Bill
4. Stampa o scarica PDF

### Personalizzazione

Puoi personalizzare il QR-Bill modificando:

- **QR-IBAN** per fattura specifica
- **Unstructured Message** per note al cliente
- **Amount** (automatico dal totale fattura)
- **Currency** (CHF o EUR)

## 📊 Struttura QR-Bill

Il QR-Bill generato include:

### Sezione Pagamento
- **Importo**: Totale fattura in CHF/EUR
- **Valuta**: CHF o EUR
- **Scadenza**: Due date della fattura
- **Debitore**: Dati cliente (nome, indirizzo)
- **Creditore**: Dati azienda (nome, indirizzo, IBAN)

### QR Code
- **QR Reference**: Numero riferimento SCOR (27 cifre)
- **IBAN/QR-IBAN**: Codice bancario
- **Swiss Cross**: Logo centrale per autenticità
- **Formato**: Swiss Payment Standards 2.3 compliant

### Sezione Ricevuta
- Informazioni pagamento duplicate
- Sezione perforabile per distacco
- Layout conforme standard svizzero

## 🔍 Validazione

Il sistema valida automaticamente:

### IBAN Validation
- ✅ Formato IBAN svizzero (CH)
- ✅ Check digit verification
- ✅ Lunghezza corretta (21 caratteri)
- ✅ QR-IBAN specific validation (30000-31999)

### Reference Validation
- ✅ SCOR algorithm check digit
- ✅ Formato ISO 11649
- ✅ Lunghezza reference (max 27 caratteri)

### Amount Validation
- ✅ Currency support (CHF, EUR)
- ✅ Amount formatting svizzero
- ✅ Max 2 decimal places

### Address Validation
- ✅ Swiss address format
- ✅ Postal code format (4 digits)
- ✅ Required fields completeness

## 🛠️ Architettura

```
solede_qrbill/
├── solede_qrbill/
│   ├── qrbill/
│   │   ├── generator.py      # QR code e reference generation
│   │   ├── validator.py      # IBAN e reference validation
│   │   ├── utils.py          # Helper functions
│   │   └── overrides.py      # Sales Invoice hooks
│   │
│   ├── public/
│   │   ├── css/
│   │   │   └── qr_bill_print.css  # Print format styling
│   │   └── js/
│   │       └── sales_invoice.js   # UI enhancements
│   │
│   └── templates/            # Jinja templates for QR-Bill
│
└── README.md
```

## 📝 Custom Fields

### Sales Invoice
- `custom_qr_iban`: QR-IBAN per questo pagamento
- `custom_creditor_reference`: Riferimento strutturato SCOR
- `custom_unstructured_message`: Messaggio cliente
- `custom_qr_reference`: QR reference auto-generato (read-only)

### Company
- `custom_bc_number`: Bank Clearing number
- `custom_company_iban`: IBAN aziendale

### Customer
- `custom_customer_iban`: IBAN cliente (se applicabile)

## 🐛 Troubleshooting

### Errori Comuni

**"QR-IBAN format not valid"**
- Verifica che il QR-IBAN inizi con "CH" e abbia 21 caratteri
- Il BC number deve essere tra 30000-31999 per QR-IBAN
- Usa validator online: https://www.iban.com/

**"QR reference not generated"**
- Verifica che la fattura sia in stato "Submitted"
- Controlla che invoice_number sia compilato
- Verifica log: `logs/[sito]/error.log`

**"QR code non stampato"**
- Verifica che custom CSS sia caricato
- Controlla print format settings
- Prova a rigenerare il print

### Debug Mode

```bash
# Abilita developer mode
bench --site [sito] set-config developer_mode 1
bench --site [sito] clear-cache
bench restart

# Test generazione QR reference
bench --site [sito] console
>>> from solede_qrbill.qrbill.generator import generate_qr_reference
>>> generate_qr_reference("INV-2025-0001")
```

## 🤝 Contribuire

Contribuzioni benvenute! Leggi [CONTRIBUTING.md](CONTRIBUTING.md) per:

- Setup ambiente di sviluppo
- Convenzioni di codice (PEP 8, type hints)
- Testing guidelines
- Commit conventions
- Riferimenti Swiss Payment Standards

### Quick Start

```bash
# Fork e clone
git clone https://github.com/[your-username]/solede_qrbill.git
cd solede_qrbill

# Setup pre-commit
pre-commit install

# Crea branch
git checkout -b feature/AmazingFeature

# Commit e PR
git commit -m "feat(qr-generator): description"
git push origin feature/AmazingFeature
```

## 📚 Risorse

- [Swiss Payment Standards](https://www.paymentstandards.ch/)
- [SIX Group Documentation](https://www.six-group.com/en/products-services/banking-services/payment-standardization.html)
- [ISO 11649 Standard](https://www.iso.org/standard/50649.html)
- [ERPNext Documentation](https://docs.erpnext.com)
- [Frappe Framework](https://frappeframework.com)

## 📄 License

GNU Affero General Public License v3.0 - vedi [LICENSE](LICENSE)

Copyright (C) 2024-2025 Solede SA and contributors

Puoi usare, modificare e distribuire liberamente. Se offri come servizio web/SaaS, DEVI condividere il codice sorgente modificato.

---

**Sviluppato da Solede SA** | [GitHub Issues](https://github.com/Solede-SA/solede_qrbill/issues) | info@solede.com
