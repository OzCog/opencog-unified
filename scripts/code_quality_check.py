#!/usr/bin/env python3
"""
Comprehensive Code Quality Checker for OpenCog Unified
Analyzes code quality metrics and generates actionable reports
"""

import json
import re
from collections import defaultdict
from pathlib import Path


class CodeQualityChecker:
    def __init__(self, repo_path: str):
        """__init__ implementation."""
        self.repo_path = Path(repo_path)
        self.metrics = defaultdict(dict)
        self.issues = []

    def check_todo_fixme(self) -> dict[str, int]:
        """Count TODO, FIXME, and similar markers"""
        patterns = {
            "TODO": r"TODO|@todo",
            "FIXME": r"FIXME|@fixme",
            "XXX": r"XXX",
            "HACK": r"HACK",
            "PLACEHOLDER": r"PLACEHOLDER|placeholder",
            "BUG": r"BUG|@bug",
            "OPTIMIZE": r"OPTIMIZE|@optimize",
        }

        counts = defaultdict(int)
        files_with_markers = defaultdict(list)

        for ext in ["*.cpp", "*.h", "*.py", "*.scm", "*.cmake"]:
            for file_path in self.repo_path.rglob(ext):
                if "build" in str(file_path) or ".git" in str(file_path):
                    continue

                try:
                    with open(file_path, encoding="utf-8", errors="ignore") as f:
                        content = f.read()

                    for marker, pattern in patterns.items():
                        matches = re.findall(pattern, content, re.IGNORECASE)
                        if matches:
                            counts[marker] += len(matches)
                            rel_path = file_path.relative_to(self.repo_path)
                            files_with_markers[marker].append(str(rel_path))
                except Exception:
                    pass

        self.metrics["markers"] = dict(counts)
        self.metrics["files_with_markers"] = {k: v[:10] for k, v in files_with_markers.items()}

        return dict(counts)

    def check_code_complexity(self) -> dict[str, any]:
        """Analyze code complexity metrics"""
        complexity = {
            "total_files": 0,
            "total_lines": 0,
            "code_lines": 0,
            "comment_lines": 0,
            "blank_lines": 0,
        }

        for ext in ["*.cpp", "*.h", "*.py", "*.scm"]:
            for file_path in self.repo_path.rglob(ext):
                if "build" in str(file_path) or ".git" in str(file_path):
                    continue

                try:
                    with open(file_path, encoding="utf-8", errors="ignore") as f:
                        lines = f.readlines()

                    complexity["total_files"] += 1
                    complexity["total_lines"] += len(lines)

                    for line in lines:
                        stripped = line.strip()
                        if not stripped:
                            complexity["blank_lines"] += 1
                        elif stripped.startswith("//") or stripped.startswith("#"):
                            complexity["comment_lines"] += 1
                        else:
                            complexity["code_lines"] += 1
                except Exception:
                    pass

        if complexity["total_lines"] > 0:
            complexity["comment_ratio"] = complexity["comment_lines"] / complexity["total_lines"]

        self.metrics["complexity"] = complexity
        return complexity

    def check_documentation(self) -> dict[str, list[str]]:
        """Check for missing or incomplete documentation"""
        missing_docs = []

        # Check for README files in major components
        major_components = [
            "cogutil",
            "atomspace",
            "cogserver",
            "attention",
            "ure",
            "miner",
            "pln",
            "spacetime",
            "unify",
        ]

        for component in major_components:
            component_path = self.repo_path / component
            if component_path.exists():
                readme_path = component_path / "README.md"
                if not readme_path.exists():
                    missing_docs.append(f"{component}/README.md")

        # Check for undocumented C++ headers
        undocumented_headers = []
        for header in self.repo_path.rglob("*.h"):
            if "build" in str(header) or ".git" in str(header):
                continue

            try:
                with open(header, encoding="utf-8", errors="ignore") as f:
                    content = f.read()

                # Check for Doxygen-style comments
                if not re.search(r"/\*\*|\*\s*@brief|///\s*@brief", content):
                    rel_path = header.relative_to(self.repo_path)
                    undocumented_headers.append(str(rel_path))
            except Exception:
                pass

        self.metrics["documentation"] = {
            "missing_readmes": missing_docs,
            "undocumented_headers": undocumented_headers[:20],
            "undocumented_headers_count": len(undocumented_headers),
        }

        return self.metrics["documentation"]

    def check_code_style(self) -> dict[str, any]:
        """Check code style consistency"""
        style_issues = {
            "long_lines": 0,
            "trailing_whitespace": 0,
            "mixed_indentation": 0,
            "missing_newline_eof": 0,
        }

        for ext in ["*.cpp", "*.h", "*.py"]:
            for file_path in self.repo_path.rglob(ext):
                if "build" in str(file_path) or ".git" in str(file_path):
                    continue

                try:
                    with open(file_path, encoding="utf-8", errors="ignore") as f:
                        lines = f.readlines()

                    for _i, line in enumerate(lines):
                        # Check line length (120 chars)
                        if len(line.rstrip()) > 120:
                            style_issues["long_lines"] += 1

                        # Check trailing whitespace
                        if line.rstrip() != line.rstrip("\n").rstrip("\r"):
                            style_issues["trailing_whitespace"] += 1

                        # Check mixed indentation
                        if "\t" in line and "    " in line:
                            style_issues["mixed_indentation"] += 1

                    # Check for newline at EOF
                    if lines and not lines[-1].endswith("\n"):
                        style_issues["missing_newline_eof"] += 1

                except Exception:
                    pass

        self.metrics["style"] = style_issues
        return style_issues

    def check_security_patterns(self) -> list[dict[str, str]]:
        """Check for common security anti-patterns"""
        security_issues = []

        patterns = {
            "unsafe_functions": r"\b(strcpy|strcat|sprintf|gets)\s*\(",
            "hardcoded_secrets": r'(password|secret|api_key)\s*=\s*["\'][^"\']+["\']',
            "sql_injection": r"(execute|query)\s*\([^)]*\+[^)]*\)",
            "command_injection": r"(system|exec|popen)\s*\([^)]*\+[^)]*\)",
        }

        for ext in ["*.cpp", "*.h", "*.py"]:
            for file_path in self.repo_path.rglob(ext):
                if "build" in str(file_path) or ".git" in str(file_path):
                    continue

                try:
                    with open(file_path, encoding="utf-8", errors="ignore") as f:
                        content = f.read()

                    for issue_type, pattern in patterns.items():
                        matches = re.finditer(pattern, content, re.IGNORECASE)
                        for match in matches:
                            rel_path = file_path.relative_to(self.repo_path)
                            security_issues.append(
                                {"type": issue_type, "file": str(rel_path), "snippet": match.group(0)}
                            )
                except Exception:
                    pass

        self.metrics["security"] = security_issues[:20]
        return security_issues

    def generate_report(self) -> dict:
        """Generate comprehensive quality report"""
        print("🔍 Analyzing code quality...")

        print("  ➤ Checking TODO/FIXME markers...")
        markers = self.check_todo_fixme()

        print("  ➤ Analyzing code complexity...")
        complexity = self.check_code_complexity()

        print("  ➤ Checking documentation...")
        documentation = self.check_documentation()

        print("  ➤ Checking code style...")
        style = self.check_code_style()

        print("  ➤ Checking security patterns...")
        security = self.check_security_patterns()

        report = {
            "summary": {
                "total_markers": sum(markers.values()),
                "total_files": complexity["total_files"],
                "total_lines": complexity["total_lines"],
                "comment_ratio": complexity.get("comment_ratio", 0),
                "missing_docs": len(documentation["missing_readmes"]),
                "style_issues": sum(style.values()),
                "security_issues": len(security),
            },
            "details": self.metrics,
            "recommendations": self._generate_recommendations(),
        }

        return report

    def _generate_recommendations(self) -> list[str]:
        """Generate actionable recommendations"""
        recommendations = []

        markers = self.metrics.get("markers", {})
        if markers.get("TODO", 0) > 100:
            recommendations.append("High number of TODOs detected. Consider creating GitHub issues for tracking.")

        if markers.get("FIXME", 0) > 50:
            recommendations.append("Many FIXMEs found. Prioritize resolving critical bugs.")

        complexity = self.metrics.get("complexity", {})
        if complexity.get("comment_ratio", 0) < 0.1:
            recommendations.append("Low comment ratio. Improve code documentation.")

        style = self.metrics.get("style", {})
        if style.get("long_lines", 0) > 100:
            recommendations.append("Many long lines detected. Consider using a code formatter.")

        if style.get("trailing_whitespace", 0) > 50:
            recommendations.append("Trailing whitespace detected. Configure editor to remove on save.")

        security = self.metrics.get("security", [])
        if len(security) > 0:
            recommendations.append("Security issues detected. Review and address immediately.")

        documentation = self.metrics.get("documentation", {})
        if len(documentation.get("missing_readmes", [])) > 0:
            recommendations.append("Missing README files in major components. Add documentation.")

        return recommendations


def main():
    """main implementation."""
    repo_path = "/home/ubuntu/opencog-unified"

    print("=" * 60)
    print("OpenCog Unified - Code Quality Analysis")
    print("=" * 60)
    print()

    checker = CodeQualityChecker(repo_path)
    report = checker.generate_report()

    # Save report
    output_path = Path(repo_path) / "code_quality_report.json"
    with open(output_path, "w") as f:
        json.dump(report, f, indent=2)

    # Print summary
    print()
    print("=" * 60)
    print("Summary")
    print("=" * 60)
    for key, value in report["summary"].items():
        print(f"  {key}: {value}")

    print()
    print("=" * 60)
    print("Recommendations")
    print("=" * 60)
    for i, rec in enumerate(report["recommendations"], 1):
        print(f"  {i}. {rec}")

    print()
    print(f"✅ Full report saved to: {output_path}")
    print()


if __name__ == "__main__":
    main()
