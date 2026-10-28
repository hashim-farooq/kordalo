// Copyright (c) 2019, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

frappe.ui.form.on("Newsletter", {
	refresh() {
		kordalo.toggle_naming_series();
	},
});
