# Copyright (c) 2013, Guillaume Libersat and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import flt, cint, getdate
from frappe.exceptions import DataError

from collections import defaultdict

from erpnext.stock.get_item_details import (
        get_conversion_factor,
        get_basic_details
)

def get_conditions(filters, table=None):
        conditions = ""

        if table:
                table += "."
        else:
                table = ""

        if not filters.get("from_date") or not filters.get("to_date"):
		        frappe.throw(_("'From and To Date' are required"))
        else:
                conditions = "{table}posting_date >= '{from_date}' and {table}posting_date <= '{to_date}' ".format(table=table,
                                                                                                                   from_date=filters['from_date'],
                                                                                                                   to_date=filters["to_date"])
        return conditions

def get_stock_from_warehouse(filters, scrap=False):
        item_stocks = frappe.db.sql("""
            select sle.item_code item_code, sle.actual_qty qty
            FROM `tabStock Ledger Entry` sle, `tabWarehouse` warehouse
            WHERE sle.docstatus = 1
            AND sle.warehouse = warehouse.name
            AND warehouse.is_scrap={scrap}
            AND {conditions}
        """.format(scrap=scrap, conditions=get_conditions(filters, table="sle")), as_dict=1)

        return item_stocks

def get_scrapped_items(filters):
        """
        From warehouses, get the quantity scrapped
        """
        return get_stock_from_warehouse(filters, scrap=True)

def get_manufactured_items(filters):
        """
        From warehouses, get the quantity manufactured
        """
        item_stocks = frappe.db.sql("""
            select sle.item_code item_code, sle.actual_qty qty
            FROM `tabStock Ledger Entry` sle, `tabStock Entry` se, `tabWarehouse` warehouse
            WHERE se.docstatus = 1 AND sle.docstatus = 1
            AND sle.voucher_no = se.name
            AND sle.warehouse = warehouse.name
            AND warehouse.is_scrap={scrap}
            AND {conditions}
            AND se.purpose = 'Manufacture'
        """.format(scrap=False, conditions=get_conditions(filters, table="se")), as_dict=1)

        return item_stocks

def get_sold_items(filters):
        """
        From invoices, get sold quantities
        """

        sold_items = frappe.db.sql("""
            select si_item.item_code item_code, si_item.qty qty from `tabSales Invoice` si, `tabSales Invoice Item` si_item
            where si.name = si_item.parent and si.docstatus = 1 and {conditions}
        """.format(conditions=get_conditions(filters, table="si")), as_dict=1)

        return sold_items

def convert_to_liters(item, quantity):
        uom = get_conversion_factor(item.item_code, "Litre")
        conversion_factor = uom['conversion_factor']

        try:
                conversion = quantity * conversion_factor
        except TypeError, e:
                raise TypeError("Convertion to liters missing for item {0}".format(item.item_code))

        return conversion

def resolve_item_name(item):
        if item.variant_of != None:
                item_name = item.variant_of
        else:
                item_name = item.item_name

        return item_name

def execute(filters=None):

        columns = [
                _("Item") + ":Link/Item:200",
                _("ABV") + "::50",
                _("Liters manufactured") + "::100",
                _("Liters destroyed") + "::100",
                _("Liters manuf-destroyed") + "::100",
                _("Liters sold") + "::100",
                _("Liters returned") + "::100",
                _("Liters tasting") + "::100"
        ]

        data = []


        qty_per_product = defaultdict(lambda: {'manufactured': 0,
                                               'destroyed': 0,
                                               'sold': 0,
                                               'returned': 0,
                                               'scrapped': 0})

        # Calculate manufactured quantity in liters
        for sold_item in get_manufactured_items(filters):
                try:
                        item_doc = frappe.get_doc("Item", sold_item.item_code)
                except:
                        raise DataError("Error while looking up item {0}, aborting.".format(item.item_code))

                if item_doc.abv:
                        item_name = resolve_item_name(item_doc)
                        liters = convert_to_liters(item_doc, sold_item.qty)
                        if liters >= 0:
                                qty_per_product[(item_name, item_doc.abv)]['manufactured'] += liters
                        else:
                                qty_per_product[(item_name, item_doc.abv)]['destroyed'] += liters

        # Calculate sold quantity in liters
        for sold_item in get_sold_items(filters):
                item_doc = frappe.get_doc("Item", sold_item.item_code)
                if item_doc.abv:
                        item_name = resolve_item_name(item_doc)
                        liters = convert_to_liters(item_doc, sold_item.qty)
                        if liters >= 0:
                                qty_per_product[(item_name, item_doc.abv)]['sold'] += liters
                        else:
                                qty_per_product[(item_name, item_doc.abv)]['returned'] += liters


        # Calcule scrapped quantity in liters
        for scrapped_item in get_scrapped_items(filters):
                item_doc = frappe.get_doc("Item", scrapped_item.item_code)
                if item_doc.abv:
                        item_name = resolve_item_name(item_doc)
                        qty_per_product[(item_name, item_doc.abv)]['scrapped'] += convert_to_liters(item_doc, scrapped_item.qty)

        # Feed data
        for (item_name, abv), qtties in qty_per_product.items():
                data.append([item_name, "{0}%".format(abv),
                             qtties['manufactured'],
                             qtties['destroyed'],
                             qtties['manufactured'] + qtties['destroyed'],
                             qtties['sold'],
                             qtties['returned'],
                             qtties['scrapped']])

        return columns, data
