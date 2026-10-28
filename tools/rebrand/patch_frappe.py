#!/usr/bin/env python3
"""Teach the Frappe framework that `kordalo` plays the role it reserves for `erpnext`.

Frappe hardcodes the app name "erpnext" when deciding which apps get the setup
wizard and whether site setup is complete. Without this patch a Kordalo site
skips the company / chart-of-accounts setup.

Usage: patch_frappe.py <path to apps/frappe>

Each replacement must match exactly the expected number of times, so an upstream
change to these lines fails the build loudly instead of silently misbehaving.
"""

import sys
from pathlib import Path

PATCHES = {
	"frappe/__init__.py": [
		('{"app_name": ("in", ["frappe", "erpnext"])}', '{"app_name": ("in", ["frappe", "kordalo"])}', 1),
	],
	"frappe/core/doctype/installed_applications/installed_applications.py": [
		('in ["frappe", "erpnext"]', 'in ["frappe", "kordalo"]', 2),
		('app.get("app_name") == "erpnext"', 'app.get("app_name") == "kordalo"', 1),
	],
	"frappe/utils/legacy_gravatar_cleanup.py": [
		('"erpnext" in frappe.get_installed_apps()', '"kordalo" in frappe.get_installed_apps()', 1),
	],
}


def main() -> None:
	if len(sys.argv) != 2:
		sys.exit(__doc__)
	root = Path(sys.argv[1])
	for rel, replacements in PATCHES.items():
		path = root / rel
		text = path.read_text(encoding="utf-8")
		if "kordalo" in text:
			print(f"already patched: {rel}")
			continue
		for old, new, expected in replacements:
			found = text.count(old)
			if found != expected:
				sys.exit(f"{rel}: expected {expected} occurrence(s) of {old!r}, found {found}")
			text = text.replace(old, new)
		path.write_text(text, encoding="utf-8")
		print(f"patched: {rel}")


if __name__ == "__main__":
	main()
