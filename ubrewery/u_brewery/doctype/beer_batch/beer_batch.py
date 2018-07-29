# -*- coding: utf-8 -*-
# Copyright (c) 2018, Guillaume Libersat and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

from datetime import date, timedelta

class BeerBatch(Document):
    def on_submit(self):
        # Make a Stock Entry
        ste_doc = frappe.get_doc({
                "doctype": "Stock Entry",
                "purpose": "Manufacture",
                "title": "Condition {0}".format(self.beer_recipe)
        })

        # Make batches for Item Variants
        for quantity in self.quantities:
                item_variant = frappe.get_doc("Item", quantity.variant_item)
                variant_value = item_variant.attributes[0].attribute_value # FIXME, shoudln't be [0]. We get "75cl" for example

                # If quantity is zero, skip the variant
                if quantity.quantity == 0:
                        continue

                # Create a batch no for this variant
                batch_doc = frappe.get_doc({
                        "doctype": "Batch",
                        "batch_id": "{0}-{1}".format(self.batch_no,
                                                     variant_value),
                        "item": item_variant.item_code,
                        "expiry_date": date.today() + timedelta(days=365) # FIXME: should be configurable
                })

                batch_doc.insert()


                ste_doc.append('items', {
                        "item_code": item_variant.item_code,
                        "batch_no": batch_doc.batch_id,
                        "qty": quantity.quantity,
                        "t_warehouse": "Produits Finis - SI" # FIXME
                })


        ste_doc.insert()
        ste_doc.submit()
