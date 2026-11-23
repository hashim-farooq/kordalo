import importlib

import frappe

from kordalo.tests.utils import KordaloTestSuite

POST_ONLY_METHODS = (
	"kordalo.accounts.doctype.bank_account.bank_account.set_closing_balance_as_per_statement",
	"kordalo.accounts.doctype.bank_reconciliation_tool.bank_reconciliation_tool.update_bank_transaction",
	"kordalo.accounts.doctype.bank_reconciliation_tool.bank_reconciliation_tool.create_journal_entry_bts",
	"kordalo.accounts.doctype.bank_reconciliation_tool.bank_reconciliation_tool.create_payment_entry_bts",
	"kordalo.accounts.doctype.bank_reconciliation_tool.bank_reconciliation_tool.create_internal_transfer",
	"kordalo.accounts.doctype.bank_reconciliation_tool.bank_reconciliation_tool.reconcile_vouchers",
	"kordalo.accounts.doctype.bank_transaction.bank_transaction.unreconcile_transaction_entry",
	"kordalo.accounts.doctype.bisect_accounting_statements.bisect_accounting_statements.BisectAccountingStatements.bisect_left",
	"kordalo.accounts.doctype.bisect_accounting_statements.bisect_accounting_statements.BisectAccountingStatements.bisect_right",
	"kordalo.accounts.doctype.bisect_accounting_statements.bisect_accounting_statements.BisectAccountingStatements.move_up",
	"kordalo.accounts.doctype.budget.budget.revise_budget",
	"kordalo.accounts.doctype.cheque_print_template.cheque_print_template.create_or_update_cheque_print_format",
	"kordalo.accounts.doctype.payment_request.payment_request.make_payment_request",
	"kordalo.assets.doctype.location.location.add_node",
	"kordalo.buying.doctype.request_for_quotation.request_for_quotation.create_supplier_quotation",
	"kordalo.controllers.accounts_controller.update_company_master_and_address",
	"kordalo.controllers.stock_controller.make_quality_inspections",
	"kordalo.crm.doctype.lead.lead.make_lead_from_communication",
	"kordalo.crm.doctype.opportunity.opportunity.set_multiple_status",
	"kordalo.crm.doctype.opportunity.opportunity.make_opportunity_from_communication",
	"kordalo.manufacturing.doctype.work_order.work_order.set_work_order_ops",
	"kordalo.manufacturing.doctype.workstation.workstation.Workstation.start_job",
	"kordalo.manufacturing.doctype.workstation.workstation.Workstation.complete_job",
	"kordalo.projects.doctype.project.project.create_duplicate_project",
	"kordalo.projects.doctype.project.project.set_project_status",
	"kordalo.projects.doctype.task.task.set_multiple_status",
	"kordalo.projects.doctype.task.task.add_node",
	"kordalo.projects.doctype.task.task.add_multiple_tasks",
	"kordalo.quality_management.doctype.quality_procedure.quality_procedure.add_node",
	"kordalo.selling.doctype.customer.customer.Customer.get_customer_group_details",
	"kordalo.selling.doctype.sales_order.sales_order.make_work_orders",
	"kordalo.selling.page.point_of_sale.point_of_sale.set_customer_info",
	"kordalo.setup.doctype.company.company.add_node",
	"kordalo.setup.doctype.company.company.create_transaction_deletion_request",
	"kordalo.setup.doctype.department.department.add_node",
	"kordalo.setup.doctype.employee.employee.create_user",
	"kordalo.stock.doctype.batch.batch.split_batch",
	"kordalo.stock.doctype.material_request.material_request.raise_work_orders",
	"kordalo.stock.doctype.warehouse.warehouse.add_node",
	"kordalo.stock.report.stock_and_account_value_comparison.stock_and_account_value_comparison.create_reposting_entries",
	"kordalo.stock.report.stock_ledger_invariant_check.stock_ledger_invariant_check.create_reposting_entries",
	"kordalo.subcontracting.doctype.subcontracting_receipt.subcontracting_receipt.make_purchase_receipt",
	"kordalo.support.doctype.issue.issue.Issue.split_issue",
	"kordalo.support.doctype.issue.issue.make_issue_from_communication",
	"kordalo.support.doctype.service_level_agreement.service_level_agreement.reset_service_level_agreement",
	"kordalo.telephony.doctype.call_log.call_log.add_call_summary_and_call_type",
)


class TestWhitelistedMethodsPostOnly(KordaloTestSuite):
	def test_state_changing_methods_accept_only_post(self):
		for path in POST_ONLY_METHODS:
			with self.subTest(path=path):
				method = resolve(path)
				self.assertIn(method, frappe.whitelisted)
				self.assertEqual(frappe.allowed_http_methods_for_whitelisted_func.get(method), ["POST"])


def resolve(path: str):
	"""Resolve a dotted path to a module function or a class method."""
	module_path, _, attribute = path.rpartition(".")
	try:
		return getattr(importlib.import_module(module_path), attribute)
	except ModuleNotFoundError:
		module_path, _, class_name = module_path.rpartition(".")
		return getattr(getattr(importlib.import_module(module_path), class_name), attribute)
