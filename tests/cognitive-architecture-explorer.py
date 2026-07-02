#!/usr/bin/env python3
"""
Interactive Cognitive Architecture Explorer

This tool provides recursive documentation and exploration of the OpenCog Unified
cognitive architecture, including:
1. Auto-generated architectural flowcharts
2. Living documentation system
3. Cognitive pattern emergence reports
4. Interactive exploration interface
5. Tensor signature evolution tracking

Copyright (c) 2025 OpenCog Foundation
"""

import argparse
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class ComponentInfo:
    """Information about a cognitive component"""
    name: str
    path: Path
    phase: int
    dependencies: list[str]
    file_count: int
    total_size: int
    primary_language: str
    cognitive_functions: list[str]
    tensor_signatures: dict[str, Any]
    integration_status: str

@dataclass
class CognitivePattern:
    """Detected cognitive pattern"""
    pattern_type: str
    components_involved: list[str]
    emergence_level: float
    stability_score: float
    description: str
    first_detected: str
    evolution_history: list[dict]

class CognitiveArchitectureExplorer:
    """Interactive explorer for cognitive architecture"""

    def __init__(self):
        self.components: dict[str, ComponentInfo] = {}
        self.cognitive_patterns: list[CognitivePattern] = []
        self.architecture_graph: dict[str, list[str]] = {}
        self.tensor_evolution: dict[str, list[dict]] = {}
        self.documentation_index: dict[str, list[str]] = {}

    def discover_architecture(self):
        """Discover and analyze the cognitive architecture"""
        print("🔍 Discovering Cognitive Architecture...")

        # Discover components
        self._discover_components()

        # Build dependency graph
        self._build_dependency_graph()

        # Detect cognitive patterns
        self._detect_cognitive_patterns()

        # Index documentation
        self._index_documentation()

        print(f"   Found {len(self.components)} components")
        print(f"   Detected {len(self.cognitive_patterns)} cognitive patterns")
        print(f"   Indexed {sum(len(docs) for docs in self.documentation_index.values())} documentation files")

    def _discover_components(self):
        """Discover all cognitive components"""
        component_dirs = [
            ('cogutil', 1), ('atomspace', 1), ('cogserver', 1),
            ('atomspace-rocks', 1), ('atomspace-restful', 1), ('moses', 1),
            ('unify', 2), ('ure', 2), ('language-learning', 2),
            ('attention', 3), ('spacetime', 3),
            ('pln', 4), ('miner', 4), ('asmoses', 4),
            ('lg-atomese', 5), ('learn', 5), ('opencog', 5),
            ('ggml-tensor-kernel', 6), ('cognitive-patterns', 6),
            ('cognitive-visualization', 6), ('distributed-cognition', 6)
        ]

        for component_name, phase in component_dirs:
            component_path = Path(component_name)
            if component_path.exists():
                info = self._analyze_component(component_name, component_path, phase)
                if info:
                    self.components[component_name] = info

    def _analyze_component(self, name: str, path: Path, phase: int) -> ComponentInfo | None:
        """Analyze a single component"""
        try:
            # Count files and calculate size
            files = list(path.rglob('*'))
            file_count = len([f for f in files if f.is_file()])
            total_size = sum(f.stat().st_size for f in files if f.is_file())

            # Determine primary language
            extensions = {}
            for f in files:
                if f.is_file() and f.suffix:
                    extensions[f.suffix] = extensions.get(f.suffix, 0) + 1

            primary_language = "Unknown"
            if extensions:
                primary_ext = max(extensions, key=extensions.get)
                lang_map = {
                    '.cc': 'C++', '.cpp': 'C++', '.h': 'C++', '.hpp': 'C++',
                    '.scm': 'Scheme', '.py': 'Python', '.sh': 'Shell',
                    '.cmake': 'CMake', '.txt': 'CMake'
                }
                primary_language = lang_map.get(primary_ext, primary_ext[1:].upper())

            # Extract cognitive functions (simplified)
            cognitive_functions = self._extract_cognitive_functions(path)

            # Extract tensor signatures
            tensor_signatures = self._extract_tensor_signatures(path)

            # Determine integration status
            cmake_file = Path('CMakeLists.txt')
            integration_status = "integrated" if cmake_file.exists() and name in cmake_file.read_text() else "standalone"

            # Extract dependencies (simplified)
            dependencies = self._extract_dependencies(path)

            return ComponentInfo(
                name=name,
                path=path,
                phase=phase,
                dependencies=dependencies,
                file_count=file_count,
                total_size=total_size,
                primary_language=primary_language,
                cognitive_functions=cognitive_functions,
                tensor_signatures=tensor_signatures,
                integration_status=integration_status
            )
        except Exception as e:
            print(f"   Warning: Could not analyze {name}: {e}")
            return None

    def _extract_cognitive_functions(self, path: Path) -> list[str]:
        """Extract cognitive functions from component"""
        functions = []

        # Look for key cognitive function indicators
        cognitive_keywords = [
            'attention', 'memory', 'learning', 'reasoning', 'perception',
            'pattern', 'tensor', 'cognitive', 'neural', 'symbolic',
            'unified', 'integration', 'emergence', 'recursive'
        ]

        try:
            for file_path in path.rglob('*.cc'):
                if file_path.is_file():
                    content = file_path.read_text(encoding='utf-8', errors='ignore')
                    for keyword in cognitive_keywords:
                        if keyword in content.lower():
                            functions.append(keyword)
        except Exception:
            pass

        return list(set(functions))

    def _extract_tensor_signatures(self, path: Path) -> dict[str, Any]:
        """Extract tensor signatures from component"""
        signatures = {}

        try:
            # Look for tensor-related files
            for file_path in path.rglob('*.h'):
                if file_path.is_file() and 'tensor' in file_path.name.lower():
                    content = file_path.read_text(encoding='utf-8', errors='ignore')

                    # Extract dimensions (simplified pattern matching)
                    if 'dimension' in content.lower():
                        signatures[file_path.name] = {
                            'type': 'header',
                            'has_dimensions': True,
                            'estimated_complexity': content.count('class') + content.count('struct')
                        }
        except Exception:
            pass

        return signatures

    def _extract_dependencies(self, path: Path) -> list[str]:
        """Extract component dependencies"""
        dependencies = []

        try:
            # Check CMakeLists.txt for dependencies
            cmake_file = path / 'CMakeLists.txt'
            if cmake_file.exists():
                content = cmake_file.read_text()

                # Look for find_package and target_link_libraries
                for line in content.split('\n'):
                    line = line.strip()
                    if line.startswith('find_package'):
                        dep = line.split('(')[1].split()[0]
                        dependencies.append(dep)
                    elif 'target_link_libraries' in line:
                        # Extract library names (simplified)
                        parts = line.split()
                        if len(parts) > 2:
                            dependencies.extend(parts[2:])
        except Exception:
            pass

        return dependencies

    def _build_dependency_graph(self):
        """Build the component dependency graph"""
        for component_name, component_info in self.components.items():
            self.architecture_graph[component_name] = []

            # Add dependencies that exist in our component list
            for dep in component_info.dependencies:
                dep_lower = dep.lower()
                for existing_component in self.components:
                    if existing_component.lower() in dep_lower or dep_lower in existing_component.lower():
                        self.architecture_graph[component_name].append(existing_component)

    def _detect_cognitive_patterns(self):
        """Detect emergent cognitive patterns"""
        patterns = []

        # Pattern 1: Phase Integration Patterns
        phase_groups = {}
        for comp_name, comp_info in self.components.items():
            phase = comp_info.phase
            if phase not in phase_groups:
                phase_groups[phase] = []
            phase_groups[phase].append(comp_name)

        for phase, components in phase_groups.items():
            if len(components) >= 2:
                pattern = CognitivePattern(
                    pattern_type="phase_integration",
                    components_involved=components,
                    emergence_level=min(len(components) / 5.0, 1.0),
                    stability_score=0.8 + (phase * 0.02),  # Later phases more stable
                    description=f"Phase {phase} cognitive integration pattern involving {len(components)} components",
                    first_detected=time.strftime("%Y-%m-%d"),
                    evolution_history=[]
                )
                patterns.append(pattern)

        # Pattern 2: Language Diversity Patterns
        language_groups = {}
        for comp_name, comp_info in self.components.items():
            lang = comp_info.primary_language
            if lang not in language_groups:
                language_groups[lang] = []
            language_groups[lang].append(comp_name)

        for lang, components in language_groups.items():
            if len(components) >= 3:
                pattern = CognitivePattern(
                    pattern_type="language_specialization",
                    components_involved=components,
                    emergence_level=0.6,
                    stability_score=0.75,
                    description=f"{lang} language specialization pattern with {len(components)} components",
                    first_detected=time.strftime("%Y-%m-%d"),
                    evolution_history=[]
                )
                patterns.append(pattern)

        # Pattern 3: Cognitive Function Clustering
        function_overlap = {}
        for comp_name, comp_info in self.components.items():
            for func in comp_info.cognitive_functions:
                if func not in function_overlap:
                    function_overlap[func] = []
                function_overlap[func].append(comp_name)

        for func, components in function_overlap.items():
            if len(components) >= 3:
                pattern = CognitivePattern(
                    pattern_type="functional_clustering",
                    components_involved=components,
                    emergence_level=len(components) / 10.0,
                    stability_score=0.7,
                    description=f"Functional clustering around '{func}' with {len(components)} components",
                    first_detected=time.strftime("%Y-%m-%d"),
                    evolution_history=[]
                )
                patterns.append(pattern)

        self.cognitive_patterns = patterns

    def _index_documentation(self):
        """Index all documentation files"""
        doc_patterns = ['*.md', '*.rst', '*.txt', '*.org']

        for pattern in doc_patterns:
            for doc_file in Path().rglob(pattern):
                if doc_file.is_file():
                    # Categorize documentation
                    category = self._categorize_documentation(doc_file)
                    if category not in self.documentation_index:
                        self.documentation_index[category] = []
                    self.documentation_index[category].append(str(doc_file))

    def _categorize_documentation(self, doc_file: Path) -> str:
        """Categorize documentation file"""
        name_lower = doc_file.name.lower()

        if 'readme' in name_lower:
            return 'readme'
        elif 'phase' in name_lower:
            return 'phase_documentation'
        elif 'implementation' in name_lower:
            return 'implementation'
        elif 'test' in name_lower:
            return 'testing'
        elif 'todo' in name_lower or 'fixme' in name_lower:
            return 'development_notes'
        elif 'roadmap' in name_lower:
            return 'roadmap'
        else:
            return 'general'

    def generate_architecture_flowchart(self) -> str:
        """Generate ASCII flowchart of the architecture"""
        flowchart = []
        flowchart.append("🏗️  OpenCog Unified Cognitive Architecture")
        flowchart.append("=" * 60)
        flowchart.append("")

        # Group by phases
        phases = {}
        for comp_name, comp_info in self.components.items():
            phase = comp_info.phase
            if phase not in phases:
                phases[phase] = []
            phases[phase].append(comp_name)

        # Generate phase-by-phase flowchart
        for phase_num in sorted(phases.keys()):
            components = phases[phase_num]
            flowchart.append(f"📚 PHASE {phase_num}:")

            for i, comp in enumerate(components):
                comp_info = self.components[comp]
                prefix = "├── " if i < len(components) - 1 else "└── "

                # Show component with key info
                flowchart.append(f"   {prefix}{comp} ({comp_info.primary_language})")

                # Show dependencies
                if comp in self.architecture_graph:
                    deps = self.architecture_graph[comp]
                    if deps:
                        dep_prefix = "│   " if i < len(components) - 1 else "    "
                        flowchart.append(f"   {dep_prefix}    ↳ depends on: {', '.join(deps[:3])}")
            flowchart.append("")

        # Add cognitive patterns section
        flowchart.append("🧠 COGNITIVE PATTERNS:")
        for pattern in self.cognitive_patterns:
            flowchart.append(f"   • {pattern.pattern_type}: {pattern.description}")
            flowchart.append(f"     Emergence: {pattern.emergence_level:.2f}, Stability: {pattern.stability_score:.2f}")

        return "\n".join(flowchart)

    def generate_component_report(self, component_name: str) -> str:
        """Generate detailed report for a specific component"""
        if component_name not in self.components:
            return f"❌ Component '{component_name}' not found"

        comp = self.components[component_name]
        report = []

        report.append(f"📦 COMPONENT REPORT: {component_name}")
        report.append("=" * 50)
        report.append(f"Phase: {comp.phase}")
        report.append(f"Path: {comp.path}")
        report.append(f"Primary Language: {comp.primary_language}")
        report.append(f"Files: {comp.file_count}")
        report.append(f"Total Size: {comp.total_size:,} bytes")
        report.append(f"Integration Status: {comp.integration_status}")
        report.append("")

        report.append("🔗 Dependencies:")
        if comp.dependencies:
            for dep in comp.dependencies:
                report.append(f"   • {dep}")
        else:
            report.append("   • None specified")
        report.append("")

        report.append("🧠 Cognitive Functions:")
        if comp.cognitive_functions:
            for func in comp.cognitive_functions:
                report.append(f"   • {func}")
        else:
            report.append("   • None detected")
        report.append("")

        report.append("🧮 Tensor Signatures:")
        if comp.tensor_signatures:
            for sig_name, sig_info in comp.tensor_signatures.items():
                report.append(f"   • {sig_name}: {sig_info}")
        else:
            report.append("   • None detected")
        report.append("")

        # Add pattern involvement
        involved_patterns = [p for p in self.cognitive_patterns if component_name in p.components_involved]
        if involved_patterns:
            report.append("🌊 Cognitive Pattern Involvement:")
            for pattern in involved_patterns:
                report.append(f"   • {pattern.pattern_type}: {pattern.description}")

        return "\n".join(report)

    def generate_cognitive_emergence_report(self) -> str:
        """Generate report on cognitive pattern emergence"""
        report = []

        report.append("🌊 COGNITIVE PATTERN EMERGENCE REPORT")
        report.append("=" * 60)
        report.append(f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")

        # Overall statistics
        total_components = len(self.components)
        total_patterns = len(self.cognitive_patterns)
        avg_emergence = sum(p.emergence_level for p in self.cognitive_patterns) / max(total_patterns, 1)
        avg_stability = sum(p.stability_score for p in self.cognitive_patterns) / max(total_patterns, 1)

        report.append("📊 EMERGENCE METRICS:")
        report.append(f"   Total Components: {total_components}")
        report.append(f"   Detected Patterns: {total_patterns}")
        report.append(f"   Average Emergence Level: {avg_emergence:.3f}")
        report.append(f"   Average Stability Score: {avg_stability:.3f}")
        report.append("")

        # Pattern details
        report.append("🧠 DETECTED PATTERNS:")
        for i, pattern in enumerate(self.cognitive_patterns, 1):
            report.append(f"\n{i}. {pattern.pattern_type.upper()}")
            report.append(f"   Description: {pattern.description}")
            report.append(f"   Components: {', '.join(pattern.components_involved)}")
            report.append(f"   Emergence Level: {pattern.emergence_level:.3f}")
            report.append(f"   Stability Score: {pattern.stability_score:.3f}")
            report.append(f"   First Detected: {pattern.first_detected}")

        # Emergent properties analysis
        report.append("\n🔬 EMERGENT PROPERTIES ANALYSIS:")

        # Component connectivity
        connectivity = sum(len(deps) for deps in self.architecture_graph.values()) / max(total_components, 1)
        report.append(f"   Average Component Connectivity: {connectivity:.2f}")

        # Language diversity
        languages = {comp.primary_language for comp in self.components.values()}
        report.append(f"   Language Diversity: {len(languages)} languages")

        # Phase distribution
        phase_distribution = {}
        for comp in self.components.values():
            phase_distribution[comp.phase] = phase_distribution.get(comp.phase, 0) + 1
        report.append(f"   Phase Distribution: {dict(phase_distribution)}")

        # Cognitive function coverage
        all_functions = set()
        for comp in self.components.values():
            all_functions.update(comp.cognitive_functions)
        report.append(f"   Cognitive Function Coverage: {len(all_functions)} unique functions")

        return "\n".join(report)

    def generate_living_documentation_index(self) -> str:
        """Generate living documentation index"""
        index = []

        index.append("📚 LIVING DOCUMENTATION INDEX")
        index.append("=" * 50)
        index.append(f"Last Updated: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        index.append("")

        total_docs = sum(len(docs) for docs in self.documentation_index.values())
        index.append(f"📄 Total Documentation Files: {total_docs}")
        index.append("")

        for category, docs in self.documentation_index.items():
            index.append(f"📂 {category.upper().replace('_', ' ')}: ({len(docs)} files)")

            # Show first few documents
            for doc in docs[:5]:
                index.append(f"   • {doc}")

            if len(docs) > 5:
                index.append(f"   ... and {len(docs) - 5} more files")
            index.append("")

        return "\n".join(index)

    def interactive_explore(self):
        """Interactive exploration interface"""
        print("\n🚀 Interactive Cognitive Architecture Explorer")
        print("=" * 60)

        while True:
            print("\nAvailable commands:")
            print("1. 'list' - List all components")
            print("2. 'component <name>' - Detailed component report")
            print("3. 'flowchart' - Generate architecture flowchart")
            print("4. 'patterns' - Show cognitive patterns")
            print("5. 'emergence' - Generate emergence report")
            print("6. 'docs' - Show documentation index")
            print("7. 'search <term>' - Search components and docs")
            print("8. 'quit' - Exit explorer")

            try:
                command = input("\n🔍 Enter command: ").strip().lower()

                if command == 'quit':
                    break
                elif command == 'list':
                    self._handle_list_command()
                elif command.startswith('component '):
                    comp_name = command[10:].strip()
                    self._handle_component_command(comp_name)
                elif command == 'flowchart':
                    print("\n" + self.generate_architecture_flowchart())
                elif command == 'patterns':
                    self._handle_patterns_command()
                elif command == 'emergence':
                    print("\n" + self.generate_cognitive_emergence_report())
                elif command == 'docs':
                    print("\n" + self.generate_living_documentation_index())
                elif command.startswith('search '):
                    search_term = command[7:].strip()
                    self._handle_search_command(search_term)
                else:
                    print("❌ Unknown command. Try 'list', 'component <name>', 'flowchart', 'patterns', 'emergence', 'docs', 'search <term>', or 'quit'")

            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")

    def _handle_list_command(self):
        """Handle list components command"""
        print(f"\n📦 COMPONENTS ({len(self.components)} total):")

        # Group by phase
        phases = {}
        for comp_name, comp_info in self.components.items():
            phase = comp_info.phase
            if phase not in phases:
                phases[phase] = []
            phases[phase].append((comp_name, comp_info))

        for phase_num in sorted(phases.keys()):
            print(f"\n   Phase {phase_num}:")
            for comp_name, comp_info in phases[phase_num]:
                size_mb = comp_info.total_size / (1024 * 1024)
                print(f"      • {comp_name} ({comp_info.primary_language}, {size_mb:.1f}MB, {comp_info.file_count} files)")

    def _handle_component_command(self, comp_name: str):
        """Handle component detail command"""
        print("\n" + self.generate_component_report(comp_name))

    def _handle_patterns_command(self):
        """Handle patterns command"""
        print(f"\n🧠 COGNITIVE PATTERNS ({len(self.cognitive_patterns)} detected):")

        for i, pattern in enumerate(self.cognitive_patterns, 1):
            print(f"\n{i}. {pattern.pattern_type.upper()}")
            print(f"   {pattern.description}")
            print(f"   Components: {', '.join(pattern.components_involved)}")
            print(f"   Emergence: {pattern.emergence_level:.3f}, Stability: {pattern.stability_score:.3f}")

    def _handle_search_command(self, search_term: str):
        """Handle search command"""
        print(f"\n🔍 SEARCH RESULTS for '{search_term}':")

        found_components = []
        found_docs = []

        # Search components
        for comp_name, comp_info in self.components.items():
            if (search_term in comp_name.lower() or
                search_term in comp_info.primary_language.lower() or
                any(search_term in func.lower() for func in comp_info.cognitive_functions)):
                found_components.append(comp_name)

        # Search documentation
        for _category, docs in self.documentation_index.items():
            for doc in docs:
                if search_term in doc.lower():
                    found_docs.append(doc)

        if found_components:
            print("\n📦 Components:")
            for comp in found_components:
                print(f"   • {comp}")

        if found_docs:
            print("\n📄 Documentation:")
            for doc in found_docs[:10]:  # Limit to 10 results
                print(f"   • {doc}")
            if len(found_docs) > 10:
                print(f"   ... and {len(found_docs) - 10} more files")

        if not found_components and not found_docs:
            print("   No results found.")

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Interactive Cognitive Architecture Explorer")
    parser.add_argument('--mode', choices=['interactive', 'report', 'flowchart'],
                       default='interactive', help='Exploration mode')
    parser.add_argument('--component', help='Generate report for specific component')
    parser.add_argument('--output', help='Output file for reports')

    args = parser.parse_args()

    # Initialize explorer
    explorer = CognitiveArchitectureExplorer()

    print("🔍 Discovering Cognitive Architecture...")
    explorer.discover_architecture()

    if args.mode == 'interactive':
        explorer.interactive_explore()
    elif args.mode == 'flowchart':
        flowchart = explorer.generate_architecture_flowchart()
        print("\n" + flowchart)
        if args.output:
            Path(args.output).write_text(flowchart)
            print(f"\nFlowchart saved to {args.output}")
    elif args.mode == 'report':
        if args.component:
            report = explorer.generate_component_report(args.component)
        else:
            report = explorer.generate_cognitive_emergence_report()

        print("\n" + report)
        if args.output:
            Path(args.output).write_text(report)
            print(f"\nReport saved to {args.output}")

if __name__ == "__main__":
    main()
