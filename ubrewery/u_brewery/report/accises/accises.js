// Copyright (c) 2016, Guillaume Libersat and contributors
// For license information, please see license.txt



frappe.query_reports["Accises"] = {
	  "filters": [

        {
			      "fieldname":"from_date",
			      "label": __("From Date"),
			      "fieldtype": "Date",
			      "default": frappe.defaults.get_default("year_start_date"),
			      "width": "80"
		    },
		    {
			      "fieldname":"to_date",
			      "label": __("To Date"),
			      "fieldtype": "Date"
		    },
		    {
			      "fieldname":"company",
			      "label": __("Company"),
			      "fieldtype": "Link",
			      "options": "Company",
			      "default": frappe.defaults.get_user_default("Company")
		    },
	]
}
