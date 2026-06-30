// Copyright (c) 2024, Solede SA and contributors
// Client-side script for Sales Invoice QR-Bill functionality

frappe.ui.form.on('Sales Invoice', {
    refresh: function(frm) {
        // Su refresh aggiorna solo la visibilita': NON impostare/azzerare valori
        // (set_value sporcherebbe il form -> "Not Saved" all'apertura di una bozza).
        toggle_qr_fields_visibility_and_set_defaults(frm, false);

        // Add QR-Bill preview button if bank account is selected
        if (frm.doc.custom_qr_bank_account && frm.doc.company_address && frm.doc.customer_address) {
            frm.add_custom_button(__('Preview QR-Bill'), function() {
                preview_qr_bill(frm);
            }, __('Actions'));
        }

        // Set bank account filter
        set_bank_account_filter(frm);
    },
    
    customer_address: function(frm) {
        // Check visibility when customer address changes
        toggle_qr_fields_visibility_and_set_defaults(frm, true);
    },

    company_address: function(frm) {
        // Check visibility when company address changes
        toggle_qr_fields_visibility_and_set_defaults(frm, true);
    },

    company: function(frm) {
        // Clear bank account when company changes
        frm.set_value('custom_qr_bank_account', '');
        set_bank_account_filter(frm);
        toggle_qr_fields_visibility_and_set_defaults(frm, true);
    },

    customer: function(frm) {
        // Check visibility and set defaults when customer changes
        toggle_qr_fields_visibility_and_set_defaults(frm, true);
    },
    
    custom_qr_bank_account: function(frm) {
        // Validate selected bank account
        if (frm.doc.custom_qr_bank_account) {
            validate_qr_bank_account(frm);
        }
    }
});

function set_bank_account_filter(frm) {
    // Filter bank accounts to show only QR-IBAN enabled accounts for the selected company
    frm.set_query('custom_qr_bank_account', function() {
        return {
            filters: {
                'company': frm.doc.company,
                'custom_is_qr_iban': 1,
                'disabled': 0
            }
        };
    });
}

function validate_qr_bank_account(frm) {
    // Check if both company and customer have Swiss addresses
    if (!frm.doc.company_address || !frm.doc.customer_address) {
        return;
    }
    
    frappe.call({
        method: 'frappe.client.get_value',
        args: {
            doctype: 'Address',
            filters: { name: frm.doc.company_address },
            fieldname: 'country'
        },
        callback: function(r) {
            if (r.message && r.message.country !== 'Switzerland') {
                frappe.msgprint({
                    title: __('QR-Bill Notice'),
                    message: __('Company address is not in Switzerland. QR-Bill will not be generated.'),
                    indicator: 'orange'
                });
            }
        }
    });
}

function preview_qr_bill(frm) {
    // Save current state if document is new
    if (frm.is_new()) {
        frappe.call({
            method: 'frappe.desk.form.save.savedocs',
            args: {
                doc: frm.doc,
                action: 'Save'
            },
            callback: function(r) {
                if (!r.exc) {
                    frm.reload_doc();
                    // Generate preview after save
                    generate_preview(frm);
                }
            }
        });
    } else {
        // Generate preview directly for existing documents
        generate_preview(frm);
    }
}

function generate_preview(frm) {
    // Preview QR-Bill in a dialog
    frappe.call({
        method: 'solede_qrbill.qrbill.generator.generate_qr_bill_svg',
        args: {
            sales_invoice_name: frm.doc.name
        },
        callback: function(r) {
            if (r.message) {
                let d = new frappe.ui.Dialog({
                    title: __('QR-Bill Preview'),
                    size: 'extra-large'
                });
                
                d.$body.html(`
                    <div style="background: white; padding: 20px; overflow: auto;">
                        <style>
                            .qr-bill-preview {
                                width: 210mm;
                                height: 105mm;
                                border: 1px solid #ccc;
                                margin: 0 auto;
                                display: block;
                                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                            }
                            @media screen and (max-width: 800mm) {
                                .qr-bill-preview {
                                    transform: scale(0.8);
                                    transform-origin: top center;
                                }
                            }
                        </style>
                        <div class="qr-bill-preview">
                            ${r.message}
                        </div>
                        <div style="text-align: center; margin-top: 20px; color: #666;">
                            <small>${__('This is a preview. The actual QR-Bill will be generated when printing the invoice.')}</small>
                        </div>
                    </div>
                `);
                
                d.show();
            } else {
                frappe.msgprint(__('QR-Bill cannot be generated for this invoice. Please check that both company and customer have Swiss addresses.'));
            }
        }
    });
}

function toggle_qr_fields_visibility(frm) {
    // Show/hide QR fields based on customer address country
    if (!frm.doc.customer_address || !frm.doc.company_address) {
        // Hide fields if no addresses selected
        frm.set_df_property('custom_qr_bank_account', 'hidden', 1);
        frm.set_df_property('custom_qr_additional_info', 'hidden', 1);
        return;
    }

    // Check both company and customer addresses
    Promise.all([
        frappe.db.get_value('Address', frm.doc.customer_address, 'country'),
        frappe.db.get_value('Address', frm.doc.company_address, 'country')
    ]).then(results => {
        const customer_country = results[0].message.country;
        const company_country = results[1].message.country;

        // Show fields only if both are Swiss addresses
        const show_qr_fields = customer_country === 'Switzerland' && company_country === 'Switzerland';

        frm.set_df_property('custom_qr_bank_account', 'hidden', !show_qr_fields);
        frm.set_df_property('custom_qr_additional_info', 'hidden', !show_qr_fields);

        // Clear values if hiding fields
        if (!show_qr_fields && (frm.doc.custom_qr_bank_account || frm.doc.custom_qr_additional_info)) {
            frm.set_value('custom_qr_bank_account', '');
            frm.set_value('custom_qr_additional_info', '');
        }

        // Refresh field area to apply changes
        frm.refresh_field('custom_qr_bank_account');
        frm.refresh_field('custom_qr_additional_info');
    });
}

function toggle_qr_fields_visibility_and_set_defaults(frm, allow_set) {
    // Show/hide QR fields based on customer address country
    if (!frm.doc.customer_address || !frm.doc.company_address) {
        // Hide fields if no addresses selected
        frm.set_df_property('custom_qr_bank_account', 'hidden', 1);
        frm.set_df_property('custom_qr_additional_info', 'hidden', 1);
        return;
    }

    // Check both company and customer addresses
    Promise.all([
        frappe.db.get_value('Address', frm.doc.customer_address, 'country'),
        frappe.db.get_value('Address', frm.doc.company_address, 'country')
    ]).then(results => {
        const customer_country = results[0].message.country;
        const company_country = results[1].message.country;

        // Show fields only if both are Swiss addresses
        const show_qr_fields = customer_country === 'Switzerland' && company_country === 'Switzerland';

        frm.set_df_property('custom_qr_bank_account', 'hidden', !show_qr_fields);
        frm.set_df_property('custom_qr_additional_info', 'hidden', !show_qr_fields);

        // Imposta/azzera i valori solo se richiesto (cambio campo dell'utente) o su doc nuovo;
        // mai sul refresh di un doc gia' salvato, altrimenti il form diventa "Not Saved".
        const may_set = allow_set || frm.is_new();
        if (show_qr_fields) {
            // Set default QR bank account if not already set and both addresses are Swiss
            if (may_set && !frm.doc.custom_qr_bank_account && frm.doc.customer && frm.doc.company) {
                set_default_qr_bank_account(frm);
            }
        } else {
            // Clear values if hiding fields
            if (may_set && (frm.doc.custom_qr_bank_account || frm.doc.custom_qr_additional_info)) {
                frm.set_value('custom_qr_bank_account', '');
                frm.set_value('custom_qr_additional_info', '');
            }
        }

        // Refresh field area to apply changes
        frm.refresh_field('custom_qr_bank_account');
        frm.refresh_field('custom_qr_additional_info');
    });
}

function set_default_qr_bank_account(frm) {
    // Set default QR Bank Account with priority: Customer > Company > First Available

    // Priority 1: Check customer default
    frappe.db.get_value('Customer', frm.doc.customer, 'custom_default_qr_bank_account').then(r => {
        if (r.message && r.message.custom_default_qr_bank_account) {
            // Validate that the account belongs to the current company and is QR-enabled
            validate_and_set_bank_account(frm, r.message.custom_default_qr_bank_account);
        } else {
            // Priority 2: Check company default
            frappe.db.get_value('Company', frm.doc.company, 'custom_default_qr_bank_account').then(r => {
                if (r.message && r.message.custom_default_qr_bank_account) {
                    validate_and_set_bank_account(frm, r.message.custom_default_qr_bank_account);
                } else {
                    // Priority 3: Get first available QR bank account
                    frappe.call({
                        method: 'frappe.client.get_list',
                        args: {
                            doctype: 'Bank Account',
                            filters: {
                                'company': frm.doc.company,
                                'custom_is_qr_iban': 1,
                                'disabled': 0
                            },
                            fields: ['name'],
                            limit: 1
                        },
                        callback: function(r) {
                            if (r.message && r.message.length > 0) {
                                frm.set_value('custom_qr_bank_account', r.message[0].name);
                            }
                        }
                    });
                }
            });
        }
    });
}

function validate_and_set_bank_account(frm, bank_account) {
    // Validate that the bank account is valid for this company and is QR-enabled
    frappe.db.get_value('Bank Account', bank_account, ['company', 'custom_is_qr_iban', 'disabled']).then(r => {
        if (r.message &&
            r.message.company === frm.doc.company &&
            r.message.custom_is_qr_iban === 1 &&
            r.message.disabled === 0) {
            frm.set_value('custom_qr_bank_account', bank_account);
        }
    });
}