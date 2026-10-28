# Copyright (c) 2026, Frappe Technologies Pvt. Ltd. and Contributors
# See license.txt

import frappe

from kordalo.crm.doctype.lead.test_lead import make_lead
from kordalo.selling.report.address_and_contacts.address_and_contacts import execute
from kordalo.tests.utils import KordaloTestSuite


class TestAddressAndContacts(KordaloTestSuite):
	def test_lead_uses_its_own_name_field(self):
		# Lead has no `partner_name`; the report must query `lead_name` instead of erroring out.
		lead = make_lead()

		_columns, data = execute(frappe._dict({"party_type": "Lead", "party_name": lead.name}))

		self.assertTrue(any(row[0] == lead.name for row in data))
