# -*- coding: utf-8 -*-
# Copyright (c) 2018, Guillaume Libersat and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

from datetime import date, timedelta

class BeerBatch(Document):
    def on_submit(self):
            # Make Beer variants
            for quantity in self.quantities:
                    item_variant = frappe.get_doc("Item", quantity.variant_item)
                    variant_value = item_variant.attributes[0].attribute_value # FIXME, shoudln't be [0]

                    batch_doc = frappe.get_doc({
                            "doctype": "Batch",
                            "batch_id": "{0}-{1}".format(self.batch_no,
                                                         variant_value),
                            "item": item_variant.item_code,
                            "expiry_date": date.today() + timedelta(days=365)
                    })

                    batch_doc.insert()
