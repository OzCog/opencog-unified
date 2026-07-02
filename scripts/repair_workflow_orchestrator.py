#!/usr/bin/env python3
"""
Entelechy Repair Workflow Orchestrator

Coordinates the complete repair workflow:
1. Upstream sync for latest fixes
2. Intelligent repair analysis
3. Automated safe repairs
4. Manual review queue generation
5. Progress tracking and reporting

Part of the Entelechy Framework repair process.
"""

import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path


class RepairWorkflowOrchestrator:
    """Orchestrates the complete repair workflow."""

    def __init__(self, repo_root: str = '.'):
        self.repo_root = Path(repo_root).resolve()
        self.scripts_dir = self.repo_root / 'scripts'
        self.results = {}

    def step_1_upstream_sync(self, days_back: int = 90, max_repos: int = 3) -> dict:
        """Step 1: Sync with upstream OpenCog repos."""
        print("\n" + "=" * 70)
        print("STEP 1: UPSTREAM SYNC")
        print("=" * 70)

        sync_script = self.scripts_dir / 'sync_upstream_fixes.py'

        if not sync_script.exists():
            print("⚠ Upstream sync script not found, skipping...")
            return {'skipped': True}

        try:
            result = subprocess.run(
                [sys.executable, str(sync_script),
                 '--repo', str(self.repo_root),
                 '--days', str(days_back),
                 '--max-repos', str(max_repos),
                 '--export', 'upstream_sync_report.json'],
                capture_output=True,
                text=True,
                timeout=300  # 5 minutes max
            )

            print(result.stdout)

            if result.returncode == 0:
                # Load report
                report_file = self.repo_root / 'upstream_sync_report.json'
                if report_file.exists():
                    with open(report_file) as f:
                        report = json.load(f)
                    return {'success': True, 'report': report}

            return {'success': False, 'error': result.stderr}

        except subprocess.TimeoutExpired:
            print("⚠ Upstream sync timed out, continuing...")
            return {'timeout': True}
        except Exception as e:
            print(f"⚠ Upstream sync error: {e}")
            return {'error': str(e)}

    def step_2_analyze_markers(self) -> dict:
        """Step 2: Run marker analysis."""
        print("\n" + "=" * 70)
        print("STEP 2: MARKER ANALYSIS")
        print("=" * 70)

        analyzer_script = self.repo_root / 'entelechy_marker_analyzer.py'

        if not analyzer_script.exists():
            print("⚠ Analyzer script not found")
            return {'error': 'Script not found'}

        try:
            result = subprocess.run(
                [sys.executable, str(analyzer_script),
                 '--repo', str(self.repo_root),
                 '--output', 'entelechy_marker_analysis.json'],
                capture_output=True,
                text=True,
                timeout=120  # 2 minutes
            )

            print(result.stdout)

            if result.returncode == 0:
                analysis_file = self.repo_root / 'entelechy_marker_analysis.json'
                if analysis_file.exists():
                    with open(analysis_file) as f:
                        analysis = json.load(f)
                    return {'success': True, 'analysis': analysis}

            return {'success': False, 'error': result.stderr}

        except Exception as e:
            print(f"⚠ Analysis error: {e}")
            return {'error': str(e)}

    def step_3_intelligent_repair(self) -> dict:
        """Step 3: Run intelligent repair analysis."""
        print("\n" + "=" * 70)
        print("STEP 3: INTELLIGENT REPAIR ANALYSIS")
        print("=" * 70)

        repair_script = self.scripts_dir / 'intelligent_marker_repair.py'

        if not repair_script.exists():
            print("⚠ Repair script not found")
            return {'error': 'Script not found'}

        try:
            result = subprocess.run(
                [sys.executable, str(repair_script),
                 '--repo', str(self.repo_root),
                 '--analyze',
                 '--export', 'repair_plan.json'],
                capture_output=True,
                text=True,
                timeout=120
            )

            print(result.stdout)

            if result.returncode == 0:
                plan_file = self.repo_root / 'repair_plan.json'
                if plan_file.exists():
                    with open(plan_file) as f:
                        plan = json.load(f)
                    return {'success': True, 'plan': plan}

            return {'success': False, 'error': result.stderr}

        except Exception as e:
            print(f"⚠ Repair analysis error: {e}")
            return {'error': str(e)}

    def step_4_apply_safe_repairs(self, dry_run: bool = True) -> dict:
        """Step 4: Apply safe automated repairs."""
        print("\n" + "=" * 70)
        print(f"STEP 4: APPLY SAFE REPAIRS {'(DRY RUN)' if dry_run else ''}")
        print("=" * 70)

        repair_script = self.scripts_dir / 'intelligent_marker_repair.py'

        if not repair_script.exists():
            print("⚠ Repair script not found")
            return {'error': 'Script not found'}

        cmd = [
            sys.executable, str(repair_script),
            '--repo', str(self.repo_root),
            '--apply'
        ]

        if dry_run:
            cmd.append('--dry-run')

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60
            )

            print(result.stdout)

            return {
                'success': result.returncode == 0,
                'output': result.stdout,
                'dry_run': dry_run
            }

        except Exception as e:
            print(f"⚠ Apply repairs error: {e}")
            return {'error': str(e)}

    def step_5_generate_reports(self) -> dict:
        """Step 5: Generate comprehensive reports."""
        print("\n" + "=" * 70)
        print("STEP 5: GENERATE REPORTS")
        print("=" * 70)

        reports = {}

        # Consolidate all reports
        report_files = [
            'entelechy_marker_analysis.json',
            'repair_plan.json',
            'upstream_sync_report.json',
        ]

        for report_file in report_files:
            path = self.repo_root / report_file
            if path.exists():
                with open(path) as f:
                    reports[report_file] = json.load(f)

        # Generate master report
        master_report = {
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'workflow_version': '1.0',
            'steps_completed': list(self.results.keys()),
            'reports': reports,
            'summary': self._generate_summary(reports)
        }

        master_path = self.repo_root / 'entelechy_repair_master_report.json'
        with open(master_path, 'w') as f:
            json.dump(master_report, f, indent=2)

        print(f"\n✓ Master report saved to {master_path.name}")

        return {'success': True, 'report': master_report}

    def _generate_summary(self, reports: dict) -> dict:
        """Generate summary from all reports."""
        summary = {
            'markers_analyzed': 0,
            'upstream_fixes_found': 0,
            'repairs_planned': 0,
            'safe_repairs_available': 0,
            'manual_reviews_needed': 0
        }

        # From marker analysis
        if 'entelechy_marker_analysis.json' in reports:
            analysis = reports['entelechy_marker_analysis.json']
            summary['markers_analyzed'] = analysis.get('summary', {}).get('total_markers', 0)

        # From upstream sync
        if 'upstream_sync_report.json' in reports:
            upstream = reports['upstream_sync_report.json']
            summary['upstream_fixes_found'] = upstream.get('summary', {}).get('total_fixes', 0)

        # From repair plan
        if 'repair_plan.json' in reports:
            plan = reports['repair_plan.json']
            plan_summary = plan.get('summary', {})
            summary['repairs_planned'] = plan_summary.get('total_repairs', 0)
            summary['safe_repairs_available'] = plan_summary.get('safe_auto', 0)
            summary['manual_reviews_needed'] = plan_summary.get('needs_review', 0)

        return summary

    def run_workflow(self, apply_safe_repairs: bool = False,
                    dry_run: bool = True) -> dict:
        """
        Run the complete repair workflow.

        Args:
            apply_safe_repairs: Whether to apply safe automated repairs
            dry_run: If True, don't actually modify files

        Returns:
            Dict with workflow results
        """
        print("🚀 ENTELECHY REPAIR WORKFLOW")
        print("=" * 70)
        print(f"Repository: {self.repo_root}")
        print(f"Timestamp: {datetime.utcnow().isoformat()}Z")

        # Step 1: Upstream sync
        self.results['upstream_sync'] = self.step_1_upstream_sync(
            days_back=30,  # Last month
            max_repos=3    # Top 3 repos for speed
        )

        # Step 2: Marker analysis
        self.results['marker_analysis'] = self.step_2_analyze_markers()

        # Step 3: Intelligent repair
        self.results['repair_analysis'] = self.step_3_intelligent_repair()

        # Step 4: Apply safe repairs (optional)
        if apply_safe_repairs:
            self.results['apply_repairs'] = self.step_4_apply_safe_repairs(dry_run)

        # Step 5: Generate reports
        self.results['reports'] = self.step_5_generate_reports()

        # Final summary
        print("\n" + "=" * 70)
        print("🎯 WORKFLOW COMPLETE")
        print("=" * 70)

        if 'reports' in self.results and self.results['reports'].get('success'):
            summary = self.results['reports']['report']['summary']
            print("\n📊 Summary:")
            print(f"  Markers analyzed: {summary['markers_analyzed']}")
            print(f"  Upstream fixes found: {summary['upstream_fixes_found']}")
            print(f"  Repairs planned: {summary['repairs_planned']}")
            print(f"  Safe auto-repairs: {summary['safe_repairs_available']}")
            print(f"  Manual reviews needed: {summary['manual_reviews_needed']}")

        print("\n✓ All reports saved to repository root")

        return self.results


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Orchestrate the complete entelechy repair workflow'
    )
    parser.add_argument(
        '--repo', default='.',
        help='Repository root path'
    )
    parser.add_argument(
        '--apply-safe', action='store_true',
        help='Apply safe automated repairs'
    )
    parser.add_argument(
        '--no-dry-run', action='store_true',
        help='Actually modify files (default is dry-run)'
    )

    args = parser.parse_args()

    orchestrator = RepairWorkflowOrchestrator(args.repo)

    results = orchestrator.run_workflow(
        apply_safe_repairs=args.apply_safe,
        dry_run=not args.no_dry_run
    )

    # Exit code based on success
    all_success = all(
        r.get('success', False) or r.get('skipped', False)
        for r in results.values()
    )

    sys.exit(0 if all_success else 1)


if __name__ == '__main__':
    main()
