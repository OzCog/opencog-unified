#!/usr/bin/env python3
"""
Comprehensive Placeholder Detection Script
Finds all TODO, FIXME, XXX, NotImplementedError, stub implementations, and empty functions
"""

import json
import re
from collections import defaultdict
from pathlib import Path


class PlaceholderDetector:
    def __init__(self, repo_root):
        self.repo_root = Path(repo_root)
        self.placeholders = []

        # Patterns to detect
        self.patterns = {
            "TODO": r"(//|#|;|/\*)\s*TODO[:\s]",
            "FIXME": r"(//|#|;|/\*)\s*(FIXME|XXX)[:\s]",
            "NotImplementedError": r"(raise\s+NotImplementedError|throw.*not.*implemented)",
            "pass_only": r"def\s+\w+\([^)]*\):\s*pass\s*$",
            "empty_function": r"def\s+\w+\([^)]*\):\s*\.\.\.\s*$",
            "stub": r"(//|#|;)\s*STUB[:\s]",
        }

    def scan_file(self, filepath):
        """Scan a single file for placeholders"""
        try:
            with open(filepath, encoding="utf-8", errors="ignore") as f:
                lines = f.readlines()

            for i, line in enumerate(lines, 1):
                for ptype, pattern in self.patterns.items():
                    if re.search(pattern, line, re.IGNORECASE):
                        # Skip if it's in a string or comment about placeholders
                        if "placeholder" in line.lower() and "find" in line.lower():
                            continue

                        self.placeholders.append(
                            {
                                "file": str(filepath.relative_to(self.repo_root)),
                                "line": i,
                                "type": ptype,
                                "content": line.strip(),
                                "context": self._get_context(lines, i - 1),
                            }
                        )
        except Exception:
            pass

    def _get_context(self, lines, line_idx, context_size=3):
        """Get surrounding context for a placeholder"""
        start = max(0, line_idx - context_size)
        end = min(len(lines), line_idx + context_size + 1)
        return "".join(lines[start:end])

    def scan_repository(self):
        """Scan entire repository"""
        extensions = {".py", ".cc", ".cpp", ".h", ".hpp", ".scm", ".c"}

        for ext in extensions:
            for filepath in self.repo_root.rglob(f"*{ext}"):
                # Skip certain directories
                if any(skip in str(filepath) for skip in ["build", ".git", "__pycache__", "node_modules"]):
                    continue
                self.scan_file(filepath)

    def categorize_by_type(self):
        """Categorize placeholders by type"""
        by_type = defaultdict(list)
        for p in self.placeholders:
            by_type[p["type"]].append(p)
        return dict(by_type)

    def categorize_by_file(self):
        """Categorize placeholders by file"""
        by_file = defaultdict(list)
        for p in self.placeholders:
            by_file[p["file"]].append(p)
        return dict(by_file)

    def generate_report(self):
        """Generate comprehensive report"""
        by_type = self.categorize_by_type()
        by_file = self.categorize_by_file()

        report = {
            "total_placeholders": len(self.placeholders),
            "by_type": {k: len(v) for k, v in by_type.items()},
            "by_file_count": len(by_file),
            "detailed_placeholders": self.placeholders,
            "summary_by_type": by_type,
            "files_with_most_placeholders": sorted(
                [(f, len(items)) for f, items in by_file.items()], key=lambda x: x[1], reverse=True
            )[:20],
        }

        return report


if __name__ == "__main__":
    detector = PlaceholderDetector("/home/ubuntu/opencog-unified")
    print("Scanning repository for placeholders...")
    detector.scan_repository()
    print(f"Found {len(detector.placeholders)} placeholders")

    report = detector.generate_report()

    # Save to JSON
    with open("placeholder_analysis.json", "w") as f:
        json.dump(report, f, indent=2)

    print("\nPlaceholder Summary:")
    print(f"Total: {report['total_placeholders']}")
    print("\nBy Type:")
    for ptype, count in sorted(report["by_type"].items(), key=lambda x: x[1], reverse=True):
        print(f"  {ptype}: {count}")

    print("\nTop 10 Files with Most Placeholders:")
    for filename, count in report["files_with_most_placeholders"][:10]:
        print(f"  {filename}: {count}")
