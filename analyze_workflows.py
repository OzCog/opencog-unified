#!/usr/bin/env python3
"""
Comprehensive workflow analysis for opencog-unified repository
Identifies improvement opportunities and generates actionable recommendations
"""

import json
import re
from collections import defaultdict
from pathlib import Path

import yaml


class WorkflowAnalyzer:
    def __init__(self, repo_path):
        self.repo_path = Path(repo_path)
        self.workflows_dir = self.repo_path / ".github" / "workflows"
        self.issues = defaultdict(list)
        self.improvements = defaultdict(list)

    def analyze_all(self):
        """Run all analysis checks"""
        print("🔍 Analyzing GitHub Actions workflows...")

        for workflow_file in self.workflows_dir.glob("*.yml"):
            self.analyze_workflow(workflow_file)

        return self.generate_report()

    def analyze_workflow(self, workflow_path):
        """Analyze a single workflow file"""
        workflow_name = workflow_path.name

        try:
            with open(workflow_path) as f:
                content = f.read()

            # Parse YAML
            try:
                workflow_data = yaml.safe_load(content)
            except yaml.YAMLError as e:
                self.issues["yaml_errors"].append({"file": workflow_name, "error": str(e)})
                return

            # Check for outdated actions
            self.check_outdated_actions(workflow_name, content)

            # Check for missing error handling
            self.check_error_handling(workflow_name, content)

            # Check for cache optimization opportunities
            self.check_cache_usage(workflow_name, content, workflow_data)

            # Check for security issues
            self.check_security(workflow_name, content, workflow_data)

            # Check for redundant rebuilds
            self.check_redundant_builds(workflow_name, content)

            # Check for missing concurrency controls
            self.check_concurrency(workflow_name, workflow_data)

            # Check for missing timeout settings
            self.check_timeouts(workflow_name, workflow_data)

            # Check for placeholder/TODO comments
            self.check_placeholders(workflow_name, content)

        except Exception as e:
            self.issues["analysis_errors"].append({"file": workflow_name, "error": str(e)})

    def check_outdated_actions(self, workflow_name, content):
        """Check for outdated GitHub Actions versions"""
        # Check for old checkout versions
        if re.search(r"actions/checkout@v[12]", content):
            self.improvements["outdated_actions"].append(
                {
                    "file": workflow_name,
                    "issue": "Using outdated checkout action (v1 or v2)",
                    "recommendation": "Update to actions/checkout@v4",
                }
            )

        # Check for old cache versions
        if re.search(r"actions/cache@v[12]", content):
            self.improvements["outdated_actions"].append(
                {
                    "file": workflow_name,
                    "issue": "Using outdated cache action (v1 or v2)",
                    "recommendation": "Update to actions/cache@v4",
                }
            )

        # Check for old upload-artifact versions
        if re.search(r"actions/upload-artifact@v[123]", content):
            self.improvements["outdated_actions"].append(
                {
                    "file": workflow_name,
                    "issue": "Using outdated upload-artifact action",
                    "recommendation": "Update to actions/upload-artifact@v4",
                }
            )

    def check_error_handling(self, workflow_name, content):
        """Check for proper error handling"""
        # Check for set -e usage
        if "run:" in content and "set -e" not in content and "set -euo pipefail" not in content:
            bash_blocks = len(re.findall(r"run:\s*\|", content))
            error_handling = len(re.findall(r"set -e", content))

            if bash_blocks > error_handling:
                self.improvements["error_handling"].append(
                    {
                        "file": workflow_name,
                        "issue": "Some bash scripts missing error handling",
                        "recommendation": 'Add "set -euo pipefail" to all multi-line bash scripts',
                    }
                )

    def check_cache_usage(self, workflow_name, content, workflow_data):
        """Check for cache optimization opportunities"""
        if "apt-get install" in content and "actions/cache" not in content:
            self.improvements["cache_optimization"].append(
                {
                    "file": workflow_name,
                    "issue": "Installing packages without caching",
                    "recommendation": "Add cache for apt packages to speed up builds",
                }
            )

        if "pip install" in content or "pip3 install" in content:
            if "actions/cache" not in content or "~/.cache/pip" not in content:
                self.improvements["cache_optimization"].append(
                    {
                        "file": workflow_name,
                        "issue": "Installing Python packages without pip cache",
                        "recommendation": "Add cache for ~/.cache/pip",
                    }
                )

    def check_security(self, workflow_name, content, workflow_data):
        """Check for security issues"""
        # Check for write permissions
        if workflow_data and "permissions" in workflow_data:
            perms = workflow_data["permissions"]
            if isinstance(perms, dict):
                for perm, value in perms.items():
                    if value == "write" and perm not in ["contents", "pull-requests", "issues"]:
                        self.issues["security"].append(
                            {
                                "file": workflow_name,
                                "issue": f"Potentially unnecessary write permission: {perm}",
                                "recommendation": "Review and minimize permissions",
                            }
                        )

        # Check for secrets in logs
        if re.search(r"echo.*\$\{\{.*secret", content, re.IGNORECASE):
            self.issues["security"].append(
                {
                    "file": workflow_name,
                    "issue": "Potential secret exposure in logs",
                    "recommendation": "Never echo secrets, use ::add-mask:: if needed",
                }
            )

    def check_redundant_builds(self, workflow_name, content):
        """Check for redundant rebuild patterns"""
        rebuild_count = len(re.findall(r"Rebuild and Install", content))
        if rebuild_count > 3:
            self.improvements["redundant_builds"].append(
                {
                    "file": workflow_name,
                    "issue": f"Multiple redundant rebuilds detected ({rebuild_count})",
                    "recommendation": "Use build artifacts or Docker images to avoid rebuilding dependencies",
                }
            )

    def check_concurrency(self, workflow_name, workflow_data):
        """Check for missing concurrency controls"""
        if workflow_data and "concurrency" not in workflow_data:
            # Check if it's a workflow that could benefit from concurrency control
            if workflow_data.get("on", {}).get("pull_request") or workflow_data.get("on", {}).get("push"):
                self.improvements["concurrency"].append(
                    {
                        "file": workflow_name,
                        "issue": "Missing concurrency control",
                        "recommendation": "Add concurrency group to cancel outdated runs",
                    }
                )

    def check_timeouts(self, workflow_name, workflow_data):
        """Check for missing timeout settings"""
        if workflow_data and "jobs" in workflow_data:
            for job_name, job_data in workflow_data["jobs"].items():
                if isinstance(job_data, dict) and "timeout-minutes" not in job_data:
                    self.improvements["timeouts"].append(
                        {
                            "file": workflow_name,
                            "job": job_name,
                            "issue": "Missing timeout setting",
                            "recommendation": "Add timeout-minutes to prevent hung jobs",
                        }
                    )

    def check_placeholders(self, workflow_name, content):
        """Check for placeholder implementations and TODOs"""
        placeholders = re.findall(r"#.*?(TODO|FIXME|XXX|HACK|TBD|placeholder).*", content, re.IGNORECASE)
        if placeholders:
            self.improvements["placeholders"].append(
                {
                    "file": workflow_name,
                    "count": len(placeholders),
                    "samples": placeholders[:3],
                    "recommendation": "Resolve placeholder comments and TODOs",
                }
            )

    def generate_report(self):
        """Generate comprehensive analysis report"""
        report = {
            "summary": {
                "total_workflows": len(list(self.workflows_dir.glob("*.yml"))),
                "total_issues": sum(len(v) for v in self.issues.values()),
                "total_improvements": sum(len(v) for v in self.improvements.values()),
            },
            "issues": dict(self.issues),
            "improvements": dict(self.improvements),
        }

        return report


if __name__ == "__main__":
    analyzer = WorkflowAnalyzer("/home/ubuntu/opencog-unified")
    report = analyzer.analyze_all()

    # Save report
    with open("/home/ubuntu/opencog-unified/workflow_analysis_report.json", "w") as f:
        json.dump(report, f, indent=2)

    print("\n📊 Analysis Complete!")
    print(f"   Total workflows: {report['summary']['total_workflows']}")
    print(f"   Issues found: {report['summary']['total_issues']}")
    print(f"   Improvements identified: {report['summary']['total_improvements']}")
    print("\n📄 Report saved to: workflow_analysis_report.json")
