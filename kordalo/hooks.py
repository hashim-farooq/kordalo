app_name = "kordalo"
app_title = "Kordalo"
app_publisher = "Frappe Technologies Pvt. Ltd."
app_description = """ERP made simple"""
app_icon = "fa fa-th"
app_color = "#e74c3c"
app_email = "hello@frappe.io"
app_license = "GNU General Public License (v3)"
source_link = "https://github.com/hashim-farooq/kordalo"
app_logo_url = "/assets/kordalo/images/kordalo-logo.svg"
app_home = "/desk/home"

add_to_apps_screen = [
	{
		"name": app_name,
		"logo": "/assets/kordalo/images/kordalo-logo.svg",
		"title": app_title,
		"route": app_home,
		"setup_wizard_text": "Let's give your business a home.",
		"has_permission": "kordalo.check_app_permission",
		"sequence_id": 1,
	}
]

# Modules that are only accessible via code and not via the UI. These modules are not shown in the sidebar or in the modules list.
code_only_modules = {
	# Integrations and Utilities are a handful of settings and tools each, so they sit in the Setup
	# sidebar with the rest of the configuration rather than taking two places in the dock.
	"Kordalo Integrations": ["Setup"],
	"Utilities": ["Setup"],
	"Telephony": ["Setup"],
	# Its one doctype, Communication Medium, describes how a call reaches someone, so it sits in
	# the Integrations section beside the call settings rather than in a shell of its own.
	"Communication": ["Setup"],
	"EDI": ["Setup"],
	"Bulk Transaction": ["Setup"],
	# Subcontracting is sending work out to be manufactured, so its orders and receipts live in the
	# Manufacturing sidebar.
	"Subcontracting": ["Manufacturing"],
	# Its records are country-specific tax settings and returns, so they sit with the rest of the
	# tax setup and reports in Accounts.
	"Regional": ["Accounts"],
	# Maintenance schedules and visits are after-sales upkeep of what was sold, so they live in a
	# Maintenance section of the Quality sidebar.
	"Maintenance": ["Quality Management"],
}

develop_version = "15.x.x-develop"

app_include_js = "kordalo.bundle.js"
app_include_css = "kordalo.bundle.css"
web_include_css = "kordalo-web.bundle.css"
email_css = "email_kordalo.bundle.css"

app_include_icons = [
	"/assets/kordalo/icons/pos-icons.svg",
	"/assets/kordalo/icons/module-icons.svg",
]

web_include_icons = [
	"/assets/kordalo/icons/pos-icons.svg",
]

doctype_js = {
	"Address": "public/js/address.js",
	"Communication": "public/js/communication.js",
	"Event": "public/js/event.js",
	"Newsletter": "public/js/newsletter.js",
	"Contact": "public/js/contact.js",
}
doctype_list_js = {
	"Code List": [
		"edi/doctype/code_list/code_list_import.js",
	],
	"Common Code": [
		"edi/doctype/code_list/code_list_import.js",
	],
}

page_js = {"print": "public/js/print.js"}

extend_doctype_class = {"Address": "kordalo.accounts.custom.address.KordaloAddress"}

override_whitelisted_methods = {"frappe.www.contact.send_message": "kordalo.templates.utils.send_message"}

welcome_email = "kordalo.setup.utils.welcome_email"

# setup wizard
setup_wizard_requires = "assets/kordalo/js/setup_wizard.js"
setup_wizard_stages = "kordalo.setup.setup_wizard.setup_wizard.get_setup_stages"

after_install = "kordalo.setup.install.after_install"

after_app_install = "kordalo.setup.install.after_app_install"
after_app_uninstall = "kordalo.setup.install.after_app_uninstall"

# patches that must stop the migration when they fail, even with `bench migrate --skip-failing`
never_skip_patches = ["kordalo.patches.v16_0.update_serial_batch_entries"]

boot_session = "kordalo.startup.boot.boot_session"
notification_config = "kordalo.startup.notifications.get_notification_config"
get_help_messages = "kordalo.utilities.activation.get_help_messages"
filters_config = "kordalo.startup.filters.get_filters_config"
additional_print_settings = "kordalo.controllers.print_settings.get_print_settings"

on_session_creation = "kordalo.portal.utils.create_customer_or_supplier"

treeviews = [
	"Account",
	"Cost Center",
	"Warehouse",
	"Item Group",
	"Customer Group",
	"Supplier Group",
	"Sales Person",
	"Territory",
	"Department",
]

demo_master_doctypes = [
	"item_group",
	"item",
	"customer_group",
	"supplier_group",
	"customer",
	"supplier",
]

jinja = {
	"methods": [
		"kordalo.stock.serial_batch_bundle.get_serial_or_batch_nos",
	],
}

# website
webform_list_context = "kordalo.controllers.website_list_for_contact.get_webform_list_context"

calendars = ["Task", "Work Order", "Sales Order", "Holiday List", "ToDo"]

website_generators = ["BOM", "Sales Partner"]

website_context = {
	"favicon": "/assets/kordalo/images/kordalo-favicon.svg",
	"splash_image": "/assets/kordalo/images/kordalo-logo.svg",
}

# nosemgrep
website_route_rules = [
	{"from_route": "/orders", "to_route": "Sales Order"},
	{
		"from_route": "/orders/<path:name>",
		"to_route": "order",
		"defaults": {"doctype": "Sales Order", "parents": [{"label": "Orders", "route": "orders"}]},
	},
	{"from_route": "/invoices", "to_route": "Sales Invoice"},
	{
		"from_route": "/invoices/<path:name>",
		"to_route": "order",
		"defaults": {
			"doctype": "Sales Invoice",
			"parents": [{"label": "Invoices", "route": "invoices"}],
		},
	},
	{"from_route": "/supplier-quotations", "to_route": "Supplier Quotation"},
	{
		"from_route": "/supplier-quotations/<path:name>",
		"to_route": "order",
		"defaults": {
			"doctype": "Supplier Quotation",
			"parents": [{"label": "Supplier Quotation", "route": "supplier-quotations"}],
		},
	},
	{"from_route": "/purchase-orders", "to_route": "Purchase Order"},
	{
		"from_route": "/purchase-orders/<path:name>",
		"to_route": "order",
		"defaults": {
			"doctype": "Purchase Order",
			"parents": [{"label": "Purchase Order", "route": "purchase-orders"}],
		},
	},
	{
		"from_route": "/purchase-orders/<path:name>",
		"to_route": "order",
		"defaults": {
			"doctype": "Purchase Order",
			"parents": [{"label": "Purchase Order", "route": "purchase-orders"}],
		},
	},
	{"from_route": "/purchase-invoices", "to_route": "Purchase Invoice"},
	{
		"from_route": "/purchase-invoices/<path:name>",
		"to_route": "order",
		"defaults": {
			"doctype": "Purchase Invoice",
			"parents": [{"label": "Purchase Invoice", "route": "purchase-invoices"}],
		},
	},
	{"from_route": "/quotations", "to_route": "Quotation"},
	{
		"from_route": "/quotations/<path:name>",
		"to_route": "order",
		"defaults": {
			"doctype": "Quotation",
			"parents": [{"label": "Quotations", "route": "quotations"}],
		},
	},
	{"from_route": "/shipments", "to_route": "Delivery Note"},
	{
		"from_route": "/shipments/<path:name>",
		"to_route": "order",
		"defaults": {
			"doctype": "Delivery Note",
			"parents": [{"label": "Shipments", "route": "shipments"}],
		},
	},
	{"from_route": "/rfq", "to_route": "Request for Quotation"},
	{
		"from_route": "/rfq/<path:name>",
		"to_route": "rfq",
		"defaults": {
			"doctype": "Request for Quotation",
			"parents": [{"label": "Request for Quotation", "route": "rfq"}],
		},
	},
	{"from_route": "/addresses", "to_route": "Address"},
	{
		"from_route": "/addresses/<path:name>",
		"to_route": "addresses",
		"defaults": {"doctype": "Address", "parents": [{"label": "Addresses", "route": "addresses"}]},
	},
	{"from_route": "/boms", "to_route": "BOM"},
	{"from_route": "/timesheets", "to_route": "Timesheet"},
	{"from_route": "/material-requests", "to_route": "Material Request"},
	{
		"from_route": "/material-requests/<path:name>",
		"to_route": "material_request_info",
		"defaults": {
			"doctype": "Material Request",
			"parents": [{"label": "Material Request", "route": "material-requests"}],
		},
	},
	{"from_route": "/project", "to_route": "Project"},
	{"from_route": "/tasks", "to_route": "Task"},
	{"from_route": "/banking/<path:app_path>", "to_route": "banking"},
]

standard_navbar_items = [
	{
		"item_label": "Delete Demo Data",
		"item_type": "Action",
		"action": "kordalo.demo.clear_demo();",
		"is_standard": 1,
		"condition": "eval: frappe.boot.sysdefaults.demo_company && frappe.boot.sysdefaults.demo_company.length > 0",
		"icon": "trash",
	},
]

standard_portal_menu_items = [
	{"title": "Projects", "route": "/project", "reference_doctype": "Project", "role": "Customer"},
	{
		"title": "Request for Quotations",
		"route": "/rfq",
		"reference_doctype": "Request for Quotation",
		"role": "Supplier",
	},
	{
		"title": "Supplier Quotation",
		"route": "/supplier-quotations",
		"reference_doctype": "Supplier Quotation",
		"role": "Supplier",
	},
	{
		"title": "Purchase Orders",
		"route": "/purchase-orders",
		"reference_doctype": "Purchase Order",
		"role": "Supplier",
	},
	{
		"title": "Purchase Invoices",
		"route": "/purchase-invoices",
		"reference_doctype": "Purchase Invoice",
		"role": "Supplier",
	},
	{
		"title": "Quotations",
		"route": "/quotations",
		"reference_doctype": "Quotation",
		"role": "Customer",
	},
	{
		"title": "Orders",
		"route": "/orders",
		"reference_doctype": "Sales Order",
		"role": "Customer",
	},
	{
		"title": "Invoices",
		"route": "/invoices",
		"reference_doctype": "Sales Invoice",
		"role": "Customer",
	},
	{
		"title": "Shipments",
		"route": "/shipments",
		"reference_doctype": "Delivery Note",
		"role": "Customer",
	},
	{"title": "Issues", "route": "/issues", "reference_doctype": "Issue", "role": "Customer"},
	{"title": "Addresses", "route": "/addresses", "reference_doctype": "Address", "role": "Customer"},
	{
		"title": "Timesheets",
		"route": "/timesheets",
		"reference_doctype": "Timesheet",
		"role": "Customer",
	},
	{"title": "Newsletter", "route": "/newsletters", "reference_doctype": "Newsletter"},
	{
		"title": "Material Request",
		"route": "/material-requests",
		"reference_doctype": "Material Request",
		"role": "Customer",
	},
	{"title": "Appointment Booking", "route": "/book_appointment"},
]

sounds = [
	{"name": "incoming-call", "src": "/assets/kordalo/sounds/incoming-call.mp3", "volume": 0.2},
	{"name": "call-disconnect", "src": "/assets/kordalo/sounds/call-disconnect.mp3", "volume": 0.2},
	{"name": "numpad-touch", "src": "/assets/kordalo/sounds/numpad-touch.mp3", "volume": 0.8},
]

has_upload_permission = {"Employee": "kordalo.setup.doctype.employee.employee.has_upload_permission"}

has_website_permission = {
	"Sales Order": "kordalo.controllers.website_list_for_contact.has_website_permission",
	"Quotation": "kordalo.controllers.website_list_for_contact.has_website_permission",
	"Sales Invoice": "kordalo.controllers.website_list_for_contact.has_website_permission",
	"Supplier Quotation": "kordalo.controllers.website_list_for_contact.has_website_permission",
	"Purchase Order": "kordalo.controllers.website_list_for_contact.has_website_permission",
	"Purchase Invoice": "kordalo.controllers.website_list_for_contact.has_website_permission",
	"Material Request": "kordalo.controllers.website_list_for_contact.has_website_permission",
	"Delivery Note": "kordalo.controllers.website_list_for_contact.has_website_permission",
	"Issue": "kordalo.support.doctype.issue.issue.has_website_permission",
	"Timesheet": "kordalo.controllers.website_list_for_contact.has_website_permission",
	"Project": "kordalo.controllers.website_list_for_contact.has_website_permission",
}


period_closing_doctypes = [
	"Sales Invoice",
	"Purchase Invoice",
	"Journal Entry",
	"Bank Clearance",
	"Stock Entry",
	"Dunning",
	"Invoice Discounting",
	"Payment Entry",
	"Period Closing Voucher",
	"Process Deferred Accounting",
	"Asset",
	"Asset Capitalization",
	"Asset Repair",
	"Delivery Note",
	"Landed Cost Voucher",
	"Purchase Receipt",
	"Stock Reconciliation",
	"Subcontracting Receipt",
]

sqlite_search = ["kordalo.stock.doctype.item.item_search.ItemSearch"]

doc_events = {
	"*": {
		"validate": [
			"kordalo.support.doctype.service_level_agreement.service_level_agreement.apply",
			"kordalo.setup.doctype.transaction_deletion_record.transaction_deletion_record.check_for_running_deletion_job",
		],
	},
	tuple(period_closing_doctypes): {
		"validate": "kordalo.accounts.doctype.accounting_period.accounting_period.validate_accounting_period_on_doc_save",
	},
	"Item": {
		"on_update": "kordalo.stock.doctype.item.item_search.reindex_item",
		"after_rename": "kordalo.stock.doctype.item.item_search.reindex_renamed_item",
	},
	"Stock Entry": {
		"on_submit": "kordalo.stock.doctype.material_request.material_request.update_completed_and_requested_qty",
		"on_cancel": "kordalo.stock.doctype.material_request.material_request.update_completed_and_requested_qty",
	},
	"User": {
		"after_insert": "frappe.contacts.doctype.contact.contact.update_contact",
		"validate": "kordalo.setup.doctype.employee.employee.validate_employee_role",
		"on_update": "kordalo.portal.utils.set_default_role",
	},
	"Communication": {
		"on_update": [
			"kordalo.support.doctype.service_level_agreement.service_level_agreement.on_communication_update",
			"kordalo.support.doctype.issue.issue.set_first_response_time",
		],
		"after_insert": [
			"kordalo.crm.utils.link_communications_with_prospect",
			"kordalo.crm.utils.update_modified_timestamp",
		],
	},
	"Event": {
		"after_insert": "kordalo.crm.utils.link_events_with_prospect",
	},
	"Contact Us Settings": {
		"on_update": "kordalo.crm.utils.disable_opportunity_creation_on_contact_us_disabled",
	},
	"Sales Invoice": {
		"on_submit": [
			"kordalo.regional.italy.utils.sales_invoice_on_submit",
		],
		"on_cancel": [
			"kordalo.regional.italy.utils.sales_invoice_on_cancel",
		],
		"on_trash": "kordalo.regional.check_deletion_permission",
	},
	"Purchase Invoice": {
		"validate": [
			"kordalo.regional.united_arab_emirates.utils.update_grand_total_for_rcm",
			"kordalo.regional.united_arab_emirates.utils.validate_returns",
		],
	},
	"Payment Entry": {
		"on_trash": "kordalo.regional.check_deletion_permission",
	},
	"Address": {
		"validate": [
			"kordalo.regional.italy.utils.set_state_code",
		],
	},
	"Contact": {
		"on_trash": "kordalo.support.doctype.issue.issue.update_issue",
		"after_insert": "kordalo.telephony.doctype.call_log.call_log.link_existing_conversations",
		"validate": ["kordalo.crm.utils.update_lead_phone_numbers"],
	},
	"Email Unsubscribe": {
		"after_insert": "kordalo.crm.doctype.email_campaign.email_campaign.unsubscribe_recipient"
	},
	"Integration Request": {
		"validate": "kordalo.accounts.doctype.payment_request.payment_request.validate_payment"
	},
}

# function should expect the variable and doc as arguments
naming_series_variables_list = ["FY", "TFY", "ABBR", "MM", "DD", "YY", "YYYY", "JJJ", "WW"]
naming_series_variables = {
	variable: "kordalo.accounts.utils.parse_naming_series_variable"
	for variable in naming_series_variables_list
}

# On cancel event Payment Entry will be exempted and all linked submittable doctype will get cancelled.
# to maintain data integrity we exempted payment entry. it will un-link when sales invoice get cancelled.
# if payment entry not in auto cancel exempted doctypes it will cancel payment entry.
auto_cancel_exempted_doctypes = [
	"Payment Entry",
]

scheduler_events = {
	"cron": {
		"0/15 * * * *": [
			"kordalo.manufacturing.doctype.bom_update_log.bom_update_log.resume_bom_cost_update_jobs",
			"kordalo.stock.doctype.repost_item_valuation.repost_item_valuation.run_parallel_reposting",
		],
		# Hourly but offset by 30 minutes
		"30 * * * *": [
			"kordalo.accounts.doctype.gl_entry.gl_entry.rename_gle_sle_docs",
		],
		# Daily but offset by 45 minutes
		"45 0 * * *": [],
	},
	"hourly": [
		"kordalo.projects.doctype.project.project.hourly_reminder",
	],
	"hourly_long": [],
	"hourly_maintenance": [
		"kordalo.crm.doctype.appointment.appointment.handle_expired_unverified_appointments",
		"kordalo.stock.doctype.repost_item_valuation.repost_item_valuation.repost_entries",
		"kordalo.utilities.bulk_transaction.retry",
		"kordalo.projects.doctype.project.project.collect_project_status",
		"kordalo.projects.doctype.project.project.project_status_update_reminder",
		"kordalo.kordalo_integrations.doctype.plaid_settings.plaid_settings.automatic_synchronization",
		"kordalo.utilities.doctype.video.video.update_youtube_data",
		"kordalo.accounts.doctype.bank_transaction_rule.bank_transaction_rule.scheduler_run_rule_evaluation",
	],
	"daily": [],
	"daily_long": [],
	"daily_maintenance": [
		"kordalo.support.doctype.issue.issue.auto_close_tickets",
		"kordalo.crm.doctype.opportunity.opportunity.auto_close_opportunity",
		"kordalo.controllers.accounts_controller.update_invoice_status",
		"kordalo.accounts.doctype.fiscal_year.fiscal_year.auto_create_fiscal_year",
		"kordalo.projects.doctype.task.task.set_tasks_as_overdue",
		"kordalo.stock.doctype.serial_no.serial_no.update_maintenance_status",
		"kordalo.buying.doctype.supplier_scorecard.supplier_scorecard.refresh_scorecards",
		"kordalo.setup.doctype.company.company.cache_companies_monthly_sales_history",
		"kordalo.assets.doctype.asset.asset.update_maintenance_status",
		"kordalo.assets.doctype.asset.asset.make_post_gl_entry",
		"kordalo.crm.doctype.contract.contract.update_status_for_contracts",
		"kordalo.projects.doctype.project.project.update_project_sales_billing",
		"kordalo.projects.doctype.project.project.send_project_status_email_to_users",
		"kordalo.quality_management.doctype.quality_review.quality_review.review",
		"kordalo.support.doctype.service_level_agreement.service_level_agreement.check_agreement_status",
		"kordalo.crm.doctype.email_campaign.email_campaign.send_email_to_leads_or_contacts",
		"kordalo.crm.doctype.email_campaign.email_campaign.set_email_campaign_status",
		"kordalo.selling.doctype.quotation.quotation.set_expired_status",
		"kordalo.buying.doctype.supplier_quotation.supplier_quotation.set_expired_status",
		"kordalo.accounts.doctype.process_statement_of_accounts.process_statement_of_accounts.send_auto_email",
		"kordalo.accounts.utils.auto_create_exchange_rate_revaluation_daily",
		"kordalo.accounts.utils.run_ledger_health_checks",
		"kordalo.assets.doctype.asset_maintenance_log.asset_maintenance_log.update_asset_maintenance_log_status",
		"kordalo.stock.reorder_item.reorder_item",
		"kordalo.accounts.doctype.process_subscription.process_subscription.create_subscription_process",
		"kordalo.setup.doctype.email_digest.email_digest.send",
		"kordalo.manufacturing.doctype.bom_update_tool.bom_update_tool.auto_update_latest_price_in_all_boms",
		"kordalo.crm.utils.open_leads_opportunities_based_on_todays_event",
		"kordalo.assets.doctype.asset.depreciation.post_depreciation_entries",
	],
	"weekly": [
		"kordalo.accounts.utils.auto_create_exchange_rate_revaluation_weekly",
		"kordalo.stock.doctype.stock_reposting_settings.stock_reposting_settings.repost_incorrect_valuation_entries",
	],
	"monthly_long": [
		"kordalo.accounts.deferred_revenue.process_deferred_accounting",
		"kordalo.accounts.utils.auto_create_exchange_rate_revaluation_monthly",
	],
}

email_brand_image = "assets/kordalo/images/kordalo-logo.jpg"

default_mail_footer = """
	<span>
		Sent via
		<a class="text-muted" href="https://frappe.io/erpnext?source=via_email_footer" target="_blank">
			Kordalo
		</a>
	</span>
"""

get_translated_dict = {("doctype", "Global Defaults"): "frappe.geo.country_info.get_translated_dict"}

bot_parsers = [
	"kordalo.utilities.bot.FindItemBot",
]

get_site_info = "kordalo.utilities.get_site_info"

payment_gateway_enabled = "kordalo.accounts.utils.create_payment_gateway_account"

communication_doctypes = ["Customer", "Supplier"]

advance_payment_receivable_doctypes = ["Sales Order"]
advance_payment_payable_doctypes = ["Purchase Order"]

invoice_doctypes = ["Sales Invoice", "Purchase Invoice"]

bank_reconciliation_doctypes = [
	"Payment Entry",
	"Journal Entry",
	"Purchase Invoice",
	"Sales Invoice",
]

accounting_dimension_doctypes = [
	"GL Entry",
	"Payment Ledger Entry",
	"Sales Invoice",
	"Purchase Invoice",
	"Payment Entry",
	"Asset",
	"Stock Entry",
	"Budget",
	"Delivery Note",
	"Sales Invoice Item",
	"Purchase Invoice Item",
	"Purchase Order Item",
	"Sales Order Item",
	"Journal Entry Account",
	"Journal Entry Template Account",
	"Material Request Item",
	"Delivery Note Item",
	"Purchase Receipt Item",
	"Stock Entry Detail",
	"Payment Entry Deduction",
	"Sales Taxes and Charges",
	"Purchase Taxes and Charges",
	"Shipping Rule",
	"Landed Cost Item",
	"Landed Cost Taxes and Charges",
	"Asset Value Adjustment",
	"Asset Repair",
	"Asset Capitalization",
	"Loyalty Program",
	"Stock Reconciliation",
	"POS Profile",
	"Opening Invoice Creation Tool",
	"Opening Invoice Creation Tool Item",
	"Subscription",
	"Subscription Plan",
	"POS Invoice",
	"POS Invoice Item",
	"Purchase Order",
	"Purchase Receipt",
	"Sales Order",
	"Subcontracting Order",
	"Subcontracting Order Item",
	"Subcontracting Receipt",
	"Subcontracting Receipt Item",
	"Account Closing Balance",
	"Supplier Quotation",
	"Supplier Quotation Item",
	"Payment Reconciliation",
	"Payment Reconciliation Allocation",
	"Payment Request",
	"Asset Movement Item",
	"Asset Depreciation Schedule",
	"Advance Taxes and Charges",
]

subscription_doctypes = ["Sales Invoice", "Purchase Invoice", "Payment Request", "POS Invoice"]

get_matching_queries = (
	"kordalo.accounts.doctype.bank_reconciliation_tool.bank_reconciliation_tool.get_matching_queries"
)

get_amounts_not_reflected_in_system_for_bank_reconciliation_statement = "kordalo.accounts.report.bank_reconciliation_statement.bank_reconciliation_statement.get_amounts_not_reflected_in_system_for_bank_reconciliation_statement"

get_payment_entries_for_bank_clearance = (
	"kordalo.accounts.doctype.bank_clearance.bank_clearance.get_payment_entries_for_bank_clearance"
)

get_entries_for_bank_clearance_summary = "kordalo.accounts.report.bank_clearance_summary.bank_clearance_summary.get_entries_for_bank_clearance_summary"

get_entries_for_bank_reconciliation_statement = "kordalo.accounts.report.bank_reconciliation_statement.bank_reconciliation_statement.get_entries_for_bank_reconciliation_statement"

regional_overrides = {
	"France": {"kordalo.tests.test_regional.test_method": "kordalo.regional.france.utils.test_method"},
	"United Arab Emirates": {
		"kordalo.controllers.taxes_and_totals.update_itemised_tax_data": "kordalo.regional.united_arab_emirates.utils.update_itemised_tax_data",
		"kordalo.accounts.doctype.purchase_invoice.purchase_invoice.make_regional_gl_entries": "kordalo.regional.united_arab_emirates.utils.make_regional_gl_entries",
	},
	"Saudi Arabia": {
		"kordalo.controllers.taxes_and_totals.update_itemised_tax_data": "kordalo.regional.united_arab_emirates.utils.update_itemised_tax_data"
	},
	"Italy": {
		"kordalo.controllers.taxes_and_totals.update_itemised_tax_data": "kordalo.regional.italy.utils.update_itemised_tax_data",
		"kordalo.controllers.accounts_controller.validate_regional": "kordalo.regional.italy.utils.sales_invoice_validate",
	},
}
user_data_fields = [
	{
		"doctype": "Lead",
		"filter_by": "email_id",
		"redact_fields": ["phone", "mobile_no", "fax", "website", "lead_name"],
	},
	{
		"doctype": "Opportunity",
		"filter_by": "contact_email",
		"redact_fields": ["contact_mobile", "contact_display", "customer_name"],
	},
]


# Kordalo doctypes for Global Search
global_search_doctypes = {
	"Default": [
		{"doctype": "Customer", "index": 0},
		{"doctype": "Supplier", "index": 1},
		{"doctype": "Item", "index": 2},
		{"doctype": "Sales Invoice", "index": 3},
		{"doctype": "Purchase Invoice", "index": 4},
		{"doctype": "Sales Order", "index": 5},
		{"doctype": "Purchase Order", "index": 6},
		{"doctype": "Quotation", "index": 7},
		{"doctype": "Delivery Note", "index": 8},
		{"doctype": "Purchase Receipt", "index": 9},
		{"doctype": "Payment Entry", "index": 10},
		{"doctype": "Journal Entry", "index": 11},
		{"doctype": "Lead", "index": 12},
		{"doctype": "Opportunity", "index": 13},
		{"doctype": "Supplier Quotation", "index": 14},
		{"doctype": "Material Request", "index": 15},
		{"doctype": "Stock Entry", "index": 16},
		{"doctype": "Work Order", "index": 17},
		{"doctype": "BOM", "index": 18},
		{"doctype": "Project", "index": 19},
		{"doctype": "Task", "index": 20},
		{"doctype": "Issue", "index": 21},
		{"doctype": "Asset", "index": 22},
		{"doctype": "Serial No", "index": 23},
		{"doctype": "Batch", "index": 24},
		{"doctype": "Employee", "index": 25},
	],
}

ignore_links_on_delete = [
	"Tax Withholding Entry",
]

additional_timeline_content = {"*": ["kordalo.telephony.doctype.call_log.call_log.get_linked_call_logs"]}


extend_bootinfo = [
	"kordalo.support.doctype.service_level_agreement.service_level_agreement.add_sla_doctypes",
	"kordalo.startup.boot.bootinfo",
]


default_log_clearing_doctypes = {
	"Repost Item Valuation": 60,
}

export_python_type_annotations = True

fields_for_group_similar_items = ["qty", "amount"]

# Translation
# ------------
# List of apps whose translatable strings should be excluded from this app's translations.
ignore_translatable_strings_from = ["frappe"]
repost_allowed_doctypes = [
	"Sales Invoice",
	"Purchase Invoice",
	"Journal Entry",
	"Payment Entry",
	"Purchase Receipt",
]


# Data Import
# -----------
# Import a Customer or Supplier with its contacts and addresses in one file.
data_import_providers = {
	"Customer": "kordalo.utilities.party_import_provider.PartyImportProvider",
	"Supplier": "kordalo.utilities.party_import_provider.PartyImportProvider",
}
