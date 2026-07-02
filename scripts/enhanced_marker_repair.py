#!/usr/bin/env python3
"""
Enhanced Marker Repair System - Phase 2

This script extends the intelligent_marker_repair.py with:
1. More comprehensive pattern recognition for quick wins
2. Obsolete marker detection (code that says "not needed", "obsolete", "deprecated")
3. Empty marker cleanup
4. Documentation conversion for bare TODO/FIXME comments
5. Safe bare except cleanup for Python files

Part of the Entelechy Framework repair process - Next Phase.
"""

import json
import re
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path


@dataclass
class EnhancedRepairAction:
    """Enhanced repair action with more context."""
    file_path: str
    line_number: int
    marker_type: str
    original_line: str
    repair_type: str  # remove, replace, document, convert, implement, defer
    new_content: str | None = None
    confidence: float = 0.0
    reason: str = ""
    category: str = "general"  # obsolete, empty, documentation, bare_except, etc.
    requires_review: bool = True
    applied: bool = False


class EnhancedMarkerRepair:
    """Enhanced repair system with more patterns and actual fix application."""

    # Patterns for markers that indicate obsolete/unnecessary code
    OBSOLETE_PATTERNS = [
        (r'(?:XXX\s*)?(?:FIXME|TODO):?\s*.*?(?:not\s+needed|unnecessary|obsolete|deprecated|remove\s+this|can\s+be\s+removed)',
         'obsolete', 'Marker indicates code is obsolete or not needed'),
        (r'(?:XXX\s*)?(?:FIXME|TODO):?\s*.*?(?:should\s+be\s+(?:removed|deleted)|no\s+longer\s+(?:needed|required|used))',
         'obsolete', 'Marker indicates code should be removed'),
        (r'(?:XXX\s*)?(?:FIXME|TODO):?\s*.*?(?:this\s+is\s+(?:a\s+)?(?:hack|temporary|workaround)\s+.*?(?:remove|fix))',
         'obsolete', 'Temporary hack that should be addressed'),
    ]

    # Empty or near-empty markers
    EMPTY_PATTERNS = [
        (r'^\s*(?:#|//|;)\s*(?:TODO|FIXME|XXX|HACK):?\s*$', 'empty', 'Empty marker with no description'),
        (r'^\s*(?:#|//|;)\s*(?:TODO|FIXME|XXX|HACK):?\s*\.{1,3}\s*$', 'empty', 'Marker with only dots'),
        (r'^\s*(?:#|//|;)\s*(?:TODO|FIXME|XXX|HACK):?\s*\?\s*$', 'empty', 'Marker with only question mark'),
    ]

    # Bare except patterns (Python - common anti-pattern)
    BARE_EXCEPT_PATTERNS = [
        (r'except:\s*#\s*(?:FIXME|TODO)', 'bare_except', 'Bare except with FIXME marker'),
    ]

    # Documentation markers that can be converted
    DOC_CONVERSION_PATTERNS = [
        (r'(?:TODO|FIXME):?\s*(?:add\s+)?(?:document(?:ation)?|comment|explain)',
         'documentation', 'Request for documentation'),
        (r'(?:TODO|FIXME):?\s*(?:describe|explain)\s+(?:this|what)',
         'documentation', 'Request for explanation'),
    ]

    # Patterns indicating completed work (safe to remove)
    COMPLETED_PATTERNS = [
        (r'(?:XXX\s*)?(?:TODO|FIXME):?\s*.*?(?:done|completed|fixed|resolved|implemented)',
         'completed', 'Marker indicates work is done'),
    ]

    def __init__(self, repo_root: str = '.'):
        self.repo_root = Path(repo_root).resolve()
        self.repairs: list[EnhancedRepairAction] = []
        self.stats = {
            'scanned_files': 0,
            'total_markers_found': 0,
            'repairs_identified': 0,
            'by_category': {},
            'by_confidence': {'high': 0, 'medium': 0, 'low': 0},
            'applied': 0,
            'errors': []
        }

    def scan_file(self, file_path: Path) -> list[EnhancedRepairAction]:
        """Scan a single file for repairable markers."""
        repairs = []

        try:
            with open(file_path, encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
        except Exception as e:
            self.stats['errors'].append(f"Error reading {file_path}: {e}")
            return repairs

        rel_path = str(file_path.relative_to(self.repo_root))

        for line_num, line in enumerate(lines, 1):
            # Check for marker presence first
            if not re.search(r'(?:TODO|FIXME|XXX|HACK|STUB|MOCK|PLACEHOLDER)', line, re.IGNORECASE):
                continue

            self.stats['total_markers_found'] += 1

            # Check each pattern category
            repair = self._analyze_line(rel_path, line_num, line)
            if repair:
                repairs.append(repair)
                self.stats['repairs_identified'] += 1

                # Track by category
                cat = repair.category
                self.stats['by_category'][cat] = self.stats['by_category'].get(cat, 0) + 1

                # Track by confidence
                if repair.confidence >= 0.8:
                    self.stats['by_confidence']['high'] += 1
                elif repair.confidence >= 0.5:
                    self.stats['by_confidence']['medium'] += 1
                else:
                    self.stats['by_confidence']['low'] += 1

        return repairs

    def _analyze_line(self, file_path: str, line_num: int, line: str) -> EnhancedRepairAction | None:
        """Analyze a line for repair opportunities."""
        line_stripped = line.strip()

        # Check empty patterns (highest confidence)
        for pattern, category, reason in self.EMPTY_PATTERNS:
            if re.search(pattern, line, re.IGNORECASE):
                return EnhancedRepairAction(
                    file_path=file_path,
                    line_number=line_num,
                    marker_type=self._extract_marker_type(line),
                    original_line=line_stripped,
                    repair_type='remove',
                    confidence=0.95,
                    reason=reason,
                    category=category,
                    requires_review=False
                )

        # Check completed patterns
        for pattern, category, reason in self.COMPLETED_PATTERNS:
            if re.search(pattern, line, re.IGNORECASE):
                return EnhancedRepairAction(
                    file_path=file_path,
                    line_number=line_num,
                    marker_type=self._extract_marker_type(line),
                    original_line=line_stripped,
                    repair_type='remove',
                    confidence=0.75,
                    reason=reason,
                    category=category,
                    requires_review=True  # Still review completed work markers
                )

        # Check obsolete patterns
        for pattern, category, reason in self.OBSOLETE_PATTERNS:
            if re.search(pattern, line, re.IGNORECASE):
                return EnhancedRepairAction(
                    file_path=file_path,
                    line_number=line_num,
                    marker_type=self._extract_marker_type(line),
                    original_line=line_stripped,
                    repair_type='review',
                    confidence=0.6,
                    reason=reason,
                    category=category,
                    requires_review=True
                )

        # Check bare except patterns (Python files only)
        if file_path.endswith('.py'):
            for pattern, category, reason in self.BARE_EXCEPT_PATTERNS:
                if re.search(pattern, line, re.IGNORECASE):
                    return EnhancedRepairAction(
                        file_path=file_path,
                        line_number=line_num,
                        marker_type='FIXME',
                        original_line=line_stripped,
                        repair_type='convert',
                        new_content=re.sub(r'except:', 'except Exception:', line.rstrip()),
                        confidence=0.85,
                        reason=reason,
                        category=category,
                        requires_review=False
                    )

        # Check documentation patterns
        for pattern, category, reason in self.DOC_CONVERSION_PATTERNS:
            if re.search(pattern, line, re.IGNORECASE):
                return EnhancedRepairAction(
                    file_path=file_path,
                    line_number=line_num,
                    marker_type=self._extract_marker_type(line),
                    original_line=line_stripped,
                    repair_type='document',
                    confidence=0.5,
                    reason=reason,
                    category=category,
                    requires_review=True
                )

        return None

    def _extract_marker_type(self, line: str) -> str:
        """Extract the marker type from a line."""
        match = re.search(r'\b(TODO|FIXME|XXX|HACK|STUB|MOCK|PLACEHOLDER)\b', line, re.IGNORECASE)
        return match.group(1).upper() if match else 'UNKNOWN'

    def scan_repository(self, extensions: list[str] | None = None) -> int:
        """Scan the entire repository for repairable markers."""
        if extensions is None:
            extensions = ['.py', '.cc', '.cpp', '.h', '.hpp', '.c', '.scm', '.sql', '.cmake']

        print("🔍 Scanning repository for repairable markers...")
        print(f"   Extensions: {', '.join(extensions)}")

        # Find all files
        for ext in extensions:
            for file_path in self.repo_root.rglob(f'*{ext}'):
                # Skip certain directories
                rel = file_path.relative_to(self.repo_root)
                skip_dirs = ['.git', '.upstream_cache', 'build', '__pycache__', 'node_modules']
                if any(part in skip_dirs for part in rel.parts):
                    continue

                self.stats['scanned_files'] += 1
                file_repairs = self.scan_file(file_path)
                self.repairs.extend(file_repairs)

        print(f"✓ Scanned {self.stats['scanned_files']} files")
        print(f"✓ Found {self.stats['total_markers_found']} markers")
        print(f"✓ Identified {len(self.repairs)} repair opportunities")

        return len(self.repairs)

    def apply_safe_repairs(self, dry_run: bool = True, confidence_threshold: float = 0.85) -> dict:
        """Apply repairs above the confidence threshold that don't require review."""
        safe_repairs = [
            r for r in self.repairs
            if not r.requires_review and r.confidence >= confidence_threshold and not r.applied
        ]

        if not safe_repairs:
            return {
                'applied': 0,
                'message': 'No safe repairs above threshold',
                'dry_run': dry_run
            }

        print(f"\n🔧 {'[DRY RUN] ' if dry_run else ''}Applying {len(safe_repairs)} safe repairs...")

        # Group by file
        by_file: dict[str, list[EnhancedRepairAction]] = {}
        for repair in safe_repairs:
            by_file.setdefault(repair.file_path, []).append(repair)

        applied = 0

        for file_path, file_repairs in by_file.items():
            full_path = self.repo_root / file_path

            if not full_path.exists():
                self.stats['errors'].append(f"File not found: {file_path}")
                continue

            try:
                with open(full_path, encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()

                # Sort by line number descending to preserve line numbers
                file_repairs.sort(key=lambda r: r.line_number, reverse=True)

                modified = False
                for repair in file_repairs:
                    idx = repair.line_number - 1
                    if idx < 0 or idx >= len(lines):
                        continue

                    if repair.repair_type == 'remove':
                        # Remove the line entirely
                        del lines[idx]
                        modified = True
                        applied += 1
                        repair.applied = True
                        print(f"  ✓ Removed: {file_path}:{repair.line_number}")

                    elif repair.repair_type == 'convert' and repair.new_content:
                        # Replace with new content
                        lines[idx] = repair.new_content + '\n'
                        modified = True
                        applied += 1
                        repair.applied = True
                        print(f"  ✓ Converted: {file_path}:{repair.line_number}")

                if modified and not dry_run:
                    with open(full_path, 'w', encoding='utf-8') as f:
                        f.writelines(lines)

            except Exception as e:
                self.stats['errors'].append(f"Error processing {file_path}: {e}")

        self.stats['applied'] = applied

        return {
            'applied': applied,
            'files_modified': len(by_file),
            'dry_run': dry_run,
            'errors': self.stats['errors'][-10:]  # Last 10 errors
        }

    def get_review_queue(self) -> list[EnhancedRepairAction]:
        """Get repairs that need human review, sorted by confidence."""
        needs_review = [r for r in self.repairs if r.requires_review and not r.applied]
        needs_review.sort(key=lambda r: (-r.confidence, r.file_path))
        return needs_review

    def export_report(self, output_file: str = 'enhanced_repair_report.json') -> dict:
        """Export comprehensive repair report."""
        report = {
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'statistics': self.stats,
            'repairs': [asdict(r) for r in self.repairs],
            'review_queue': [asdict(r) for r in self.get_review_queue()[:50]],
            'quick_wins': [
                asdict(r) for r in self.repairs
                if not r.requires_review and r.confidence >= 0.85
            ]
        }

        output_path = self.repo_root / output_file
        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2)

        print(f"\n✓ Report exported to {output_file}")
        return report

    def print_summary(self):
        """Print a summary of findings."""
        print("\n" + "=" * 60)
        print("📊 ENHANCED REPAIR ANALYSIS SUMMARY")
        print("=" * 60)
        print(f"Files scanned:     {self.stats['scanned_files']}")
        print(f"Markers found:     {self.stats['total_markers_found']}")
        print(f"Repairs identified: {len(self.repairs)}")
        print()
        print("By Category:")
        for cat, count in sorted(self.stats['by_category'].items()):
            print(f"  {cat:20} {count:5}")
        print()
        print("By Confidence:")
        print(f"  High (≥0.8):     {self.stats['by_confidence']['high']}")
        print(f"  Medium (0.5-0.8): {self.stats['by_confidence']['medium']}")
        print(f"  Low (<0.5):      {self.stats['by_confidence']['low']}")
        print()

        quick_wins = [r for r in self.repairs if not r.requires_review and r.confidence >= 0.85]
        if quick_wins:
            print(f"🎯 Quick Wins (auto-apply): {len(quick_wins)}")
            for r in quick_wins[:10]:
                print(f"  • {r.file_path}:{r.line_number} - {r.reason}")
        print("=" * 60)


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description='Enhanced marker repair system')
    parser.add_argument('--repo', default='.', help='Repository root')
    parser.add_argument('--scan', action='store_true', help='Scan for repairs')
    parser.add_argument('--apply', action='store_true', help='Apply safe repairs')
    parser.add_argument('--dry-run', action='store_true', default=True, help='Dry run mode')
    parser.add_argument('--no-dry-run', action='store_true', help='Actually apply changes')
    parser.add_argument('--threshold', type=float, default=0.85, help='Confidence threshold')
    parser.add_argument('--export', default='enhanced_repair_report.json', help='Report file')

    args = parser.parse_args()

    repairer = EnhancedMarkerRepair(args.repo)

    if args.scan or args.apply:
        repairer.scan_repository()
        repairer.print_summary()
        repairer.export_report(args.export)

    if args.apply:
        dry_run = not args.no_dry_run
        results = repairer.apply_safe_repairs(dry_run=dry_run, confidence_threshold=args.threshold)
        print(f"\n{'[DRY RUN] ' if dry_run else ''}Applied {results['applied']} repairs")

        if dry_run:
            print("\nTo apply for real: --apply --no-dry-run")


if __name__ == '__main__':
    main()
