# # Copyright (c) 2025, efeone and contributors
# # For license information, please see license.txt

import frappe

def execute(filters=None):
    data = []

    # Initialize grand totals
    grand_total_invoice_amount = 0
    grand_total_vat = 0
    grand_total_grand_total = 0

    # Get the selected tax category filter
    tax_category_filter = filters.get("tax_category") if filters else None

    # Get tax categories
    tax_categories = (
        [{"tax_category": tax_category_filter}]
        if tax_category_filter
        else frappe.db.get_all(
            "Sales Invoice",
            filters={"docstatus": 1},
            fields=["distinct tax_category"],
            order_by="tax_category"
        )
    )

    for tax in tax_categories:
        tax_category = tax.get("tax_category")

        # Link to Tax Category (clickable to open the detailed report)
        report_link = f"<a href='/app/query-report/Detailed VAT Output Report - Sales?tax_category={tax_category}' target='_blank'>{tax_category}</a>" if tax_category else "No Tax Category"

        # Invoice filters
        invoice_filters = {"docstatus": 1}
        if tax_category:
            invoice_filters["tax_category"] = tax_category
        else:
            invoice_filters["tax_category"] = ["in", ["", None]]

        invoices = frappe.db.get_all(
            "Sales Invoice",
            filters=invoice_filters,
            fields=["name", "total", "total_taxes_and_charges", "grand_total"]
        )

        # Totals for this category
        total_invoice_amount = 0
        total_vat = 0
        total_grand_total = 0

        for inv in invoices:
            total_invoice_amount += inv.total
            total_vat += inv.total_taxes_and_charges
            total_grand_total += inv.grand_total

            invoice_link = f"<a href='{frappe.utils.get_url_to_form('Sales Invoice', inv.name)}' target='_blank'>{inv.name}</a>"

            data.append({
                "value": invoice_link,
                "invoice_amount": inv.total,
                "vat_amount": inv.total_taxes_and_charges,
                "total_invoice_amount": inv.grand_total,
                "indent": 1
            })

        if invoices:
            # Add category header
            data.insert(len(data) - len(invoices), {
                "value": report_link,
                "invoice_amount": total_invoice_amount,
                "vat_amount": total_vat,
                "total_invoice_amount": total_grand_total,
                "is_group": 1,
                "indent": 0
            })

            # Update grand totals
            grand_total_invoice_amount += total_invoice_amount
            grand_total_vat += total_vat
            grand_total_grand_total += total_grand_total

    # Grand total row
    if data:
        data.append({
            "value": "<b>Grand Total</b>",
            "invoice_amount": grand_total_invoice_amount,
            "vat_amount": grand_total_vat,
            "total_invoice_amount": grand_total_grand_total,
            "indent": 0
        })

    columns = [
        {"label": " ", "fieldname": "value", "fieldtype": "HTML", "width": 300},
        {"label": "Invoice Amount (Excluding VAT)", "fieldname": "invoice_amount", "fieldtype": "Currency", "width": 250},
        {"label": "VAT Amount", "fieldname": "vat_amount", "fieldtype": "Currency", "width": 200},
        {"label": "Total Invoice Amount", "fieldname": "total_invoice_amount", "fieldtype": "Currency", "width": 250},
    ]

    return columns, data
