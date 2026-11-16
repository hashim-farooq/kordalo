# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

import frappe

from kordalo.stock.doctype.item.test_item import make_item
from kordalo.tests.utils import KordaloTestSuite


class TestUOM(KordaloTestSuite):
	def test_merge_refuses_duplicate_item_conversion_uom(self):
		source_uom = frappe.get_doc({"doctype": "UOM", "uom_name": frappe.generate_hash(length=12)}).insert()
		target_uom = frappe.get_doc({"doctype": "UOM", "uom_name": frappe.generate_hash(length=12)}).insert()
		make_item(
			properties={"stock_uom": target_uom.name},
			uoms=[{"uom": source_uom.name, "conversion_factor": 12}],
		)

		self.assertRaises(
			frappe.ValidationError, frappe.rename_doc, "UOM", source_uom.name, target_uom.name, merge=True
		)
