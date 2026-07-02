#!/usr/bin/env python3
"""
FIXME Instance Analysis and Categorization Tool

This script analyzes all FIXME instances in the OpenCog Unified repository
and categorizes them by implementation difficulty based on:
- Code complexity and context
- Required expertise level
- Dependencies and architectural impact
- Time estimation for implementation

Categories:
- EASY: Simple fixes, documentation, basic features
- MEDIUM: Algorithmic improvements, feature completions
- HARD: Performance optimizations, thread safety, complex algorithms
- VERY_HARD: Distributed systems, architectural changes, research-level work
"""

import json
import re
from collections import defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass
class FIXMEInstance:
    file_path: str
    line_number: int
    fixme_text: str
    context_lines: list[str]
    difficulty: str = "UNKNOWN"
    category: str = "UNKNOWN"
    estimated_effort: str = "UNKNOWN"
    dependencies: list[str] = None
    reasoning: str = ""

    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []

class FIXMEAnalyzer:
    def __init__(self, repo_root: str):
        self.repo_root = Path(repo_root)
        self.fixme_instances = []
        self.patterns = {
            'thread_safety': r'thread[_\-\s]safe|race\s+condition|atomic|mutex|lock|concurrent|synchroniz',
            'performance': r'performance|optimization|O\(|efficient|speed|fast|slow|bottleneck|cache',
            'distributed': r'distributed|cluster|consensus|partition|byzantine|quorum|node|network',
            'algorithm': r'algorithm|implement|complex|exponential|quadratic|recursive|stack',
            'documentation': r'docs?|documentation|comment|explain|describe',
            'simple_todo': r'simple|easy|quick|straightforward|minor|small',
            'architecture': r'architecture|design|refactor|restructure|framework|system',
            'research': r'research|paper|theory|mathematical|proof|novel'
        }

    def extract_fixme_instances(self):
        """Extract all FIXME instances from source files."""
        file_extensions = {'.cc', '.cpp', '.h', '.hpp', '.scm', '.py', '.c'}

        for file_path in self.repo_root.rglob('*'):
            if file_path.suffix.lower() in file_extensions:
                self._process_file(file_path)

        print(f"Found {len(self.fixme_instances)} FIXME instances")

    def _process_file(self, file_path: Path):
        """Process a single file for FIXME instances."""
        try:
            with open(file_path, encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()

            for i, line in enumerate(lines):
                if self._is_fixme_line(line):
                    context_start = max(0, i - 2)
                    context_end = min(len(lines), i + 3)
                    context = [l.strip() for l in lines[context_start:context_end]]

                    fixme_instance = FIXMEInstance(
                        file_path=str(file_path.relative_to(self.repo_root)),
                        line_number=i + 1,
                        fixme_text=line.strip(),
                        context_lines=context
                    )

                    self.fixme_instances.append(fixme_instance)

        except Exception as e:
            print(f"Error processing {file_path}: {e}")

    def _is_fixme_line(self, line: str) -> bool:
        """Check if a line contains a FIXME comment."""
        line_stripped = line.strip()
        line_lower = line_stripped.lower()

        # Skip string literals and regex patterns
        if (line_stripped.startswith('"') and line_stripped.endswith('"')) or \
           (line_stripped.startswith("'") and line_stripped.endswith("'")) or \
           ("r'" in line_stripped) or ('r"' in line_stripped):
            return False

        # Skip meta-comments about FIXME processing
        if ('fixme instances' in line_lower) or \
           ('fixme text' in line_lower) or \
           ('todo/fixme' in line_lower and ('pattern' in line_lower or 'report' in line_lower or 'verification' in line_lower or 'marker' in line_lower)) or \
           ('analyze' in line_lower and 'fixme' in line_lower) or \
           ('catalog' in line_lower and 'fixme' in line_lower) or \
           ('contain' in line_lower and 'todo/fixme' in line_lower) or \
           ('check' in line_lower and 'todo/fixme' in line_lower) or \
           ('skip meta-comments about fix-me processing' in line_lower) or \
           ('look for actual fix-me patterns in comments' in line_lower) or \
           ('for other cases, convert fixme to descriptive' in line_lower) or \
           ('pre-commit hook to prevent new fixmes' in line_lower) or \
           ('include this in your main makefile' in line_lower) or \
           ('{' in line_stripped and '}' in line_stripped):  # template variables
            return False

        # Must start with comment syntax (not just contain it)
        comment_starts = line_stripped.startswith('//') or \
                        line_stripped.startswith('#') or \
                        line_stripped.startswith(';') or \
                        line_stripped.startswith('/*') or \
                        line_stripped.startswith('*')  # for multi-line comments

        if not comment_starts:
            return False

        # Must not be metadata about FIXME processing
        if ('clean up' in line_lower and 'fixme' in line_lower) or \
           ('issue:' in line_lower) or \
           ('markdown' in line_lower) or \
           ('metadata about fixme' in line_lower):
            return False

        # Look for actual FIXME patterns in comments
        return (('fixme' in line_lower) or
                ('xxx' in line_lower and (line_lower.strip().startswith('#') or line_lower.strip().startswith('//'))) or  # XXX comments
                ('xxx' in line_lower and ('fix' in line_lower or 'todo' in line_lower)) or
                ('todo' in line_lower and 'fixme' in line_lower))

    def categorize_instances(self):
        """Categorize each FIXME instance by difficulty."""
        for instance in self.fixme_instances:
            self._analyze_instance(instance)

    def _analyze_instance(self, instance: FIXMEInstance):
        """Analyze a single FIXME instance to determine difficulty."""
        full_text = (instance.fixme_text + ' ' + ' '.join(instance.context_lines)).lower()

        # Count pattern matches
        pattern_matches = {}
        for pattern_name, pattern in self.patterns.items():
            matches = len(re.findall(pattern, full_text, re.IGNORECASE))
            if matches > 0:
                pattern_matches[pattern_name] = matches

        # Determine difficulty based on patterns and context
        difficulty, category, effort, reasoning = self._classify_difficulty(
            instance, pattern_matches, full_text
        )

        instance.difficulty = difficulty
        instance.category = category
        instance.estimated_effort = effort
        instance.reasoning = reasoning

    def _classify_difficulty(self, instance: FIXMEInstance, patterns: dict, full_text: str):
        """Classify the difficulty of implementing the FIXME."""

        # Very Hard criteria
        if (patterns.get('distributed', 0) >= 2 or
            patterns.get('research', 0) >= 1 or
            'byzantine' in full_text or
            'consensus' in full_text or
            'exponential time' in full_text):
            return "VERY_HARD", "Distributed Systems/Research", "2-6 months", \
                   "Requires distributed systems expertise or research-level work"

        # Hard criteria
        if (patterns.get('thread_safety', 0) >= 2 or
            patterns.get('performance', 0) >= 2 or
            patterns.get('algorithm', 0) >= 2 or
            'thread-safe' in full_text or
            'race condition' in full_text or
            'recursive design' in full_text):
            return "HARD", "Performance/Threading/Complex Algorithm", "2-8 weeks", \
                   "Requires deep technical expertise and careful implementation"

        # Medium criteria
        if (patterns.get('algorithm', 0) >= 1 or
            patterns.get('performance', 0) >= 1 or
            patterns.get('architecture', 0) >= 1 or
            'implement' in full_text or
            'not implemented' in full_text or
            'missing feature' in full_text):
            return "MEDIUM", "Feature Implementation/Algorithm", "1-4 weeks", \
                   "Requires moderate technical knowledge and implementation effort"

        # Easy criteria
        if (patterns.get('documentation', 0) >= 1 or
            patterns.get('simple_todo', 0) >= 1 or
            'documentation' in full_text or
            'comment' in full_text or
            'explain' in full_text or
            'minor' in full_text):
            return "EASY", "Documentation/Simple Fix", "1-3 days", \
                   "Simple documentation updates or minor code changes"

        # Default classification based on file type and content
        if instance.file_path.endswith('.scm'):
            return "MEDIUM", "Scheme/Logic Implementation", "1-2 weeks", \
                   "Scheme code implementation or logic system update"

        if 'stub' in full_text or 'placeholder' in full_text or 'mock' in full_text:
            return "MEDIUM", "Stub Implementation", "1-3 weeks", \
                   "Replace stub/placeholder with real implementation"

        return "MEDIUM", "General Implementation", "1-2 weeks", \
               "General implementation task requiring moderate effort"

    def generate_report(self) -> dict:
        """Generate a comprehensive report of FIXME instances."""
        # Group by difficulty
        by_difficulty = defaultdict(list)
        by_category = defaultdict(list)
        by_file = defaultdict(list)

        for instance in self.fixme_instances:
            by_difficulty[instance.difficulty].append(instance)
            by_category[instance.category].append(instance)
            by_file[instance.file_path].append(instance)

        # Create summary statistics
        stats = {
            'total_instances': len(self.fixme_instances),
            'by_difficulty': {k: len(v) for k, v in by_difficulty.items()},
            'by_category': {k: len(v) for k, v in by_category.items()},
            'files_affected': len(by_file),
        }

        return {
            'summary': stats,
            'by_difficulty': {k: [asdict(i) for i in v] for k, v in by_difficulty.items()},
            'by_category': {k: [asdict(i) for i in v] for k, v in by_category.items()},
            'by_file': {k: [asdict(i) for i in v] for k, v in by_file.items()}
        }

    def save_report(self, output_file: str):
        """Save the analysis report to a JSON file."""
        report = self.generate_report()
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2, default=str)

        print(f"Report saved to {output_file}")
        return report

def main():
    """Main analysis function."""
    repo_root = "/home/runner/work/opencog-unified/opencog-unified"
    analyzer = FIXMEAnalyzer(repo_root)

    print("Extracting FIXME instances...")
    analyzer.extract_fixme_instances()

    print("Categorizing by difficulty...")
    analyzer.categorize_instances()

    print("Generating report...")
    report = analyzer.save_report("fixme_analysis_report.json")

    # Print summary
    print("\n" + "="*60)
    print("FIXME ANALYSIS SUMMARY")
    print("="*60)
    print(f"Total FIXME instances found: {report['summary']['total_instances']}")
    print("\nBy Difficulty:")
    for difficulty, count in sorted(report['summary']['by_difficulty'].items()):
        print(f"  {difficulty}: {count} instances")

    print(f"\nFiles affected: {report['summary']['files_affected']}")

    return analyzer

if __name__ == "__main__":
    main()
