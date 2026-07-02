#!/usr/bin/env python3
"""
Comprehensive test coverage analysis for opencog-unified
Identifies gaps and opportunities for improvement
"""

import json
from collections import defaultdict
from pathlib import Path


class TestCoverageAnalyzer:
    def __init__(self, repo_path):
        self.repo_path = Path(repo_path)
        self.components = []
        self.coverage_data = defaultdict(dict)

    def analyze(self):
        """Analyze test coverage across all components"""
        print("🔍 Analyzing test coverage...")

        # Find all components with source code
        self.identify_components()

        # Analyze each component
        for component in self.components:
            self.analyze_component(component)

        return self.generate_report()

    def identify_components(self):
        """Identify all components in the repository"""
        # Major components based on directory structure
        component_dirs = [
            'cogutil', 'atomspace', 'atomspace-storage', 'atomspace-rocks',
            'atomspace-restful', 'cogserver', 'attention', 'unify', 'ure',
            'miner', 'moses', 'asmoses', 'learn', 'pln', 'spacetime',
            'lg-atomese', 'language-learning', 'opencog', 'meta-cognition',
            'neural-symbolic-integration', 'ggml-tensor-kernel',
            'agentic-kernels-catalog', 'cognitive-patterns',
            'distributed-cognition', 'evolutionary-optimization'
        ]

        for comp_dir in component_dirs:
            comp_path = self.repo_path / comp_dir
            if comp_path.exists() and comp_path.is_dir():
                self.components.append({
                    'name': comp_dir,
                    'path': comp_path
                })

    def analyze_component(self, component):
        """Analyze test coverage for a single component"""
        name = component['name']
        path = component['path']

        # Count source files
        source_files = self.count_files(path, ['*.cc', '*.cpp', '*.h', '*.hpp'])

        # Count test files
        test_path = path / 'tests'
        if test_path.exists():
            test_files = self.count_files(test_path, ['*.cc', '*.cxxtest', '*.py', '*.scm'])
        else:
            test_files = 0

        # Check for CMake test configuration
        has_cmake_tests = (path / 'tests' / 'CMakeLists.txt').exists()

        # Calculate coverage ratio
        if source_files > 0:
            coverage_ratio = test_files / source_files
        else:
            coverage_ratio = 0

        self.coverage_data[name] = {
            'source_files': source_files,
            'test_files': test_files,
            'has_test_dir': test_path.exists(),
            'has_cmake_tests': has_cmake_tests,
            'coverage_ratio': round(coverage_ratio, 2),
            'priority': self.calculate_priority(source_files, test_files, coverage_ratio)
        }

    def count_files(self, path, patterns):
        """Count files matching patterns"""
        count = 0
        for pattern in patterns:
            count += len(list(path.rglob(pattern)))
        return count

    def calculate_priority(self, source_files, test_files, ratio):
        """Calculate priority for test implementation"""
        if source_files == 0:
            return 'N/A'
        elif ratio == 0:
            return 'CRITICAL'
        elif ratio < 0.3:
            return 'HIGH'
        elif ratio < 0.7:
            return 'MEDIUM'
        else:
            return 'LOW'

    def generate_report(self):
        """Generate comprehensive coverage report"""
        report = {
            'summary': {
                'total_components': len(self.components),
                'components_with_tests': sum(1 for c in self.coverage_data.values() if c['has_test_dir']),
                'components_without_tests': sum(1 for c in self.coverage_data.values() if not c['has_test_dir']),
                'critical_priority': sum(1 for c in self.coverage_data.values() if c['priority'] == 'CRITICAL'),
                'high_priority': sum(1 for c in self.coverage_data.values() if c['priority'] == 'HIGH')
            },
            'components': dict(self.coverage_data)
        }

        return report

if __name__ == '__main__':
    analyzer = TestCoverageAnalyzer('/home/ubuntu/opencog-unified')
    report = analyzer.analyze()

    # Save report
    with open('/home/ubuntu/opencog-unified/test_coverage_analysis.json', 'w') as f:
        json.dump(report, f, indent=2)

    print("\n📊 Analysis Complete!")
    print(f"   Total components: {report['summary']['total_components']}")
    print(f"   Components with tests: {report['summary']['components_with_tests']}")
    print(f"   Components without tests: {report['summary']['components_without_tests']}")
    print(f"   Critical priority: {report['summary']['critical_priority']}")
    print(f"   High priority: {report['summary']['high_priority']}")
    print("\n📄 Report saved to: test_coverage_analysis.json")
