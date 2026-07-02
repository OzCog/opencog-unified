#!/usr/bin/env python3
"""
Obsolete Marker Resolution Script

This script identifies and resolves markers indicating obsolete or deprecated code.
It adds proper deprecation notices and documentation rather than just removing files.

Part of the Entelechy Framework repair process - Phase 3.
"""

from datetime import datetime
from pathlib import Path


class ObsoleteMarkerResolver:
    """Resolves obsolete code markers with proper deprecation notices."""

    # Files identified as potentially obsolete
    OBSOLETE_FILES = [
        {
            "file": "components/integration/opencog/opencog/eva/src/btree.scm",
            "replacement": "components/integration/opencog/opencog/eva/src/btree-psi.scm",
            "reason": "Replaced by btree-psi.scm with PSI integration",
            "action": "add_deprecation_notice",
        },
        {
            "file": "components/integration/opencog/opencog/eva/chatbot-eva/imperative-alt.scm",
            "replacement": None,
            "reason": "r2l-sets format changed, code may be outdated",
            "action": "add_review_notice",
        },
    ]

    # Deprecation notice templates
    DEPRECATION_TEMPLATES = {
        ".scm": """;
; DEPRECATED: {reason}
; Replacement: {replacement}
; Date: {date}
;
""",
        ".py": '''"""
DEPRECATED: {reason}
Replacement: {replacement}
Date: {date}
"""

''',
        ".cc": """/**
 * DEPRECATED: {reason}
 * Replacement: {replacement}
 * Date: {date}
 */

""",
        ".h": """/**
 * DEPRECATED: {reason}
 * Replacement: {replacement}
 * Date: {date}
 */

""",
    }

    def __init__(self, repo_root: str = "."):
        self.repo_root = Path(repo_root).resolve()
        self.changes_made = []

    def add_deprecation_notice(self, file_info: dict, dry_run: bool = True) -> bool:
        """Add a deprecation notice to a file."""
        file_path = self.repo_root / file_info["file"]

        if not file_path.exists():
            print(f"  ⚠ File not found: {file_info['file']}")
            return False

        ext = file_path.suffix
        template = self.DEPRECATION_TEMPLATES.get(ext)

        if not template:
            print(f"  ⚠ No template for extension: {ext}")
            return False

        # Read current content
        with open(file_path, encoding="utf-8", errors="ignore") as f:
            content = f.read()

        # Check if already deprecated
        if "DEPRECATED" in content[:500]:
            print(f"  ℹ Already deprecated: {file_info['file']}")
            return False

        # Prepare deprecation notice
        notice = template.format(
            reason=file_info["reason"],
            replacement=file_info.get("replacement", "None specified"),
            date=datetime.now().strftime("%Y-%m-%d"),
        )

        # For Scheme files, preserve any existing shebang or module definition
        if ext == ".scm":
            # Find the first non-comment line that's not empty
            lines = content.split("\n")
            insert_pos = 0
            for i, line in enumerate(lines):
                stripped = line.strip()
                if stripped and not stripped.startswith(";"):
                    insert_pos = i
                    break
            # Insert after initial comments
            new_lines = [*lines[:insert_pos], notice, *lines[insert_pos:]]
            new_content = "\n".join(new_lines)
        else:
            new_content = notice + content

        if dry_run:
            print(f"  [DRY RUN] Would add deprecation notice to: {file_info['file']}")
            return True

        # Write updated content
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)

        self.changes_made.append(
            {"file": file_info["file"], "action": "added_deprecation_notice", "reason": file_info["reason"]}
        )

        print(f"  ✓ Added deprecation notice to: {file_info['file']}")
        return True

    def resolve_all(self, dry_run: bool = True) -> int:
        """Resolve all known obsolete markers."""
        print("\n🔧 Resolving obsolete markers...")
        if dry_run:
            print("   (DRY RUN - no files will be modified)")

        resolved = 0

        for file_info in self.OBSOLETE_FILES:
            action = file_info.get("action", "add_deprecation_notice")

            if action == "add_deprecation_notice":
                if self.add_deprecation_notice(file_info, dry_run):
                    resolved += 1
            elif action == "add_review_notice":
                # Same as deprecation but marks for review
                file_info["reason"] = f"NEEDS REVIEW: {file_info['reason']}"
                if self.add_deprecation_notice(file_info, dry_run):
                    resolved += 1

        return resolved

    def get_summary(self) -> dict:
        """Get summary of changes made."""
        return {"total_changes": len(self.changes_made), "changes": self.changes_made}


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Resolve obsolete markers")
    parser.add_argument("--repo", default=".", help="Repository root")
    parser.add_argument("--apply", action="store_true", help="Apply changes")
    parser.add_argument("--dry-run", action="store_true", default=True, help="Dry run")
    parser.add_argument("--no-dry-run", action="store_true", help="Actually apply")

    args = parser.parse_args()

    resolver = ObsoleteMarkerResolver(args.repo)

    dry_run = not args.no_dry_run
    resolved = resolver.resolve_all(dry_run=dry_run)

    print(f"\n✓ Resolved {resolved} obsolete markers")

    if dry_run:
        print("\nTo apply for real: --apply --no-dry-run")


if __name__ == "__main__":
    main()
