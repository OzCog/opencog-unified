#!/usr/bin/env python3
"""
Upstream Sync and Repair Assistant

Syncs with upstream OpenCog repositories to:
1. Identify resolved markers that we can learn from
2. Pull in recent fixes and improvements
3. Align our repairs with OpenCog best practices
4. Track upstream development patterns

Part of the Entelechy Framework repair process.
"""

import json
import re
import subprocess
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path


@dataclass
class UpstreamFix:
    """Represents a fix found in upstream repos."""

    repo: str
    commit_sha: str
    commit_date: str
    file_path: str
    marker_type: str
    fix_description: str
    diff_snippet: str
    applicable: bool = False


@dataclass
class SyncReport:
    """Report of upstream sync results."""

    timestamp: str
    repos_checked: list[str]
    fixes_found: int
    applicable_fixes: int
    markers_resolved_upstream: int
    recommendations: list[str]


class UpstreamSyncAssistant:
    """Manages syncing with upstream OpenCog repositories."""

    OPENCOG_REPOS = [
        "atomspace",
        "cogutil",
        "cogserver",
        "atomspace-rocks",
        "atomspace-restful",
        "ure",
        "pln",
        "moses",
        "attention",
        "spacetime",
        "unify",
        "miner",
        "lg-atomese",
        "learn",
        "language-learning",
        "opencog",
    ]

    MARKER_PATTERNS = [
        r"\bTODO\b",
        r"\bFIXME\b",
        r"\bXXX\b",
        r"\bHACK\b",
        r"\bSTUB\b",
        r"\bMOCK\b",
        r"\bNOT[_\s]?IMPLEMENTED\b",
        r"\bPLACEHOLDER\b",
    ]

    def __init__(self, repo_root: str = "."):
        self.repo_root = Path(repo_root).resolve()
        self.cache_dir = self.repo_root / ".upstream_cache"
        self.cache_dir.mkdir(exist_ok=True)
        self.fixes: list[UpstreamFix] = []

    def sync_repo(self, repo_name: str, days_back: int = 90) -> list[UpstreamFix]:
        """
        Sync with a specific upstream repo and find marker-related fixes.

        Args:
            repo_name: Name of the OpenCog repository
            days_back: How many days of history to check

        Returns:
            List of fixes found
        """
        print(f"\n🔍 Checking upstream: {repo_name}")

        repo_url = f"https://github.com/opencog/{repo_name}.git"
        repo_cache = self.cache_dir / repo_name

        fixes = []

        try:
            # Clone or update cache
            if repo_cache.exists():
                print("  Updating cache...")
                subprocess.run(["git", "-C", str(repo_cache), "fetch", "origin"], capture_output=True, check=True)
            else:
                print("  Cloning (this may take a moment)...")
                subprocess.run(
                    ["git", "clone", "--depth=100", repo_url, str(repo_cache)], capture_output=True, check=True
                )

            # Get commits that touch markers
            since_date = f"--since={days_back} days ago"

            # Search for commits that removed markers
            for pattern in self.MARKER_PATTERNS:
                result = subprocess.run(
                    ["git", "-C", str(repo_cache), "log", since_date, "--all", "-p", f"-G{pattern}"],
                    capture_output=True,
                    text=True,
                )

                if result.returncode == 0 and result.stdout:
                    commits = self._parse_git_log(result.stdout, repo_name, pattern)
                    fixes.extend(commits)

            print(f"  ✓ Found {len(fixes)} relevant commits")

        except subprocess.CalledProcessError as e:
            print(f"  ⚠ Error syncing {repo_name}: {e}")
        except Exception as e:
            print(f"  ⚠ Unexpected error: {e}")

        return fixes

    def _parse_git_log(self, log_output: str, repo: str, marker_pattern: str) -> list[UpstreamFix]:
        """Parse git log output to extract fixes."""
        fixes = []

        # Split into commits
        commits = re.split(r"^commit ", log_output, flags=re.MULTILINE)[1:]

        for commit_text in commits:
            lines = commit_text.split("\n")
            if not lines:
                continue

            sha = lines[0].strip()

            # Extract date
            date_match = re.search(r"^Date:\s+(.+)$", commit_text, re.MULTILINE)
            date = date_match.group(1).strip() if date_match else "Unknown"

            # Extract message
            msg_match = re.search(r"^\s{4,}(.+)$", commit_text, re.MULTILINE)
            description = msg_match.group(1).strip() if msg_match else "No description"

            # Check if markers were removed (lines with -)
            removed_markers = re.findall(rf"^-.*?({marker_pattern}).*?$", commit_text, re.MULTILINE | re.IGNORECASE)

            if removed_markers:
                # Extract file path
                file_match = re.search(r"^diff --git a/(\S+)", commit_text, re.MULTILINE)
                file_path = file_match.group(1) if file_match else "unknown"

                # Get diff snippet
                diff_lines = [l for l in lines if l.startswith(("-", "+")) and len(l) > 1]
                diff_snippet = "\n".join(diff_lines[:10])  # First 10 lines

                fix = UpstreamFix(
                    repo=repo,
                    commit_sha=sha[:8],
                    commit_date=date,
                    file_path=file_path,
                    marker_type=marker_pattern,
                    fix_description=description[:200],
                    diff_snippet=diff_snippet,
                )
                fixes.append(fix)

        return fixes

    def sync_all_repos(self, days_back: int = 90, max_repos: int = 5) -> SyncReport:
        """
        Sync with multiple upstream repos.

        Args:
            days_back: Days of history to check
            max_repos: Maximum number of repos to check (for time)

        Returns:
            SyncReport with findings
        """
        print("🔄 Syncing with upstream OpenCog repositories...")
        print(f"   Checking last {days_back} days across {max_repos} repos")

        all_fixes = []
        repos_to_check = self.OPENCOG_REPOS[:max_repos]

        for repo in repos_to_check:
            fixes = self.sync_repo(repo, days_back)
            all_fixes.extend(fixes)

        # Analyze applicability
        applicable_count = 0
        for fix in all_fixes:
            if self._is_applicable(fix):
                fix.applicable = True
                applicable_count += 1

        # Generate recommendations
        recommendations = self._generate_recommendations(all_fixes)

        report = SyncReport(
            timestamp=datetime.utcnow().isoformat() + "Z",
            repos_checked=repos_to_check,
            fixes_found=len(all_fixes),
            applicable_fixes=applicable_count,
            markers_resolved_upstream=len({f.file_path for f in all_fixes}),
            recommendations=recommendations,
        )

        self.fixes = all_fixes

        return report

    def _is_applicable(self, fix: UpstreamFix) -> bool:
        """Determine if a fix is applicable to our repo."""
        # Check if similar file exists
        local_file = self.repo_root / fix.file_path
        if local_file.exists():
            return True

        # Check in components
        component_match = re.match(r"^([\w-]+)/", fix.file_path)
        if component_match:
            component_match.group(1)
            for comp_dir in [
                "components/core",
                "components/logic",
                "components/cognitive",
                "components/advanced",
                "components/learning",
                "components/language",
            ]:
                potential = self.repo_root / comp_dir / fix.file_path
                if potential.exists():
                    return True

        return False

    def _generate_recommendations(self, fixes: list[UpstreamFix]) -> list[str]:
        """Generate actionable recommendations from upstream fixes."""
        recommendations = []

        # Group by repo
        by_repo = {}
        for fix in fixes:
            if fix.applicable:
                by_repo.setdefault(fix.repo, []).append(fix)

        if by_repo:
            recommendations.append(f"Found applicable fixes in {len(by_repo)} upstream repos")

            for repo, repo_fixes in sorted(by_repo.items(), key=lambda x: len(x[1]), reverse=True)[:3]:
                recommendations.append(f"- {repo}: {len(repo_fixes)} fixes to review")

        # Pattern analysis
        marker_counts = {}
        for fix in fixes:
            marker_counts[fix.marker_type] = marker_counts.get(fix.marker_type, 0) + 1

        if marker_counts:
            top_marker = max(marker_counts.items(), key=lambda x: x[1])
            recommendations.append(f"Most frequently resolved upstream: {top_marker[0]} ({top_marker[1]} times)")

        return recommendations

    def export_report(self, output_file: str = "upstream_sync_report.json"):
        """Export sync results to JSON."""
        output_path = self.repo_root / output_file

        data = {
            "fixes": [asdict(f) for f in self.fixes],
            "summary": {
                "total_fixes": len(self.fixes),
                "applicable_fixes": len([f for f in self.fixes if f.applicable]),
                "repos_with_fixes": len({f.repo for f in self.fixes}),
            },
        }

        with open(output_path, "w") as f:
            json.dump(data, f, indent=2)

        print(f"\n✓ Report exported to {output_file}")

    def show_applicable_fixes(self, max_count: int = 10):
        """Display applicable fixes for manual review."""
        applicable = [f for f in self.fixes if f.applicable]

        if not applicable:
            print("\n⚠ No applicable fixes found")
            return

        print(f"\n📋 {len(applicable)} Applicable Fixes Found:")
        print("=" * 70)

        for i, fix in enumerate(applicable[:max_count], 1):
            print(f"\n{i}. [{fix.repo}] {fix.file_path}")
            print(f"   Commit: {fix.commit_sha} ({fix.commit_date[:10]})")
            print(f"   Marker: {fix.marker_type}")
            print(f"   Fix: {fix.fix_description[:100]}")
            if fix.diff_snippet:
                print("   Preview:")
                for line in fix.diff_snippet.split("\n")[:3]:
                    print(f"     {line}")


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Sync with upstream OpenCog repos for repair guidance")
    parser.add_argument("--repo", default=".", help="Repository root path")
    parser.add_argument("--days", type=int, default=90, help="Days of history to check (default: 90)")
    parser.add_argument("--max-repos", type=int, default=5, help="Maximum repos to check (default: 5)")
    parser.add_argument("--export", default="upstream_sync_report.json", help="Export file name")
    parser.add_argument("--show", action="store_true", help="Show applicable fixes interactively")

    args = parser.parse_args()

    assistant = UpstreamSyncAssistant(args.repo)
    report = assistant.sync_all_repos(args.days, args.max_repos)

    # Display summary
    print("\n" + "=" * 70)
    print("📊 UPSTREAM SYNC SUMMARY")
    print("=" * 70)
    print(f"Repos checked: {len(report.repos_checked)}")
    print(f"Fixes found: {report.fixes_found}")
    print(f"Applicable fixes: {report.applicable_fixes}")
    print(f"Files with resolved markers: {report.markers_resolved_upstream}")

    print("\n💡 Recommendations:")
    for rec in report.recommendations:
        print(f"  • {rec}")

    # Export
    assistant.export_report(args.export)

    # Show fixes if requested
    if args.show:
        assistant.show_applicable_fixes()

    print("\n✓ Sync complete!")


if __name__ == "__main__":
    main()
