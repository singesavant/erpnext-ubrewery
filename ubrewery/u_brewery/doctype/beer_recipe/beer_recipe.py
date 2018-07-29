# -*- coding: utf-8 -*-
# Copyright (c) 2018, Guillaume Libersat and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document


class BeerRecipe(Document):
    def before_insert(self):
            variant_name = "Conditionnement"
            default_unit = "Unité" # fixme
            item_group = "Produits" # fixme

            item_attribute_variant_doc = frappe.get_doc('Item Attribute', variant_name)

            # Create Beer Template
            beer_doc_template = frappe.get_doc({
                    "doctype": "Item",
                    "item_name": self.recipe_name,
                    "item_code": self.recipe_name,
                    "item_group": item_group, # fixme
                    "status": "Open",
                    "stock_uom": default_unit, # fixme
                    "default_material_request_type": "Manufacture",
                    "is_stock_item": 0,
                    "has_batch_no": False,
                    "has_expiry_date": False,
                    "has_variants": True,
                    "variant_based_on": "Item Attribute",
                    "attributes": [{"attribute": variant_name}], # fixme
                    "is_purchase_item": False,
                    "is_sales_item": False,
                    "publish_in_hub": False
            })

            beer_doc_template.insert()

            # Set beer template as the one we've just created
            self.item_template = beer_doc_template.item_code

            # Make Beer variants
            for attribute_value in item_attribute_variant_doc.item_attribute_values:
                    beer_variant_doc = frappe.get_doc({
                            "doctype": "Item",
                            "variant_of": beer_doc_template.item_code,
                            "item_group": item_group, # fixme
                            "item_code": "{0}-{1}".format(beer_doc_template.item_code, attribute_value.abbr),
                            "stock_uom": default_unit, # fixme,
                            "default_material_request_type": "Manufacture",
                            "is_stock_item": 1,
                            "has_batch_no" : True,
                            "has_expiry_date": True,
                            "status": "Open",
                            "attributes": [{"attribute": variant_name, "attribute_value": attribute_value.attribute_value}],
                            "is_purchase_item": False,
                            "is_sales_item": True,
                            "publish_in_hub": False
                    })

                    beer_variant_doc.insert()



