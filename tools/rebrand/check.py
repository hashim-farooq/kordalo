#!/usr/bin/env python3
"""Fail if the old product name appears anywhere it shouldn't.

Usage: check.py [repo-dir]

Allowed: links to upstream documentation (see rebrand.DOC_URL), the legal files
kept verbatim, NOTICE.md, and this tooling itself.
"""

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from rebrand import DOC_URL, NAME, VERBATIM, is_binary  # noqa: E402

ALLOWED_FILES = VERBATIM | {"NOTICE.md"}
SKIP_DIRS = {".git", "node_modules", "tools"}
# The upstream-sync workflow has to name the upstream repository it pulls from,
# and the smoke test searches the rendered login page for the old name.
ALLOWED_PATHS = {".github/workflows/upstream-sync.yml", ".github/helper/smoke-test.sh"}


def main() -> None:
	root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
	hits = []
	for dirpath, dirnames, filenames in os.walk(root):
		rel_dir = Path(dirpath).relative_to(root)
		dirnames[:] = [
			d for d in dirnames if not (rel_dir == Path(".") and d in SKIP_DIRS) and d != "node_modules"
		]
		for name in dirnames + filenames:
			if NAME.search(name):
				hits.append(f"{(rel_dir / name).as_posix()}: name contains old brand")
		for name in filenames:
			rel = (rel_dir / name).as_posix()
			if (rel_dir == Path(".") and name in ALLOWED_FILES) or rel in ALLOWED_PATHS:
				continue
			data = (Path(dirpath) / name).read_bytes()
			if is_binary(data):
				continue
			text = data.decode("utf-8", "ignore")
			for lineno, line in enumerate(text.splitlines(), 1):
				if NAME.search(DOC_URL.sub("", line)):
					hits.append(f"{rel}:{lineno}: {line.strip()[:160]}")

	if hits:
		print(f"Found {len(hits)} leftover reference(s) to the old name:")
		print("\n".join(hits[:200]))
		sys.exit(1)
	print("Rebrand check passed: no leftover references.")


if __name__ == "__main__":
	main()
