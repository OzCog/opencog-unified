#!/usr/bin/env python3
"""
Comprehensive workflow improvement implementation
Applies engineering excellence to GitHub Actions workflows
"""

import re
from pathlib import Path


class WorkflowImprover:
    def __init__(self, repo_path):
        self.repo_path = Path(repo_path)
        self.workflows_dir = self.repo_path / ".github" / "workflows"
        self.improvements_applied = []

    def improve_all(self):
        """Apply all improvements to workflows"""
        print("🚀 Applying workflow improvements...")

        for workflow_file in self.workflows_dir.glob("*.yml"):
            self.improve_workflow(workflow_file)

        return self.improvements_applied

    def improve_workflow(self, workflow_path):
        """Improve a single workflow file"""
        workflow_name = workflow_path.name
        print(f"\n📝 Processing: {workflow_name}")

        try:
            with open(workflow_path) as f:
                content = f.read()
                original_content = content

            # Apply improvements
            content = self.add_concurrency_control(workflow_name, content)
            content = self.add_timeout_settings(workflow_name, content)
            content = self.improve_caching(workflow_name, content)
            content = self.fix_security_issues(workflow_name, content)
            content = self.add_error_handling(workflow_name, content)
            content = self.optimize_redundant_builds(workflow_name, content)

            # Write back if changed
            if content != original_content:
                with open(workflow_path, "w") as f:
                    f.write(content)
                print(f"   ✅ Improved {workflow_name}")
                self.improvements_applied.append(workflow_name)
            else:
                print(f"   ℹ️  No changes needed for {workflow_name}")

        except Exception as e:
            print(f"   ❌ Error processing {workflow_name}: {e}")

    def add_concurrency_control(self, workflow_name, content):
        """Add concurrency control to cancel outdated runs"""
        # Check if already has concurrency
        if "concurrency:" in content:
            return content

        # Check if workflow triggers on push or PR
        if not ("on:" in content and ("push:" in content or "pull_request:" in content)):
            return content

        # Add concurrency control after 'on:' section
        concurrency_block = """
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
"""

        # Find the position after 'on:' section and before 'env:' or 'jobs:'
        pattern = r"(on:.*?(?=\n(?:env:|jobs:|$)))"
        match = re.search(pattern, content, re.DOTALL)

        if match:
            insert_pos = match.end()
            content = content[:insert_pos] + "\n" + concurrency_block + content[insert_pos:]
            print("   + Added concurrency control")

        return content

    def add_timeout_settings(self, workflow_name, content):
        """Add timeout settings to jobs"""
        lines = content.split("\n")
        new_lines = []
        in_job = False
        job_indent = 0
        timeout_added = False

        for i, line in enumerate(lines):
            new_lines.append(line)

            # Detect job definition
            if re.match(r"^  \w+:", line) and i > 0 and "jobs:" in lines[i - 1]:
                in_job = True
                job_indent = len(line) - len(line.lstrip())
                timeout_added = False

            # Check if timeout already exists
            if in_job and "timeout-minutes:" in line:
                timeout_added = True

            # Add timeout after runs-on if not present
            if in_job and not timeout_added and "runs-on:" in line:
                indent = " " * (job_indent + 2)
                new_lines.append(f"{indent}timeout-minutes: 120")
                timeout_added = True
                print("   + Added timeout to job")

            # Reset when next job starts
            if in_job and re.match(r"^  \w+:", line) and i > 0:
                in_job = False

        return "\n".join(new_lines)

    def improve_caching(self, workflow_name, content):
        """Add caching for apt packages and pip"""
        # Add apt cache if apt-get install is used but no apt cache exists
        if "apt-get install" in content and "path: /var/cache/apt" not in content:
            # Find first apt-get install step
            pattern = r"(- name: Install Dependencies\n      run: \|)"
            replacement = r"""\1
        # Cache apt packages
      - name: Cache APT packages
        uses: actions/cache@v4
        with:
          path: /var/cache/apt/archives
          key: apt-cache-${{ runner.os }}-${{ hashFiles('**/*.yml') }}
          restore-keys: |
            apt-cache-${{ runner.os }}-

      - name: Install Dependencies
        run: |"""

            if re.search(pattern, content):
                content = re.sub(pattern, replacement, content, count=1)
                print("   + Added APT package caching")

        # Add pip cache if pip install is used but no pip cache exists
        if ("pip install" in content or "pip3 install" in content) and "~/.cache/pip" not in content:
            pattern = r"(- name: .*[Pp]ip.*\n      run: \|)"
            if re.search(pattern, content):
                # Add pip cache before first pip install
                pip_cache = """
      - name: Cache pip packages
        uses: actions/cache@v4
        with:
          path: ~/.cache/pip
          key: pip-${{ runner.os }}-${{ hashFiles('**/requirements.txt') }}
          restore-keys: |
            pip-${{ runner.os }}-
"""
                # Insert before first pip-related step
                lines = content.split("\n")
                for i, line in enumerate(lines):
                    if "pip install" in line or "pip3 install" in line:
                        # Find the step name above
                        for j in range(i - 1, max(0, i - 10), -1):
                            if "- name:" in lines[j]:
                                lines.insert(j, pip_cache)
                                print("   + Added pip caching")
                                content = "\n".join(lines)
                                break
                        break

        return content

    def fix_security_issues(self, workflow_name, content):
        """Fix security issues like unnecessary permissions"""
        # Fix unnecessary 'actions: write' permission
        if "actions: write" in content:
            # Check if it's actually needed (for workflow dispatch or similar)
            if "workflow_dispatch" not in content and "repository_dispatch" not in content:
                content = content.replace("actions: write", "actions: read")
                print("   + Reduced actions permission from write to read")

        return content

    def add_error_handling(self, workflow_name, content):
        """Add proper error handling to bash scripts"""
        # Find multi-line run blocks without set -e

        def add_set_e(match):
            return match.group(1) + "        set -euo pipefail\n" + match.group(2) + match.group(3)

        # Only add if not already present
        lines = content.split("\n")
        new_lines = []
        in_multiline_run = False
        has_set_e = False

        for line in lines:
            if "run: |" in line:
                in_multiline_run = True
                has_set_e = False
                new_lines.append(line)
            elif in_multiline_run:
                if "set -e" in line or "set -euo pipefail" in line:
                    has_set_e = True
                    new_lines.append(line)
                elif not has_set_e and line.strip() and not line.strip().startswith("#"):
                    # First non-comment line in run block
                    indent = len(line) - len(line.lstrip())
                    new_lines.append(" " * indent + "set -euo pipefail")
                    new_lines.append(line)
                    has_set_e = True
                    print("   + Added error handling (set -euo pipefail)")
                else:
                    new_lines.append(line)

                # Check if we're exiting the run block
                if line and not line.startswith(" " * 8) and line.strip():
                    in_multiline_run = False
            else:
                new_lines.append(line)

        return "\n".join(new_lines)

    def optimize_redundant_builds(self, workflow_name, content):
        """Optimize redundant rebuild patterns"""
        # Count rebuild patterns
        rebuild_count = len(re.findall(r"Rebuild and Install", content))

        if rebuild_count > 3:
            # Add a comment suggesting Docker-based builds
            suggestion = """
# NOTE: This workflow rebuilds dependencies multiple times.
# Consider using Docker images or build artifacts to optimize build time.
# See: https://docs.github.com/en/actions/using-workflows/caching-dependencies-to-speed-up-workflows
"""
            if suggestion not in content:
                # Add at the top after the initial comments
                lines = content.split("\n")
                for i, line in enumerate(lines):
                    if line.startswith("on:"):
                        lines.insert(i, suggestion)
                        content = "\n".join(lines)
                        print("   + Added optimization suggestion comment")
                        break

        return content


if __name__ == "__main__":
    improver = WorkflowImprover("/home/ubuntu/opencog-unified")
    improved = improver.improve_all()

    print(f"\n{'=' * 60}")
    print("✅ Workflow Improvement Complete!")
    print(f"{'=' * 60}")
    print(f"Total workflows improved: {len(improved)}")
    if improved:
        print("\nImproved workflows:")
        for wf in improved:
            print(f"  - {wf}")
