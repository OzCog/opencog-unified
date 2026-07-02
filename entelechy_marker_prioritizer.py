#!/usr/bin/env python3
"""
Entelechy Marker Prioritization Tool

Analyzes code markers (TODO, FIXME, STUB) and prioritizes them based on:
- Component criticality
- Marker context and severity
- Impact on system actualization
"""

import argparse
import json
import os
import re
from collections import defaultdict
from pathlib import Path


class MarkerPrioritizer:
    """Prioritize code markers for systematic resolution"""

    # Component criticality scores (0.0 - 1.0)
    COMPONENT_CRITICALITY = {
        "cogutil": 1.0,  # Foundation - highest priority
        "atomspace": 1.0,  # Core knowledge representation
        "cogserver": 0.9,  # Core server
        "unify": 0.8,  # Logic system
        "ure": 0.8,  # Rule engine
        "attention": 0.7,  # Cognitive system
        "spacetime": 0.7,  # Cognitive system
        "pln": 0.7,  # Advanced reasoning
        "miner": 0.6,  # Pattern mining
        "asmoses": 0.6,  # Learning
        "moses": 0.6,  # Learning
        "learn": 0.5,  # Language learning
        "lg-atomese": 0.5,  # Language
        "language-learning": 0.4,  # Language
        "opencog": 0.8,  # Integration
        "tests": 0.3,  # Testing infrastructure
        "scripts": 0.2,  # Utility scripts
        "documentation": 0.1,  # Documentation
    }

    # Marker type urgency (0.0 - 1.0)
    MARKER_URGENCY = {
        "FIXME": 1.0,  # Highest - indicates broken/incorrect code
        "BUG": 1.0,  # Highest - actual bugs
        "STUB": 0.8,  # High - incomplete implementations
        "NOT_IMPLEMENTED": 0.8,  # High - missing functionality
        "HACK": 0.7,  # Medium-high - technical debt
        "TODO": 0.5,  # Medium - future work
        "PLACEHOLDER": 0.4,  # Medium-low - temporary solutions
        "MOCK": 0.3,  # Low - test/development artifacts
        "NOTE": 0.1,  # Lowest - informational
    }

    # Context keywords that affect priority
    CRITICAL_KEYWORDS = [
        "crash",
        "error",
        "fail",
        "broken",
        "wrong",
        "incorrect",
        "security",
        "memory leak",
        "deadlock",
        "race condition",
        "critical",
        "urgent",
        "asap",
        "blocker",
    ]

    LOWPRI_KEYWORDS = [
        "maybe",
        "consider",
        "nice to have",
        "future",
        "eventually",
        "optimization",
        "refactor",
        "cleanup",
        "documentation",
    ]

    def __init__(self, repo_path: str = "."):
        self.repo_path = Path(repo_path)
        self.markers = []

    def scan_repository(self):
        """Scan repository for markers"""
        print("🔍 Scanning repository for markers...")

        extensions = {".cc", ".h", ".cpp", ".hpp", ".c", ".py", ".scm"}
        skip_dirs = {".git", "__pycache__", "build", ".github", "cognitive-patterns"}

        marker_patterns = {
            "TODO": re.compile(r"(//|#|;)\s*TODO[:\s](.+)", re.IGNORECASE),
            "FIXME": re.compile(r"(//|#|;)\s*FIXME[:\s](.+)", re.IGNORECASE),
            "STUB": re.compile(r"(//|#|;)\s*STUB[:\s]?(.+)", re.IGNORECASE),
            "BUG": re.compile(r"(//|#|;)\s*BUG[:\s](.+)", re.IGNORECASE),
            "HACK": re.compile(r"(//|#|;)\s*HACK[:\s](.+)", re.IGNORECASE),
            "NOT_IMPLEMENTED": re.compile(r"(//|#|;)\s*NOT\s+IMPLEMENTED[:\s](.+)", re.IGNORECASE),
        }

        for root, dirs, files in os.walk(self.repo_path):
            # Filter directories
            dirs[:] = [d for d in dirs if d not in skip_dirs]

            for file in files:
                file_path = Path(root) / file
                if file_path.suffix in extensions:
                    self._scan_file(file_path, marker_patterns)

        print(f"  Found {len(self.markers)} markers")
        return self.markers

    def _scan_file(self, file_path: Path, patterns: dict):
        """Scan a single file for markers"""
        try:
            with open(file_path, encoding="utf-8", errors="ignore") as f:
                lines = f.readlines()

            for line_num, line in enumerate(lines, 1):
                for marker_type, pattern in patterns.items():
                    match = pattern.search(line)
                    if match:
                        content = match.group(2).strip() if len(match.groups()) > 1 else line.strip()

                        # Determine component
                        component = self._get_component(file_path)

                        # Calculate priority score
                        priority_score = self._calculate_priority(marker_type, content, component, file_path)

                        self.markers.append(
                            {
                                "file": str(file_path.relative_to(self.repo_path)),
                                "line": line_num,
                                "type": marker_type,
                                "content": content,
                                "component": component,
                                "priority_score": priority_score,
                                "full_line": line.strip(),
                            }
                        )

        except Exception:
            pass

    def _get_component(self, file_path: Path) -> str:
        """Determine component from file path"""
        parts = file_path.relative_to(self.repo_path).parts
        if len(parts) > 0:
            component = parts[0]
            if component in self.COMPONENT_CRITICALITY:
                return component
            # Check if in tests
            if "test" in str(file_path).lower():
                return "tests"
            # Check if in scripts directory specifically
            if "script" in str(file_path).lower() and "scripts" in parts:
                return "scripts"
            # Check if in docs
            if "doc" in str(file_path).lower() or "README" in str(file_path):
                return "documentation"
        return "root"

    def _calculate_priority(self, marker_type: str, content: str, component: str, file_path: Path) -> float:
        """Calculate priority score for a marker (0.0 - 1.0)"""
        # Base score from marker type
        base_score = self.MARKER_URGENCY.get(marker_type, 0.5)

        # Component weight
        component_weight = self.COMPONENT_CRITICALITY.get(component, 0.3)

        # Context modifiers
        content_lower = content.lower()
        context_modifier = 1.0

        # Check for critical keywords
        if any(kw in content_lower for kw in self.CRITICAL_KEYWORDS):
            context_modifier = 1.5

        # Check for low priority keywords
        elif any(kw in content_lower for kw in self.LOWPRI_KEYWORDS):
            context_modifier = 0.7

        # Calculate final score
        priority = (base_score * 0.4 + component_weight * 0.6) * context_modifier

        # Clamp to [0, 1]
        return min(1.0, max(0.0, priority))

    def generate_priority_report(self) -> dict:
        """Generate prioritized marker report"""
        if not self.markers:
            self.scan_repository()

        # Sort by priority
        sorted_markers = sorted(self.markers, key=lambda x: x["priority_score"], reverse=True)

        # Categorize
        critical = [m for m in sorted_markers if m["priority_score"] >= 0.8]
        high = [m for m in sorted_markers if 0.6 <= m["priority_score"] < 0.8]
        medium = [m for m in sorted_markers if 0.4 <= m["priority_score"] < 0.6]
        low = [m for m in sorted_markers if m["priority_score"] < 0.4]

        # Statistics by component
        by_component = defaultdict(list)
        for marker in sorted_markers:
            by_component[marker["component"]].append(marker)

        # Statistics by type
        by_type = defaultdict(list)
        for marker in sorted_markers:
            by_type[marker["type"]].append(marker)

        report = {
            "total_markers": len(sorted_markers),
            "by_priority": {
                "critical": len(critical),
                "high": len(high),
                "medium": len(medium),
                "low": len(low),
            },
            "critical_markers": critical[:50],  # Top 50 critical
            "high_priority_markers": high[:50],  # Top 50 high
            "by_component": {k: len(v) for k, v in by_component.items()},
            "by_type": {k: len(v) for k, v in by_type.items()},
        }

        return report

    def print_summary(self, report: dict):
        """Print summary report"""
        print("\n" + "=" * 70)
        print("ENTELECHY MARKER PRIORITIZATION REPORT")
        print("=" * 70)

        print("\n📊 OVERALL STATISTICS")
        print(f"Total markers: {report['total_markers']}")

        print("\n⚠️  BY PRIORITY")
        for priority, count in report["by_priority"].items():
            pct = (count / report["total_markers"] * 100) if report["total_markers"] > 0 else 0
            print(f"  {priority.upper():10s}: {count:4d} ({pct:5.1f}%)")

        print("\n🗂️  BY COMPONENT (Top 10)")
        sorted_comp = sorted(report["by_component"].items(), key=lambda x: x[1], reverse=True)
        for component, count in sorted_comp[:10]:
            print(f"  {component:20s}: {count:4d}")

        print("\n📋 BY TYPE")
        for marker_type, count in sorted(report["by_type"].items(), key=lambda x: x[1], reverse=True):
            print(f"  {marker_type:20s}: {count:4d}")

        print("\n🔥 TOP 10 CRITICAL MARKERS")
        for i, marker in enumerate(report["critical_markers"][:10], 1):
            file_short = marker["file"] if len(marker["file"]) < 50 else "..." + marker["file"][-47:]
            print(f"{i:2d}. [{marker['priority_score']:.2f}] {file_short}:{marker['line']}")
            content_short = marker["content"][:60] + "..." if len(marker["content"]) > 60 else marker["content"]
            print(f"    {marker['type']}: {content_short}")

        print("\n" + "=" * 70)


def main():
    parser = argparse.ArgumentParser(description="Prioritize entelechy markers")
    parser.add_argument("--repo-path", default=".", help="Repository path")
    parser.add_argument("--output", default="entelechy_marker_priorities.json", help="Output JSON file")
    args = parser.parse_args()

    prioritizer = MarkerPrioritizer(args.repo_path)
    report = prioritizer.generate_priority_report()
    prioritizer.print_summary(report)

    # Save report
    with open(args.output, "w") as f:
        json.dump(report, f, indent=2)

    print(f"\n💾 Detailed report saved to: {args.output}")


if __name__ == "__main__":
    main()
