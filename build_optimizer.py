#!/usr/bin/env python3
"""
OpenCog Build Sequence Optimizer
Generates optimal build sequences with critical paths and parallelization analysis
Integrates with existing OpenCog unified build system
"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

from dependency_analyzer import DependencyAnalyzer


class BuildOptimizer:
    """Optimizes OpenCog build sequences based on dependency analysis"""

    def __init__(self, root_dir: str = "."):
        self.root_dir = Path(root_dir).resolve()
        self.analyzer = DependencyAnalyzer()
        self.available_components = self._detect_available_components()

    def _detect_available_components(self) -> set[str]:
        """Detect which components are actually available in the repository"""
        available = set()

        # Check for directories with CMakeLists.txt
        for item in self.root_dir.iterdir():
            if item.is_dir() and (item / "CMakeLists.txt").exists():
                # Convert directory name to component name format
                comp_name = item.name.replace("-", "_")
                available.add(comp_name)

        return available

    def generate_optimal_sequence(self) -> dict:
        """Generate optimal build sequence for available components only"""
        report = self.analyzer.generate_report()

        # Filter to only available components
        available_topo = [
            comp for comp in report["build_sequence"]["topological_order"] if comp in self.available_components
        ]

        available_parallel = {}
        for level, components in report["build_sequence"]["parallel_groups"].items():
            available_comps = [comp for comp in components if comp in self.available_components]
            if available_comps:
                available_parallel[level] = available_comps

        # Recalculate critical path for available components only
        available_critical_path = self._find_available_critical_path(available_topo)

        return {
            "available_components": sorted(self.available_components),
            "total_available": len(self.available_components),
            "topological_order": available_topo,
            "critical_path": available_critical_path,
            "parallel_groups": available_parallel,
            "build_phases": self._generate_available_phases(available_parallel),
            "external_dependencies": self._get_available_external_deps(),
            "build_instructions": self._generate_build_instructions(available_parallel),
            "cmake_optimization": self._generate_cmake_optimization(available_parallel),
        }

    def _find_available_critical_path(self, topo_order: list[str]) -> list[str]:
        """Find critical path among available components"""
        if not topo_order:
            return []

        # Simple approach: follow longest dependency chain
        # This is a simplified version for available components
        longest_chain = []

        for comp in topo_order:
            if comp in self.analyzer.components:
                deps = self.analyzer.components[comp].dependencies
                available_deps = [d for d in deps if d in self.available_components]

                if not available_deps:  # Root component
                    chain = [comp]
                    current = comp

                    # Follow the chain
                    while True:
                        dependents = [
                            c
                            for c in topo_order
                            if current in self.analyzer.components[c].dependencies and c in self.available_components
                        ]
                        if not dependents:
                            break
                        # Choose the one with most dependencies
                        next_comp = max(dependents, key=lambda x: len(self.analyzer.components[x].dependencies))
                        chain.append(next_comp)
                        current = next_comp

                    if len(chain) > len(longest_chain):
                        longest_chain = chain

        return longest_chain

    def _generate_available_phases(self, parallel_groups: dict[int, list[str]]) -> dict[str, list[str]]:
        """Generate build phases for available components"""
        phases = {
            "Phase 1 - Foundation": [],
            "Phase 2 - Core Systems": [],
            "Phase 3 - Logic & Reasoning": [],
            "Phase 4 - Advanced Systems": [],
            "Phase 5 - Integration": [],
        }

        for level, components in parallel_groups.items():
            for comp in components:
                if comp not in self.available_components:
                    continue

                if comp == "cogutil" or level == 0:
                    phases["Phase 1 - Foundation"].append(comp)
                elif comp in ["atomspace", "atomspace_storage", "cogserver", "atomspace_rocks", "atomspace_restful"]:
                    phases["Phase 2 - Core Systems"].append(comp)
                elif comp in ["unify", "ure", "pln", "miner"]:
                    phases["Phase 3 - Logic & Reasoning"].append(comp)
                elif comp in ["attention", "spacetime", "moses", "asmoses"]:
                    phases["Phase 4 - Advanced Systems"].append(comp)
                else:
                    phases["Phase 5 - Integration"].append(comp)

        return {k: v for k, v in phases.items() if v}

    def _get_available_external_deps(self) -> dict[str, list[str]]:
        """Get external dependencies for available components"""
        external_deps = {}
        for comp in self.available_components:
            if comp in self.analyzer.components:
                deps = list(self.analyzer.components[comp].external_deps)
                if deps:
                    external_deps[comp] = deps
        return external_deps

    def _generate_build_instructions(self, parallel_groups: dict[int, list[str]]) -> list[str]:
        """Generate step-by-step build instructions"""
        instructions = [
            "# OpenCog Unified Build Instructions",
            "# Optimized sequence based on dependency analysis",
            "",
            "## Prerequisites",
            "# Install system dependencies first:",
            "sudo apt-get update",
            "sudo apt-get install -y cmake build-essential libboost-all-dev",
            "sudo apt-get install -y python3-dev guile-2.2-dev librocksdb-dev",
            "",
            "## Build Sequence",
        ]

        for level, components in parallel_groups.items():
            available_comps = [comp for comp in components if comp in self.available_components]
            if not available_comps:
                continue

            instructions.append("")
            instructions.append(f"### Level {level} - {len(available_comps)} components (can build in parallel)")

            if len(available_comps) == 1:
                comp = available_comps[0]
                dir_name = comp.replace("_", "-")
                instructions.extend(
                    [
                        f"cd {dir_name}",
                        "mkdir -p build && cd build",
                        "cmake ..",
                        "make -j$(nproc)",
                        "cd ../..",
                    ]
                )
            else:
                instructions.append("# Parallel build possible:")
                for comp in available_comps:
                    dir_name = comp.replace("_", "-")
                    instructions.append(f"# Component: {comp} (directory: {dir_name})")

                instructions.extend(
                    [
                        "# Build all in parallel:",
                        f"parallel -j{len(available_comps)} --tagstring '{{1}}' '{{{{",
                        "  cd {1} && mkdir -p build && cd build && cmake .. && make -j$(nproc) && cd ../..;",
                        f"}}}}' ::: {' '.join(comp.replace('_', '-') for comp in available_comps)}",
                    ]
                )

        return instructions

    def _generate_cmake_optimization(self, parallel_groups: dict[int, list[str]]) -> str:
        """Generate CMake file optimized for available components"""
        cmake_lines = [
            "# OpenCog Unified - Optimized for Available Components",
            "cmake_minimum_required(VERSION 3.10)",
            "project(opencog-unified VERSION 1.0.0)",
            "",
            "set(CMAKE_CXX_STANDARD 17)",
            "set(CMAKE_CXX_STANDARD_REQUIRED ON)",
            "",
            "# Module path setup",
            "set(CMAKE_MODULE_PATH",
            "    ${CMAKE_CURRENT_SOURCE_DIR}/cmake",
            "    ${CMAKE_CURRENT_SOURCE_DIR}/cogutil/cmake",
            "    ${CMAKE_MODULE_PATH}",
            ")",
            "",
            "# Dependency-optimized build sequence",
        ]

        for level, components in parallel_groups.items():
            available_comps = [comp for comp in components if comp in self.available_components]
            if not available_comps:
                continue

            cmake_lines.append("")
            cmake_lines.append(f"# Level {level} - Parallel builds: {', '.join(available_comps)}")

            for comp in available_comps:
                dir_name = comp.replace("_", "-")
                cmake_lines.extend(
                    [
                        f'if(EXISTS "${{CMAKE_CURRENT_SOURCE_DIR}}/{dir_name}/CMakeLists.txt")',
                        f"    add_subdirectory({dir_name})",
                        "endif()",
                    ]
                )

        # Add explicit dependencies
        cmake_lines.extend(
            [
                "",
                "# Explicit dependency relationships for available components",
            ]
        )

        for comp in self.available_components:
            if comp in self.analyzer.components:
                deps = self.analyzer.components[comp].dependencies
                available_deps = [d for d in deps if d in self.available_components]

                if available_deps:
                    comp_dir = comp.replace("_", "-")
                    for dep in available_deps:
                        dep_dir = dep.replace("_", "-")
                        cmake_lines.extend(
                            [
                                f"if(TARGET {comp_dir} AND TARGET {dep_dir})",
                                f"    add_dependencies({comp_dir} {dep_dir})",
                                "endif()",
                            ]
                        )

        return "\n".join(cmake_lines)

    def save_optimization_report(self, filename: str = "build_optimization_report.json"):
        """Save comprehensive build optimization report"""
        optimization = self.generate_optimal_sequence()

        with open(filename, "w") as f:
            json.dump(optimization, f, indent=2)

        print(f"Build optimization report saved to {filename}")
        return optimization

    def save_build_instructions(self, filename: str = "OPTIMAL_BUILD_SEQUENCE.md"):
        """Save markdown build instructions"""
        optimization = self.generate_optimal_sequence()

        lines = [
            "# OpenCog Unified - Optimal Build Sequence",
            "",
            f"**Generated for {optimization['total_available']} available components**",
            "",
            "## Summary",
            f"- **Critical Path**: {' → '.join(optimization['critical_path'])}",
            f"- **Maximum Parallelization**: {max(len(comps) for comps in optimization['parallel_groups'].values())} components",
            f"- **Build Phases**: {len(optimization['build_phases'])}",
            "",
            "## Available Components",
            "",
        ]

        for comp in optimization["available_components"]:
            lines.append(f"- {comp}")

        lines.extend(
            [
                "",
                "## Build Phases",
                "",
            ]
        )

        for phase, components in optimization["build_phases"].items():
            lines.extend(
                [
                    f"### {phase}",
                    f"Components: {', '.join(components)}",
                    "",
                ]
            )

        lines.extend(
            [
                "## Parallelization Opportunities",
                "",
            ]
        )

        for level, components in optimization["parallel_groups"].items():
            if len(components) > 1:
                lines.extend(
                    [
                        f"**Level {level}**: {len(components)} parallel builds possible",
                        f"- {', '.join(components)}",
                        "",
                    ]
                )

        lines.extend(
            [
                "## External Dependencies",
                "",
            ]
        )

        for comp, deps in optimization["external_dependencies"].items():
            lines.append(f"**{comp}**: {', '.join(deps)}")

        lines.extend(
            [
                "",
                "## Build Instructions",
                "",
            ]
        )

        lines.extend(optimization["build_instructions"])

        with open(filename, "w") as f:
            f.write("\n".join(lines))

        print(f"Build instructions saved to {filename}")

    def save_optimized_cmake(self, filename: str = "CMakeLists_available.txt"):
        """Save CMake file optimized for available components"""
        optimization = self.generate_optimal_sequence()

        with open(filename, "w") as f:
            f.write(optimization["cmake_optimization"])

        print(f"Optimized CMake file saved to {filename}")

    def run_build_validation(self) -> bool:
        """Validate that the optimized build sequence works"""
        print("Validating optimized build sequence...")

        try:
            # Run the existing validation script
            result = subprocess.run(
                ["python3", "validate-integration.py", "--no-build"], capture_output=True, text=True, cwd=self.root_dir
            )

            print("Validation output:")
            print(result.stdout)

            if result.stderr:
                print("Validation warnings/errors:")
                print(result.stderr)

            return result.returncode == 0

        except FileNotFoundError:
            print("Warning: validate-integration.py not found")
            return False

    def display_optimization_summary(self):
        """Display comprehensive optimization summary"""
        optimization = self.generate_optimal_sequence()

        print("=" * 60)
        print("OpenCog Build Sequence Optimization Summary")
        print("=" * 60)

        print("\n📊 OVERVIEW")
        print(f"   Available Components: {optimization['total_available']}")
        print(f"   Build Phases: {len(optimization['build_phases'])}")
        print(f"   Critical Path Length: {len(optimization['critical_path'])}")

        print(f"\n🎯 CRITICAL PATH ({len(optimization['critical_path'])} components)")
        if optimization["critical_path"]:
            print(f"   {' → '.join(optimization['critical_path'])}")
        else:
            print("   No critical path identified")

        print("\n⚡ PARALLELIZATION OPPORTUNITIES")
        max_parallel = 0
        for level, components in optimization["parallel_groups"].items():
            if len(components) > 1:
                print(f"   Level {level}: {len(components)} parallel builds")
                print(f"     Components: {', '.join(components)}")
                max_parallel = max(max_parallel, len(components))

        print(f"\n   Maximum parallel jobs: {max_parallel}")

        print("\n🏗️ BUILD PHASES")
        for phase, components in optimization["build_phases"].items():
            print(f"   {phase}: {len(components)} components")
            print(f"     {', '.join(components)}")

        print("\n📦 EXTERNAL DEPENDENCIES")
        for comp, deps in optimization["external_dependencies"].items():
            print(f"   {comp}: {', '.join(deps[:3])}{'...' if len(deps) > 3 else ''}")

        print("\n💡 RECOMMENDATIONS")
        print("   • Focus optimization on critical path components")
        print("   • Use parallel builds for levels with multiple components")
        print("   • Ensure external dependencies are installed first")
        print("   • Consider containerization for reproducible builds")


def main():
    parser = argparse.ArgumentParser(description="OpenCog Build Sequence Optimizer")
    parser.add_argument("--summary", action="store_true", help="Display optimization summary")
    parser.add_argument("--save-all", action="store_true", help="Save all optimization files")
    parser.add_argument("--validate", action="store_true", help="Validate the optimized build sequence")
    parser.add_argument("--output-dir", default=".", help="Output directory for generated files")

    args = parser.parse_args()

    optimizer = BuildOptimizer()

    # Set output directory
    output_dir = Path(args.output_dir)
    output_dir.mkdir(exist_ok=True)

    # Always display summary unless only saving files
    if args.summary or not args.save_all:
        optimizer.display_optimization_summary()

    if args.save_all:
        os.chdir(output_dir)
        optimizer.save_optimization_report("build_optimization_report.json")
        optimizer.save_build_instructions("OPTIMAL_BUILD_SEQUENCE.md")
        optimizer.save_optimized_cmake("CMakeLists_available.txt")
        print(f"\nAll optimization files saved to {output_dir}")

    if args.validate:
        success = optimizer.run_build_validation()
        print(f"\nBuild validation: {'PASSED' if success else 'FAILED'}")
        return 0 if success else 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
