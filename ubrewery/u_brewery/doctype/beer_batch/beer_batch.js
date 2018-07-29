// Copyright (c) 2018, Guillaume Libersat and contributors
// For license information, please see license.txt


function update_variants_table(frm, item_template_code) {
    frappe.call({
        method: "frappe.client.get_list",
        args: {
            doctype: "Item",
            filters: {'variant_of': item_template_code},
            fields: ["item_code"]
        },
        callback: function (r) {
            var attribute_values = [];

            if (r.message) {
			          $.each(r.message, function(i, variant_item) {
                    attribute_values.push({"variant_item": variant_item.item_code, "quantity": 0});
                });
            }

            frm.set_value("quantities", attribute_values);
        }
	  });
};


frappe.ui.form.on('Beer Batch', {
	  beer_recipe: function(frm) {
        var item_code = frm.fields_dict['beer_recipe'].value;

        if (item_code) {
            frappe.call({
                method: "frappe.client.get_value",
                args: {
                    fieldname: "item_template",
                    doctype: "Beer Recipe",
                    filters: {'recipe_name': item_code}
                },
                callback: function (r) {
                    if (r.message.item_template) {
                        update_variants_table(frm, r.message.item_template);
                    } else {
                        frm.set_value("quantities", []);
                    }
                }
            });
        }
    },
});
