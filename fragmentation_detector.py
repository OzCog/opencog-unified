#!/usr/bin/env python3
"""
Fragmentation Detector for OpenCog Unified

Identifies specific fragmented aspects of the cognitive architecture
by analyzing TODO/FIXME/STUB markers and their context.
"""

import json
import re
from collections import defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass
class CodeFragment:
    """Represents a specific code fragmentation"""

    file_path: str
    line_number: int
    marker_type: str  # TODO, FIXME, STUB
    content: str
    context_before: list[str]
    context_after: list[str]
    component: str
    severity: float
    category: str
    repair_suggestion: str


class FragmentationDetector:
    """Detects and categorizes fragmented code"""

    # Severity keywords
    HIGH_SEVERITY_KEYWORDS = ["critical", "urgent", "blocking", "broken", "crash", "security"]
    MEDIUM_SEVERITY_KEYWORDS = ["important", "needed", "should", "must"]

    # Category patterns
    CATEGORIES = {
        "thread_safety": r"\b(thread|race|lock|mutex|atomic|concurrent)\b",
        "performance": r"\b(optimize|slow|performance|faster|efficient)\b",
        "integration": r"\b(integrate|dependency|link|connect)\b",
        "implementation": r"\b(implement|complete|finish|add)\b",
        "error_handling": r"\b(error|exception|check|validate)\b",
        "testing": r"\b(test|unittest|coverage)\b",
        "documentation": r"\b(document|comment|explain)\b",
    }

    def __init__(self, repo_path: Path):
        self.repo_path = repo_path
        self.fragments: list[CodeFragment] = []

    def detect_all_fragments(self) -> list[CodeFragment]:
        """Detect all code fragmentations in repository"""
        print("🔍 Detecting Code Fragmentations...")

        extensions = [".cc", ".h", ".cpp", ".hpp", ".scm", ".py"]

        for ext in extensions:
            for file_path in self.repo_path.rglob(f"*{ext}"):
                if self._should_skip_file(file_path):
                    continue

                self._scan_file(file_path)

        print(f"  Found {len(self.fragments)} fragmentations")
        return self.fragments

    def _should_skip_file(self, file_path: Path) -> bool:
        """Check if file should be skipped"""
        skip_dirs = [".git", "build", "node_modules", "__pycache__", ".venv"]
        return any(skip in file_path.parts for skip in skip_dirs)

    def _scan_file(self, file_path: Path):
        """Scan a single file for fragmentations"""
        try:
            with open(file_path, encoding="utf-8", errors="ignore") as f:
                lines = f.readlines()

            for i, line in enumerate(lines):
                # Check for TODO/FIXME/STUB
                for marker in ["TODO", "FIXME", "STUB"]:
                    if re.search(rf"\b{marker}\b", line, re.IGNORECASE):
                        fragment = self._create_fragment(file_path, i, marker, line, lines)
                        if fragment:
                            self.fragments.append(fragment)
                        break  # Only one marker per line

        except Exception:
            pass  # Skip files that can't be read

    def _create_fragment(
        self, file_path: Path, line_num: int, marker: str, line: str, all_lines: list[str]
    ) -> CodeFragment:
        """Create a CodeFragment from marker"""
        # Extract comment content
        content = self._extract_comment_content(line, marker)

        # Get context
        context_before = all_lines[max(0, line_num - 3) : line_num]
        context_after = all_lines[line_num + 1 : min(len(all_lines), line_num + 4)]

        # Determine component
        component = self._determine_component(file_path)

        # Calculate severity
        severity = self._calculate_severity(marker, content)

        # Categorize
        category = self._categorize_fragment(content)

        # Generate repair suggestion
        repair_suggestion = self._suggest_repair(marker, content, category)

        return CodeFragment(
            file_path=str(file_path.relative_to(self.repo_path)),
            line_number=line_num + 1,
            marker_type=marker,
            content=content,
            context_before=[l.rstrip() for l in context_before],
            context_after=[l.rstrip() for l in context_after],
            component=component,
            severity=severity,
            category=category,
            repair_suggestion=repair_suggestion,
        )

    def _extract_comment_content(self, line: str, marker: str) -> str:
        """Extract comment text after marker"""
        # Find marker and extract rest of line
        match = re.search(rf"{marker}[\s:]*(.+)", line, re.IGNORECASE)
        if match:
            return match.group(1).strip()
        return ""

    def _determine_component(self, file_path: Path) -> str:
        """Determine which component this file belongs to"""
        parts = file_path.relative_to(self.repo_path).parts
        if len(parts) > 0:
            return parts[0]
        return "unknown"

    def _calculate_severity(self, marker: str, content: str) -> float:
        """Calculate severity score 0.0-1.0"""
        content_lower = content.lower()

        # Base severity by marker type
        base_severity = {
            "FIXME": 0.7,
            "TODO": 0.5,
            "STUB": 0.6,
        }.get(marker, 0.5)

        # Adjust for keywords
        if any(kw in content_lower for kw in self.HIGH_SEVERITY_KEYWORDS):
            return min(1.0, base_severity + 0.3)
        elif any(kw in content_lower for kw in self.MEDIUM_SEVERITY_KEYWORDS):
            return min(1.0, base_severity + 0.15)

        return base_severity

    def _categorize_fragment(self, content: str) -> str:
        """Categorize the fragmentation"""
        content_lower = content.lower()

        for category, pattern in self.CATEGORIES.items():
            if re.search(pattern, content_lower):
                return category

        return "general"

    def _suggest_repair(self, marker: str, content: str, category: str) -> str:
        """Generate repair suggestion"""
        suggestions = {
            "thread_safety": "Review for thread-safety issues and implement proper locking/synchronization",
            "performance": "Profile code and optimize critical paths",
            "integration": "Implement integration with dependent components",
            "implementation": "Complete implementation of described functionality",
            "error_handling": "Add robust error handling and validation",
            "testing": "Write comprehensive tests for this functionality",
            "documentation": "Document the code with clear comments and usage examples",
            "general": "Address the noted issue or complete the implementation",
        }

        return suggestions.get(category, suggestions["general"])

    def generate_report(self) -> dict:
        """Generate comprehensive fragmentation report"""
        report = {
            "total_fragments": len(self.fragments),
            "by_component": self._group_by_component(),
            "by_category": self._group_by_category(),
            "by_severity": self._group_by_severity(),
            "critical_fragments": self._get_critical_fragments(),
            "top_fragmented_components": self._get_top_fragmented(),
        }
        return report

    def _group_by_component(self) -> dict:
        """Group fragments by component"""
        grouped = defaultdict(list)
        for fragment in self.fragments:
            grouped[fragment.component].append(asdict(fragment))
        return dict(grouped)

    def _group_by_category(self) -> dict:
        """Group fragments by category"""
        grouped = defaultdict(list)
        for fragment in self.fragments:
            grouped[fragment.category].append(asdict(fragment))
        return dict(grouped)

    def _group_by_severity(self) -> dict:
        """Group fragments by severity level"""
        levels = {"critical": [], "high": [], "medium": [], "low": []}

        for fragment in self.fragments:
            if fragment.severity >= 0.8:
                levels["critical"].append(asdict(fragment))
            elif fragment.severity >= 0.6:
                levels["high"].append(asdict(fragment))
            elif fragment.severity >= 0.4:
                levels["medium"].append(asdict(fragment))
            else:
                levels["low"].append(asdict(fragment))

        return levels

    def _get_critical_fragments(self, top_n: int = 50) -> list[dict]:
        """Get top N critical fragments"""
        sorted_fragments = sorted(self.fragments, key=lambda f: f.severity, reverse=True)
        return [asdict(f) for f in sorted_fragments[:top_n]]

    def _get_top_fragmented(self, top_n: int = 10) -> list[dict]:
        """Get top N most fragmented components"""
        component_counts = defaultdict(int)
        component_severity = defaultdict(float)

        for fragment in self.fragments:
            component_counts[fragment.component] += 1
            component_severity[fragment.component] += fragment.severity

        # Calculate average severity per component
        component_metrics = []
        for component, count in component_counts.items():
            avg_severity = component_severity[component] / count
            component_metrics.append(
                {
                    "component": component,
                    "fragment_count": count,
                    "average_severity": avg_severity,
                    "total_severity": component_severity[component],
                }
            )

        # Sort by total severity
        sorted_metrics = sorted(component_metrics, key=lambda x: x["total_severity"], reverse=True)

        return sorted_metrics[:top_n]


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description="Detect code fragmentations in OpenCog Unified")
    parser.add_argument("--repo-path", default=".", help="Path to repository")
    parser.add_argument("--output", default="fragmentations.json", help="Output JSON file")

    args = parser.parse_args()

    detector = FragmentationDetector(Path(args.repo_path))
    detector.detect_all_fragments()
    report = detector.generate_report()

    # Save report
    output_path = Path(args.repo_path) / args.output
    with open(output_path, "w") as f:
        json.dump(report, f, indent=2)

    print(f"\n💾 Saved fragmentation report: {args.output}")
    print(f"\nTotal Fragmentations: {report['total_fragments']}")
    print(f"Critical: {len(report['by_severity']['critical'])}")
    print(f"High: {len(report['by_severity']['high'])}")
    print(f"Medium: {len(report['by_severity']['medium'])}")
    print(f"Low: {len(report['by_severity']['low'])}")

    print("\nTop 10 Most Fragmented Components:")
    for i, comp in enumerate(report["top_fragmented_components"][:10], 1):
        print(
            f"  {i}. {comp['component']}: {comp['fragment_count']} fragments "
            f"(avg severity: {comp['average_severity']:.2f})"
        )


if __name__ == "__main__":
    main()
