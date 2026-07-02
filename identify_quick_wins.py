#!/usr/bin/env python3
"""
Quick Win Identifier for Placeholder Resolution

This tool identifies placeholder markers (TODO, FIXME, STUB) that can be
easily resolved, categorized into:
- Obsolete markers (completed work)
- Documentation-only fixes
- Simple implementations (< 5 lines)
- Straightforward error handling
"""

import json
import os
import re


class QuickWinIdentifier:
    def __init__(self, repo_path: str = '.'):
        self.repo_path = repo_path
        self.quick_wins = {
            'obsolete': [],
            'documentation': [],
            'simple_implementation': [],
            'error_handling': [],
            'comment_cleanup': []
        }

        # Patterns for identifying quick wins
        self.obsolete_patterns = [
            r'(obsolete|deprecated|no longer|completed|done|finished)',
            r'(already implemented|now implemented|implemented in)',
            r'(not needed|unnecessary|removed)'
        ]

        self.doc_patterns = [
            r'(document|documentation|explain|describe)',
            r'(add comment|needs comment)',
            r'(clarify|unclear)'
        ]

        self.simple_impl_patterns = [
            r'(add check|add validation|validate)',
            r'(return null|return false|throw exception)',
            r'(simple|trivial|straightforward)'
        ]

        self.error_patterns = [
            r'(error handling|error check|null check)',
            r'(validate input|check input|input validation)',
            r'(exception|throw|catch)'
        ]

    def scan_file(self, filepath: str) -> None:
        """Scan a single file for quick win opportunities"""
        try:
            with open(filepath, encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()

            for i, line in enumerate(lines):
                # Skip std::placeholders
                if 'std::placeholders' in line or 'boost/mpl/placeholders' in line:
                    continue

                match = re.search(r'(TODO|FIXME|STUB|XXX)', line, re.IGNORECASE)
                if not match:
                    continue

                marker_type = match.group(1).upper()

                # Get context (5 lines before and after)
                start = max(0, i - 5)
                end = min(len(lines), i + 6)
                context = ''.join(lines[start:end])

                marker_info = {
                    'file': filepath,
                    'line': i + 1,
                    'marker_type': marker_type,
                    'content': line.strip(),
                    'context': context[:300]  # Limit context size
                }

                # Categorize the marker
                self._categorize_marker(marker_info, line.lower())

        except Exception as e:
            print(f"Error scanning {filepath}: {e}")

    def _categorize_marker(self, marker_info: dict, line_lower: str) -> None:
        """Categorize a marker as a potential quick win"""

        # Check for obsolete markers
        for pattern in self.obsolete_patterns:
            if re.search(pattern, line_lower):
                self.quick_wins['obsolete'].append(marker_info)
                return

        # Check for documentation needs
        for pattern in self.doc_patterns:
            if re.search(pattern, line_lower):
                self.quick_wins['documentation'].append(marker_info)
                return

        # Check for simple implementations
        for pattern in self.simple_impl_patterns:
            if re.search(pattern, line_lower):
                self.quick_wins['simple_implementation'].append(marker_info)
                return

        # Check for error handling
        for pattern in self.error_patterns:
            if re.search(pattern, line_lower):
                self.quick_wins['error_handling'].append(marker_info)
                return

        # Check for comment cleanup (remove stub language, etc.)
        if 'stub' in line_lower or 'placeholder' in line_lower:
            # Check if it's just describing existing code
            if 'fallback' in line_lower or 'compatibility' in line_lower:
                self.quick_wins['comment_cleanup'].append(marker_info)
                return

    def scan_repository(self) -> None:
        """Scan the entire repository for quick wins"""
        extensions = {'.cc', '.cpp', '.h', '.hpp', '.scm', '.py'}
        skip_dirs = {'.git', 'build', 'components', '__pycache__', '.devcontainer'}

        for root, dirs, files in os.walk(self.repo_path):
            # Filter out directories to skip
            dirs[:] = [d for d in dirs if d not in skip_dirs and not d.startswith('.')]

            for file in files:
                if any(file.endswith(ext) for ext in extensions):
                    filepath = os.path.join(root, file)
                    self.scan_file(filepath)

    def generate_report(self) -> dict:
        """Generate a comprehensive report of quick wins"""
        total_wins = sum(len(v) for v in self.quick_wins.values())

        report = {
            'summary': {
                'total_quick_wins': total_wins,
                'by_category': {k: len(v) for k, v in self.quick_wins.items()}
            },
            'quick_wins': self.quick_wins
        }

        return report

    def print_summary(self) -> None:
        """Print a summary of quick wins to console"""
        print("\n" + "="*60)
        print("QUICK WIN ANALYSIS - Placeholder Resolution Opportunities")
        print("="*60 + "\n")

        total = sum(len(v) for v in self.quick_wins.values())
        print(f"Total Quick Wins Identified: {total}\n")

        print("By Category:")
        print("-" * 60)

        categories = [
            ('obsolete', 'Obsolete markers (can be removed)', '✅'),
            ('documentation', 'Documentation only', '📝'),
            ('simple_implementation', 'Simple implementations', '⚡'),
            ('error_handling', 'Error handling additions', '🛡️'),
            ('comment_cleanup', 'Comment cleanup', '🧹')
        ]

        for cat_key, cat_name, emoji in categories:
            count = len(self.quick_wins[cat_key])
            if count > 0:
                print(f"{emoji} {cat_name:40} {count:4} markers")

        print("\n" + "-" * 60)
        print("\nTop 10 Easiest Fixes:\n")

        # Show samples from each category
        for cat_key, cat_name, emoji in categories[:3]:
            items = self.quick_wins[cat_key][:3]
            if items:
                print(f"\n{emoji} {cat_name}:")
                for item in items:
                    print(f"  {item['file']}:{item['line']}")
                    print(f"    {item['content'][:100]}")

        print("\n" + "="*60)
        print("\nNext Steps:")
        print("  1. Review the generated JSON report: quick_wins_report.json")
        print("  2. Start with obsolete markers (easiest)")
        print("  3. Move to documentation fixes")
        print("  4. Address simple implementations")
        print("  5. Track progress with entelechy_marker_resolver.py")
        print("="*60 + "\n")


def main():
    """Main entry point"""
    print("Scanning repository for quick win opportunities...")

    identifier = QuickWinIdentifier()
    identifier.scan_repository()

    # Generate report
    report = identifier.generate_report()

    # Save to JSON
    with open('quick_wins_report.json', 'w') as f:
        json.dump(report, f, indent=2)

    # Print summary
    identifier.print_summary()

    print("Detailed report saved to: quick_wins_report.json")


if __name__ == '__main__':
    main()
