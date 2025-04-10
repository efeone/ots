// Copyright (c) 2025, efeone and contributors
// For license information, please see license.txt

frappe.query_reports["Detailed VAT Output Report - Sales"] = {
    filters: [
        {
            fieldname: "tax_category",
            label: "Tax Category",
            fieldtype: "Link",
            options: "Tax Category",
            reqd: 0
        },
				{
            fieldname: "from_date",
            label: "From Date",
            fieldtype: "Date",
            default: frappe.datetime.add_months(frappe.datetime.get_today(), -1),
            reqd: 0
        },
        {
            fieldname: "to_date",
            label: "To Date",
            fieldtype: "Date",
            default: frappe.datetime.get_today(),
            reqd: 0
        },
        {
            fieldname: "sales_invoice",
            label: "Sales Invoice",
            fieldtype: "Link",
            options: "Sales Invoice"
        }
    ]
};
