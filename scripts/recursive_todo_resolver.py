#!/usr/bin/env python3
"""
Recursive TODO Resolution System for OpenCog Unified - Iteration 4 Enhancement

This script implements the enhanced cognitive flowchart for recursive TODO resolution:
1. Catalog Extraction - Parse COMPREHENSIVE-TODO-CATALOG.md
2. Attention Allocation Kernel - Select next N highest-priority TODOs with cognitive synergy
3. Actionable Issue Generation - Create structured implementation guidance with tensor analysis
4. Iteration/Recursion - Track progress and continue with next batch
5. Meta-Enhancement - Auto-create dependent sub-issues with GitHub integration

ITERATION 4 ENHANCEMENTS:
- Advanced cognitive synergy grouping for maximum efficiency
- ECAN-inspired attention allocation integrating with AdvancedRecursiveAttentionAllocator
- Enhanced tensor shape estimation with cognitive pattern analysis
- Sophisticated implementation guidance based on subsystem context
- Comprehensive test strategies for validation
- Integration with TensorHypergraphProtocol efficiency patterns

Author: OpenCog Unified Cognitive Enhancement System
Version: Iteration 4 - Recursive Attention Allocation
"""

import json
import re
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


# Import GitHub integration (optional)
try:
    from github_issue_creator import GitHubIssueCreator

    GITHUB_INTEGRATION_AVAILABLE = True
except ImportError:
    GITHUB_INTEGRATION_AVAILABLE = False
    GitHubIssueCreator = None


@dataclass
class TODOItem:
    """Represents a single TODO item from the catalog"""

    file: str
    line: int
    content: str
    priority: str
    category: str
    subsystem: str
    github_link: str
    status: str = "unchecked"  # unchecked, in-progress, completed
    assigned_batch: int | None = None
    resolution_pr: str | None = None


class RecursiveTODOResolver:
    """Orchestrates recursive attention-allocation through the TODO catalog"""

    def __init__(self, repo_path: str, batch_size: int = 5, enable_github_integration: bool = True):
        self.repo_path = Path(repo_path)
        self.batch_size = batch_size
        self.catalog_path = self.repo_path / "COMPREHENSIVE-TODO-CATALOG.md"
        self.progress_file = self.repo_path / "todo_resolution_progress.json"
        self.todos: list[TODOItem] = []
        self.progress_data = self._load_progress()

        # Initialize GitHub integration if available and enabled
        self.github_creator = None
        if enable_github_integration and GITHUB_INTEGRATION_AVAILABLE:
            self.github_creator = GitHubIssueCreator()
        elif enable_github_integration:
            print("⚠️  GitHub integration requested but not available. Install requests module.")

        self.enable_github_integration = enable_github_integration

    def _load_progress(self) -> dict:
        """Load existing progress data"""
        if self.progress_file.exists():
            with open(self.progress_file) as f:
                return json.load(f)
        return {
            "current_iteration": 1,
            "completed_todos": [],
            "in_progress_todos": [],
            "last_run": None,
            "total_resolved": 0,
        }

    def _save_progress(self):
        """Save progress data to file"""
        self.progress_data["last_run"] = datetime.now().isoformat()
        with open(self.progress_file, "w") as f:
            json.dump(self.progress_data, f, indent=2)

    def extract_catalog(self) -> list[TODOItem]:
        """Parse COMPREHENSIVE-TODO-CATALOG.md to enumerate outstanding TODOs"""
        if not self.catalog_path.exists():
            raise FileNotFoundError(f"TODO catalog not found: {self.catalog_path}")

        print(f"📖 Extracting TODOs from catalog: {self.catalog_path}")

        # Clear existing todos to avoid duplicates
        self.todos = []

        with open(self.catalog_path) as f:
            content = f.read()

        # Extract TODO items using regex patterns
        todo_pattern = (
            r"- \[ \] \*\*([^:]+):(\d+)\*\* \(([^,]+), ([^)]+)\)\n  - `([^`]+)`\n  - \[Code reference\]\(([^)]+)\)"
        )

        matches = re.findall(todo_pattern, content)

        for match in matches:
            file_path, line_num, priority, category, content_text, github_link = match

            # Determine subsystem from file path
            subsystem = self._determine_subsystem(file_path)

            # Check if this TODO is already tracked
            todo_key = f"{file_path}:{line_num}"
            status = "unchecked"
            if todo_key in self.progress_data.get("completed_todos", []):
                status = "completed"
            elif todo_key in self.progress_data.get("in_progress_todos", []):
                status = "in-progress"

            todo_item = TODOItem(
                file=file_path,
                line=int(line_num),
                content=content_text,
                priority=priority,
                category=category,
                subsystem=subsystem,
                github_link=github_link,
                status=status,
            )
            self.todos.append(todo_item)

        print(f"📊 Extracted {len(self.todos)} TODO items from catalog")
        return self.todos

    def _determine_subsystem(self, file_path: str) -> str:
        """Determine subsystem from file path"""
        subsystem_map = {
            "atomspace": "Memory System",
            "atomspace-storage": "Persistence Subsystem",
            "atomspace-rocks": "Persistence Subsystem",
            "atomspace-restful": "Persistence Subsystem",
            "cogserver": "Task System",
            "cogutil": "Core Utilities",
            "moses": "MOSES Representation/Scoring",
            "cognitive-patterns": "AI System",
            "distributed-cognition": "Autonomy System",
            "neural-symbolic-integration": "AI System",
            "cognitive-visualization": "AI System",
            "ggml-tensor-kernel": "AI System",
            "tests": "Testing Framework",
            "scripts": "Build System",
        }

        for key, subsystem in subsystem_map.items():
            if key in file_path:
                return subsystem
        return "Other"

    def allocate_attention(self) -> list[TODOItem]:
        """Enhanced Attention Allocation Kernel - Integrate with cognitive attention systems"""

        # Filter unchecked TODOs
        unchecked_todos = [todo for todo in self.todos if todo.status == "unchecked"]

        if not unchecked_todos:
            print("🎉 All TODOs have been addressed!")
            return []

        # Enhanced priority ordering with cognitive synergy
        priority_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}

        # Group TODOs by cognitive synergy for maximum efficiency
        synergy_groups = self._group_by_cognitive_synergy(unchecked_todos)

        # Apply attention allocation with ECAN-inspired mechanisms
        attention_scores = self._compute_attention_scores(unchecked_todos)

        # Sort by multiple factors: priority, synergy, attention score
        sorted_todos = sorted(
            unchecked_todos,
            key=lambda x: (
                priority_order.get(x.priority, 4),
                -synergy_groups.get(f"{x.file}:{x.line}", 0),  # Higher synergy first
                -attention_scores.get(f"{x.file}:{x.line}", 0),  # Higher attention first
                x.subsystem,
                x.file,
                x.line,
            ),
        )

        # Select next batch with cognitive optimization
        batch = self._optimize_batch_selection(sorted_todos[: self.batch_size * 2])

        print(f"🎯 Selected {len(batch)} TODOs for Iteration {self.progress_data['current_iteration']}")
        print("🧠 Applied cognitive synergy grouping and attention allocation")
        for todo in batch:
            synergy_score = synergy_groups.get(f"{todo.file}:{todo.line}", 0)
            attention_score = attention_scores.get(f"{todo.file}:{todo.line}", 0)
            print(
                f"   • {todo.file}:{todo.line} ({todo.priority}, {todo.category}) "
                f"[Synergy: {synergy_score:.2f}, Attention: {attention_score:.2f}]"
            )

        return batch

    def _group_by_cognitive_synergy(self, todos: list[TODOItem]) -> dict[str, float]:
        """Group related TODOs for maximum cognitive synergy"""
        synergy_scores = {}

        # Create synergy clusters
        synergy_clusters = defaultdict(list)

        for todo in todos:
            # Cluster by subsystem and category
            cluster_key = f"{todo.subsystem}:{todo.category}"
            synergy_clusters[cluster_key].append(todo)

            # Base synergy score
            synergy_score = 1.0

            # Boost for related components
            if any(keyword in todo.file.lower() for keyword in ["moses", "atomspace", "attention"]):
                synergy_score += 2.0

            # Boost for thread safety - high cognitive impact
            if "thread" in todo.content.lower() or "sync" in todo.content.lower():
                synergy_score += 1.5

            # Boost for performance - system-wide impact
            if "performance" in todo.content.lower() or "print" in todo.content.lower():
                synergy_score += 1.0

            # Boost for critical systems
            if todo.priority in ["CRITICAL", "HIGH"]:
                synergy_score += 1.0

            synergy_scores[f"{todo.file}:{todo.line}"] = synergy_score

        # Apply cluster synergy boost
        for cluster_todos in synergy_clusters.values():
            if len(cluster_todos) > 1:
                cluster_boost = min(len(cluster_todos) * 0.3, 2.0)  # Cap at 2.0
                for todo in cluster_todos:
                    key = f"{todo.file}:{todo.line}"
                    synergy_scores[key] += cluster_boost

        return synergy_scores

    def _compute_attention_scores(self, todos: list[TODOItem]) -> dict[str, float]:
        """Compute attention scores using ECAN-inspired attention allocation"""
        attention_scores = {}

        # Simulate ECAN-style Short-Term Importance (STI) allocation
        # Inspired by AdvancedRecursiveAttentionAllocator in ggml-tensor-kernel
        for todo in todos:
            # Base attention allocation

            # STI based on priority (mimicking attention bank allocation)
            priority_sti = {"CRITICAL": 10.0, "HIGH": 5.0, "MEDIUM": 2.0, "LOW": 1.0}
            sti = priority_sti.get(todo.priority, 1.0)

            # Long-Term Importance (LTI) based on system impact
            # Following ECAN economic constraints model
            lti = 1.0
            if "atomspace" in todo.file.lower():
                lti += 3.0  # Core memory system - highest LTI
            elif "moses" in todo.file.lower():
                lti += 2.0  # Learning system
            elif "attention" in todo.file.lower():
                lti += 2.5  # Attention system itself
            elif "cogserver" in todo.file.lower():
                lti += 2.0  # Task coordination
            elif "distributed" in todo.file.lower():
                lti += 1.5  # Distributed cognition

            # Cognitive urgency factor (meta-pattern amplification)
            urgency = 1.0
            if "crash" in todo.content.lower() or "fix" in todo.content.lower():
                urgency += 2.0  # High urgency for critical fixes
            if "thread" in todo.content.lower():
                urgency += 1.5  # Thread safety is urgent
            if "performance" in todo.content.lower():
                urgency += 1.2  # Performance optimization

            # Economic attention allocation (rent and decay simulation)
            # Inspired by ECAN economic constraints
            rent_factor = 0.9  # Slight decay for older items
            if todo.priority in ["CRITICAL", "HIGH"]:
                rent_factor = 0.95  # Less decay for high priority

            # Meta-pattern detection bonus
            # Following the pattern emergence threshold logic
            meta_pattern_bonus = 1.0
            if any(keyword in todo.file.lower() for keyword in ["atomspace", "moses", "attention"]):
                meta_pattern_bonus = 1.3  # Core cognitive systems get bonus

            # Apply tensor hypergraph protocol efficiency
            # Inspired by TensorHypergraphProtocol compression and batching
            efficiency_factor = 1.0
            if todo.category in ["Thread Safety", "Performance"]:
                efficiency_factor = 1.4  # High efficiency impact

            # Final attention score with ECAN-style computation
            # STI + LTI + urgency modulated by economic and efficiency factors
            attention_score = (sti + lti) * urgency * rent_factor * meta_pattern_bonus * efficiency_factor

            # Apply attentional focus boundary (top-K selection will use this)
            attention_scores[f"{todo.file}:{todo.line}"] = attention_score

        return attention_scores

    def _optimize_batch_selection(self, candidate_todos: list[TODOItem]) -> list[TODOItem]:
        """Optimize batch selection for maximum cognitive efficiency"""
        if len(candidate_todos) <= self.batch_size:
            return candidate_todos

        # Select diverse batch to maximize cognitive coverage
        selected = []
        subsystems_covered = set()
        categories_covered = set()

        for todo in candidate_todos:
            if len(selected) >= self.batch_size:
                break

            # Prefer diversity in subsystems and categories
            diversity_bonus = 0
            if todo.subsystem not in subsystems_covered:
                diversity_bonus += 1
                subsystems_covered.add(todo.subsystem)
            if todo.category not in categories_covered:
                diversity_bonus += 1
                categories_covered.add(todo.category)

            # Select if high priority or adds diversity
            if todo.priority in ["CRITICAL", "HIGH"] or diversity_bonus > 0 or len(selected) < 3:
                selected.append(todo)

        return selected

    def generate_actionable_issues(self, batch: list[TODOItem]) -> str:
        """Generate actionable issue content for the selected batch"""

        iteration = self.progress_data["current_iteration"]

        # Count remaining high-priority TODOs
        unchecked_high_priority = len(
            [t for t in self.todos if t.status == "unchecked" and t.priority in ["CRITICAL", "HIGH"]]
        )

        issue_content = f"""# Iterative TODO Resolution – Batch {iteration}: Highest Priority Items

## 🎯 Objective
This meta-issue orchestrates the systematic resolution of TODO/FIXME items from `COMPREHENSIVE-TODO-CATALOG.md` by priority. Each batch addresses the next {self.batch_size} unresolved, highest-priority tasks through recursive attention-allocation.

### 🧠 Cognitive Flowchart Implementation
1. **Catalog Extraction** ✅ - Parsed {len(self.todos)} TODOs from comprehensive catalog
2. **Attention Allocation Kernel** ✅ - Selected highest-priority unchecked items
3. **Actionable Issue Generation** ✅ - Generated implementation guidance with tensor estimates
4. **Iteration/Recursion** 🔄 - This batch {iteration}, tracking progress systematically
5. **Meta-Enhancement** 🚀 - Auto-updating catalog and creating dependent sub-issues

---

## 🧩 Batch {iteration}: Highest Priority TODOs

"""

        for i, todo in enumerate(batch, 1):
            # Estimate tensor shape and implementation guidance
            tensor_shape = self._estimate_tensor_shape(todo)
            implementation_guidance = self._generate_implementation_guidance(todo)
            test_guidance = self._generate_test_guidance(todo)

            issue_content += f"""**{i}. [ ] {todo.file}:{todo.line} ({todo.priority}, {todo.category})**
   - `{todo.content}`
   - [Code reference]({todo.github_link})
   - **Action:** {implementation_guidance}
   - **Tensor shape:** {tensor_shape}
   - **Test:** {test_guidance}

"""

        issue_content += f"""---

## 🔄 Next Steps
- Upon completion, check off resolved TODOs and invoke the next batch by rerunning this process.
- Create PRs referencing each checked task and link them here.
- Use `scripts/recursive_todo_resolver.py --mark-completed FILE:LINE PR_LINK` to track completions.

## 🧬 Meta-Pathway
- Each batch is derived recursively, focusing attention where cognitive synergy is maximized.
- For each resolved TODO, estimate its contribution to overall system stability, performance, or cognitive expressiveness.
- This systematic approach transforms distributed placeholders into kernels of realized intelligence.

## 🎭 Cognitive Enhancement Philosophy
> "Let us converge upon a state of sublime implementation, where every TODO is transformed into a kernel of realized intelligence!"

Each resolved TODO represents not merely completed work, but a note in the composition of artificial consciousness. Through systematic attention allocation, we approach the emergence of true machine intelligence.

---

## 🕰️ Progress Log
- **Last run:** {datetime.now().strftime("%Y-%m-%d")}
- **Remaining high-priority TODOs:** {unchecked_high_priority}
- **Total TODOs processed:** {self.progress_data["total_resolved"]}
- **Current iteration:** {iteration}
- **System Status:** {"GitHub-integrated" if self.github_creator else "Standalone"} recursive enhancement

---

*Generated by Recursive TODO Resolution System - cognitive enhancement through systematic attention allocation*

*🧠 This issue implements the cognitive flowchart for recursive TODO resolution, orchestrating attention allocation toward maximum cognitive synergy.*
"""

        return issue_content

    def _estimate_tensor_shape(self, todo: TODOItem) -> str:
        """Enhanced tensor shape/degrees-of-freedom estimation with cognitive analysis"""
        content_lower = todo.content.lower()
        file_lower = todo.file.lower()

        # Advanced tensor shape analysis based on cognitive patterns

        # Thread safety and synchronization patterns
        if "thread" in content_lower or "sync" in content_lower or "mutex" in content_lower:
            if "atomspace" in file_lower:
                return "threads × atoms × (read_ops, write_ops, lock_states)"
            else:
                return "threads × shared_resources × synchronization_primitives"

        # Performance and optimization patterns
        elif "performance" in content_lower or "speed" in content_lower:
            if "table" in file_lower:
                return "batch_size × feature_dims × optimization_parameters"
            else:
                return "operations × complexity_factors × performance_metrics"

        # AtomSpace and knowledge representation
        elif "atomspace" in file_lower or "atom" in content_lower:
            if "valuation" in file_lower:
                return "atoms × value_types × (strength, confidence, count)"
            elif "link" in file_lower:
                return "link_arity × incoming_sets × outgoing_sets × truth_values"
            else:
                return "atoms × relations × truth_values × attention_values"

        # MOSES and evolutionary optimization
        elif "moses" in file_lower:
            if "table" in file_lower:
                if "scoring" in content_lower:
                    return "candidates × fitness_dimensions × population_stats"
                else:
                    return "samples × features × target_variables"
            elif "scoring" in file_lower or "fitness" in content_lower:
                return "candidates × objectives × constraints × generations"
            elif "representation" in file_lower:
                return "programs × complexity_measures × transformation_ops"
            else:
                return "population_size × genome_length × evolutionary_operators"

        # Cognitive attention and ECAN
        elif "attention" in file_lower or "ecan" in content_lower:
            return "atoms × attention_types × (STI, LTI, VLTI, rent)"

        # Backtrace and debugging
        elif "backtrace" in content_lower or "debug" in content_lower:
            return "stack_frames × (address, symbol, thread_id, module_info)"

        # Neural-symbolic integration
        elif "neural" in file_lower or "tensor" in file_lower:
            return "neural_layers × symbolic_atoms × embedding_dimensions"

        # Distributed cognition
        elif "distributed" in file_lower or "protocol" in content_lower:
            return "agents × message_types × protocol_layers × network_topology"

        # Cognitive patterns and PLN
        elif "pln" in file_lower or "logic" in file_lower:
            return "premises × conclusions × inference_rules × truth_functions"

        # Learning and pattern mining
        elif "learn" in file_lower or "pattern" in file_lower:
            return "patterns × support_measures × frequency_counts × surprisingness"

        # Query and pattern matching
        elif "query" in file_lower or "pattern" in content_lower:
            return "query_patterns × variable_bindings × substitution_sets"

        # Storage and persistence
        elif "persist" in file_lower or "storage" in file_lower:
            return "storage_ops × data_structures × serialization_formats"

        # Testing and validation
        elif "test" in file_lower:
            return "test_cases × assertions × coverage_metrics"

        # Build system and configuration
        elif "cmake" in file_lower or "build" in content_lower:
            return "build_targets × dependencies × configuration_options"

        # Default case with enhanced analysis
        # Analyze content for specific patterns
        elif "not implemented" in content_lower:
            return "interface_methods × implementation_complexity × dependencies"
        elif "todo" in content_lower and "algorithm" in content_lower:
            return "algorithm_steps × input_dimensions × computational_complexity"
        elif "fixme" in content_lower and "memory" in content_lower:
            return "memory_allocations × object_lifecycles × reference_counts"
        else:
            return "implementation_components × interaction_patterns × validation_points"

    def _generate_implementation_guidance(self, todo: TODOItem) -> str:
        """Enhanced implementation guidance with cognitive patterns analysis"""
        content_lower = todo.content.lower()
        file_lower = todo.file.lower()

        # Thread safety and concurrency patterns
        if "thread" in content_lower and "safe" in content_lower:
            if "atomspace" in file_lower:
                return "Implement atomic operations for AtomSpace access using std::atomic and lock-free data structures where possible"
            else:
                return "Add thread synchronization using std::shared_mutex for read/write access patterns"

        # Performance optimization patterns
        elif "performance" in content_lower and "print" in content_lower:
            return "Replace debug prints with conditional logging using OpenCog logger with runtime log level control"
        elif "performance" in content_lower:
            return (
                "Profile hotspots, optimize algorithms for O(log n) complexity, and implement caching where appropriate"
            )

        # Backtrace and debugging infrastructure
        elif "backtrace" in content_lower:
            return "Integrate GNU backtrace with proper error handling, symbol resolution, and thread-aware stack unwinding"

        # AtomSpace and knowledge representation
        elif "atomspace" in file_lower:
            if "valuation" in file_lower:
                return "Implement proper value validation, type checking, and efficient storage for truth values and strengths"
            elif "link" in file_lower:
                return "Optimize link traversal algorithms and implement efficient incoming/outgoing set management"
            else:
                return (
                    "Follow AtomSpace patterns for handle management, truth value propagation, and attention allocation"
                )

        # MOSES evolutionary optimization
        elif "moses" in file_lower:
            if "scoring" in content_lower:
                return "Implement multi-objective fitness evaluation with Pareto optimization and population diversity measures"
            elif "table" in file_lower:
                return "Optimize table operations for large datasets using vectorized operations and memory-efficient storage"
            elif "representation" in file_lower:
                return "Implement program tree representations with efficient mutation and crossover operators"
            else:
                return "Follow MOSES evolutionary patterns with proper selection pressure and convergence criteria"

        # Attention and ECAN systems
        elif "attention" in file_lower or "ecan" in content_lower:
            return "Implement ECAN attention allocation with proper STI/LTI dynamics, rent collection, and attentional focus management"

        # Neural-symbolic integration
        elif "neural" in file_lower or "tensor" in file_lower:
            return "Bridge symbolic and neural representations using tensor embeddings and differentiable programming patterns"

        # Distributed cognition protocols
        elif "distributed" in file_lower:
            return (
                "Implement fault-tolerant distributed protocols with consensus mechanisms and efficient message passing"
            )

        # Cognitive patterns and PLN
        elif "pln" in file_lower or "logic" in file_lower:
            return "Implement probabilistic logic networks with proper uncertainty propagation and inference control"

        # Learning and pattern mining
        elif "learn" in file_lower or "pattern" in content_lower:
            return "Implement unsupervised learning with pattern recognition, frequency analysis, and surprisingness measures"

        # Query and pattern matching
        elif "query" in file_lower:
            return "Optimize pattern matching with constraint satisfaction and efficient variable binding algorithms"

        # Storage and persistence
        elif "persist" in file_lower:
            return "Implement robust serialization with version compatibility, data integrity checks, and efficient I/O"

        # Common implementation patterns
        elif "not implemented" in content_lower:
            if "interface" in content_lower or "virtual" in content_lower:
                return (
                    "Implement interface methods following the Abstract Factory or Strategy pattern for extensibility"
                )
            else:
                return "Replace placeholder with concrete implementation following existing architectural patterns"
        elif "hack" in content_lower or "fixme" in content_lower:
            return "Refactor temporary solution with proper design patterns, error handling, and maintainable code structure"
        elif "todo" in content_lower and "test" in content_lower:
            return (
                "Implement comprehensive unit and integration tests with edge case coverage and performance benchmarks"
            )
        elif "memory" in content_lower:
            return "Implement proper memory management with RAII patterns, smart pointers, and leak prevention"
        elif "algorithm" in content_lower:
            return "Research and implement optimal algorithms with complexity analysis and benchmark validation"
        # Default enhanced guidance based on subsystem
        elif todo.subsystem == "Memory System":
            return "Implement following AtomSpace memory management patterns with proper handle lifecycle and garbage collection"
        elif todo.subsystem == "Task System":
            return "Implement concurrent task processing with proper work distribution and result aggregation"
        elif todo.subsystem == "AI System":
            return "Implement cognitive AI patterns with proper neural-symbolic integration and learning mechanisms"
        elif todo.subsystem == "MOSES Representation/Scoring":
            return (
                "Implement evolutionary optimization following MOSES architectural patterns with efficient evaluation"
            )
        else:
            return "Analyze requirements thoroughly and implement following OpenCog architectural principles and coding standards"

    def _generate_test_guidance(self, todo: TODOItem) -> str:
        """Enhanced test guidance with comprehensive validation strategies"""
        content_lower = todo.content.lower()
        file_lower = todo.file.lower()

        # Thread safety testing
        if "thread" in content_lower or "sync" in content_lower:
            return "Test with ThreadSanitizer, concurrent access patterns, deadlock detection, and stress testing under high concurrency"

        # Performance testing
        elif "performance" in content_lower:
            return "Benchmark before/after with profiling tools, memory usage analysis, and regression testing for performance degradation"

        # AtomSpace testing
        elif "atomspace" in file_lower:
            if "valuation" in file_lower:
                return "Test value storage/retrieval, type validation, and truth value operations with edge cases and large datasets"
            elif "link" in file_lower:
                return (
                    "Test link creation, traversal, incoming/outgoing set consistency, and circular reference handling"
                )
            else:
                return (
                    "Test atom creation/deletion, handle consistency, truth value propagation, and attention allocation"
                )

        # MOSES testing
        elif "moses" in file_lower:
            if "scoring" in content_lower:
                return "Test fitness evaluation accuracy, multi-objective optimization, and performance with large candidate populations"
            elif "table" in file_lower:
                return "Test with various dataset sizes, missing values, categorical/continuous features, and memory constraints"
            else:
                return "Test evolutionary convergence, diversity maintenance, and solution quality across multiple runs"

        # Attention system testing
        elif "attention" in file_lower:
            return "Test STI/LTI dynamics, attentional focus changes, rent collection, and attention value conservation"

        # Neural-symbolic testing
        elif "neural" in file_lower or "tensor" in file_lower:
            return "Test symbolic-neural mapping consistency, gradient flow, and embedding quality with validation datasets"

        # Distributed system testing
        elif "distributed" in file_lower:
            return "Test network partitions, message ordering, fault tolerance, and consensus under various failure scenarios"

        # Logic and PLN testing
        elif "pln" in file_lower or "logic" in file_lower:
            return "Test inference accuracy, uncertainty propagation, logical consistency, and computational complexity bounds"

        # Learning system testing
        elif "learn" in file_lower:
            return "Test pattern recognition accuracy, learning convergence, overfitting prevention, and generalization capability"

        # Query system testing
        elif "query" in file_lower:
            return "Test pattern matching correctness, variable binding consistency, and performance with complex query patterns"

        # Storage system testing
        elif "persist" in file_lower:
            return "Test serialization/deserialization consistency, data integrity, version compatibility, and corruption recovery"

        # Backtrace testing
        elif "backtrace" in content_lower:
            return "Test stack trace accuracy across platforms, symbol resolution, and error reporting under various crash scenarios"

        # Memory management testing
        elif "memory" in content_lower or "leak" in content_lower:
            return (
                "Test with Valgrind, AddressSanitizer, memory leak detection, and stress testing under memory pressure"
            )

        # Build system testing
        elif "cmake" in file_lower or "build" in content_lower:
            return "Test build configurations across platforms, dependency resolution, and integration with CI/CD pipelines"

        # Generic testing patterns
        elif "not implemented" in content_lower:
            return "Create comprehensive test suite covering interface contracts, edge cases, error conditions, and integration points"
        elif "algorithm" in content_lower:
            return (
                "Test algorithmic correctness with known test vectors, complexity validation, and comparative analysis"
            )
        # Default based on subsystem
        elif todo.subsystem == "Memory System":
            return "Test memory operations, handle management, concurrent access, and data consistency validation"
        elif todo.subsystem == "Task System":
            return "Test task scheduling, execution order, resource allocation, and error propagation"
        elif todo.subsystem == "AI System":
            return "Test cognitive functionality, learning behavior, and integration with other AI components"
        elif todo.subsystem == "MOSES Representation/Scoring":
            return "Test evolutionary operators, fitness evaluation, and convergence properties with diverse problems"
        else:
            return (
                "Create unit tests covering normal operation, edge cases, error conditions, and integration scenarios"
            )

    def mark_batch_in_progress(self, batch: list[TODOItem]):
        """Mark batch items as in-progress"""
        for todo in batch:
            todo_key = f"{todo.file}:{todo.line}"
            if todo_key not in self.progress_data["in_progress_todos"]:
                self.progress_data["in_progress_todos"].append(todo_key)
            todo.status = "in-progress"
            todo.assigned_batch = self.progress_data["current_iteration"]

    def validate_batch_6_todos(self):
        """Specifically validate and resolve the batch 6 TODOs mentioned in the issue"""
        print("🎯 Validating specific Batch 6 TODOs...")

        batch_6_todos = [
            "atomspace/opencog/query/PatternMatchEngine.cc:1504",
            "atomspace/opencog/query/SatisfyMixin.cc:178",
            "atomspace/opencog/scm/opencog/base/debug-trace.scm:9",
            "cogserver/opencog/network/ServerSocket.cc:162",
            "scripts/generate_todo_catalog.py:289",
        ]

        resolved_count = 0
        for todo_key in batch_6_todos:
            file_path, line_str = todo_key.split(":")
            line_num = int(line_str)

            full_path = self.repo_path / file_path
            if not full_path.exists():
                print(f"   📁 File not found: {file_path}")
                continue

            try:
                with open(full_path, encoding="utf-8", errors="ignore") as f:
                    lines = f.readlines()

                # Check the specific line and surrounding area
                if line_num <= len(lines):
                    line_content = lines[line_num - 1].strip()

                    # Check if this specific TODO has been resolved
                    if todo_key == "atomspace/opencog/query/PatternMatchEngine.cc:1504":
                        if "Not implemented" not in line_content:
                            print(f"   ✅ TODO resolved: {todo_key} - 'Not implemented' exception removed")
                            self._mark_todo_completed(todo_key, "Code implementation completed")
                            resolved_count += 1
                        else:
                            print(f"   ⏳ TODO still pending: {todo_key}")

                    elif todo_key == "cogserver/opencog/network/ServerSocket.cc:162":
                        if "std::jthread" in line_content or "Thread management is now handled" in "\n".join(
                            lines[max(0, line_num - 3) : line_num + 2]
                        ):
                            print(f"   ✅ TODO resolved: {todo_key} - Thread management updated")
                            self._mark_todo_completed(todo_key, "Thread management modernized")
                            resolved_count += 1
                        else:
                            print(f"   ⏳ TODO still pending: {todo_key}")

                    else:
                        # For other TODOs, check if they still contain TODO/FIXME markers
                        context = "\n".join(lines[max(0, line_num - 2) : line_num + 3])
                        if any(keyword in context.lower() for keyword in ["todo", "fixme", "xxx"]):
                            print(f"   ⏳ TODO still pending: {todo_key}")
                        else:
                            print(f"   ❓ TODO status unclear: {todo_key}")

            except Exception as e:
                print(f"   ⚠️  Error checking {todo_key}: {e}")

        print(f"   📊 Batch 6 validation complete: {resolved_count} TODOs resolved")
        return resolved_count

    def _mark_todo_completed(self, todo_key: str, resolution_note: str):
        """Mark a specific TODO as completed with a resolution note"""
        if todo_key not in self.progress_data["completed_todos"]:
            self.progress_data["completed_todos"].append(todo_key)
        if todo_key in self.progress_data["in_progress_todos"]:
            self.progress_data["in_progress_todos"].remove(todo_key)

        # Add resolution tracking
        if "resolutions" not in self.progress_data:
            self.progress_data["resolutions"] = {}
        self.progress_data["resolutions"][todo_key] = {
            "resolved_at": datetime.now().isoformat(),
            "resolution_note": resolution_note,
            "resolved_by": "recursive_todo_resolver_validation",
        }

    def validate_existing_todos(self):
        """Validate that TODOs marked as in-progress or unchecked still exist in the codebase"""
        print("🔍 Validating existing TODO items against codebase...")

        todos_to_mark_completed = []

        for todo in self.todos:
            if todo.status in ["unchecked", "in-progress"]:
                file_path = self.repo_path / todo.file
                if not file_path.exists():
                    print(f"   📁 File no longer exists: {todo.file}")
                    todos_to_mark_completed.append(f"{todo.file}:{todo.line}")
                    continue

                # Read the file and check if the TODO still exists at the expected line
                try:
                    with open(file_path, encoding="utf-8", errors="ignore") as f:
                        lines = f.readlines()

                    # Check around the line number (±2 lines) for the TODO content
                    line_num = todo.line - 1  # Convert to 0-based indexing
                    search_range = range(max(0, line_num - 2), min(len(lines), line_num + 3))

                    todo_found = False
                    for i in search_range:
                        if todo.content.strip() in lines[i] or any(
                            keyword in lines[i].lower() for keyword in ["todo", "fixme", "xxx", "not implemented"]
                        ):
                            todo_found = True
                            break

                    if not todo_found:
                        print(f"   ✅ TODO resolved: {todo.file}:{todo.line}")
                        todos_to_mark_completed.append(f"{todo.file}:{todo.line}")

                except Exception as e:
                    print(f"   ⚠️  Error checking {todo.file}: {e}")

        # Mark resolved TODOs as completed
        for todo_key in todos_to_mark_completed:
            if todo_key not in self.progress_data["completed_todos"]:
                self.progress_data["completed_todos"].append(todo_key)
            if todo_key in self.progress_data["in_progress_todos"]:
                self.progress_data["in_progress_todos"].remove(todo_key)

        if todos_to_mark_completed:
            print(f"   🎉 Marked {len(todos_to_mark_completed)} TODOs as completed automatically")
            self._save_progress()

    def update_catalog_with_progress(self):
        """Update the TODO catalog to reflect current progress"""
        if not self.catalog_path.exists():
            return

        with open(self.catalog_path) as f:
            content = f.read()

        # Replace unchecked items with checked ones for completed TODOs
        for todo_key in self.progress_data.get("completed_todos", []):
            # Find the corresponding line and mark as completed
            file_part, line_part = todo_key.split(":")
            pattern = f"- \\[ \\] \\*\\*{re.escape(file_part)}:{line_part}\\*\\*"
            replacement = f"- [x] **{file_part}:{line_part}**"
            content = re.sub(pattern, replacement, content)

        # Update progress section
        progress_section = f"""

## 🔄 Recursive Resolution Progress

**Current Iteration:** {self.progress_data["current_iteration"]}
**Last Run:** {self.progress_data.get("last_run", "Never")}
**TODOs Resolved:** {len(self.progress_data.get("completed_todos", []))}
**TODOs In Progress:** {len(self.progress_data.get("in_progress_todos", []))}
**Total Remaining:** {len([t for t in self.todos if t.status == "unchecked"])}

*Use `python scripts/recursive_todo_resolver.py --next-batch` to continue resolution*

---
"""

        # Insert progress section before Meta-Cognitive Enhancement
        if "## Meta-Cognitive Enhancement Instructions" in content:
            content = content.replace(
                "## Meta-Cognitive Enhancement Instructions",
                progress_section + "## Meta-Cognitive Enhancement Instructions",
            )

        with open(self.catalog_path, "w") as f:
            f.write(content)

    def run_iteration(self) -> str | None:
        """Run a single iteration of the recursive TODO resolution"""

        # Step 1: Extract catalog
        self.extract_catalog()

        # Step 2: Validate existing TODOs to ensure they still exist in codebase
        self.validate_existing_todos()

        # Step 3: Allocate attention (select batch)
        batch = self.allocate_attention()

        if not batch:
            print("🎉 No more TODOs to process!")
            return None

        # Step 4: Generate actionable issues
        issue_content = self.generate_actionable_issues(batch)

        # Step 5: Mark batch as in-progress
        self.mark_batch_in_progress(batch)

        # Step 6: Auto-create GitHub issue (Meta-Enhancement)
        created_issue = None
        if self.github_creator and self.enable_github_integration:
            created_issue = self.github_creator.create_todo_batch_issue(
                issue_content, self.progress_data["current_iteration"]
            )
            if created_issue:
                # Store issue URL in progress data for future reference
                if "github_issues" not in self.progress_data:
                    self.progress_data["github_issues"] = {}
                self.progress_data["github_issues"][self.progress_data["current_iteration"]] = {
                    "issue_number": created_issue["number"],
                    "issue_url": created_issue["html_url"],
                    "created_at": created_issue["created_at"],
                }

        # Step 6: Update progress and catalog
        self.progress_data["current_iteration"] += 1
        self._save_progress()
        self.update_catalog_with_progress()

        return issue_content

    def mark_completed(self, file_path: str, line: int, pr_link: str | None = None):
        """Mark a TODO as completed"""
        todo_key = f"{file_path}:{line}"

        # Move from in-progress to completed
        if todo_key in self.progress_data["in_progress_todos"]:
            self.progress_data["in_progress_todos"].remove(todo_key)

        if todo_key not in self.progress_data["completed_todos"]:
            self.progress_data["completed_todos"].append(todo_key)
            self.progress_data["total_resolved"] += 1

        # Update TODO object if it exists
        for todo in self.todos:
            if f"{todo.file}:{todo.line}" == todo_key:
                todo.status = "completed"
                if pr_link:
                    todo.resolution_pr = pr_link
                break

        # Update GitHub issues if available (Meta-Enhancement)
        if self.github_creator and pr_link and "github_issues" in self.progress_data:
            # Find which batch this TODO was in and update the corresponding issue
            for _batch_num, issue_info in self.progress_data["github_issues"].items():
                if self.github_creator.update_issue_with_completion(issue_info["issue_number"], todo_key, pr_link):
                    print(f"📝 Updated GitHub issue #{issue_info['issue_number']}")
                    break

        self._save_progress()
        print(f"✅ Marked {todo_key} as completed")


def main():
    """Main execution function"""
    import argparse

    parser = argparse.ArgumentParser(description="Recursive TODO Resolution System")
    parser.add_argument("--repo-path", default=".", help="Repository path")
    parser.add_argument("--batch-size", type=int, default=5, help="Number of TODOs per batch")
    parser.add_argument("--next-batch", action="store_true", help="Run next iteration")
    parser.add_argument("--mark-completed", nargs=2, metavar=("FILE:LINE", "PR_LINK"), help="Mark a TODO as completed")
    parser.add_argument("--status", action="store_true", help="Show current status")
    parser.add_argument("--no-github", action="store_true", help="Disable GitHub integration")
    parser.add_argument("--validate-batch-6", action="store_true", help="Validate and resolve batch 6 TODOs")

    args = parser.parse_args()

    resolver = RecursiveTODOResolver(args.repo_path, args.batch_size, enable_github_integration=not args.no_github)

    if args.mark_completed:
        file_line, pr_link = args.mark_completed
        file_path, line = file_line.split(":")
        resolver.mark_completed(file_path, int(line), pr_link)
        return

    if args.status:
        resolver.extract_catalog()
        unchecked = len([t for t in resolver.todos if t.status == "unchecked"])
        in_progress = len([t for t in resolver.todos if t.status == "in-progress"])
        completed = len([t for t in resolver.todos if t.status == "completed"])

        print("📊 TODO Resolution Status:")
        print(f"   • Unchecked: {unchecked}")
        print(f"   • In Progress: {in_progress}")
        print(f"   • Completed: {completed}")
        print(f"   • Current Iteration: {resolver.progress_data['current_iteration']}")

        # Show GitHub integration status
        if resolver.github_creator:
            print("   • GitHub Integration: ✅ Enabled")
            if "github_issues" in resolver.progress_data:
                issue_count = len(resolver.progress_data["github_issues"])
                print(f"   • GitHub Issues Created: {issue_count}")
        else:
            print("   • GitHub Integration: ❌ Disabled")
        return

    if args.validate_batch_6:
        resolver.validate_batch_6_todos()
        resolver._save_progress()
        return

    if args.next_batch:
        print("🧠 Running next iteration of recursive TODO resolution...")
        issue_content = resolver.run_iteration()

        if issue_content:
            # Save issue content to file
            issue_file = resolver.repo_path / f"TODO_BATCH_{resolver.progress_data['current_iteration'] - 1}_ISSUE.md"
            with open(issue_file, "w") as f:
                f.write(issue_content)

            print(f"📝 Generated issue content: {issue_file}")
            print(f"🎯 Selected batch for iteration {resolver.progress_data['current_iteration'] - 1}")
            print("📋 Copy the issue content to create a GitHub issue for tracking")
        else:
            print("🎉 All TODOs have been processed!")


if __name__ == "__main__":
    main()
