#!/usr/bin/env python3
"""Turn an upstream ERPNext checkout into Kordalo.

Usage:
  rebrand.py sync <upstream-erpnext-dir> <kordalo-repo-dir>
      Replace the app code in the Kordalo repo with a renamed copy of upstream.
      Paths listed in KEEP (our own CI, tooling, deploy kit, docs) are left alone.
  rebrand.py inplace <app-dir>
      Rename erpnext -> kordalo inside another app's source tree (used for the
      `payments` app in CI, which imports erpnext directly).

Every "erpnext" in file names and contents becomes "kordalo", preserving case
(erpnext -> kordalo, ERPNEXT -> KORDALO, ERPNext/Erpnext -> Kordalo). Links to
upstream documentation are kept as-is because Kordalo has no docs site yet;
check.py allows exactly those.
"""

import os
import re
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
BRANDING = HERE / "branding"

# Top-level paths in the Kordalo repo that belong to us, not upstream.
KEEP = {".git", ".github", "tools", "deploy", "docker", "README.md", "NOTICE.md", ".dockerignore"}

# Upstream files that only make sense for Frappe's own project/infrastructure.
DROP = {
	".github",
	".greptile",
	".coderabbit.yml",
	".git-blame-ignore-revs",
	".mergify.yml",
	".releaserc",
	"CODEOWNERS",
	"README.md",
	"SECURITY.md",
	"TRADEMARK_POLICY.md",
	"codecov.yml",
	"crowdin.yml",
	"sider.yml",
	"sponsors.md",
}

# Kept verbatim: legal notices must not be altered.
VERBATIM = {"license.txt", "attributions.md"}

# Documentation links that still point at upstream docs (no Kordalo equivalent yet).
DOC_URL = re.compile(
	r"https?://(?:"
	r"docs\.erpnext\.com|discuss\.erpnext\.com|(?:www\.)?erpnext\.com/docs"
	r"|docs\.frappe\.io/erpnext|frappe\.io/erpnext|school\.frappe\.io"
	r"|frappecloud\.com/marketplace/apps/erpnext"
	r")[^\s\"'<>)`\]]*",
	re.IGNORECASE,
)
# The product homepage (bare, no deeper path) becomes ours.
HOMEPAGE_URL = re.compile(
	r"https?://(?:www\.)?(?:frappe\.io/erpnext|erpnext\.com)/?(?![\w/.-])", re.IGNORECASE
)
GITHUB_URL = re.compile(r"github\.com/frappe/erpnext(?![\w-])", re.IGNORECASE)
NAME = re.compile(r"erpnext", re.IGNORECASE)

BRANDED_IMAGES = {
	"erpnext-logo.svg": "logo.svg",
	"erpnext-favicon.svg": "logo.svg",
	"v16/erpnext.svg": "logo.svg",
	"erpnext-logo.png": "logo.png",
	"erpnext-logo-blue.png": "logo.png",
}


def kordalo_case(match: re.Match) -> str:
	word = match.group(0)
	if word.isupper():
		return "KORDALO"
	if word.islower():
		return "kordalo"
	return "Kordalo"


def rename_text(text: str) -> str:
	protected: list[str] = []

	def protect(match: re.Match) -> str:
		protected.append(match.group(0))
		return f"\x00{len(protected) - 1}\x00"

	text = HOMEPAGE_URL.sub("https://kordalo.com", text)
	text = DOC_URL.sub(protect, text)
	text = GITHUB_URL.sub("github.com/hashim-farooq/kordalo", text)
	text = NAME.sub(kordalo_case, text)
	return re.sub(r"\x00(\d+)\x00", lambda m: protected[int(m.group(1))], text)


def is_binary(data: bytes) -> bool:
	return b"\x00" in data[:8192]


def rename_file_contents(path: Path) -> None:
	data = path.read_bytes()
	if is_binary(data) or not NAME.search(data.decode("utf-8", "ignore")):
		return
	try:
		text = data.decode("utf-8")
	except UnicodeDecodeError:
		return
	new = rename_text(text)
	if new != text:
		path.write_bytes(new.encode("utf-8"))


def rename_tree(root: Path, skip_top: set[str] = frozenset()) -> None:
	"""Rename contents, then files and directories (deepest first), under root."""
	for dirpath, dirnames, filenames in os.walk(root, topdown=True):
		rel = Path(dirpath).relative_to(root)
		if rel == Path("."):
			dirnames[:] = [d for d in dirnames if d not in skip_top]
			filenames = [f for f in filenames if f not in skip_top]
		dirnames[:] = [d for d in dirnames if d not in {".git", "node_modules"}]
		for name in filenames:
			if rel == Path(".") and name in VERBATIM:
				continue
			rename_file_contents(Path(dirpath) / name)

	for dirpath, dirnames, filenames in os.walk(root, topdown=False):
		rel = Path(dirpath).relative_to(root)
		if rel.parts and (rel.parts[0] in skip_top or rel.parts[0] in {".git", "node_modules"}):
			continue
		for name in filenames + dirnames:
			if rel == Path(".") and name in skip_top:
				continue
			if NAME.search(name):
				src = Path(dirpath) / name
				src.rename(src.with_name(NAME.sub(kordalo_case, name)))


def apply_branding(app_root: Path) -> None:
	images = app_root / "kordalo" / "public" / "images"
	for upstream_name, ours in BRANDED_IMAGES.items():
		target = images / NAME.sub(kordalo_case, upstream_name)
		if target.exists():
			shutil.copyfile(BRANDING / ours, target)


def sync(upstream: Path, repo: Path) -> None:
	if not (upstream / "erpnext" / "hooks.py").exists():
		sys.exit(f"{upstream} does not look like an ERPNext checkout")

	for child in repo.iterdir():
		if child.name not in KEEP:
			shutil.rmtree(child) if child.is_dir() else child.unlink()

	for child in upstream.iterdir():
		if child.name in DROP or child.name in KEEP or child.name == ".git":
			continue
		dest = repo / child.name
		if child.is_dir():
			shutil.copytree(child, dest, symlinks=True)
		else:
			shutil.copy2(child, dest)

	rename_tree(repo, skip_top=KEEP)
	apply_branding(repo)
	print(f"Synced and renamed {upstream} -> {repo}")


def main() -> None:
	if len(sys.argv) == 4 and sys.argv[1] == "sync":
		sync(Path(sys.argv[2]).resolve(), Path(sys.argv[3]).resolve())
	elif len(sys.argv) == 3 and sys.argv[1] == "inplace":
		rename_tree(Path(sys.argv[2]).resolve())
	else:
		sys.exit(__doc__)


if __name__ == "__main__":
	main()
