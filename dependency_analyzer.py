#!/usr/bin/env python3
"""
OpenCog Complete Dependency Analyzer
Generates optimal build sequences with critical paths and parallelization opportunities
Based on the complete dependency diagram from issue #85
"""

import argparse
import json
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

import networkx as nx


@dataclass
class Component:
    name: str
    category: str
    dependencies: set[str]
    external_deps: set[str]


class DependencyAnalyzer:
    """Analyzes OpenCog component dependencies and generates optimal build sequences"""

    def __init__(self):
        self.components = {}
        self.dependency_graph = nx.DiGraph()
        self.external_deps = set()
        self._initialize_dependencies()

    def _initialize_dependencies(self):
        """Initialize the complete dependency graph from the issue description"""

        # Component categories for styling and organization
        categories = {
            "foundation": [
                "cogutil",
                "blender_api_msgs",
                "blender_api",
                "asmoses",
                "moses",
                "ocpkg",
                "rust_crates",
                "external_tools",
                "cogprotolab",
                "src",
                "integrated_output",
                "guile_dbi",
                "test_datasets",
                "node_modules",
            ],
            "core": [
                "atomspace_agents",
                "atomspace_dht",
                "atomspace",
                "atomspace_storage",
                "atomspace_rocks",
                "atomspace_ipfs",
                "atomspace_websockets",
                "atomspace_restful",
                "atomspace_typescript",
                "atomspace_explorer",
                "atomspace_js",
                "atomspace_bridge",
                "atomspace_metta",
                "atomspace_rpc",
                "atomspace_cog",
                "agents",
            ],
            "logic": ["unify", "ure"],
            "cognitive": [
                "attention",
                "spacetime",
                "logicmoo_cogserver",
                "cogserver",
                "pattern_index",
                "tv_toolbox",
                "kokkos_integrations",
                "dimensional_embedding",
                "distributional_value",
                "profile",
                "rocca",
            ],
            "advanced": ["pln_brca_xp", "benchmark", "miner", "pln", "destin"],
            "learning": ["language_learning", "generate", "learn"],
            "specialized": [
                "cheminformatics",
                "semantic_vision",
                "pi_vision",
                "vision",
                "sensory",
                "visualization",
                "agi_bio",
                "pau2motors",
                "perception",
                "ros_behavior_scripting",
                "robots_config",
                "loving_ai_ghost",
                "loving_ai",
                "ghost_bridge",
                "relex",
                "linkgrammar_relex_web",
                "stochastic_language_generation",
                "link_grammar",
                "lg_atomese",
                "link_grammar_website",
                "TinyCog",
            ],
            "integration": [
                "opencog_rpi",
                "ros_opencog_robot_embodiment",
                "unity3d_opencog_game",
                "opencog_to_minecraft",
                "opencog_nix",
                "opencog",
                "opencog_cycl",
                "opencog_neo4j",
                "opencog_debian",
                "opencog_org",
                "rest_api_documentation",
                "python_client",
                "python_destin",
                "python_attic",
            ],
        }

        # OpenCog component dependencies (cleaned names for Python identifiers)
        component_deps = {
            # Foundation layer
            "cogutil": set(),
            # Core layer
            "atomspace": {"cogutil"},
            "atomspace_storage": {"cogutil", "atomspace"},
            "cogserver": {"cogutil", "atomspace", "atomspace_storage"},
            "atomspace_rocks": {"cogutil", "atomspace", "atomspace_storage"},
            "atomspace_restful": {"cogutil", "atomspace", "cogserver"},
            "atomspace_agents": {"cogutil", "atomspace"},
            "atomspace_dht": {"cogutil", "atomspace"},
            "atomspace_ipfs": {"cogutil", "atomspace"},
            "atomspace_websockets": {"cogutil", "atomspace"},
            "atomspace_bridge": {"cogutil", "atomspace"},
            "atomspace_metta": {"cogutil", "atomspace"},
            "atomspace_rpc": {"cogutil", "atomspace"},
            "atomspace_cog": {"cogutil", "atomspace", "cogserver"},
            # Logic layer
            "unify": {"cogutil", "atomspace"},
            "ure": {"cogutil", "atomspace", "unify", "cogserver"},
            "pattern_index": {"cogutil", "atomspace"},
            # Cognitive layer
            "attention": {"cogutil", "atomspace", "cogserver"},
            "spacetime": {"cogutil", "atomspace"},
            "dimensional_embedding": {"cogutil", "atomspace"},
            # Advanced systems
            "pln": {"cogutil", "atomspace", "ure", "unify", "spacetime"},
            "miner": {"cogutil", "atomspace", "ure", "unify"},
            "benchmark": {"cogutil", "atomspace", "ure"},
            # Learning systems
            "moses": {"cogutil"},
            "asmoses": {"cogutil", "atomspace", "ure"},
            "learn": {"cogutil", "atomspace", "cogserver", "unify"},
            "language_learning": {"cogutil"},
            "generate": {"cogutil", "atomspace"},
            # Language processing
            "lg_atomese": {"cogutil", "atomspace"},
            "relex": {"cogutil"},
            # Specialized components
            "cheminformatics": {"cogutil", "atomspace"},
            "agi_bio": {"cogutil", "atomspace"},
            "vision": {"cogutil", "atomspace"},
            "sensory": {"cogutil", "atomspace"},
            "visualization": {"cogutil", "atomspace"},
            "TinyCog": {"atomspace"},
            # Integration layer
            "opencog": {"cogutil", "atomspace", "cogserver", "attention", "ure", "lg_atomese", "pln"},
            # External dependencies tracked for reference
            "python_attic": {"cogutil", "atomspace", "cogserver", "ure", "pln"},
        }

        # External/system dependencies
        external_deps_map = {
            "cogutil": {
                "boost",
                "doxygen",
                "gnubacktrace",
                "iberty",
                "parallelstl",
                "cxxtest",
                "pthreads",
                "bfd",
                "stlport",
            },
            "atomspace": {"boost", "doxygen", "pgsql", "unixodbc", "valgrind", "cxxtest", "stack", "folly", "ocaml"},
            "atomspace_storage": {"boost", "doxygen", "cxxtest", "guile"},
            "cogserver": {"boost", "doxygen", "valgrind", "cxxtest", "openssl"},
            "atomspace_rocks": {"doxygen", "valgrind", "cxxtest", "rocksdb"},
            "atomspace_restful": {"boost", "doxygen", "attentionbank", "jsoncpp", "cxxtest", "zmq", "pkgconfig", "tbb"},
            "vision": {"doxygen", "valgrind", "catch2", "opencv"},
            "lg_atomese": {"doxygen", "cxxtest", "linkgrammar", "uuid"},
            "moses": {"boost", "doxygen", "valgrind", "cxxtest", "mpi"},
            "pln": {"boost"},
            "ure": {"boost", "valgrind", "cxxtest"},
            "unify": {"boost", "valgrind", "cxxtest"},
            "attention": {"boost", "doxygen", "valgrind", "cxxtest"},
            "spacetime": {"boost", "doxygen", "cxxtest", "octomap"},
            "miner": {"boost", "valgrind", "cxxtest"},
            "asmoses": {"boost", "doxygen", "valgrind", "cxxtest", "mpi"},
            "TinyCog": {
                "festival",
                "openmp",
                "est",
                "opencv",
                "wiringpi",
                "raspicam",
                "alsa",
                "guile",
                "pkgconfig",
                "pocketsphinx",
                "dlib",
                "protobuf",
            },
            "opencog": {"doxygen", "attentionbank", "valgrind", "cxxtest", "ghc", "stack", "lgatomese", "boost"},
        }

        # Initialize components
        for comp_name, deps in component_deps.items():
            category = "other"
            for cat, comps in categories.items():
                if comp_name in comps:
                    category = cat
                    break

            external_deps = external_deps_map.get(comp_name, set())
            self.external_deps.update(external_deps)

            self.components[comp_name] = Component(
                name=comp_name, category=category, dependencies=deps, external_deps=external_deps
            )

            # Add to graph
            self.dependency_graph.add_node(comp_name, category=category)

        # Add dependency edges
        for comp_name, component in self.components.items():
            for dep in component.dependencies:
                if dep in self.components:
                    self.dependency_graph.add_edge(dep, comp_name)

    def topological_sort(self) -> list[str]:
        """Generate topological sort order for build sequence"""
        try:
            return list(nx.topological_sort(self.dependency_graph))
        except nx.NetworkXError as e:
            print(f"Error: Circular dependency detected: {e}")
            return []

    def find_critical_path(self) -> tuple[list[str], int]:
        """Find the critical path (longest dependency chain)"""
        # For DAG, we need to find longest path
        # Since networkx doesn't have longest_path for DAG directly, we'll compute it

        # Get all nodes with no dependencies (sources)
        sources = [n for n in self.dependency_graph.nodes() if self.dependency_graph.in_degree(n) == 0]

        # Compute longest paths from each source
        longest_path = []
        max_length = 0

        for source in sources:
            # Use DFS to find longest path from this source
            path, length = self._longest_path_from_node(source)
            if length > max_length:
                max_length = length
                longest_path = path

        return longest_path, max_length

    def _longest_path_from_node(self, start_node: str) -> tuple[list[str], int]:
        """Find longest path from a given node using DFS"""
        visited = set()
        path = []
        max_path = []
        max_length = 0

        def dfs(node):
            nonlocal max_path, max_length
            visited.add(node)
            path.append(node)

            # Check if this is a longer path
            if len(path) > max_length:
                max_length = len(path)
                max_path = path.copy()

            # Visit all successors
            for successor in self.dependency_graph.successors(node):
                if successor not in visited:
                    dfs(successor)

            path.pop()
            visited.remove(node)

        dfs(start_node)
        return max_path, max_length

    def find_parallel_builds(self) -> dict[int, list[str]]:
        """Find components that can be built in parallel at each level"""
        topo_order = self.topological_sort()
        if not topo_order:
            return {}

        # Assign levels based on maximum dependency depth
        levels = {}
        for node in topo_order:
            if not list(self.dependency_graph.predecessors(node)):
                levels[node] = 0
            else:
                levels[node] = max(levels[pred] for pred in self.dependency_graph.predecessors(node)) + 1

        # Group by level
        parallel_groups = defaultdict(list)
        for node, level in levels.items():
            parallel_groups[level].append(node)

        return dict(parallel_groups)

    def analyze_component_complexity(self) -> dict[str, dict]:
        """Analyze build complexity for each component"""
        complexity = {}

        for comp_name, component in self.components.items():
            # Complexity metrics
            dep_count = len(component.dependencies)
            external_dep_count = len(component.external_deps)
            self.dependency_graph.in_degree(comp_name)
            out_degree = self.dependency_graph.out_degree(comp_name)

            # Simple complexity score
            complexity_score = dep_count * 2 + external_dep_count + out_degree

            complexity[comp_name] = {
                "internal_dependencies": dep_count,
                "external_dependencies": external_dep_count,
                "dependents": out_degree,
                "complexity_score": complexity_score,
                "category": component.category,
                "external_deps": list(component.external_deps),
            }

        return complexity

    def generate_build_phases(self) -> dict[str, list[str]]:
        """Generate logical build phases based on dependency layers"""
        parallel_groups = self.find_parallel_builds()

        phases = {
            "Phase 1 - Foundation": [],
            "Phase 2 - Core Systems": [],
            "Phase 3 - Logic Layer": [],
            "Phase 4 - Cognitive Systems": [],
            "Phase 5 - Advanced Systems": [],
            "Phase 6 - Learning Systems": [],
            "Phase 7 - Specialized Components": [],
            "Phase 8 - Integration Layer": [],
        }

        # Map levels to phases based on component categories
        for _level, components in parallel_groups.items():
            for comp in components:
                category = self.components[comp].category

                if category == "foundation" or comp == "cogutil":
                    phases["Phase 1 - Foundation"].append(comp)
                elif category == "core" or comp in ["atomspace", "cogserver"]:
                    phases["Phase 2 - Core Systems"].append(comp)
                elif category == "logic" or comp in ["unify", "ure"]:
                    phases["Phase 3 - Logic Layer"].append(comp)
                elif category == "cognitive":
                    phases["Phase 4 - Cognitive Systems"].append(comp)
                elif category == "advanced":
                    phases["Phase 5 - Advanced Systems"].append(comp)
                elif category == "learning":
                    phases["Phase 6 - Learning Systems"].append(comp)
                elif category == "specialized":
                    phases["Phase 7 - Specialized Components"].append(comp)
                else:
                    phases["Phase 8 - Integration Layer"].append(comp)

        # Remove empty phases
        return {k: v for k, v in phases.items() if v}

    def generate_cmake_sequence(self) -> str:
        """Generate optimized CMake build sequence"""
        self.topological_sort()
        parallel_groups = self.find_parallel_builds()

        cmake_content = """# OpenCog Unified - Optimized Build Sequence
# Generated by dependency_analyzer.py

cmake_minimum_required(VERSION 3.10)
project(opencog-unified VERSION 1.0.0)

# Set C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Add cmake directory to module path
set(CMAKE_MODULE_PATH
    ${CMAKE_CURRENT_SOURCE_DIR}/cmake
    ${CMAKE_CURRENT_SOURCE_DIR}/cogutil/cmake
    ${CMAKE_MODULE_PATH}
)

"""

        # Add components in dependency order
        cmake_content += "# Optimized build sequence based on dependency analysis\n"

        for level, components in parallel_groups.items():
            cmake_content += f"\n# Level {level} - Parallel builds possible\n"
            for comp in components:
                comp_dir = comp.replace("_", "-")  # Convert to directory naming convention
                cmake_content += f"""if(EXISTS "${{CMAKE_CURRENT_SOURCE_DIR}}/{comp_dir}/CMakeLists.txt")
    add_subdirectory({comp_dir})
endif()
"""

        # Add dependency relationships
        cmake_content += "\n# Explicit dependency relationships\n"
        for comp_name, component in self.components.items():
            if component.dependencies:
                comp_dir = comp_name.replace("_", "-")
                for dep in component.dependencies:
                    dep_dir = dep.replace("_", "-")
                    cmake_content += f"if(TARGET {comp_dir} AND TARGET {dep_dir})\n"
                    cmake_content += f"    add_dependencies({comp_dir} {dep_dir})\n"
                    cmake_content += "endif()\n"

        return cmake_content

    def generate_report(self) -> dict:
        """Generate comprehensive dependency analysis report"""
        topo_order = self.topological_sort()
        critical_path, critical_length = self.find_critical_path()
        parallel_groups = self.find_parallel_builds()
        complexity = self.analyze_component_complexity()
        phases = self.generate_build_phases()

        report = {
            "analysis_summary": {
                "total_components": len(self.components),
                "external_dependencies": len(self.external_deps),
                "critical_path_length": critical_length,
                "parallelization_levels": len(parallel_groups),
                "has_cycles": not bool(topo_order),
            },
            "build_sequence": {
                "topological_order": topo_order,
                "critical_path": critical_path,
                "parallel_groups": parallel_groups,
                "build_phases": phases,
            },
            "component_analysis": complexity,
            "external_dependencies": sorted(self.external_deps),
            "recommendations": self._generate_recommendations(critical_path, parallel_groups, complexity),
        }

        return report

    def _generate_recommendations(
        self, critical_path: list[str], parallel_groups: dict[int, list[str]], complexity: dict[str, dict]
    ) -> list[str]:
        """Generate build optimization recommendations"""
        recommendations = []

        # Critical path recommendations
        if critical_path:
            recommendations.append(f"Critical path: {' -> '.join(critical_path)}")
            recommendations.append("Focus optimization efforts on critical path components")

        # Parallelization opportunities
        max_parallel = max(len(group) for group in parallel_groups.values())
        recommendations.append(f"Maximum parallelization: {max_parallel} components simultaneously")

        # High complexity components
        high_complexity = sorted(complexity.items(), key=lambda x: x[1]["complexity_score"], reverse=True)[:5]
        recommendations.append("Highest complexity components:")
        for comp, data in high_complexity:
            recommendations.append(f"  - {comp}: score {data['complexity_score']}")

        # External dependency analysis
        high_external_deps = [comp for comp, data in complexity.items() if data["external_dependencies"] > 3]
        if high_external_deps:
            recommendations.append(f"Components with many external deps: {', '.join(high_external_deps)}")

        return recommendations

    def save_report(self, filename: str = "dependency_analysis_report.json"):
        """Save analysis report to JSON file"""
        report = self.generate_report()
        with open(filename, "w") as f:
            json.dump(report, f, indent=2)
        print(f"Report saved to {filename}")

    def save_cmake_file(self, filename: str = "CMakeLists_optimized.txt"):
        """Save optimized CMake file"""
        cmake_content = self.generate_cmake_sequence()
        with open(filename, "w") as f:
            f.write(cmake_content)
        print(f"Optimized CMake file saved to {filename}")

    def visualize_dependencies(self, output_file: str = "dependency_graph.png"):
        """Generate dependency graph visualization"""
        try:
            import matplotlib.pyplot as plt

            plt.figure(figsize=(20, 16))

            # Create layout
            pos = nx.spring_layout(self.dependency_graph, k=3, iterations=50)

            # Color nodes by category
            category_colors = {
                "foundation": "#e8f5e8",
                "core": "#e3f2fd",
                "logic": "#fff3e0",
                "cognitive": "#f3e5f5",
                "advanced": "#ffebee",
                "learning": "#f1f8e9",
                "specialized": "#e0f2f1",
                "integration": "#fce4ec",
                "other": "#f5f5f5",
            }

            node_colors = [
                category_colors.get(self.components[node].category, "#f5f5f5") for node in self.dependency_graph.nodes()
            ]

            # Draw graph
            nx.draw(
                self.dependency_graph,
                pos,
                node_color=node_colors,
                node_size=1000,
                font_size=8,
                font_weight="bold",
                arrows=True,
                arrowsize=20,
                edge_color="gray",
                alpha=0.8,
            )

            # Add labels
            nx.draw_networkx_labels(self.dependency_graph, pos, font_size=6)

            plt.title("OpenCog Complete Dependency Graph", size=16)
            plt.axis("off")
            plt.tight_layout()
            plt.savefig(output_file, dpi=300, bbox_inches="tight")
            print(f"Dependency graph saved to {output_file}")

        except ImportError:
            print("matplotlib not available for visualization")


def main():
    parser = argparse.ArgumentParser(description="OpenCog Dependency Analyzer")
    parser.add_argument("--report", action="store_true", help="Generate comprehensive analysis report")
    parser.add_argument("--cmake", action="store_true", help="Generate optimized CMake file")
    parser.add_argument("--visualize", action="store_true", help="Generate dependency graph visualization")
    parser.add_argument("--output-dir", default=".", help="Output directory for generated files")

    args = parser.parse_args()

    analyzer = DependencyAnalyzer()

    # Set output directory
    output_dir = Path(args.output_dir)
    output_dir.mkdir(exist_ok=True)

    if args.report or not any([args.cmake, args.visualize]):
        # Generate and display report
        report = analyzer.generate_report()

        print("=== OpenCog Complete Dependency Analysis ===\n")

        print("SUMMARY:")
        for key, value in report["analysis_summary"].items():
            print(f"  {key}: {value}")

        print(f"\nCRITICAL PATH ({len(report['build_sequence']['critical_path'])} components):")
        print(f"  {' -> '.join(report['build_sequence']['critical_path'])}")

        print("\nBUILD PHASES:")
        for phase, components in report["build_sequence"]["build_phases"].items():
            print(f"  {phase}: {len(components)} components")
            print(f"    {', '.join(components)}")

        print("\nPARALLELIZATION OPPORTUNITIES:")
        for level, components in report["build_sequence"]["parallel_groups"].items():
            if len(components) > 1:
                print(f"  Level {level}: {len(components)} parallel builds")
                print(f"    {', '.join(components)}")

        print("\nRECOMMENDATIONS:")
        for rec in report["recommendations"]:
            print(f"  • {rec}")

        # Save detailed report
        analyzer.save_report(output_dir / "dependency_analysis_report.json")

    if args.cmake:
        analyzer.save_cmake_file(output_dir / "CMakeLists_optimized.txt")

    if args.visualize:
        analyzer.visualize_dependencies(output_dir / "dependency_graph.png")


if __name__ == "__main__":
    main()
