#!/usr/bin/env python3
"""
Intelligent Marker Repair System

Automated repair system for code markers with:
1. Smart categorization and prioritization
2. Pattern-based repair suggestions
3. Safe automated fixes for simple cases
4. Human review workflow for complex cases
5. Continuous validation and testing

Part of the Entelechy Framework repair process.
"""

import json
import re
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path


@dataclass
class RepairAction:
    """Represents a repair action to be taken."""
    file_path: str
    line_number: int
    marker_type: str
    original_line: str
    repair_type: str  # remove, document, implement, defer
    new_content: str | None = None
    confidence: float = 0.0  # 0.0 to 1.0
    reason: str = ""
    requires_review: bool = True
    tests_needed: list[str] = None


class IntelligentMarkerRepair:
    """Intelligent system for automated marker repair."""

    # Safe removal patterns - comments that can be safely removed
    SAFE_REMOVAL_PATTERNS = [
        r'^\s*#\s*TODO:?\s*$',  # Empty TODO
        r'^\s*//\s*TODO:?\s*$',  # Empty TODO
        r'^\s*#\s*FIXME:?\s*$',  # Empty FIXME
        r'^\s*//\s*FIXME:?\s*$',  # Empty FIXME
    ]

    # Documentation markers - should become proper docs
    DOC_MARKERS = [
        r'TODO.*document',
        r'TODO.*explain',
        r'TODO.*describe',
        r'FIXME.*comment',
    ]

    # Test markers - need test implementation
    TEST_MARKERS = [
        r'TODO.*test',
        r'TODO.*verify',
        r'FIXME.*test',
        r'STUB.*test',
    ]

    # Implementation markers - need actual code
    IMPL_MARKERS = [
        r'STUB\b',
        r'NOT[_\s]?IMPLEMENTED',
        r'PLACEHOLDER',
        r'MOCK\b',
        r'TODO.*implement',
        r'FIXME.*implement',
    ]

    def __init__(self, repo_root: str = '.'):
        self.repo_root = Path(repo_root).resolve()
        self.repairs: list[RepairAction] = []
        self.stats = {
            'total_analyzed': 0,
            'safe_removals': 0,
            'doc_needed': 0,
            'impl_needed': 0,
            'test_needed': 0,
            'deferred': 0
        }

    def analyze_marker(self, file_path: str, line_num: int,
                      line_content: str, marker_type: str) -> RepairAction:
        """
        Analyze a marker and determine repair action.

        Returns:
            RepairAction with recommended fix
        """
        content_lower = line_content.lower()

        # Check for safe removal
        for pattern in self.SAFE_REMOVAL_PATTERNS:
            if re.search(pattern, line_content, re.IGNORECASE):
                return RepairAction(
                    file_path=file_path,
                    line_number=line_num,
                    marker_type=marker_type,
                    original_line=line_content,
                    repair_type='remove',
                    new_content=None,
                    confidence=0.9,
                    reason='Empty marker with no information',
                    requires_review=False
                )

        # Check for documentation needs
        for pattern in self.DOC_MARKERS:
            if re.search(pattern, content_lower):
                self.stats['doc_needed'] += 1
                return self._suggest_documentation(
                    file_path, line_num, line_content, marker_type
                )

        # Check for test needs
        for pattern in self.TEST_MARKERS:
            if re.search(pattern, content_lower):
                self.stats['test_needed'] += 1
                return self._suggest_test(
                    file_path, line_num, line_content, marker_type
                )

        # Check for implementation needs
        for pattern in self.IMPL_MARKERS:
            if re.search(pattern, content_lower):
                self.stats['impl_needed'] += 1
                return self._suggest_implementation(
                    file_path, line_num, line_content, marker_type
                )

        # Default: defer for manual review
        self.stats['deferred'] += 1
        return RepairAction(
            file_path=file_path,
            line_number=line_num,
            marker_type=marker_type,
            original_line=line_content,
            repair_type='defer',
            confidence=0.0,
            reason='Requires manual analysis',
            requires_review=True
        )

    def _suggest_documentation(self, file_path: str, line_num: int,
                              line_content: str, marker_type: str) -> RepairAction:
        """Suggest documentation improvement."""

        # Extract what needs documentation
        doc_match = re.search(
            r'(?:TODO|FIXME):?\s*(.+)',
            line_content,
            re.IGNORECASE
        )
        doc_desc = doc_match.group(1).strip() if doc_match else 'Add documentation'

        # Generate docstring template based on file type
        file_ext = Path(file_path).suffix

        if file_ext in ['.py']:
            new_content = f'    """{doc_desc}"""'
            confidence = 0.7
        elif file_ext in ['.cc', '.cpp', '.h']:
            new_content = f'    /// {doc_desc}'
            confidence = 0.7
        elif file_ext in ['.scm']:
            new_content = f'    ;; {doc_desc}'
            confidence = 0.7
        else:
            new_content = None
            confidence = 0.3

        return RepairAction(
            file_path=file_path,
            line_number=line_num,
            marker_type=marker_type,
            original_line=line_content,
            repair_type='document',
            new_content=new_content,
            confidence=confidence,
            reason=f'Convert marker to proper documentation: {doc_desc[:50]}',
            requires_review=True
        )

    def _suggest_test(self, file_path: str, line_num: int,
                     line_content: str, marker_type: str) -> RepairAction:
        """Suggest test implementation."""

        test_desc = re.search(
            r'(?:TODO|FIXME|STUB):?\s*(.+)',
            line_content,
            re.IGNORECASE
        )
        desc = test_desc.group(1).strip() if test_desc else 'Add test'

        return RepairAction(
            file_path=file_path,
            line_number=line_num,
            marker_type=marker_type,
            original_line=line_content,
            repair_type='test',
            confidence=0.5,
            reason=f'Test needed: {desc[:50]}',
            requires_review=True,
            tests_needed=[desc]
        )

    def _suggest_implementation(self, file_path: str, line_num: int,
                               line_content: str, marker_type: str) -> RepairAction:
        """Suggest implementation approach."""

        impl_desc = re.search(
            r'(?:STUB|TODO|FIXME|NOT[_\s]?IMPLEMENTED):?\s*(.+)',
            line_content,
            re.IGNORECASE
        )
        desc = impl_desc.group(1).strip() if impl_desc else 'Implement functionality'

        return RepairAction(
            file_path=file_path,
            line_number=line_num,
            marker_type=marker_type,
            original_line=line_content,
            repair_type='implement',
            confidence=0.3,
            reason=f'Implementation needed: {desc[:50]}',
            requires_review=True
        )

    def scan_and_analyze(self, marker_file: str = 'entelechy_marker_analysis.json') -> int:
        """
        Scan markers from analysis and create repair actions.

        Returns:
            Number of repair actions created
        """
        marker_path = self.repo_root / marker_file

        if not marker_path.exists():
            print(f"⚠ Marker analysis not found: {marker_path}")
            print("  Run: python3 entelechy_marker_analyzer.py")
            return 0

        with open(marker_path) as f:
            analysis = json.load(f)

        markers = analysis.get('markers', [])
        self.stats['total_analyzed'] = len(markers)

        print(f"🔍 Analyzing {len(markers)} markers...")

        for marker in markers:
            action = self.analyze_marker(
                marker['file_path'],
                marker['line_number'],
                marker.get('content', marker.get('line_content', '')),
                marker['marker_type']
            )
            self.repairs.append(action)

        return len(self.repairs)

    def apply_safe_repairs(self, dry_run: bool = True) -> dict:
        """
        Apply repairs with high confidence that don't require review.

        Args:
            dry_run: If True, don't actually modify files

        Returns:
            Dict with results
        """
        safe_repairs = [
            r for r in self.repairs
            if not r.requires_review and r.confidence >= 0.8
        ]

        if not safe_repairs:
            return {
                'applied': 0,
                'message': 'No safe repairs available'
            }

        print(f"🔧 Applying {len(safe_repairs)} safe repairs...")

        if dry_run:
            print("  (DRY RUN - no files will be modified)")

        applied = 0
        errors = []

        # Group by file for efficiency
        by_file = {}
        for repair in safe_repairs:
            by_file.setdefault(repair.file_path, []).append(repair)

        for file_path, file_repairs in by_file.items():
            try:
                full_path = self.repo_root / file_path

                if not full_path.exists():
                    errors.append(f"File not found: {file_path}")
                    continue

                # Read file
                with open(full_path, encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()

                # Apply repairs (in reverse order to preserve line numbers)
                for repair in sorted(file_repairs,
                                   key=lambda r: r.line_number,
                                   reverse=True):
                    line_idx = repair.line_number - 1

                    if line_idx < 0 or line_idx >= len(lines):
                        errors.append(
                            f"Invalid line {repair.line_number} in {file_path}"
                        )
                        continue

                    if repair.repair_type == 'remove':
                        # Remove the line
                        del lines[line_idx]
                        applied += 1
                    elif repair.repair_type == 'document' and repair.new_content:
                        # Replace with documentation
                        lines[line_idx] = repair.new_content + '\n'
                        applied += 1

                # Write back
                if not dry_run and applied > 0:
                    with open(full_path, 'w', encoding='utf-8') as f:
                        f.writelines(lines)

            except Exception as e:
                errors.append(f"Error processing {file_path}: {e}")

        return {
            'applied': applied,
            'errors': errors,
            'dry_run': dry_run
        }

    def export_repair_plan(self, output_file: str = 'repair_plan.json'):
        """Export repair plan for review and tracking."""
        output_path = self.repo_root / output_file

        plan = {
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'statistics': self.stats,
            'repairs': [asdict(r) for r in self.repairs],
            'summary': {
                'total_repairs': len(self.repairs),
                'safe_auto': len([r for r in self.repairs if not r.requires_review]),
                'needs_review': len([r for r in self.repairs if r.requires_review]),
                'by_type': {
                    'remove': len([r for r in self.repairs if r.repair_type == 'remove']),
                    'document': len([r for r in self.repairs if r.repair_type == 'document']),
                    'implement': len([r for r in self.repairs if r.repair_type == 'implement']),
                    'test': len([r for r in self.repairs if r.repair_type == 'test']),
                    'defer': len([r for r in self.repairs if r.repair_type == 'defer']),
                }
            }
        }

        with open(output_path, 'w') as f:
            json.dump(plan, f, indent=2)

        print(f"\n✓ Repair plan exported to {output_file}")

        return plan

    def generate_quick_wins_list(self, max_count: int = 20) -> list[RepairAction]:
        """Generate list of quick wins for immediate action."""
        quick_wins = [
            r for r in self.repairs
            if r.confidence >= 0.7 and r.repair_type in ['remove', 'document']
        ]

        # Sort by confidence
        quick_wins.sort(key=lambda r: r.confidence, reverse=True)

        return quick_wins[:max_count]


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Intelligent marker repair system'
    )
    parser.add_argument(
        '--repo', default='.',
        help='Repository root path'
    )
    parser.add_argument(
        '--analyze', action='store_true',
        help='Analyze markers and create repair plan'
    )
    parser.add_argument(
        '--apply', action='store_true',
        help='Apply safe repairs'
    )
    parser.add_argument(
        '--dry-run', action='store_true', default=True,
        help='Dry run mode (default: True)'
    )
    parser.add_argument(
        '--export', default='repair_plan.json',
        help='Export repair plan file'
    )

    args = parser.parse_args()

    repairer = IntelligentMarkerRepair(args.repo)

    if args.analyze:
        count = repairer.scan_and_analyze()
        print(f"\n✓ Analyzed {count} markers")

        # Show statistics
        print("\n📊 Repair Analysis:")
        print(f"  Safe removals: {repairer.stats['safe_removals']}")
        print(f"  Documentation needed: {repairer.stats['doc_needed']}")
        print(f"  Implementation needed: {repairer.stats['impl_needed']}")
        print(f"  Test needed: {repairer.stats['test_needed']}")
        print(f"  Deferred: {repairer.stats['deferred']}")

        # Export plan
        repairer.export_repair_plan(args.export)

        print("\n💡 Quick Wins:")
        quick_wins = repairer.generate_quick_wins_list(10)
        for i, win in enumerate(quick_wins, 1):
            print(f"  {i}. {win.file_path}:{win.line_number}")
            print(f"     {win.reason} (confidence: {win.confidence:.0%})")

    if args.apply:
        results = repairer.apply_safe_repairs(dry_run=args.dry_run)

        print("\n✓ Results:")
        print(f"  Applied: {results['applied']}")
        if results.get('errors'):
            print(f"  Errors: {len(results['errors'])}")
            for err in results['errors'][:5]:
                print(f"    - {err}")

        if results['dry_run']:
            print("\n  To apply for real, use: --apply --no-dry-run")


if __name__ == '__main__':
    main()
