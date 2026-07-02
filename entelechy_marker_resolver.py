#!/usr/bin/env python3
"""
Entelechy Marker Resolver

Systematic tool for resolving code markers to improve entelechy actualization.
Provides prioritization, tracking, and automation capabilities.

Features:
1. Prioritized resolution queue based on severity and impact
2. Progress tracking with milestone reporting
3. Automated resolution suggestions for common patterns
4. Integration with version control
5. Continuous measurement of entelechy improvement

Part of the Entelechy Framework for self-actualizing cognitive systems.
"""

import json
from collections import defaultdict
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path


@dataclass
class MarkerResolution:
    """Tracks resolution of a specific marker."""
    file_path: str
    line_number: int
    marker_type: str
    original_content: str
    status: str = "OPEN"  # OPEN, IN_PROGRESS, RESOLVED, DEFERRED, WONT_FIX
    priority: str = "MEDIUM"  # CRITICAL, HIGH, MEDIUM, LOW
    assignee: str | None = None
    start_date: str | None = None
    completion_date: str | None = None
    resolution_type: str | None = None  # fixed, documented, removed, refactored
    resolution_notes: str | None = None
    commit_sha: str | None = None

class EntelechyMarkerResolver:
    """Manages systematic resolution of code markers."""

    def __init__(self, repo_root: str, analysis_file: str = 'entelechy_marker_analysis.json'):
        self.repo_root = Path(repo_root)
        self.analysis_file = self.repo_root / analysis_file
        self.tracking_file = self.repo_root / 'entelechy_marker_resolution_tracking.json'

        self.analysis_data = None
        self.resolutions: dict[str, MarkerResolution] = {}

        self._load_analysis()
        self._load_tracking()

    def _load_analysis(self):
        """Load the marker analysis data."""
        if self.analysis_file.exists():
            with open(self.analysis_file) as f:
                self.analysis_data = json.load(f)
            print(f"✓ Loaded analysis with {self.analysis_data['summary']['total_markers']} markers")
        else:
            print(f"⚠ Analysis file not found: {self.analysis_file}")
            print("  Run entelechy_marker_analyzer.py first")

    def _load_tracking(self):
        """Load existing resolution tracking data."""
        if self.tracking_file.exists():
            with open(self.tracking_file) as f:
                data = json.load(f)
                for key, item in data.items():
                    self.resolutions[key] = MarkerResolution(**item)
            print(f"✓ Loaded tracking for {len(self.resolutions)} markers")
        else:
            print("⚠ No existing tracking data found, starting fresh")

    def _save_tracking(self):
        """Save resolution tracking data."""
        data = {key: asdict(res) for key, res in self.resolutions.items()}
        with open(self.tracking_file, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"✓ Saved tracking for {len(self.resolutions)} markers")

    def initialize_tracking(self):
        """Initialize tracking entries for all markers from analysis."""
        if not self.analysis_data:
            print("⚠ No analysis data available")
            return

        markers = self.analysis_data.get('markers', [])
        new_count = 0

        for marker in markers:
            key = f"{marker['file_path']}:{marker['line_number']}"

            if key not in self.resolutions:
                # Determine priority from severity
                if marker['severity'] >= 0.8:
                    priority = 'CRITICAL'
                elif marker['severity'] >= 0.7:
                    priority = 'HIGH'
                elif marker['severity'] >= 0.6:
                    priority = 'MEDIUM'
                else:
                    priority = 'LOW'

                self.resolutions[key] = MarkerResolution(
                    file_path=marker['file_path'],
                    line_number=marker['line_number'],
                    marker_type=marker['marker_type'],
                    original_content=marker['content'],
                    priority=priority
                )
                new_count += 1

        self._save_tracking()
        print(f"✓ Initialized tracking for {new_count} new markers")

    def get_priority_queue(self, status: str = "OPEN", limit: int = 50) -> list[MarkerResolution]:
        """Get prioritized list of markers to resolve."""
        # Priority order
        priority_order = {'CRITICAL': 0, 'HIGH': 1, 'MEDIUM': 2, 'LOW': 3}

        # Filter by status and sort by priority
        queue = [
            res for res in self.resolutions.values()
            if res.status == status
        ]

        queue.sort(key=lambda r: (priority_order.get(r.priority, 4), r.file_path))

        return queue[:limit]

    def get_easy_wins(self, limit: int = 20) -> list[MarkerResolution]:
        """Get markers that are easy to resolve (documentation, simple todos)."""
        easy_wins = []

        for _marker_key, resolution in self.resolutions.items():
            if resolution.status != "OPEN":
                continue

            # Find corresponding marker data
            marker_data = self._find_marker_data(resolution.file_path, resolution.line_number)
            if marker_data:
                category = marker_data.get('category', '')
                if category == 'documentation' or \
                   (resolution.marker_type == 'TODO' and len(resolution.original_content) < 50):
                    easy_wins.append(resolution)

        return easy_wins[:limit]

    def _find_marker_data(self, file_path: str, line_number: int) -> dict | None:
        """Find marker data from analysis."""
        if not self.analysis_data:
            return None

        for marker in self.analysis_data.get('markers', []):
            if marker['file_path'] == file_path and marker['line_number'] == line_number:
                return marker
        return None

    def get_component_summary(self) -> dict[str, dict]:
        """Get summary of markers by component."""
        by_component = defaultdict(lambda: {
            'total': 0,
            'open': 0,
            'in_progress': 0,
            'resolved': 0,
            'critical': 0,
            'high': 0
        })

        for res in self.resolutions.values():
            component = self._extract_component(res.file_path)
            by_component[component]['total'] += 1

            if res.status == 'OPEN':
                by_component[component]['open'] += 1
            elif res.status == 'IN_PROGRESS':
                by_component[component]['in_progress'] += 1
            elif res.status == 'RESOLVED':
                by_component[component]['resolved'] += 1

            if res.priority == 'CRITICAL':
                by_component[component]['critical'] += 1
            elif res.priority == 'HIGH':
                by_component[component]['high'] += 1

        return dict(by_component)

    def _extract_component(self, file_path: str) -> str:
        """Extract component name from file path."""
        parts = file_path.split('/')
        if len(parts) > 0:
            return parts[0]
        return 'root'

    def mark_in_progress(self, file_path: str, line_number: int, assignee: str = "entelechy-bot"):
        """Mark a marker as in progress."""
        key = f"{file_path}:{line_number}"
        if key in self.resolutions:
            self.resolutions[key].status = "IN_PROGRESS"
            self.resolutions[key].assignee = assignee
            self.resolutions[key].start_date = datetime.now().isoformat()
            self._save_tracking()
            return True
        return False

    def mark_resolved(
        self, file_path: str, line_number: int,
        resolution_type: str, notes: str = "", commit_sha: str = ""
    ):
        """Mark a marker as resolved."""
        key = f"{file_path}:{line_number}"
        if key in self.resolutions:
            self.resolutions[key].status = "RESOLVED"
            self.resolutions[key].resolution_type = resolution_type
            self.resolutions[key].resolution_notes = notes
            self.resolutions[key].completion_date = datetime.now().isoformat()
            if commit_sha:
                self.resolutions[key].commit_sha = commit_sha
            self._save_tracking()
            return True
        return False

    def mark_deferred(self, file_path: str, line_number: int, reason: str):
        """Mark a marker as deferred."""
        key = f"{file_path}:{line_number}"
        if key in self.resolutions:
            self.resolutions[key].status = "DEFERRED"
            self.resolutions[key].resolution_notes = f"Deferred: {reason}"
            self._save_tracking()
            return True
        return False

    def generate_progress_report(self) -> str:
        """Generate a comprehensive progress report."""
        report_lines = []
        report_lines.append("# Entelechy Marker Resolution Progress Report")
        report_lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append("")

        # Overall statistics
        stats = self._calculate_statistics()
        report_lines.append("## Overall Statistics")
        report_lines.append(f"- Total Markers: {stats['total']}")
        report_lines.append(f"- Open: {stats['open']} ({stats['open_pct']:.1f}%)")
        report_lines.append(f"- In Progress: {stats['in_progress']} ({stats['in_progress_pct']:.1f}%)")
        report_lines.append(f"- Resolved: {stats['resolved']} ({stats['resolved_pct']:.1f}%)")
        report_lines.append(f"- Deferred: {stats['deferred']} ({stats['deferred_pct']:.1f}%)")
        report_lines.append("")

        # Entelechy improvement
        if self.analysis_data and stats['total'] > 0:
            original_impact = self.analysis_data['summary']['actualization_inhibition']
            current_impact = original_impact * (stats['open'] / stats['total'])
            improvement = original_impact - current_impact

            report_lines.append("## Entelechy Impact")
            report_lines.append(f"- Original Actualization Inhibition: {original_impact:.1%}")
            report_lines.append(f"- Current Actualization Inhibition: {current_impact:.1%}")
            report_lines.append(f"- Improvement: {improvement:.1%}")
            report_lines.append("")

        # Priority breakdown
        report_lines.append("## Priority Breakdown")
        priority_stats = self._calculate_priority_stats()
        for priority in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']:
            if priority in priority_stats:
                pstats = priority_stats[priority]
                report_lines.append(f"### {priority}")
                report_lines.append(f"- Total: {pstats['total']}")
                report_lines.append(f"- Open: {pstats['open']}")
                report_lines.append(f"- Resolved: {pstats['resolved']}")
                report_lines.append("")

        # Component summary
        report_lines.append("## Component Summary")
        component_summary = self.get_component_summary()
        for component, cstats in sorted(component_summary.items(), key=lambda x: x[1]['total'], reverse=True)[:10]:
            resolved_pct = (cstats['resolved'] / cstats['total'] * 100) if cstats['total'] > 0 else 0
            report_lines.append(f"### {component}")
            report_lines.append(f"- Total: {cstats['total']}, Open: {cstats['open']}, Resolved: {cstats['resolved']} ({resolved_pct:.1f}%)")
            report_lines.append("")

        # Next actions
        report_lines.append("## Next Actions")
        easy_wins = self.get_easy_wins(10)
        if easy_wins:
            report_lines.append("### Easy Wins (Quick Resolutions)")
            for win in easy_wins:
                report_lines.append(f"- `{win.file_path}:{win.line_number}` - {win.marker_type}: {win.original_content[:60]}...")
            report_lines.append("")

        critical_items = self.get_priority_queue(limit=10)
        if critical_items:
            report_lines.append("### Critical Priority Items")
            for item in critical_items[:5]:
                report_lines.append(f"- `{item.file_path}:{item.line_number}` - {item.marker_type}: {item.original_content[:60]}...")
            report_lines.append("")

        return "\n".join(report_lines)

    def _calculate_statistics(self) -> dict:
        """Calculate overall statistics."""
        total = len(self.resolutions)
        if total == 0:
            # Return empty stats for empty tracking
            return {
                'total': 0,
                'open': 0,
                'in_progress': 0,
                'resolved': 0,
                'deferred': 0,
                'open_pct': 0.0,
                'in_progress_pct': 0.0,
                'resolved_pct': 0.0,
                'deferred_pct': 0.0,
            }

        stats = {
            'total': total,
            'open': sum(1 for r in self.resolutions.values() if r.status == 'OPEN'),
            'in_progress': sum(1 for r in self.resolutions.values() if r.status == 'IN_PROGRESS'),
            'resolved': sum(1 for r in self.resolutions.values() if r.status == 'RESOLVED'),
            'deferred': sum(1 for r in self.resolutions.values() if r.status == 'DEFERRED'),
        }

        # Calculate percentages
        for key in ['open', 'in_progress', 'resolved', 'deferred']:
            stats[f'{key}_pct'] = (stats[key] / total * 100)

        return stats

    def _calculate_priority_stats(self) -> dict:
        """Calculate statistics by priority."""
        by_priority = defaultdict(lambda: {'total': 0, 'open': 0, 'resolved': 0})

        for res in self.resolutions.values():
            by_priority[res.priority]['total'] += 1
            if res.status == 'OPEN':
                by_priority[res.priority]['open'] += 1
            elif res.status == 'RESOLVED':
                by_priority[res.priority]['resolved'] += 1

        return dict(by_priority)

    def export_actionable_items(self, output_file: str = 'entelechy_actionable_items.md'):
        """Export actionable items in markdown format."""
        lines = []
        lines.append("# Entelechy Marker Resolution - Actionable Items")
        lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("")

        # Critical items
        critical = self.get_priority_queue(limit=20)
        if critical:
            lines.append("## 🚨 Critical Priority (Address First)")
            lines.append("")
            for idx, item in enumerate(critical, 1):
                lines.append(f"### {idx}. {item.marker_type} in `{item.file_path}:{item.line_number}`")
                lines.append(f"**Content:** {item.original_content}")

                # Add context from analysis if available
                marker_data = self._find_marker_data(item.file_path, item.line_number)
                if marker_data:
                    lines.append(f"**Category:** {marker_data.get('category', 'unknown')}")
                    lines.append(f"**Estimated Effort:** {marker_data.get('estimated_effort', 'unknown')}")
                    lines.append(f"**Suggestion:** {marker_data.get('repair_suggestion', 'N/A')}")
                lines.append("")

        # Easy wins
        easy_wins = self.get_easy_wins(20)
        if easy_wins:
            lines.append("## ✅ Easy Wins (Quick Resolutions)")
            lines.append("")
            for idx, item in enumerate(easy_wins, 1):
                lines.append(f"{idx}. `{item.file_path}:{item.line_number}` - {item.marker_type}: {item.original_content[:80]}")
            lines.append("")

        output_path = self.repo_root / output_file
        with open(output_path, 'w') as f:
            f.write('\n'.join(lines))

        print(f"✓ Exported actionable items to {output_file}")

def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description='Entelechy Marker Resolver')
    parser.add_argument('--repo', default='/home/runner/work/opencog-unified/opencog-unified',
                       help='Repository root path')
    parser.add_argument('--init', action='store_true',
                       help='Initialize tracking from analysis')
    parser.add_argument('--report', action='store_true',
                       help='Generate progress report')
    parser.add_argument('--export', action='store_true',
                       help='Export actionable items')

    args = parser.parse_args()

    resolver = EntelechyMarkerResolver(args.repo)

    if args.init:
        resolver.initialize_tracking()

    if args.report:
        report = resolver.generate_progress_report()
        print("\n" + report)

        # Save to file
        report_path = resolver.repo_root / 'entelechy_marker_resolution_progress.md'
        with open(report_path, 'w') as f:
            f.write(report)
        print(f"\n✓ Report saved to {report_path}")

    if args.export:
        resolver.export_actionable_items()

if __name__ == '__main__':
    main()
