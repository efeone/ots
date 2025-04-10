// Copyright (c) 2025, efeone and contributors
// For license information, please see license.txt
frappe.query_reports["VAT Output Report - Sales"] = {
    tree: true,
    name_field: "value",
    initial_depth: 1,

    filters: [
        {
            fieldname: "tax_category",
            label: "Tax Category",
            fieldtype: "Link",
            options: "Tax Category",
            reqd: 0
        }
    ]
};
