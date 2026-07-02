#!/usr/bin/env python3
"""
Entelechy Metrics Reporter

Generates a comprehensive report on placeholder marker resolution progress.
Tracks reduction in fragmentations and improvement in code quality metrics.
"""

import json
import os
import re
from datetime import datetime


class EntelechyMetrics:
    def __init__(self, repo_path='.'):
        self.repo_path = repo_path
        self.marker_types = ['TODO', 'FIXME', 'STUB', 'XXX', 'HACK', 'NOT IMPLEMENTED']
        self.file_extensions = ['.cc', '.cpp', '.h', '.hpp', '.scm']

    def scan_markers(self):
        """Scan repository for all placeholder markers"""
        markers = {mtype: [] for mtype in self.marker_types}
        total = 0

        skip_dirs = {'.git', 'build', 'components', '__pycache__', '.devcontainer'}

        for root, dirs, files in os.walk(self.repo_path):
            dirs[:] = [d for d in dirs if d not in skip_dirs and not d.startswith('.')]

            for file in files:
                if not any(file.endswith(ext) for ext in self.file_extensions):
                    continue

                filepath = os.path.join(root, file)
                try:
                    with open(filepath, encoding='utf-8', errors='ignore') as f:
                        lines = f.readlines()

                    for i, line in enumerate(lines):
                        # Skip std::placeholders and boost placeholders
                        if 'std::placeholders' in line or 'boost/mpl/placeholders' in line:
                            continue

                        for mtype in self.marker_types:
                            if re.search(rf'\b{mtype}\b', line, re.IGNORECASE):
                                markers[mtype].append({
                                    'file': filepath,
                                    'line': i + 1,
                                    'content': line.strip()
                                })
                                total += 1
                                break  # Count each line only once
                except Exception:
                    pass

        return markers, total

    def analyze_by_component(self, markers):
        """Analyze markers by component"""
        components = {}

        for _mtype, marker_list in markers.items():
            for marker in marker_list:
                # Extract component from path
                path_parts = marker['file'].split(os.sep)
                if len(path_parts) > 1:
                    component = path_parts[1] if path_parts[0] == '.' else path_parts[0]
                else:
                    component = 'root'

                if component not in components:
                    components[component] = 0
                components[component] += 1

        return dict(sorted(components.items(), key=lambda x: x[1], reverse=True))

    def calculate_entelechy_metrics(self, total_markers):
        """Calculate entelechy-specific metrics"""
        # Baseline: Original report showed 2895 markers with 96.5% severity
        baseline_markers = 2895
        baseline_severity = 0.965

        # Current state
        if total_markers > 0:
            # Severity decreases as markers are resolved
            severity = max(0.0, baseline_severity * (total_markers / baseline_markers))
            # Actualization increases as markers decrease
            actualization = 1.0 - (total_markers / baseline_markers) * 0.1
            # Fitness score (0-1 scale)
            fitness = 1.0 - severity * 0.5
        else:
            severity = 0.0
            actualization = 1.0
            fitness = 1.0

        return {
            'baseline_markers': baseline_markers,
            'current_markers': total_markers,
            'markers_resolved': max(0, baseline_markers - total_markers),
            'resolution_rate': (max(0, baseline_markers - total_markers) / baseline_markers * 100),
            'severity': severity,
            'actualization': actualization,
            'fitness': fitness
        }

    def generate_report(self):
        """Generate comprehensive metrics report"""
        print("Scanning repository for placeholder markers...")
        markers, total = self.scan_markers()

        print("Analyzing distribution...")
        by_component = self.analyze_by_component(markers)

        print("Calculating entelechy metrics...")
        entelechy_metrics = self.calculate_entelechy_metrics(total)

        report = {
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'total_markers': total,
            'by_type': {mtype: len(mlist) for mtype, mlist in markers.items()},
            'by_component': by_component,
            'entelechy_metrics': entelechy_metrics,
            'top_components': dict(list(by_component.items())[:10])
        }

        return report

    def print_report(self, report):
        """Print formatted report to console"""
        print("\n" + "=" * 70)
        print("ENTELECHY METRICS REPORT - Placeholder Resolution Progress")
        print("=" * 70)
        print(f"\nGenerated: {report['timestamp']}\n")

        # Summary
        print("SUMMARY")
        print("-" * 70)
        total = report['total_markers']
        print(f"Total Placeholder Markers: {total}")
        print("\nBy Type:")
        for mtype, count in sorted(report['by_type'].items(), key=lambda x: x[1], reverse=True):
            if count > 0:
                percentage = (count / total * 100) if total > 0 else 0
                print(f"  {mtype:20s}: {count:4d} ({percentage:5.1f}%)")

        # Entelechy Metrics
        print("\n" + "-" * 70)
        print("ENTELECHY METRICS")
        print("-" * 70)
        em = report['entelechy_metrics']
        print(f"Baseline Markers:      {em['baseline_markers']:,}")
        print(f"Current Markers:       {em['current_markers']:,}")
        print(f"Markers Resolved:      {em['markers_resolved']:,}")
        print(f"Resolution Rate:       {em['resolution_rate']:.1f}%")
        print(f"\nActualization Level:   {em['actualization']:.1%}")
        print(f"Fragmentation Severity: {em['severity']:.1%}")
        print(f"Entelechy Fitness:     {em['fitness']:.3f}")

        # Determine stage based on metrics
        if em['actualization'] >= 0.98:
            stage = "Transcendent"
        elif em['actualization'] >= 0.95:
            stage = "Harmonized"
        elif em['actualization'] >= 0.90:
            stage = "Integrated"
        else:
            stage = "Developing"
        print(f"Development Stage:     {stage}")

        # Component Distribution
        print("\n" + "-" * 70)
        print("TOP 10 COMPONENTS BY MARKER COUNT")
        print("-" * 70)
        for i, (component, count) in enumerate(list(report['top_components'].items())[:10], 1):
            percentage = (count / total * 100) if total > 0 else 0
            print(f"{i:2d}. {component:30s}: {count:4d} ({percentage:5.1f}%)")

        # Progress Assessment
        print("\n" + "-" * 70)
        print("PROGRESS ASSESSMENT")
        print("-" * 70)

        resolved = em['markers_resolved']
        if resolved > 100:
            print("✅ Excellent progress! Significant marker reduction achieved.")
        elif resolved > 50:
            print("✅ Good progress! Steady marker resolution underway.")
        elif resolved > 10:
            print("🔄 Progress started. Continue with systematic resolution.")
        else:
            print("🔄 Initial phase. Begin with quick wins and documentation.")

        print(f"\nNext Milestone: Resolve {max(0, total - 700)} more markers")
        print("Target: < 700 markers for 97%+ actualization")

        print("\n" + "=" * 70)
        print("\nDetailed report saved to: entelechy_metrics_report.json")
        print("=" * 70 + "\n")


def main():
    """Main entry point"""
    metrics = EntelechyMetrics()
    report = metrics.generate_report()

    # Save detailed report
    with open('entelechy_metrics_report.json', 'w') as f:
        json.dump(report, f, indent=2)

    # Print summary
    metrics.print_report(report)

    print("\nRecommendations:")
    print("  1. Focus on components with highest marker counts")
    print("  2. Prioritize FIXME markers (often indicate bugs)")
    print("  3. Convert obsolete TODOs to documentation")
    print("  4. Track progress with git diff statistics")
    print("  5. Re-run this report after each resolution batch\n")


if __name__ == '__main__':
    main()
