# Copyright (c) 2025, efeone and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
    columns = [
        {"label": "Sales Invoice", "fieldname": "invoice_no", "fieldtype": "Link", "options": "Sales Invoice", "width": 230},
        {"label": "Date", "fieldname": "posting_date", "fieldtype": "Date", "width": 150},
        {"label": "Invoice Amount (Excluding VAT)", "fieldname": "total", "fieldtype": "Currency", "width": 250},
        {"label": "VAT Amount", "fieldname": "vat_amount", "fieldtype": "Currency", "width": 150},
        {"label": "Total Invoice Amount", "fieldname": "grand_total", "fieldtype": "Currency", "width": 180},
        {"label": "VAT %", "fieldname": "vat_percent", "fieldtype": "Float", "width": 100},
    ]

    data = []

    invoice_filters = {"docstatus": 1}

    if filters:
        if filters.get("tax_category"):
            invoice_filters["tax_category"] = filters["tax_category"]

        if filters.get("sales_invoice"):
            invoice_filters["name"] = filters["sales_invoice"]

        if filters.get("from_date") and filters.get("to_date"):
            invoice_filters["posting_date"] = ["between", [filters["from_date"], filters["to_date"]]]
        elif filters.get("from_date"):
            invoice_filters["posting_date"] = [">=", filters["from_date"]]
        elif filters.get("to_date"):
            invoice_filters["posting_date"] = ["<=", filters["to_date"]]

    invoices = frappe.get_all(
        "Sales Invoice",
        filters=invoice_filters,
        fields=["name", "posting_date", "total", "grand_total"]
    )

    for inv in invoices:
        tax_percent = 0
        vat_amount = 0

        taxes = frappe.get_all(
            "Sales Taxes and Charges",
            filters={"parent": inv.name},
            fields=["rate", "tax_amount"]
        )

        for tax in taxes:
            vat_amount += tax.tax_amount
            tax_percent = tax.rate

        data.append({
            "invoice_no": inv.name,
            "posting_date": inv.posting_date,
            "total": inv.total,
            "vat_amount": vat_amount,
            "grand_total": inv.grand_total,
            "vat_percent": tax_percent
        })

    return columns, data
