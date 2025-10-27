app_name = "solede_qrbill"
app_title = "Solede Qrbill"
app_publisher = "Solede SA"
app_description = "Swiss QR-Bill generator for ERPNext Sales Invoices. Automatically generates compliant QR-Bills for Swiss companies and customers."
app_email = "info@solede.com"
app_license = "AGPLv3"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "solede_qrbill",
# 		"logo": "/assets/solede_qrbill/logo.png",
# 		"title": "Solede Qrbill",
# 		"route": "/solede_qrbill",
# 		"has_permission": "solede_qrbill.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
app_include_css = "/assets/solede_qrbill/css/qr_bill_print.css"
# app_include_js = "/assets/solede_qrbill/js/solede_qrbill.js"

# include js, css files in header of web template
# web_include_css = "/assets/solede_qrbill/css/solede_qrbill.css"
# web_include_js = "/assets/solede_qrbill/js/solede_qrbill.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "solede_qrbill/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {
	"Sales Invoice" : "public/js/sales_invoice.js"
}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "solede_qrbill/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
jinja = {
	"methods": [
		"solede_qrbill.qrbill.utils.get_qr_bill_html"
	]
}

# Installation
# ------------

# before_install = "solede_qrbill.install.before_install"
# after_install = "solede_qrbill.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "solede_qrbill.uninstall.before_uninstall"
# after_uninstall = "solede_qrbill.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "solede_qrbill.utils.before_app_install"
# after_app_install = "solede_qrbill.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "solede_qrbill.utils.before_app_uninstall"
# after_app_uninstall = "solede_qrbill.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "solede_qrbill.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Sales Invoice": {
		"validate": "solede_qrbill.qrbill.overrides.validate_swiss_qr_bill",
		"on_submit": "solede_qrbill.qrbill.overrides.generate_qr_reference_on_submit"
	}
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"solede_qrbill.tasks.all"
# 	],
# 	"daily": [
# 		"solede_qrbill.tasks.daily"
# 	],
# 	"hourly": [
# 		"solede_qrbill.tasks.hourly"
# 	],
# 	"weekly": [
# 		"solede_qrbill.tasks.weekly"
# 	],
# 	"monthly": [
# 		"solede_qrbill.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "solede_qrbill.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "solede_qrbill.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "solede_qrbill.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["solede_qrbill.utils.before_request"]
# after_request = ["solede_qrbill.utils.after_request"]

# Job Events
# ----------
# before_job = ["solede_qrbill.utils.before_job"]
# after_job = ["solede_qrbill.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"solede_qrbill.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

# Fixtures
# --------
fixtures = [
	{
		"dt": "Custom Field",
		"filters": [
			["module", "=", "Solede QR Bill"]
		]
	}
]

