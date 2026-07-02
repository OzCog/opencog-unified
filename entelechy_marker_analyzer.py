#!/usr/bin/env python3
"""
Entelechy Marker Analyzer

Comprehensive analysis tool for all code markers (TODO, FIXME, STUB, PLACEHOLDER, etc.)
that contribute to entelechy fragmentation. This tool provides:

1. Complete marker inventory across all file types
2. Categorization by type, severity, and component
3. Actionable resolution roadmap
4. Progress tracking capabilities
5. Integration with entelechy metrics

Part of the Entelechy Framework for self-actualizing cognitive systems.
"""

import json
import re
from collections import defaultdict
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path


@dataclass
class CodeMarker:
    """Represents a single code marker (TODO, FIXME, etc.)."""

    file_path: str
    line_number: int
    marker_type: str  # TODO, FIXME, STUB, PLACEHOLDER, etc.
    content: str
    context_before: list[str]
    context_after: list[str]
    component: str
    severity: float  # 0.0-1.0
    category: str
    estimated_effort: str
    repair_suggestion: str

    def to_dict(self):
        return asdict(self)


class EntelechyMarkerAnalyzer:
    """Analyzes code markers to assess entelechy fragmentation."""

    # Configuration constants
    ESTIMATED_LOC_DIVISOR = 1000  # Estimated lines of code for density calculation
    ACTUALIZATION_IMPACT_MULTIPLIER = 0.3  # Factor for converting fragmentation to actualization inhibition

    # Marker patterns to search for
    MARKER_PATTERNS = {
        "TODO": r"(?://|#|;|/\*|\*)\s*TODO[:;\s]",
        "FIXME": r"(?://|#|;|/\*|\*)\s*(?:FIXME|XXX)[:;\s]",
        "STUB": r"(?://|#|;|/\*|\*)\s*STUB[:;\s]",
        "PLACEHOLDER": r"(?://|#|;|/\*|\*)\s*PLACEHOLDER[:;\s]",
        "NOT_IMPLEMENTED": r"(?://|#|;|/\*|\*)\s*NOT\s+IMPLEMENTED",
        "MOCK": r"(?://|#|;|/\*|\*)\s*MOCK[:;\s]",
        "HACK": r"(?://|#|;|/\*|\*)\s*HACK[:;\s]",
        "BUG": r"(?://|#|;|/\*|\*)\s*BUG[:;\s]",
    }

    # File extensions to analyze
    FILE_EXTENSIONS = {".cc", ".cpp", ".h", ".hpp", ".c", ".scm", ".py", ".js", ".ts"}

    # Directories to exclude
    EXCLUDE_DIRS = {
        ".git",
        "build",
        "Testing",
        "node_modules",
        "__pycache__",
        ".pytest_cache",
        "venv",
        "env",
        "dist",
        "target",
    }

    def __init__(self, repo_root: str):
        self.repo_root = Path(repo_root)
        self.markers: list[CodeMarker] = []
        self.component_map = self._build_component_map()

    def _build_component_map(self) -> dict[str, str]:
        """Build a mapping of directories to component names."""
        component_dirs = [
            "cogutil",
            "atomspace",
            "cogserver",
            "atomspace-rocks",
            "atomspace-restful",
            "unify",
            "ure",
            "attention",
            "spacetime",
            "pln",
            "miner",
            "asmoses",
            "moses",
            "lg-atomese",
            "learn",
            "language-learning",
            "opencog",
        ]
        return {comp: comp for comp in component_dirs}

    def analyze_repository(self):
        """Scan the entire repository for code markers."""
        print("🔍 Scanning repository for code markers...")

        for file_path in self._get_source_files():
            self._analyze_file(file_path)

        print(f"✓ Found {len(self.markers)} code markers")

    def _get_source_files(self) -> list[Path]:
        """Get all source files to analyze."""
        source_files = []

        for ext in self.FILE_EXTENSIONS:
            for file_path in self.repo_root.rglob(f"*{ext}"):
                # Check if file is in an excluded directory
                if any(excl in file_path.parts for excl in self.EXCLUDE_DIRS):
                    continue
                source_files.append(file_path)

        return source_files

    def _analyze_file(self, file_path: Path):
        """Analyze a single file for code markers."""
        try:
            with open(file_path, encoding="utf-8", errors="ignore") as f:
                lines = f.readlines()

            for line_num, line in enumerate(lines, start=1):
                for marker_type, pattern in self.MARKER_PATTERNS.items():
                    if re.search(pattern, line, re.IGNORECASE):
                        # Avoid false positives from meta-comments
                        if self._is_meta_comment(line):
                            continue

                        marker = self._create_marker(file_path, line_num, marker_type, line, lines)
                        self.markers.append(marker)

        except Exception as e:
            print(f"Warning: Could not analyze {file_path}: {e}")

    # Configuration constants
    META_COMMENT_THRESHOLD = 2  # Minimum indicator words to classify as meta-comment

    def _is_meta_comment(self, line: str) -> bool:
        """Check if this is a meta-comment about markers rather than an actual marker."""
        line_lower = line.lower()

        # Skip comments about marker processing
        meta_patterns = [
            "marker",
            "pattern",
            "search",
            "analyze",
            "catalog",
            "report",
            "verification",
            "check for",
            "look for",
            "contain",
            "skip",
            "meta-comment",
            "false positive",
            "template",
            "example",
        ]

        # If line contains multiple indicator words, it's likely meta
        meta_count = sum(1 for pattern in meta_patterns if pattern in line_lower)
        if meta_count >= self.META_COMMENT_THRESHOLD:
            return True

        # Skip lines with template variables
        return bool("{" in line and "}" in line)

    def _create_marker(
        self, file_path: Path, line_num: int, marker_type: str, line: str, all_lines: list[str]
    ) -> CodeMarker:
        """Create a CodeMarker object from detected marker."""

        # Extract context
        context_start = max(0, line_num - 3)
        context_end = min(len(all_lines), line_num + 2)
        context_before = [all_lines[i].strip() for i in range(context_start, line_num - 1)]
        context_after = [all_lines[i].strip() for i in range(line_num, context_end)]

        # Extract marker content
        content = self._extract_marker_content(line)

        # Determine component
        rel_path = file_path.relative_to(self.repo_root)
        component = self._get_component(rel_path)

        # Calculate severity and categorize
        severity = self._calculate_severity(marker_type, content)
        category = self._categorize_marker(marker_type, content)
        effort = self._estimate_effort(marker_type, category, severity)
        suggestion = self._generate_suggestion(marker_type, category)

        return CodeMarker(
            file_path=str(rel_path),
            line_number=line_num,
            marker_type=marker_type,
            content=content,
            context_before=context_before,
            context_after=context_after,
            component=component,
            severity=severity,
            category=category,
            estimated_effort=effort,
            repair_suggestion=suggestion,
        )

    def _extract_marker_content(self, line: str) -> str:
        """Extract the actual content of the marker comment."""
        # Remove comment syntax and marker keyword
        content = re.sub(
            r"^[/\*#;\s]*(?:TODO|FIXME|XXX|STUB|PLACEHOLDER|NOT\s+IMPLEMENTED|MOCK|HACK|BUG)[:;\s]*",
            "",
            line,
            flags=re.IGNORECASE,
        )
        return content.strip()

    def _get_component(self, rel_path: Path) -> str:
        """Determine which component a file belongs to."""
        parts = rel_path.parts
        if len(parts) > 0:
            first_dir = parts[0]
            if first_dir in self.component_map:
                return self.component_map[first_dir]
        return "root"

    def _calculate_severity(self, marker_type: str, content: str) -> float:
        """Calculate severity score (0.0-1.0) based on marker type and content."""
        base_severity = {
            "BUG": 0.95,
            "FIXME": 0.85,
            "NOT_IMPLEMENTED": 0.80,
            "STUB": 0.75,
            "PLACEHOLDER": 0.70,
            "TODO": 0.60,
            "HACK": 0.65,
            "MOCK": 0.55,
        }

        severity = base_severity.get(marker_type, 0.60)

        # Increase severity for critical keywords
        critical_keywords = ["critical", "urgent", "broken", "fails", "crash", "security"]
        if any(kw in content.lower() for kw in critical_keywords):
            severity = min(1.0, severity + 0.15)

        return severity

    def _categorize_marker(self, marker_type: str, content: str) -> str:
        """Categorize the marker by what kind of work is needed."""
        content_lower = content.lower()

        if "document" in content_lower or "comment" in content_lower or "explain" in content_lower:
            return "documentation"
        elif "test" in content_lower:
            return "testing"
        elif "performance" in content_lower or "optimize" in content_lower:
            return "performance"
        elif "refactor" in content_lower or "cleanup" in content_lower:
            return "refactoring"
        elif "implement" in content_lower or "stub" in marker_type.lower() or "placeholder" in marker_type.lower():
            return "implementation"
        elif "bug" in content_lower or "fix" in content_lower or marker_type == "BUG":
            return "bug_fix"
        elif "design" in content_lower or "architecture" in content_lower:
            return "design"
        else:
            return "general"

    def _estimate_effort(self, marker_type: str, category: str, severity: float) -> str:
        """Estimate effort required to resolve."""
        if category == "documentation":
            return "1-2 hours"
        elif category == "testing":
            return "4-8 hours"
        elif category == "bug_fix":
            return "1-3 days"
        elif category == "performance":
            return "3-7 days"
        elif category == "implementation":
            if marker_type in ["STUB", "PLACEHOLDER", "NOT_IMPLEMENTED"]:
                return "1-2 weeks"
            else:
                return "3-7 days"
        elif category == "design":
            return "2-4 weeks"
        else:
            return "1-5 days"

    def _generate_suggestion(self, marker_type: str, category: str) -> str:
        """Generate a repair suggestion."""
        suggestions = {
            "documentation": "Add comprehensive documentation explaining the code",
            "testing": "Write unit and integration tests",
            "bug_fix": "Identify root cause and implement fix with tests",
            "performance": "Profile code and implement optimizations",
            "implementation": "Complete the implementation with proper error handling",
            "refactoring": "Refactor code for clarity and maintainability",
            "design": "Review and update architectural design",
            "general": "Address the noted issue or complete the implementation",
        }
        return suggestions.get(category, "Review and address marker")

    def generate_report(self) -> dict:
        """Generate comprehensive entelechy fragmentation report."""

        # Group markers by various dimensions
        by_type = defaultdict(list)
        by_component = defaultdict(list)
        by_category = defaultdict(list)
        by_severity = {"critical": [], "high": [], "medium": [], "low": []}

        for marker in self.markers:
            by_type[marker.marker_type].append(marker)
            by_component[marker.component].append(marker)
            by_category[marker.category].append(marker)

            # Categorize by severity
            if marker.severity >= 0.8:
                by_severity["critical"].append(marker)
            elif marker.severity >= 0.7:
                by_severity["high"].append(marker)
            elif marker.severity >= 0.6:
                by_severity["medium"].append(marker)
            else:
                by_severity["low"].append(marker)

        # Calculate statistics
        total_markers = len(self.markers)
        avg_severity = sum(m.severity for m in self.markers) / total_markers if total_markers > 0 else 0

        # Calculate entelechy impact
        fragmentation_density = total_markers / self.ESTIMATED_LOC_DIVISOR if total_markers > 0 else 0
        entelechy_impact = min(1.0, fragmentation_density / 5.0)  # normalize to 0-1
        actualization_inhibition = entelechy_impact * self.ACTUALIZATION_IMPACT_MULTIPLIER

        report = {
            "timestamp": datetime.now().isoformat() + "Z",
            "summary": {
                "total_markers": total_markers,
                "average_severity": round(avg_severity, 3),
                "fragmentation_density": round(fragmentation_density, 3),
                "entelechy_impact": round(entelechy_impact, 3),
                "actualization_inhibition": round(actualization_inhibition, 3),
            },
            "by_type": {k: len(v) for k, v in by_type.items()},
            "by_component": {k: len(v) for k, v in by_component.items()},
            "by_category": {k: len(v) for k, v in by_category.items()},
            "by_severity": {k: len(v) for k, v in by_severity.items()},
            "markers": [m.to_dict() for m in self.markers],
            "repair_roadmap": self._generate_repair_roadmap(by_severity, by_category, by_component),
        }

        return report

    def _generate_repair_roadmap(self, by_severity: dict, by_category: dict, by_component: dict) -> dict:
        """Generate actionable repair roadmap."""

        roadmap = {
            "immediate_actions": [],
            "short_term_actions": [],
            "medium_term_actions": [],
            "long_term_actions": [],
        }

        # Immediate: Critical severity items
        critical_markers = by_severity["critical"]
        if critical_markers:
            for marker in sorted(critical_markers, key=lambda m: m.severity, reverse=True)[:10]:
                roadmap["immediate_actions"].append(
                    {
                        "priority": "CRITICAL",
                        "location": f"{marker.file_path}:{marker.line_number}",
                        "type": marker.marker_type,
                        "description": marker.content[:100],
                        "suggestion": marker.repair_suggestion,
                        "effort": marker.estimated_effort,
                    }
                )

        # Short-term: High severity and documentation items
        high_markers = by_severity["high"]
        doc_markers = by_category.get("documentation", [])

        if high_markers:
            roadmap["short_term_actions"].append(
                {
                    "description": f"Resolve {len(high_markers)} high-severity markers",
                    "focus": "bug fixes and missing implementations",
                    "estimated_duration": "2-4 weeks",
                }
            )

        if doc_markers:
            roadmap["short_term_actions"].append(
                {
                    "description": f"Complete {len(doc_markers)} documentation items",
                    "focus": "improve code clarity and maintainability",
                    "estimated_duration": "1-2 weeks",
                }
            )

        # Medium-term: Component-based cleanup
        for component, markers in sorted(by_component.items(), key=lambda x: len(x[1]), reverse=True)[:5]:
            if len(markers) > 20:
                roadmap["medium_term_actions"].append(
                    {
                        "description": f"Clean up {component} component",
                        "markers": len(markers),
                        "estimated_duration": "4-8 weeks",
                    }
                )

        # Long-term: Systematic elimination
        roadmap["long_term_actions"].append(
            {
                "description": "Establish zero-marker policy",
                "approach": "Prevent new markers through code review process",
                "goal": "Achieve 100% entelechy actualization",
            }
        )

        return roadmap

    def save_report(self, output_file: str = "entelechy_marker_analysis.json"):
        """Save the analysis report to a file."""
        report = self.generate_report()

        output_path = self.repo_root / output_file
        with open(output_path, "w") as f:
            json.dump(report, f, indent=2)

        print(f"✓ Report saved to {output_file}")
        return report

    def print_summary(self):
        """Print a human-readable summary."""
        report = self.generate_report()
        summary = report["summary"]

        print("\n" + "=" * 70)
        print("🧠 ENTELECHY MARKER ANALYSIS")
        print("=" * 70)
        print(f"Total Markers:            {summary['total_markers']}")
        print(f"Average Severity:         {summary['average_severity']:.1%}")
        print(f"Entelechy Impact:         {summary['entelechy_impact']:.1%}")
        print(f"Actualization Inhibition: {summary['actualization_inhibition']:.1%}")
        print()

        print("By Type:")
        for marker_type, count in sorted(report["by_type"].items(), key=lambda x: x[1], reverse=True):
            print(f"  {marker_type:20} {count:4} markers")
        print()

        print("By Severity:")
        for severity, count in report["by_severity"].items():
            print(f"  {severity.upper():20} {count:4} markers")
        print()

        print("By Category:")
        for category, count in sorted(report["by_category"].items(), key=lambda x: x[1], reverse=True):
            print(f"  {category:20} {count:4} markers")
        print()

        print("Top Components:")
        for component, count in sorted(report["by_component"].items(), key=lambda x: x[1], reverse=True)[:10]:
            print(f"  {component:20} {count:4} markers")
        print()


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Analyze code markers for entelechy fragmentation")
    parser.add_argument(
        "--repo", default="/home/runner/work/opencog-unified/opencog-unified", help="Repository root path"
    )
    parser.add_argument("--output", default="entelechy_marker_analysis.json", help="Output file for detailed report")

    args = parser.parse_args()

    analyzer = EntelechyMarkerAnalyzer(args.repo)
    analyzer.analyze_repository()
    analyzer.save_report(args.output)
    analyzer.print_summary()

    return analyzer


if __name__ == "__main__":
    main()
