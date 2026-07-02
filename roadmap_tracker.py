#!/usr/bin/env python3
"""
OpenCog Unified Development Roadmap Status Tracker

This script tracks the implementation status of the 20-week OpenCog unified
development roadmap as defined in DEVELOPMENT-ROADMAP.md.
"""

import json
import sys
from datetime import datetime
from pathlib import Path


class RoadmapTracker:
    def __init__(self, base_dir=None):
        self.base_dir = Path(base_dir) if base_dir else Path(__file__).parent
        self.components = {
            # Phase 1: Core Extensions (Weeks 1-4)
            "atomspace-rocks": {
                "phase": 1,
                "week": 1,
                "priority": "HIGH",
                "dependencies": ["atomspace"],
                "repository": "https://github.com/opencog/atomspace-rocks"
            },
            "atomspace-restful": {
                "phase": 1,
                "week": 2,
                "priority": "HIGH",
                "dependencies": ["atomspace"],
                "repository": "https://github.com/opencog/atomspace-restful"
            },
            "moses": {
                "phase": 1,
                "week": 3,
                "priority": "MEDIUM",
                "dependencies": ["cogutil"],
                "repository": "https://github.com/opencog/moses"
            },

            # Phase 2: Logic Systems (Weeks 5-8)
            "unify": {
                "phase": 2,
                "week": 5,
                "priority": "HIGH",
                "dependencies": ["atomspace"],
                "repository": "https://github.com/opencog/unify"
            },
            "ure": {
                "phase": 2,
                "week": 6,
                "priority": "HIGH",
                "dependencies": ["atomspace", "unify"],
                "repository": "https://github.com/opencog/ure"
            },
            "language-learning": {
                "phase": 2,
                "week": 7,
                "priority": "MEDIUM",
                "dependencies": ["cogutil"],
                "repository": "https://github.com/opencog/language-learning"
            },

            # Phase 3: Cognitive Systems (Weeks 9-12)
            "attention": {
                "phase": 3,
                "week": 9,
                "priority": "HIGH",
                "dependencies": ["atomspace", "cogserver"],
                "repository": "https://github.com/opencog/attention"
            },
            "spacetime": {
                "phase": 3,
                "week": 10,
                "priority": "MEDIUM",
                "dependencies": ["atomspace"],
                "repository": "https://github.com/opencog/spacetime"
            },

            # Phase 4: Advanced & Learning Systems (Weeks 13-16)
            "pln": {
                "phase": 4,
                "week": 13,
                "priority": "HIGH",
                "dependencies": ["atomspace", "ure", "spacetime"],
                "repository": "https://github.com/opencog/pln"
            },
            "miner": {
                "phase": 4,
                "week": 14,
                "priority": "MEDIUM",
                "dependencies": ["atomspace", "ure"],
                "repository": "https://github.com/opencog/miner"
            },
            "asmoses": {
                "phase": 4,
                "week": 15,
                "priority": "MEDIUM",
                "dependencies": ["atomspace", "ure"],
                "repository": "https://github.com/opencog/asmoses"
            },

            # Phase 5: Language & Final Integration (Weeks 17-20)
            "lg-atomese": {
                "phase": 5,
                "week": 17,
                "priority": "HIGH",
                "dependencies": ["atomspace"],
                "repository": "https://github.com/opencog/lg-atomese"
            },
            "learn": {
                "phase": 5,
                "week": 18,
                "priority": "HIGH",
                "dependencies": ["atomspace", "cogserver"],
                "repository": "https://github.com/opencog/learn"
            },
            "opencog": {
                "phase": 5,
                "week": 19,
                "priority": "CRITICAL",
                "dependencies": ["atomspace", "cogserver", "attention", "ure", "lg-atomese"],
                "repository": "https://github.com/opencog/opencog"
            }
        }

        # Foundation components (already integrated)
        self.foundation = {
            "cogutil": {"present": True, "has_cmake": True},
            "atomspace": {"present": True, "has_cmake": True},
            "cogserver": {"present": True, "has_cmake": True}
        }

    def check_component_status(self, component_name):
        """Check if a component is present and properly integrated"""
        component_dir = self.base_dir / component_name

        status = {
            "present": component_dir.exists() and component_dir.is_dir(),
            "has_cmake": False,
            "has_git": False,
            "buildable": False
        }

        if status["present"]:
            cmake_file = component_dir / "CMakeLists.txt"
            git_dir = component_dir / ".git"

            status["has_cmake"] = cmake_file.exists()
            status["has_git"] = git_dir.exists()

        return status

    def get_phase_status(self, phase_num):
        """Get status of all components in a specific phase"""
        phase_components = {
            name: info for name, info in self.components.items()
            if info["phase"] == phase_num
        }

        status = {}
        for component_name in phase_components:
            status[component_name] = self.check_component_status(component_name)

        return status

    def generate_status_report(self):
        """Generate comprehensive status report"""
        report = {
            "timestamp": datetime.now().isoformat(),
            "foundation_status": {},
            "phase_status": {},
            "overall_progress": {}
        }

        # Check foundation components
        for component, _info in self.foundation.items():
            report["foundation_status"][component] = self.check_component_status(component)

        # Check each phase
        for phase in range(1, 6):
            report["phase_status"][f"phase_{phase}"] = self.get_phase_status(phase)

        # Calculate overall progress
        total_components = len(self.components) + len(self.foundation)
        present_components = 0
        buildable_components = 0

        # Count foundation
        for component in self.foundation:
            status = report["foundation_status"][component]
            if status["present"]:
                present_components += 1
            if status["has_cmake"]:
                buildable_components += 1

        # Count phase components
        for phase_data in report["phase_status"].values():
            for status in phase_data.values():
                if status["present"]:
                    present_components += 1
                if status["has_cmake"]:
                    buildable_components += 1

        report["overall_progress"] = {
            "total_components": total_components,
            "present_components": present_components,
            "buildable_components": buildable_components,
            "present_percentage": (present_components / total_components) * 100,
            "buildable_percentage": (buildable_components / total_components) * 100
        }

        return report

    def save_status_report(self, filename="roadmap_status.json"):
        """Save status report to JSON file"""
        report = self.generate_status_report()
        output_file = self.base_dir / filename

        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)

        return output_file

    def print_status_summary(self):
        """Print a human-readable status summary"""
        report = self.generate_status_report()

        print("🚀 OpenCog Unified Development Roadmap Status")
        print("=" * 50)

        print("\n📊 Overall Progress:")
        progress = report["overall_progress"]
        print(f"   Components Present: {progress['present_components']}/{progress['total_components']} ({progress['present_percentage']:.1f}%)")
        print(f"   Components Buildable: {progress['buildable_components']}/{progress['total_components']} ({progress['buildable_percentage']:.1f}%)")

        print("\n🏗️ Foundation Layer Status:")
        for component, status in report["foundation_status"].items():
            icon = "✅" if status["present"] and status["has_cmake"] else "❌"
            print(f"   {icon} {component} - Present: {status['present']}, CMake: {status['has_cmake']}")

        print("\n📅 Phase-by-Phase Status:")
        for phase_key, phase_data in report["phase_status"].items():
            phase_num = int(phase_key.split('_')[1])
            present_count = sum(1 for status in phase_data.values() if status["present"])
            buildable_count = sum(1 for status in phase_data.values() if status["has_cmake"])
            total_count = len(phase_data)

            print(f"\n   Phase {phase_num}: {present_count}/{total_count} present, {buildable_count}/{total_count} buildable")
            for component, status in phase_data.items():
                icon = "✅" if status["present"] and status["has_cmake"] else "❌"
                print(f"     {icon} {component} - Present: {status['present']}, CMake: {status['has_cmake']}")

def main():
    """Main entry point"""
    if len(sys.argv) > 1 and sys.argv[1] == "--json":
        # Output JSON report
        tracker = RoadmapTracker()
        output_file = tracker.save_status_report()
        print(f"Status report saved to: {output_file}")
    else:
        # Output human-readable summary
        tracker = RoadmapTracker()
        tracker.print_status_summary()

if __name__ == "__main__":
    main()
