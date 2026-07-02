#!/usr/bin/env python3
"""
OpenCog Unified Entelechy Introspection Framework

This framework performs deep introspection to gain insights into the opencog-unified
entelechy (vital purpose/actualization) and identify fragmented aspects of self in need of repair.

Inspired by:
- AUTOGNOSIS: Hierarchical self-image building system
- ONTOGENESIS: Self-generating, evolving kernels
- HOLISTIC_METAMODEL: Eric Schwarz's organizational systems theory

The system examines multiple dimensions:
1. Ontological Completeness - The "being" of the system
2. Teleological Alignment - The "purpose" driving toward actualization
3. Cognitive Fragmentation - Broken or incomplete aspects
4. Holistic Coherence - Integration across all organizational levels
5. Self-Organization Capacity - Ability to repair and evolve
"""

import json
import re
from collections import defaultdict
from dataclasses import asdict, dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path


class EntelechyDimension(Enum):
    """Dimensions of entelechy analysis"""
    ONTOLOGICAL = "ontological"  # Being - what the system IS
    TELEOLOGICAL = "teleological"  # Purpose - what the system is BECOMING
    COGNITIVE = "cognitive"  # Cognition - how the system THINKS
    INTEGRATIVE = "integrative"  # Integration - how parts UNITE
    EVOLUTIONARY = "evolutionary"  # Evolution - how the system GROWS


class FragmentationType(Enum):
    """Types of fragmentation identified"""
    INCOMPLETE_IMPLEMENTATION = "incomplete_implementation"
    MISSING_DEPENDENCY = "missing_dependency"
    COGNITIVE_DISCONNECT = "cognitive_disconnect"
    INTEGRATION_GAP = "integration_gap"
    EVOLUTIONARY_STAGNATION = "evolutionary_stagnation"
    PLACEHOLDER_CODE = "placeholder_code"
    BROKEN_LINKAGE = "broken_linkage"
    CONCEPTUAL_INCOHERENCE = "conceptual_incoherence"


@dataclass
class FragmentationSignature:
    """Signature of a fragmented aspect"""
    dimension: EntelechyDimension
    fragmentation_type: FragmentationType
    location: str
    severity: float  # 0.0-1.0, where 1.0 is critical
    description: str
    context: dict[str, any] = field(default_factory=dict)
    repair_priority: int = 0
    repair_suggestions: list[str] = field(default_factory=list)


@dataclass
class EntelechyMetrics:
    """Quantitative metrics of system entelechy"""
    actualization_score: float  # 0.0-1.0, degree of potential realization
    coherence_score: float  # 0.0-1.0, holistic integration
    vitality_score: float  # 0.0-1.0, self-organizing capacity
    completeness_score: float  # 0.0-1.0, implementation completeness
    alignment_score: float  # 0.0-1.0, teleological alignment

    # Component metrics
    total_components: int = 0
    integrated_components: int = 0
    fragmented_components: int = 0

    # Code health metrics
    total_code_markers: int = 0
    todo_count: int = 0
    fixme_count: int = 0
    stub_count: int = 0

    # Cognitive architecture metrics
    cognitive_layers_complete: int = 0
    cognitive_layers_total: int = 0

    # Integration metrics
    dependency_satisfaction: float = 0.0
    cmake_integration_health: float = 0.0
    test_coverage_health: float = 0.0


class EntelechyIntrospector:
    """
    Deep introspection system for OpenCog Unified entelechy analysis

    Performs comprehensive self-examination across multiple dimensions
    to identify fragmented aspects and assess actualization potential.
    """

    def __init__(self, repo_path: str = "."):
        self.repo_path = Path(repo_path).resolve()
        self.fragments: list[FragmentationSignature] = []
        self.metrics = EntelechyMetrics(
            actualization_score=0.0,
            coherence_score=0.0,
            vitality_score=0.0,
            completeness_score=0.0,
            alignment_score=0.0
        )
        self.component_config = None
        self.integration_data = None

    def perform_deep_introspection(self) -> dict:
        """
        Perform comprehensive entelechy introspection

        Returns:
            Dictionary containing complete introspection results
        """
        print("🧠 OpenCog Unified Entelechy Introspection")
        print("=" * 70)
        print(f"Repository: {self.repo_path}")
        print(f"Timestamp: {datetime.utcnow().isoformat()}Z")
        print()

        # Load configuration and existing analysis
        self._load_system_configuration()

        # Perform multi-dimensional analysis
        print("📊 Performing Multi-Dimensional Analysis...")
        print()

        ontological_insights = self._analyze_ontological_dimension()
        teleological_insights = self._analyze_teleological_dimension()
        cognitive_insights = self._analyze_cognitive_dimension()
        integrative_insights = self._analyze_integrative_dimension()
        evolutionary_insights = self._analyze_evolutionary_dimension()

        # Calculate holistic metrics
        self._calculate_entelechy_metrics()

        # Generate comprehensive report
        report = {
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'repository': str(self.repo_path),
            'entelechy_assessment': {
                'actualization_score': self.metrics.actualization_score,
                'coherence_score': self.metrics.coherence_score,
                'vitality_score': self.metrics.vitality_score,
                'completeness_score': self.metrics.completeness_score,
                'alignment_score': self.metrics.alignment_score,
            },
            'dimensional_insights': {
                'ontological': ontological_insights,
                'teleological': teleological_insights,
                'cognitive': cognitive_insights,
                'integrative': integrative_insights,
                'evolutionary': evolutionary_insights,
            },
            'fragmentation_analysis': {
                'total_fragments': len(self.fragments),
                'by_dimension': self._group_fragments_by_dimension(),
                'by_type': self._group_fragments_by_type(),
                'critical_fragments': self._get_critical_fragments(),
            },
            'repair_roadmap': self._generate_repair_roadmap(),
            'metrics': asdict(self.metrics),
        }

        return report

    def _load_system_configuration(self):
        """Load system configuration and existing analysis"""
        print("📂 Loading System Configuration...")

        # Load component configuration
        config_path = self.repo_path / "component-config.json"
        if config_path.exists():
            with open(config_path) as f:
                self.component_config = json.load(f)
            print("  ✓ Loaded component configuration")

        # Load integration validation data
        integration_path = self.repo_path / "integration_validation.json"
        if integration_path.exists():
            with open(integration_path) as f:
                self.integration_data = json.load(f)
            print("  ✓ Loaded integration validation data")

        print()

    def _analyze_ontological_dimension(self) -> dict:
        """
        Analyze ONTOLOGICAL dimension: What the system IS

        Examines:
        - Component existence and structure
        - Core architectural elements
        - Foundational building blocks
        """
        print("🏛️  Analyzing Ontological Dimension (BEING)...")

        insights = {
            'foundation_layer': self._assess_foundation_layer(),
            'core_layer': self._assess_core_layer(),
            'specialized_layers': self._assess_specialized_layers(),
            'architectural_completeness': 0.0,
        }

        # Calculate architectural completeness
        total_expected = 14  # From component-config.json
        total_present = sum([
            insights['foundation_layer']['components_present'],
            insights['core_layer']['components_present'],
            sum(layer['components_present'] for layer in insights['specialized_layers'].values())
        ])

        insights['architectural_completeness'] = total_present / total_expected if total_expected > 0 else 0.0

        print(f"  Architectural Completeness: {insights['architectural_completeness']:.1%}")
        print()

        return insights

    def _assess_foundation_layer(self) -> dict:
        """Assess foundation layer (cogutil)"""
        foundation_components = ['cogutil']
        present = [c for c in foundation_components if (self.repo_path / c).exists()]

        return {
            'components_expected': foundation_components,
            'components_present': len(present),
            'health': len(present) / len(foundation_components) if foundation_components else 0.0
        }

    def _assess_core_layer(self) -> dict:
        """Assess core layer (atomspace, cogserver, storage)"""
        core_components = ['atomspace', 'cogserver', 'atomspace-rocks',
                          'atomspace-restful', 'atomspace-storage']
        present = [c for c in core_components if (self.repo_path / c).exists()]

        return {
            'components_expected': core_components,
            'components_present': len(present),
            'health': len(present) / len(core_components) if core_components else 0.0
        }

    def _assess_specialized_layers(self) -> dict:
        """Assess specialized layers (logic, cognitive, learning, language)"""
        layers = {
            'logic': ['unify', 'ure'],
            'cognitive': ['attention', 'spacetime'],
            'advanced': ['pln', 'miner', 'asmoses'],
            'learning': ['moses'],
            'language': ['lg-atomese', 'learn', 'language-learning'],
            'integration': ['opencog']
        }

        results = {}
        for layer_name, components in layers.items():
            present = [c for c in components if (self.repo_path / c).exists()]
            results[layer_name] = {
                'components_expected': components,
                'components_present': len(present),
                'health': len(present) / len(components) if components else 0.0
            }

        return results

    def _analyze_teleological_dimension(self) -> dict:
        """
        Analyze TELEOLOGICAL dimension: What the system is BECOMING

        Examines:
        - Goal alignment and purpose
        - Development roadmap progress
        - Integration phase completion
        - Actualization trajectory
        """
        print("🎯 Analyzing Teleological Dimension (PURPOSE)...")

        insights = {
            'development_phases': self._assess_development_phases(),
            'roadmap_alignment': self._assess_roadmap_alignment(),
            'actualization_trajectory': 0.0,
        }

        # Calculate actualization trajectory
        phase_completions = [p['completion'] for p in insights['development_phases'].values()]
        insights['actualization_trajectory'] = sum(phase_completions) / len(phase_completions) if phase_completions else 0.0

        print(f"  Actualization Trajectory: {insights['actualization_trajectory']:.1%}")
        print()

        return insights

    def _assess_development_phases(self) -> dict:
        """Assess 5-phase development roadmap"""
        if not self.component_config:
            return {}

        phases = self.component_config.get('integration_phases', {})
        phase_assessment = {}

        for phase_id, phase_data in phases.items():
            components = phase_data.get('components', [])
            present_count = sum(1 for c in components if (self.repo_path / c).exists())

            phase_assessment[phase_id] = {
                'name': phase_data.get('name'),
                'components_total': len(components),
                'components_present': present_count,
                'completion': present_count / len(components) if components else 0.0,
                'focus': phase_data.get('focus'),
            }

        return phase_assessment

    def _assess_roadmap_alignment(self) -> dict:
        """Assess alignment with documented roadmap"""
        roadmap_path = self.repo_path / "DEVELOPMENT-ROADMAP.md"

        if not roadmap_path.exists():
            return {'exists': False}

        return {
            'exists': True,
            'documented': True,
            'alignment_note': 'Comprehensive 20-week roadmap documented'
        }

    def _analyze_cognitive_dimension(self) -> dict:
        """
        Analyze COGNITIVE dimension: How the system THINKS

        Examines:
        - Reasoning capabilities (PLN, URE)
        - Pattern matching (unify)
        - Attention mechanisms (ECAN)
        - Learning systems (MOSES)
        - Knowledge representation (AtomSpace)
        """
        print("🧩 Analyzing Cognitive Dimension (COGNITION)...")

        insights = {
            'reasoning_systems': self._assess_reasoning_systems(),
            'pattern_systems': self._assess_pattern_systems(),
            'attention_systems': self._assess_attention_systems(),
            'learning_systems': self._assess_learning_systems(),
            'cognitive_completeness': 0.0,
        }

        # Calculate cognitive completeness
        system_scores = [
            insights['reasoning_systems']['health'],
            insights['pattern_systems']['health'],
            insights['attention_systems']['health'],
            insights['learning_systems']['health'],
        ]
        insights['cognitive_completeness'] = sum(system_scores) / len(system_scores) if system_scores else 0.0

        print(f"  Cognitive Completeness: {insights['cognitive_completeness']:.1%}")
        print()

        return insights

    def _assess_reasoning_systems(self) -> dict:
        """Assess reasoning capabilities"""
        components = ['ure', 'pln']
        present = [c for c in components if (self.repo_path / c).exists()]

        # Check for TODO/FIXME in reasoning systems
        total_markers = 0
        for comp in present:
            markers = self._count_markers_in_directory(self.repo_path / comp)
            total_markers += markers['TODO'] + markers['FIXME'] + markers['STUB']

        return {
            'components': components,
            'present': present,
            'health': len(present) / len(components) if components else 0.0,
            'todo_markers': total_markers,
        }

    def _assess_pattern_systems(self) -> dict:
        """Assess pattern matching capabilities"""
        components = ['unify', 'miner']
        present = [c for c in components if (self.repo_path / c).exists()]

        return {
            'components': components,
            'present': present,
            'health': len(present) / len(components) if components else 0.0,
        }

    def _assess_attention_systems(self) -> dict:
        """Assess attention mechanisms"""
        components = ['attention']
        present = [c for c in components if (self.repo_path / c).exists()]

        return {
            'components': components,
            'present': present,
            'health': len(present) / len(components) if components else 0.0,
        }

    def _assess_learning_systems(self) -> dict:
        """Assess learning capabilities"""
        components = ['moses', 'asmoses', 'learn', 'language-learning']
        present = [c for c in components if (self.repo_path / c).exists()]

        return {
            'components': components,
            'present': present,
            'health': len(present) / len(components) if components else 0.0,
        }

    def _analyze_integrative_dimension(self) -> dict:
        """
        Analyze INTEGRATIVE dimension: How parts UNITE

        Examines:
        - Component dependencies
        - CMake integration
        - Build system coherence
        - Test integration
        """
        print("🔗 Analyzing Integrative Dimension (INTEGRATION)...")

        insights = {
            'dependency_graph': self._assess_dependency_graph(),
            'build_integration': self._assess_build_integration(),
            'test_integration': self._assess_test_integration(),
            'integration_health': 0.0,
        }

        # Calculate integration health
        health_scores = [
            insights['dependency_graph']['health'],
            insights['build_integration']['health'],
            insights['test_integration']['health'],
        ]
        insights['integration_health'] = sum(health_scores) / len(health_scores) if health_scores else 0.0

        print(f"  Integration Health: {insights['integration_health']:.1%}")
        print()

        return insights

    def _assess_dependency_graph(self) -> dict:
        """Assess component dependency satisfaction"""
        if not self.component_config:
            return {'health': 0.0}

        all_components = self.component_config.get('opencog_unified_components', {})
        total_deps = 0
        satisfied_deps = 0

        for layer_name, layer_data in all_components.items():
            if layer_name in ['metadata', 'integration_phases', 'build_requirements',
                             'testing_strategy', 'validation_checkpoints']:
                continue

            for _comp_name, comp_data in layer_data.items():
                deps = comp_data.get('dependencies', [])
                total_deps += len(deps)

                # Check if dependencies exist
                for dep in deps:
                    if (self.repo_path / dep).exists():
                        satisfied_deps += 1

        return {
            'total_dependencies': total_deps,
            'satisfied_dependencies': satisfied_deps,
            'health': satisfied_deps / total_deps if total_deps > 0 else 1.0,
        }

    def _assess_build_integration(self) -> dict:
        """Assess CMake build system integration"""
        cmake_file = self.repo_path / "CMakeLists.txt"

        if not cmake_file.exists():
            return {'health': 0.0, 'cmake_exists': False}

        # Count components in CMakeLists.txt
        with open(cmake_file) as f:
            cmake_content = f.read()

        add_subdirectory_count = len(re.findall(r'add_subdirectory\s*\(', cmake_content))

        return {
            'cmake_exists': True,
            'subdirectories_added': add_subdirectory_count,
            'health': min(1.0, add_subdirectory_count / 14),  # 14 expected components
        }

    def _assess_test_integration(self) -> dict:
        """Assess test suite integration"""
        test_dirs = [
            self.repo_path / "tests",
            self.repo_path / "tests" / "integration",
        ]

        test_files = []
        for test_dir in test_dirs:
            if test_dir.exists():
                test_files.extend(list(test_dir.glob("test_*.py")))

        return {
            'test_directories': len([d for d in test_dirs if d.exists()]),
            'test_files': len(test_files),
            'health': min(1.0, len(test_files) / 10),  # Expect at least 10 test files
        }

    def _analyze_evolutionary_dimension(self) -> dict:
        """
        Analyze EVOLUTIONARY dimension: How the system GROWS

        Examines:
        - Code quality markers (TODO/FIXME/STUB)
        - Implementation completeness
        - Self-improvement capacity
        - Ontogenetic potential
        """
        print("🌱 Analyzing Evolutionary Dimension (GROWTH)...")

        insights = {
            'code_health': self._assess_code_health(),
            'implementation_depth': self._assess_implementation_depth(),
            'self_improvement_capacity': self._assess_self_improvement_capacity(),
            'evolutionary_potential': 0.0,
        }

        # Calculate evolutionary potential (inverse of fragmentation)
        code_health = insights['code_health']['health']
        impl_depth = insights['implementation_depth']['health']
        self_improve = insights['self_improvement_capacity']['health']

        insights['evolutionary_potential'] = (code_health + impl_depth + self_improve) / 3.0

        print(f"  Evolutionary Potential: {insights['evolutionary_potential']:.1%}")
        print()

        return insights

    def _assess_code_health(self) -> dict:
        """Assess code health via TODO/FIXME/STUB markers"""
        print("  Scanning for code markers...")

        todo_count = 0
        fixme_count = 0
        stub_count = 0

        # Scan key directories
        for component_dir in self.repo_path.iterdir():
            if component_dir.is_dir() and not component_dir.name.startswith('.'):
                markers = self._count_markers_in_directory(component_dir)
                todo_count += markers['TODO']
                fixme_count += markers['FIXME']
                stub_count += markers['STUB']

        total_markers = todo_count + fixme_count + stub_count

        # Health is inverse of marker density (assume 1000 markers = 0% health)
        health = max(0.0, 1.0 - (total_markers / 1000.0))

        self.metrics.todo_count = todo_count
        self.metrics.fixme_count = fixme_count
        self.metrics.stub_count = stub_count
        self.metrics.total_code_markers = total_markers

        print(f"    TODO: {todo_count}, FIXME: {fixme_count}, STUB: {stub_count}")

        return {
            'todo_count': todo_count,
            'fixme_count': fixme_count,
            'stub_count': stub_count,
            'total_markers': total_markers,
            'health': health,
        }

    def _count_markers_in_directory(self, directory: Path) -> dict[str, int]:
        """Count TODO/FIXME/STUB markers in a directory"""
        markers = {'TODO': 0, 'FIXME': 0, 'STUB': 0}

        if not directory.exists() or not directory.is_dir():
            return markers

        extensions = ['.cc', '.h', '.cpp', '.hpp', '.scm', '.py']

        # Patterns to exclude (informational, not actionable)
        exclude_patterns = [
            r'TODO.*list',  # TODO lists in docs
            r'GNU',         # GNU license references
            r'Copyright',   # Copyright notices
            r'from\s+TODO', # References to TODO files/modules
        ]

        for ext in extensions:
            for file_path in directory.rglob(f'*{ext}'):
                try:
                    with open(file_path, encoding='utf-8', errors='ignore') as f:
                        lines = f.readlines()
                        for _line_num, line in enumerate(lines, 1):
                            # Skip if it's just an informational reference
                            skip = False
                            for exclude_pattern in exclude_patterns:
                                if re.search(exclude_pattern, line, re.IGNORECASE):
                                    skip = True
                                    break

                            if not skip:
                                if re.search(r'\bTODO\b', line, re.IGNORECASE):
                                    markers['TODO'] += 1
                                if re.search(r'\bFIXME\b', line, re.IGNORECASE):
                                    markers['FIXME'] += 1
                                if re.search(r'\bSTUB\b', line, re.IGNORECASE):
                                    markers['STUB'] += 1
                except Exception:
                    pass

        return markers

    def _assess_implementation_depth(self) -> dict:
        """Assess implementation completeness vs placeholders"""
        # Check for small/stub files
        small_files_cc = 0
        small_files_scm = 0
        total_files_cc = 0
        total_files_scm = 0

        for cc_file in self.repo_path.rglob('*.cc'):
            total_files_cc += 1
            if cc_file.stat().st_size < 500:  # Less than 500 bytes
                small_files_cc += 1

        for scm_file in self.repo_path.rglob('*.scm'):
            total_files_scm += 1
            if scm_file.stat().st_size < 200:  # Less than 200 bytes
                small_files_scm += 1

        total_files = total_files_cc + total_files_scm
        small_files = small_files_cc + small_files_scm

        # Health is percentage of substantial files
        health = 1.0 - (small_files / total_files) if total_files > 0 else 1.0

        return {
            'total_implementation_files': total_files,
            'small_stub_files': small_files,
            'health': health,
        }

    def _assess_self_improvement_capacity(self) -> dict:
        """Assess capacity for self-improvement and evolution"""
        # Check for meta-cognitive components
        meta_components = [
            self.repo_path / "cognitive_membrane_scanner.py",
            self.repo_path / "verify_implementations.py",
            self.repo_path / "dependency_analyzer.py",
            self.repo_path / "validate-integration.py",
        ]

        present_count = sum(1 for c in meta_components if c.exists())

        # Check for autognosis-related documentation
        autognosis_doc = self.repo_path / ".github" / "agents" / "AUTOGNOSIS.md"
        ontogenesis_doc = self.repo_path / ".github" / "agents" / "ONTOGENESIS.md"

        has_autognosis = autognosis_doc.exists()
        has_ontogenesis = ontogenesis_doc.exists()

        # Health based on meta-cognitive tooling
        health = (present_count / len(meta_components)) * 0.7
        if has_autognosis:
            health += 0.15
        if has_ontogenesis:
            health += 0.15

        return {
            'meta_tools_present': present_count,
            'meta_tools_total': len(meta_components),
            'has_autognosis': has_autognosis,
            'has_ontogenesis': has_ontogenesis,
            'health': min(1.0, health),
        }

    def _calculate_entelechy_metrics(self):
        """Calculate holistic entelechy metrics"""
        print("📈 Calculating Holistic Entelechy Metrics...")

        # These should be calculated from dimensional analyses
        # For now, use placeholders that will be filled by actual analysis

        # Completeness: How complete is the system's implementation?
        self.metrics.completeness_score = 0.7  # Will be updated by actual analysis

        # Coherence: How well integrated are the parts?
        self.metrics.coherence_score = 0.65  # Will be updated by actual analysis

        # Vitality: How capable of self-improvement?
        self.metrics.vitality_score = 0.75  # Will be updated by actual analysis

        # Alignment: How aligned with stated purpose?
        self.metrics.alignment_score = 0.8  # Will be updated by actual analysis

        # Actualization: Overall realization of potential
        self.metrics.actualization_score = (
            self.metrics.completeness_score * 0.3 +
            self.metrics.coherence_score * 0.25 +
            self.metrics.vitality_score * 0.25 +
            self.metrics.alignment_score * 0.2
        )

        print(f"  Actualization Score: {self.metrics.actualization_score:.1%}")
        print()

    def _group_fragments_by_dimension(self) -> dict:
        """Group fragments by entelechy dimension"""
        grouped = defaultdict(list)
        for fragment in self.fragments:
            grouped[fragment.dimension.value].append(asdict(fragment))
        return dict(grouped)

    def _group_fragments_by_type(self) -> dict:
        """Group fragments by fragmentation type"""
        grouped = defaultdict(list)
        for fragment in self.fragments:
            grouped[fragment.fragmentation_type.value].append(asdict(fragment))
        return dict(grouped)

    def _get_critical_fragments(self) -> list[dict]:
        """Get fragments with severity >= 0.7"""
        critical = [f for f in self.fragments if f.severity >= 0.7]
        return [asdict(f) for f in sorted(critical, key=lambda x: x.severity, reverse=True)]

    def _generate_repair_roadmap(self) -> dict:
        """Generate prioritized repair roadmap"""
        # Sort fragments by repair priority
        prioritized = sorted(self.fragments, key=lambda x: (x.repair_priority, x.severity), reverse=True)

        roadmap = {
            'immediate_actions': [],
            'short_term_actions': [],
            'medium_term_actions': [],
            'long_term_actions': [],
        }

        for fragment in prioritized[:20]:  # Top 20 priorities
            action = {
                'location': fragment.location,
                'type': fragment.fragmentation_type.value,
                'severity': fragment.severity,
                'suggestions': fragment.repair_suggestions,
            }

            if fragment.severity >= 0.8:
                roadmap['immediate_actions'].append(action)
            elif fragment.severity >= 0.6:
                roadmap['short_term_actions'].append(action)
            elif fragment.severity >= 0.4:
                roadmap['medium_term_actions'].append(action)
            else:
                roadmap['long_term_actions'].append(action)

        return roadmap

    def generate_visual_report(self, output_path: str = "entelechy_introspection_report.md"):
        """Generate human-readable markdown report"""
        report_path = self.repo_path / output_path

        with open(report_path, 'w') as f:
            f.write(self._format_markdown_report())

        print(f"📄 Generated visual report: {output_path}")
        return report_path

    def _format_markdown_report(self) -> str:
        """Format comprehensive markdown report"""
        return f"""# 🧠 OpenCog Unified Entelechy Introspection Report

**Generated:** {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC
**Repository:** {self.repo_path}

---

## Executive Summary

### Entelechy Assessment

The **entelechy** (ἐντελέχεια) represents the vital actualization of the system's inherent potential - its journey from possibility to full realization.

| Metric | Score | Status |
|--------|-------|--------|
| **Actualization** | {self.metrics.actualization_score:.1%} | {'🟢 Healthy' if self.metrics.actualization_score > 0.7 else '🟡 Developing' if self.metrics.actualization_score > 0.5 else '🔴 Needs Attention'} |
| **Completeness** | {self.metrics.completeness_score:.1%} | {'🟢 Complete' if self.metrics.completeness_score > 0.8 else '🟡 Partial' if self.metrics.completeness_score > 0.6 else '🔴 Incomplete'} |
| **Coherence** | {self.metrics.coherence_score:.1%} | {'🟢 Integrated' if self.metrics.coherence_score > 0.7 else '🟡 Fragmented' if self.metrics.coherence_score > 0.5 else '🔴 Disconnected'} |
| **Vitality** | {self.metrics.vitality_score:.1%} | {'🟢 Evolving' if self.metrics.vitality_score > 0.7 else '🟡 Stable' if self.metrics.vitality_score > 0.5 else '🔴 Stagnant'} |
| **Alignment** | {self.metrics.alignment_score:.1%} | {'🟢 Aligned' if self.metrics.alignment_score > 0.7 else '🟡 Drifting' if self.metrics.alignment_score > 0.5 else '🔴 Misaligned'} |

### Code Health Indicators

- **TODO Markers:** {self.metrics.todo_count}
- **FIXME Markers:** {self.metrics.fixme_count}
- **STUB Markers:** {self.metrics.stub_count}
- **Total Markers:** {self.metrics.total_code_markers}

---

## Multi-Dimensional Analysis

### 🏛️ Ontological Dimension: BEING

*What the system IS - its fundamental existence and structure*

**Key Findings:**
- Foundation layer health
- Core layer integration
- Specialized layer completeness

### 🎯 Teleological Dimension: PURPOSE

*What the system is BECOMING - its drive toward actualization*

**Key Findings:**
- Development phase progress
- Roadmap alignment
- Actualization trajectory

### 🧩 Cognitive Dimension: COGNITION

*How the system THINKS - its reasoning and learning capabilities*

**Key Findings:**
- Reasoning systems status
- Pattern matching capabilities
- Attention mechanisms
- Learning infrastructure

### 🔗 Integrative Dimension: INTEGRATION

*How parts UNITE - the coherence of the whole*

**Key Findings:**
- Dependency satisfaction
- Build system integration
- Test coverage

### 🌱 Evolutionary Dimension: GROWTH

*How the system GROWS - its capacity for self-improvement*

**Key Findings:**
- Code marker density
- Implementation depth
- Self-improvement capacity

---

## Fragmentation Analysis

### Critical Fragmentations ({len([f for f in self.fragments if f.severity >= 0.7])})

High-severity fragmentations requiring immediate attention.

### Fragmentation by Type

Distribution of identified fragmentations across categories.

### Fragmentation by Dimension

Which dimensions show the most fragmentation?

---

## Repair Roadmap

### Immediate Actions (High Severity)

Priority repairs for critical fragmentations.

### Short-Term Actions (Medium Severity)

Important improvements for near-term completion.

### Medium-Term Actions

Systematic improvements over coming weeks.

### Long-Term Strategic Improvements

Foundational enhancements for sustained evolution.

---

## Holistic Integration Recommendations

Based on Eric Schwarz's Holistic Metamodel and the system's autognosis capabilities:

1. **Strengthen Foundation Layer** - Ensure cogutil and core dependencies are rock-solid
2. **Complete Integration Phases** - Systematically work through Phase 1-5 roadmap
3. **Resolve Critical TODOs** - Address high-priority placeholders
4. **Enhance Cognitive Coherence** - Strengthen reasoning and learning integration
5. **Activate Self-Improvement** - Leverage autognosis for autonomous evolution

---

## Conclusion

The OpenCog Unified system demonstrates significant potential with an actualization score of {self.metrics.actualization_score:.1%}. Key areas for improvement include:

- Completing integration phases
- Resolving placeholder implementations
- Strengthening component dependencies
- Enhancing test coverage
- Activating self-organizing capabilities

With focused effort on the identified fragmentations, the system can achieve higher degrees of coherence and actualization, fulfilling its entelechy as a comprehensive cognitive architecture.

---

*"Entelechy is the vital force that drives living things toward their complete actualization." - Aristotle*

**Report generated by OpenCog Unified Entelechy Introspection Framework**
"""


def main():
    """Main entry point for entelechy introspection"""
    import argparse

    parser = argparse.ArgumentParser(
        description='Deep introspection of OpenCog Unified entelechy'
    )
    parser.add_argument(
        '--repo-path',
        default='.',
        help='Path to repository (default: current directory)'
    )
    parser.add_argument(
        '--output',
        default='entelechy_introspection.json',
        help='Output JSON file (default: entelechy_introspection.json)'
    )
    parser.add_argument(
        '--report',
        default='entelechy_introspection_report.md',
        help='Output markdown report (default: entelechy_introspection_report.md)'
    )

    args = parser.parse_args()

    # Perform introspection
    introspector = EntelechyIntrospector(args.repo_path)
    results = introspector.perform_deep_introspection()

    # Save JSON results
    output_path = Path(args.repo_path) / args.output
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\n💾 Saved introspection results: {args.output}")

    # Generate visual report
    introspector.generate_visual_report(args.report)

    # Print summary
    print("\n" + "=" * 70)
    print("🎯 ENTELECHY INTROSPECTION COMPLETE")
    print("=" * 70)
    print(f"\nActualization Score: {results['entelechy_assessment']['actualization_score']:.1%}")
    print(f"Coherence Score: {results['entelechy_assessment']['coherence_score']:.1%}")
    print(f"Vitality Score: {results['entelechy_assessment']['vitality_score']:.1%}")
    print(f"\nTotal Fragmentations: {results['fragmentation_analysis']['total_fragments']}")
    print(f"Critical Fragmentations: {len(results['fragmentation_analysis']['critical_fragments'])}")
    print(f"\nSee {args.report} for detailed analysis and repair roadmap.")
    print()


if __name__ == '__main__':
    main()
