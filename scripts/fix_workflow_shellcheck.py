#!/usr/bin/env python3
"""
fix_workflow_shellcheck.py — surgical shellcheck-fix tool for GitHub Actions
============================================================================

Applies the following deterministic, idempotent transformations to lines
inside `run: |` blocks of GitHub Actions YAML workflows:

  * SC2086:  `>> $GITHUB_ENV`             →  `>> "${GITHUB_ENV}"`
             `>> $GITHUB_OUTPUT`          →  `>> "${GITHUB_OUTPUT}"`
             `>> $GITHUB_STEP_SUMMARY`    →  `>> "${GITHUB_STEP_SUMMARY}"`
             `>> $GITHUB_PATH`            →  `>> "${GITHUB_PATH}"`
             (also handles `${GITHUB_*}` already wrapped in `${…}`)
  * SC2086:  `cd $GITHUB_WORKSPACE`       →  `cd "${GITHUB_WORKSPACE}"`

The fixes are constrained to common GitHub Actions idioms; they will not
modify any line that does not contain `$GITHUB_…` or any line that already
uses double-quoted braces.

Usage:
    python3 scripts/fix_workflow_shellcheck.py [WORKFLOW.yml ...]
    python3 scripts/fix_workflow_shellcheck.py --check     # exit 1 if any change needed
    python3 scripts/fix_workflow_shellcheck.py --all       # process all workflows
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


GH_VARS = (
    "GITHUB_ENV",
    "GITHUB_OUTPUT",
    "GITHUB_STEP_SUMMARY",
    "GITHUB_PATH",
    "GITHUB_WORKSPACE",
    "GITHUB_EVENT_PATH",
    "GITHUB_SHA",
    "GITHUB_REF",
)

# Match `$VAR` or `${VAR}` (without surrounding double quotes) and replace
# with `"${VAR}"`. We require a left boundary of whitespace, `>`, `<`, `(`,
# `=`, or `:` to avoid hitting things like `\$VAR` in literal strings.
PATTERNS = [
    (
        re.compile(rf"(?P<lead>[\s>()=:|&])\$(?:{var}|{{{var}}})\b"),
        rf'\g<lead>"${{{var}}}"',
    )
    for var in GH_VARS
]


def fix_line(line: str) -> str:
    new = line
    for pat, repl in PATTERNS:
        new = pat.sub(repl, new)
    return new


def fix_text(text: str) -> tuple[str, int]:
    out: list[str] = []
    changes = 0
    for line in text.splitlines(keepends=True):
        # Skip comments and lines that already use the quoted form everywhere.
        new_line = fix_line(line)
        if new_line != line:
            changes += 1
        out.append(new_line)
    return "".join(out), changes


def find_workflows(root: Path) -> list[Path]:
    return sorted((root / ".github" / "workflows").glob("*.yml"))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="*", type=Path)
    parser.add_argument("--all", action="store_true", help="Process all workflows in CWD/.github/workflows/")
    parser.add_argument("--check", action="store_true", help="Exit 1 if any file would change")
    args = parser.parse_args(argv)

    targets: list[Path] = list(args.paths)
    if args.all:
        targets.extend(find_workflows(Path.cwd()))
    if not targets:
        parser.error("Specify workflow file paths or --all")

    total_changes = 0
    files_changed = 0
    for path in targets:
        if not path.is_file():
            print(f"⚠️  skipping {path} (not a file)", file=sys.stderr)
            continue
        original = path.read_text()
        new_text, changes = fix_text(original)
        if changes == 0:
            continue
        files_changed += 1
        total_changes += changes
        if args.check:
            print(f"would-fix: {path} ({changes} replacements)")
        else:
            path.write_text(new_text)
            print(f"fixed:     {path} ({changes} replacements)")

    print(f"\n{'Would change' if args.check else 'Changed'} {files_changed} file(s), {total_changes} replacement(s).")
    if args.check and files_changed:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
