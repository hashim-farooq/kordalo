# Copyright (c) 2026, Frappe Technologies Pvt. Ltd. and Contributors
# See license.txt

import frappe

from kordalo.selling.doctype.sales_order.test_sales_order import make_sales_order
from kordalo.stock.doctype.item.test_item import make_item
from kordalo.stock.report.items_to_be_requested.items_to_be_requested import execute
from kordalo.tests.utils import KordaloTestSuite


class TestItemsToBeRequested(KordaloTestSuite):
	def test_disabled_items_are_not_listed(self):
		item = make_item(properties={"is_stock_item": 1}).name
		make_sales_order(item_code=item, qty=3, warehouse="Stores - _TC")
		data = execute(frappe._dict())[1]
		self.assertIn(item, [row.get("item_code") for row in data])

		frappe.db.set_value("Item", item, "disabled", 1)

		data = execute(frappe._dict())[1]

		self.assertNotIn(item, [row.get("item_code") for row in data])
