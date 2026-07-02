#!/usr/bin/env python3
"""
FIXME Development Environment Setup

This script sets up the development environment and testing infrastructure
for systematic FIXME resolution as outlined in the FIXME-SORTED-CATALOG.md
next steps.

Features:
- Git hooks for FIXME prevention
- Pre-commit checks for new FIXMEs
- Development workflow integration
- Progress tracking automation
"""

from pathlib import Path
from textwrap import dedent


class FIXMEDevEnvironment:
    """Sets up development environment for FIXME resolution workflow."""

    def __init__(self, repo_root: str):
        self.repo_root = Path(repo_root)
        self.git_hooks_dir = self.repo_root / ".git" / "hooks"

    def setup_environment(self):
        """Set up the complete development environment."""
        print("🔧 Setting up FIXME development environment...")

        self._setup_git_hooks()
        self._setup_pre_commit_config()
        self._setup_ci_integration()
        self._setup_weekly_reports()
        self._create_makefile_targets()

        print("✅ FIXME development environment setup complete!")
        print("\nNext steps:")
        print("1. Run 'make fixme-status' to see current status")
        print("2. Run 'make fixme-easy-wins' to see available easy fixes")
        print("3. Use 'git commit' to automatically check for new FIXMEs")
        print("4. Weekly reports will be generated automatically")

    def _setup_git_hooks(self):
        """Set up git hooks to prevent new FIXMEs."""
        print("📝 Setting up git hooks...")

        # Create hooks directory if it doesn't exist
        self.git_hooks_dir.mkdir(parents=True, exist_ok=True)

        # Pre-commit hook to check for new FIXMEs
        pre_commit_hook = self.git_hooks_dir / "pre-commit"
        pre_commit_content = dedent(
            """
            #!/bin/bash
            # Pre-commit hook to prevent new FIXMEs

            echo "🔍 Checking for new FIXME comments..."

            # Get list of staged files
            staged_files=$(git diff --cached --name-only --diff-filter=ACM | grep -E "\\.(cc|cpp|h|hpp|scm|py|c)$" || true)

            if [ -z "$staged_files" ]; then
                exit 0
            fi

            # Check for new FIXMEs in staged content
            new_fixmes=0
            for file in $staged_files; do
                # Check staged content for FIXMEs
                if git diff --cached "$file" | grep -E "^\\+.*FIXME|^\\+.*XXX.*FIXME" > /dev/null; then
                    echo "❌ New FIXME found in $file"
                    echo "   Please use specific TODO comments instead of FIXME"
                    echo "   See FIXME_IMPLEMENTATION_GUIDE.md for guidelines"
                    new_fixmes=1
                fi
            done

            if [ $new_fixmes -eq 1 ]; then
                echo ""
                echo "💡 Tip: Use descriptive TODO comments instead:"
                echo "   // TODO: Implement error handling for edge case X"
                echo "   // TODO(v2.0): Refactor to use new API"
                echo ""
                exit 1
            fi

            echo "✅ No new FIXMEs detected"
            exit 0
        """
        ).strip()

        with open(pre_commit_hook, "w") as f:
            f.write(pre_commit_content)
        pre_commit_hook.chmod(0o755)

        # Post-commit hook to update progress
        post_commit_hook = self.git_hooks_dir / "post-commit"
        post_commit_content = dedent(
            """
            #!/bin/bash
            # Post-commit hook to update FIXME progress

            # Check if any FIXME-related files were modified
            if git diff HEAD~1 --name-only | grep -E "(FIXME|TODO)" > /dev/null; then
                echo "📊 Updating FIXME progress tracking..."
                cd "$(git rev-parse --show-toplevel)"
                if [ -f fixme_resolution_tracker.py ]; then
                    python3 fixme_resolution_tracker.py --report > /dev/null 2>&1 || true
                fi
            fi
        """
        ).strip()

        with open(post_commit_hook, "w") as f:
            f.write(post_commit_content)
        post_commit_hook.chmod(0o755)

    def _setup_pre_commit_config(self):
        """Set up pre-commit configuration file."""
        print("⚙️  Setting up pre-commit configuration...")

        pre_commit_config = self.repo_root / ".pre-commit-config.yaml"
        config_content = dedent(
            """
            # Pre-commit configuration for FIXME management
            repos:
              - repo: local
                hooks:
                  - id: no-new-fixmes
                    name: Prevent new FIXME comments
                    entry: bash -c 'if git diff --cached | grep -E "^\\+.*FIXME|^\\+.*XXX.*FIXME"; then echo "New FIXME detected! Use TODO instead."; exit 1; fi'
                    language: system
                    files: \\.(cc|cpp|h|hpp|scm|py|c)$

                  - id: fixme-progress-update
                    name: Update FIXME progress
                    entry: python3 fixme_resolution_tracker.py --report
                    language: system
                    files: .*
                    pass_filenames: false
                    always_run: false
        """
        ).strip()

        with open(pre_commit_config, "w") as f:
            f.write(config_content)

    def _setup_ci_integration(self):
        """Set up CI integration for FIXME tracking."""
        print("🤖 Setting up CI integration...")

        # Create GitHub Actions workflow
        github_dir = self.repo_root / ".github" / "workflows"
        github_dir.mkdir(parents=True, exist_ok=True)

        workflow_file = github_dir / "fixme-tracking.yml"
        workflow_content = dedent(
            """
            name: FIXME Tracking

            on:
              push:
                branches: [ main, master ]
              pull_request:
                branches: [ main, master ]
              schedule:
                # Run weekly on Sundays at 9 AM UTC
                - cron: '0 9 * * 0'

            jobs:
              fixme-check:
                runs-on: ubuntu-latest
                steps:
                - uses: actions/checkout@v3

                - name: Set up Python
                  uses: actions/setup-python@v4
                  with:
                    python-version: '3.9'

                - name: Check for new FIXMEs in PR
                  if: github.event_name == 'pull_request'
                  run: |
                    git fetch origin ${{ github.base_ref }}
                    if git diff origin/${{ github.base_ref }}...HEAD | grep -E "^\\+.*FIXME|^\\+.*XXX.*FIXME"; then
                      echo "❌ New FIXME comments detected in this PR"
                      echo "Please use specific TODO comments instead"
                      exit 1
                    else
                      echo "✅ No new FIXMEs detected"
                    fi

                - name: Generate FIXME progress report
                  if: github.event_name == 'schedule' || github.event_name == 'push'
                  run: |
                    python3 fixme_resolution_tracker.py --import-catalog FIXME-SORTED-CATALOG.md --report

                - name: Upload progress report
                  if: github.event_name == 'schedule' || github.event_name == 'push'
                  uses: actions/upload-artifact@v3
                  with:
                    name: fixme-progress-report
                    path: FIXME_RESOLUTION_PROGRESS_REPORT.md
        """
        ).strip()

        with open(workflow_file, "w") as f:
            f.write(workflow_content)

    def _setup_weekly_reports(self):
        """Set up automated weekly progress reports."""
        print("📅 Setting up weekly progress reports...")

        # Create cron script for weekly reports
        scripts_dir = self.repo_root / "scripts"
        scripts_dir.mkdir(exist_ok=True)

        weekly_script = scripts_dir / "weekly_fixme_report.sh"
        script_content = dedent(
            """
            #!/bin/bash
            # Weekly FIXME progress report generator

            cd "$(dirname "$0")/.."

            echo "📊 Generating weekly FIXME progress report..."

            # Generate progress report
            python3 fixme_resolution_tracker.py --report

            # Create date-stamped report
            date_stamp=$(date +%Y-%m-%d)
            cp FIXME_RESOLUTION_PROGRESS_REPORT.md "reports/weekly_report_$date_stamp.md"

            # Generate easy wins summary
            echo "🚀 Easy wins available:" >> "reports/weekly_report_$date_stamp.md"
            python3 fixme_resolution_tracker.py --easy-wins >> "reports/weekly_report_$date_stamp.md"

            echo "✅ Weekly report generated: reports/weekly_report_$date_stamp.md"
        """
        ).strip()

        with open(weekly_script, "w") as f:
            f.write(script_content)
        weekly_script.chmod(0o755)

        # Create reports directory
        reports_dir = self.repo_root / "reports"
        reports_dir.mkdir(exist_ok=True)

    def _create_makefile_targets(self):
        """Create Makefile targets for FIXME management."""
        print("🔨 Creating Makefile targets...")

        makefile = self.repo_root / "Makefile.fixme"
        makefile_content = dedent(
            """
            # FIXME Resolution Makefile Targets
            # Include this in your main Makefile with: include Makefile.fixme

            .PHONY: fixme-status fixme-easy-wins fixme-report fixme-setup

            fixme-status:
            	@echo "📊 Current FIXME status:"
            	@python3 fixme_resolution_tracker.py --report | head -20

            fixme-easy-wins:
            	@echo "🚀 Available easy wins:"
            	@python3 fixme_resolution_tracker.py --easy-wins

            fixme-report:
            	@echo "📈 Generating full progress report..."
            	@python3 fixme_resolution_tracker.py --report
            	@echo "Report saved to FIXME_RESOLUTION_PROGRESS_REPORT.md"

            fixme-dry-run:
            	@echo "🔍 Showing what easy fixes would be applied:"
            	@python3 fixme_easy_wins.py --dry-run

            fixme-apply-easy:
            	@echo "🛠️  Applying automated easy fixes..."
            	@python3 fixme_easy_wins.py

            fixme-setup:
            	@echo "🔧 Setting up FIXME development environment..."
            	@python3 setup_fixme_environment.py

            fixme-help:
            	@echo "FIXME Resolution Targets:"
            	@echo "  fixme-status      - Show current progress"
            	@echo "  fixme-easy-wins   - List available easy fixes"
            	@echo "  fixme-report      - Generate full progress report"
            	@echo "  fixme-dry-run     - Preview automated fixes"
            	@echo "  fixme-apply-easy  - Apply automated easy fixes"
            	@echo "  fixme-setup       - Set up development environment"
        """
        ).strip()

        with open(makefile, "w") as f:
            f.write(makefile_content)


def main():
    """Main entry point for environment setup."""
    import argparse

    parser = argparse.ArgumentParser(description="FIXME Development Environment Setup")
    parser.add_argument("--repo", default=".", help="Repository root path")

    args = parser.parse_args()

    env_setup = FIXMEDevEnvironment(args.repo)
    env_setup.setup_environment()


if __name__ == "__main__":
    main()
