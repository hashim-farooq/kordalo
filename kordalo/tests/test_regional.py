import unittest

import frappe

import kordalo
from kordalo.tests.utils import KordaloTestSuite


@kordalo.allow_regional
def test_method():
	return "original"


class TestInit(KordaloTestSuite):
	def test_regional_overrides(self):
		frappe.flags.country = "Maldives"
		self.assertEqual(test_method(), "original")
