# Contributing to Solede QR-Bill

Grazie per il tuo interesse nel contribuire a Solede QR-Bill! 🎉

## 📋 Indice

- [Codice di Condotta](#codice-di-condotta)
- [Come Contribuire](#come-contribuire)
- [Setup Ambiente di Sviluppo](#setup-ambiente-di-sviluppo)
- [Convenzioni di Codice](#convenzioni-di-codice)
- [Testing](#testing)
- [Commit Convention](#commit-convention)
- [Pull Request Process](#pull-request-process)

## Codice di Condotta

Questo progetto segue il [Contributor Covenant Code of Conduct](https://www.contributor-covenant.org/). Partecipando, ti aspettiamo che tu rispetti questo codice.

## Come Contribuire

Ci sono molti modi per contribuire:

- 🐛 Segnalare bug
- 💡 Proporre nuove funzionalità
- 📝 Migliorare la documentazione
- 🔧 Fixare bug
- ✨ Implementare nuove feature
- 🧪 Scrivere test
- 🌍 Migliorare traduzioni (DE, FR, IT, EN)

## Setup Ambiente di Sviluppo

### Prerequisiti

- Frappe Framework v15+
- ERPNext v15+
- Python 3.10+
- Node.js 18+

### Installazione

1. **Fork del repository**
   ```bash
   cd frappe-bench/apps
   git clone https://github.com/TUO-USERNAME/solede_qrbill.git
   cd solede_qrbill
   ```

2. **Installa l'app**
   ```bash
   bench --site your-site.local install-app solede_qrbill
   ```

3. **Crea branch per la tua feature**
   ```bash
   git checkout -b feature/nome-feature
   ```

4. **Setup pre-commit hooks** (opzionale ma consigliato)
   ```bash
   pre-commit install
   ```

## Convenzioni di Codice

### Python

- Seguire **PEP 8**
- Usare **type hints** quando possibile
- Docstring in formato Google style
- Principio **DRY** (Don't Repeat Yourself)
- Principio **KISS** (Keep It Simple, Stupid)
- **NO fallback**: mostrare sempre errori all'utente

```python
def validate_iban(iban: str) -> bool:
    """Valida un IBAN svizzero o internazionale.

    Args:
        iban: IBAN da validare (formato CH XX XXXXX XXXXXXXXXXXX)

    Returns:
        True se valido, False altrimenti

    Raises:
        frappe.ValidationError: Se formato non valido
    """
    if not iban or len(iban) < 15:
        frappe.throw("IBAN format not valid")

    # Validation logic
    return True
```

### JavaScript

- Usare ES6+ syntax
- Arrow functions quando possibile
- Nomi variabili descrittivi

```javascript
function generateQRBill(frm) {
    frappe.call({
        method: "solede_qrbill.qrbill.generator.generate_qr_bill",
        args: { invoice_name: frm.doc.name },
        callback: (r) => {
            if (r.message) {
                frm.set_value("custom_qr_reference", r.message.qr_reference);
                frm.refresh();
            }
        }
    });
}
```

## Testing

### Scrivere Test

Tutti i nuovi features devono includere test:

```python
# solede_qrbill/tests/test_qr_generator.py
import frappe
from frappe.tests.utils import FrappeTestCase
from solede_qrbill.qrbill.generator import generate_qr_reference

class TestQRGenerator(FrappeTestCase):
    def test_qr_reference_generation(self):
        """Test generazione QR reference con algoritmo SCOR"""
        invoice_no = "INV-2025-0001"

        qr_ref = generate_qr_reference(invoice_no)

        self.assertTrue(qr_ref.isdigit())
        self.assertEqual(len(qr_ref), 27)  # Swiss QR reference format
```

### Eseguire Test

```bash
# Tutti i test
bench --site your-site.local run-tests --app solede_qrbill

# Test specifico
bench --site your-site.local run-tests --app solede_qrbill --module test_qr_generator
```

## Commit Convention

Usa [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- `feat`: Nuova funzionalità
- `fix`: Bug fix
- `docs`: Modifiche documentazione
- `style`: Formattazione (no logic changes)
- `refactor`: Refactoring codice
- `test`: Aggiunta/modifica test
- `chore`: Maintenance tasks

### Scope Suggeriti

- `qr-generator`: Generazione QR code e reference
- `validator`: Validazione IBAN, reference, amounts
- `print`: Print format e layout
- `integration`: Integrazione con Sales Invoice
- `docs`: Documentazione

### Esempi

```bash
feat(qr-generator): add support for EUR currency

- Implement EUR amount formatting
- Add validation for EUR transactions
- Update QR code generation for multi-currency

Closes #42

fix(validator): resolve IBAN validation for Liechtenstein

The IBAN validation was failing for LI (Liechtenstein)
IBANs due to incorrect country code handling.

Fixes #38

docs(readme): update Swiss Payment Standards reference

- Update to Payment Standards 2.3
- Add link to SIX specifications
- Include QR-IBAN format examples
```

## Pull Request Process

1. **Update Documentation**
   - Aggiorna README.md se necessario
   - Aggiungi entry in CHANGELOG.md
   - Commenta il codice complesso

2. **Test Your Changes**
   ```bash
   bench --site your-site.local migrate
   bench restart
   ```

3. **Commit Changes**
   ```bash
   git add .
   git commit -m "feat(scope): description"
   ```

4. **Push to Fork**
   ```bash
   git push origin feature/nome-feature
   ```

5. **Create Pull Request**
   - Vai su GitHub
   - Clicca "New Pull Request"
   - Compila il template:
     - Descrizione chiara delle modifiche
     - Link alle issue correlate
     - Screenshots se UI changes
     - Checklist completata

6. **Code Review**
   - Rispondi ai commenti
   - Fai le modifiche richieste
   - Push aggiornamenti (stesso branch)

## Segnalazione Bug

### Template Bug Report

```markdown
**Descrizione Bug**
Descrizione chiara del problema.

**Come Riprodurre**
1. Vai a '...'
2. Clicca su '...'
3. Vedi errore

**Comportamento Atteso**
Cosa ti aspettavi che succedesse.

**Screenshots**
Se applicabile, aggiungi screenshots.

**Ambiente:**
- Frappe Version: [es. v15.10.0]
- ERPNext Version: [es. v15.8.0]
- App Version: [es. v1.0.0]
- Python: [es. 3.10.12]

**Log di Errore**
```
Paste error log here
```

**QR-Bill Example** (se applicabile)
- IBAN utilizzato
- Importo
- Valuta
```

## Richiesta Feature

### Template Feature Request

```markdown
**La tua feature risolve un problema?**
Descrizione chiara del problema.

**Descrivi la soluzione che vorresti**
Cosa vorresti che succedesse.

**Use Case**
Scenario d'uso concreto.

**Conformità Swiss Payment Standards**
Se la feature riguarda aspetti normativi, fornisci riferimenti a:
- Swiss Payment Standards specifications
- SIX Group documentation
- ISO 20022 standards

**Contesto Aggiuntivo**
Screenshots, mockup, esempi QR-Bill.
```

## Risorse Utili

### Swiss Payment Standards
- [SIX Payment Standards](https://www.six-group.com/en/products-services/banking-services/payment-standardization.html)
- [Swiss QR-Bill Specifications](https://www.paymentstandards.ch/en/home/software-partner.html)
- [ISO 11649 Creditor Reference](https://www.iso.org/standard/50649.html)

### ERPNext Development
- [Frappe Framework Documentation](https://frappeframework.com/docs)
- [ERPNext Developer Guide](https://docs.erpnext.com/docs/user/en/developer)

## Licenza

Contribuendo a questo progetto, accetti che i tuoi contributi saranno rilasciati sotto la licenza **GNU Affero General Public License v3.0**.

Tutti i file devono includere l'header copyright:

```python
# Copyright (c) 2024-2025, Solede SA and contributors
# For license information, please see license.txt
# License: GNU Affero General Public License v3 or later (AGPLv3+)
# See https://www.gnu.org/licenses/agpl-3.0.html
```

## Domande?

- 💬 Apri una [Discussion su GitHub](https://github.com/Solede-SA/solede_qrbill/discussions)
- 📧 Email: info@solede.com
- 🐛 Segnala bug: [GitHub Issues](https://github.com/Solede-SA/solede_qrbill/issues)

## Grazie! 🙏

Ogni contributo, grande o piccolo, è apprezzato e aiuta a migliorare questo progetto per tutta la community ERPNext svizzera!

---

Made with ❤️ by Solede SA and contributors
