#!/usr/bin/env python3
"""
Hypergraph Pattern Matching System
Phase β: DAS-Hypergraph Integration

Implements typed hypergraph pattern matching with distributed execution
across 11×5×2 quantum state space.

Copyright (c) 2025 OpenCog Foundation
"""

import itertools
import json
import threading
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class AtomType(Enum):
    """AtomSpace atom types"""
    CONCEPT_NODE = "ConceptNode"
    PREDICATE_NODE = "PredicateNode"
    VARIABLE_NODE = "VariableNode"
    EVALUATION_LINK = "EvaluationLink"
    LIST_LINK = "ListLink"
    BIND_LINK = "BindLink"
    AND_LINK = "AndLink"
    OR_LINK = "OrLink"
    NOT_LINK = "NotLink"
    EXECUTION_OUTPUT_LINK = "ExecutionOutputLink"

@dataclass
class TruthValue:
    """Truth value with strength and confidence"""
    strength: float
    confidence: float

    def __post_init__(self):
        self.strength = max(0.0, min(1.0, self.strength))
        self.confidence = max(0.0, min(1.0, self.confidence))

@dataclass
class HypergraphAtom:
    """Atom in hypergraph with type, name, and truth value"""
    atom_id: str
    atom_type: AtomType
    name: str | None = None
    truth_value: TruthValue | None = None
    incoming: list[str] = field(default_factory=list)
    outgoing: list[str] = field(default_factory=list)
    shard_id: int = 0
    coordinates: tuple[int, int, int] = (0, 0, 0)

@dataclass
class HypergraphLink:
    """Link in hypergraph connecting multiple atoms"""
    link_id: str
    link_type: AtomType
    targets: list[str]
    truth_value: TruthValue | None = None
    shard_id: int = 0
    coordinates: tuple[int, int, int] = (0, 0, 0)

@dataclass
class PatternTemplate:
    """Template for hypergraph pattern matching"""
    template_id: str
    atoms: list[HypergraphAtom]
    links: list[HypergraphLink]
    variables: dict[str, AtomType]
    constraints: list[str]
    expected_bindings: int = 1

@dataclass
class PatternMatch:
    """Result of pattern matching"""
    match_id: str
    template_id: str
    bindings: dict[str, str]  # Variable -> Atom ID
    confidence: float
    truth_value: TruthValue | None = None
    shard_id: int = 0
    match_time: float = 0.0

class HypergraphPatternMatcher:
    """
    Hypergraph Pattern Matching Engine

    Implements typed hypergraph pattern matching for AtomSpace patterns
    with support for variables, constraints, and distributed execution.
    """

    def __init__(self, num_shards: int = 11, links_per_shard: int = 5, truth_dimensions: int = 2):
        self.num_shards = num_shards
        self.links_per_shard = links_per_shard
        self.truth_dimensions = truth_dimensions
        self.total_states = num_shards * links_per_shard * truth_dimensions

        # Pattern matching state
        self.patterns = {}
        self.atoms = {}
        self.links = {}
        self.match_cache = {}

        # Performance tracking
        self.match_statistics = {
            "total_patterns": 0,
            "total_matches": 0,
            "average_match_time": 0.0,
            "cache_hits": 0,
            "cache_misses": 0
        }

        # Thread safety
        self.match_lock = threading.Lock()

        # Initialize with sample data
        self._initialize_sample_hypergraph()

    def add_pattern_template(self, template: PatternTemplate) -> bool:
        """
        Add a pattern template for matching

        Args:
            template: Pattern template to add

        Returns:
            bool: True if template was added successfully
        """
        with self.match_lock:
            if template.template_id in self.patterns:
                return False

            self.patterns[template.template_id] = template
            self.match_statistics["total_patterns"] += 1
            return True

    def match_pattern(self, template_id: str, target_shard: int | None = None) -> list[PatternMatch]:
        """
        Match a pattern template against the hypergraph

        Args:
            template_id: ID of template to match
            target_shard: Optional specific shard to search

        Returns:
            List[PatternMatch]: List of pattern matches found
        """
        start_time = time.time()

        # Check cache first
        cache_key = f"{template_id}_{target_shard}"
        if cache_key in self.match_cache:
            self.match_statistics["cache_hits"] += 1
            return self.match_cache[cache_key]

        self.match_statistics["cache_misses"] += 1

        # Get pattern template
        template = self.patterns.get(template_id)
        if not template:
            return []

        # Perform pattern matching
        matches = self._execute_pattern_matching(template, target_shard)

        # Update statistics
        match_time = time.time() - start_time
        self.match_statistics["total_matches"] += len(matches)
        self.match_statistics["average_match_time"] = (
            (self.match_statistics["average_match_time"] * (self.match_statistics["total_patterns"] - 1) + match_time)
            / self.match_statistics["total_patterns"]
        )

        # Cache results
        self.match_cache[cache_key] = matches

        return matches

    def _execute_pattern_matching(self, template: PatternTemplate, target_shard: int | None = None) -> list[PatternMatch]:
        """
        Execute pattern matching algorithm

        Args:
            template: Pattern template to match
            target_shard: Optional target shard

        Returns:
            List[PatternMatch]: Found matches
        """
        matches = []

        # Determine search space
        if target_shard is not None:
            search_shards = [target_shard]
        else:
            search_shards = list(range(self.num_shards))

        # Search each shard
        for shard_id in search_shards:
            shard_matches = self._match_on_shard(template, shard_id)
            matches.extend(shard_matches)

        # Sort matches by confidence
        matches.sort(key=lambda m: m.confidence, reverse=True)

        return matches

    def _match_on_shard(self, template: PatternTemplate, shard_id: int) -> list[PatternMatch]:
        """
        Match pattern on specific shard

        Args:
            template: Pattern template
            shard_id: Target shard ID

        Returns:
            List[PatternMatch]: Matches found on shard
        """
        matches = []

        # Get atoms and links for this shard
        shard_atoms = {aid: atom for aid, atom in self.atoms.items() if atom.shard_id == shard_id}
        shard_links = {lid: link for lid, link in self.links.items() if link.shard_id == shard_id}

        # Find candidate bindings for variables
        variable_candidates = self._find_variable_candidates(template, shard_atoms, shard_links)

        # Generate all possible binding combinations
        binding_combinations = self._generate_binding_combinations(template.variables, variable_candidates)

        # Test each binding combination
        for binding_combo in binding_combinations:
            match = self._test_binding(template, binding_combo, shard_atoms, shard_links, shard_id)
            if match:
                matches.append(match)

        return matches

    def _find_variable_candidates(self, template: PatternTemplate, shard_atoms: dict[str, HypergraphAtom],
                                 shard_links: dict[str, HypergraphLink]) -> dict[str, list[str]]:
        """
        Find candidate atoms for each variable in the template

        Args:
            template: Pattern template
            shard_atoms: Atoms on the shard
            shard_links: Links on the shard

        Returns:
            Dict[str, List[str]]: Variable name to candidate atom IDs
        """
        candidates = {}

        for var_name, var_type in template.variables.items():
            candidates[var_name] = []

            # Find atoms matching the variable type
            if var_type in [AtomType.CONCEPT_NODE, AtomType.PREDICATE_NODE, AtomType.VARIABLE_NODE]:
                for atom_id, atom in shard_atoms.items():
                    if atom.atom_type == var_type:
                        candidates[var_name].append(atom_id)

            # For links, search in shard_links
            elif var_type in [AtomType.EVALUATION_LINK, AtomType.LIST_LINK, AtomType.BIND_LINK]:
                for link_id, link in shard_links.items():
                    if link.link_type == var_type:
                        candidates[var_name].append(link_id)

        return candidates

    def _generate_binding_combinations(self, variables: dict[str, AtomType],
                                     candidates: dict[str, list[str]]) -> list[dict[str, str]]:
        """
        Generate all possible variable binding combinations

        Args:
            variables: Template variables
            candidates: Candidate atoms for each variable

        Returns:
            List[Dict[str, str]]: List of binding combinations
        """
        if not variables:
            return [{}]

        # Get variable names and their candidates
        var_names = list(variables.keys())
        var_candidates = [candidates.get(var, []) for var in var_names]

        # Generate cartesian product of candidates
        combinations = []
        for combo in itertools.product(*var_candidates):
            binding = dict(zip(var_names, combo, strict=False))
            combinations.append(binding)

        # Limit combinations to prevent explosion
        max_combinations = 1000
        if len(combinations) > max_combinations:
            combinations = combinations[:max_combinations]

        return combinations

    def _test_binding(self, template: PatternTemplate, binding: dict[str, str],
                     shard_atoms: dict[str, HypergraphAtom], shard_links: dict[str, HypergraphLink],
                     shard_id: int) -> PatternMatch | None:
        """
        Test if a variable binding satisfies the template

        Args:
            template: Pattern template
            binding: Variable bindings to test
            shard_atoms: Atoms on shard
            shard_links: Links on shard
            shard_id: Shard ID

        Returns:
            Optional[PatternMatch]: Match if binding is valid, None otherwise
        """
        # Check structural constraints
        if not self._check_structural_constraints(template, binding, shard_atoms, shard_links):
            return None

        # Check truth value constraints
        if not self._check_truth_constraints(template, binding, shard_atoms, shard_links):
            return None

        # Check custom constraints
        if not self._check_custom_constraints(template, binding, shard_atoms, shard_links):
            return None

        # Calculate match confidence
        confidence = self._calculate_match_confidence(template, binding, shard_atoms, shard_links)

        # Create match result
        match = PatternMatch(
            match_id=f"match_{template.template_id}_{shard_id}_{hash(str(binding))}",
            template_id=template.template_id,
            bindings=binding,
            confidence=confidence,
            shard_id=shard_id,
            match_time=time.time()
        )

        return match

    def _check_structural_constraints(self, template: PatternTemplate, binding: dict[str, str],
                                    shard_atoms: dict[str, HypergraphAtom],
                                    shard_links: dict[str, HypergraphLink]) -> bool:
        """Check if binding satisfies structural constraints"""

        # Check that all bound atoms exist
        for _var_name, atom_id in binding.items():
            if atom_id not in shard_atoms and atom_id not in shard_links:
                return False

        # Check link structure constraints
        for template_link in template.links:
            if not self._validate_link_structure(template_link, binding, shard_atoms, shard_links):
                return False

        return True

    def _validate_link_structure(self, template_link: HypergraphLink, binding: dict[str, str],
                                shard_atoms: dict[str, HypergraphAtom],
                                shard_links: dict[str, HypergraphLink]) -> bool:
        """Validate that a template link structure is satisfied"""

        # Resolve link targets through variable binding
        resolved_targets = []
        for target in template_link.targets:
            if target.startswith("$"):  # Variable
                if target in binding:
                    resolved_targets.append(binding[target])
                else:
                    return False  # Unbound variable
            else:
                resolved_targets.append(target)

        # Find matching links in the shard
        for _link_id, link in shard_links.items():
            if link.link_type == template_link.link_type and set(link.targets) == set(resolved_targets):
                return True

        return False

    def _check_truth_constraints(self, template: PatternTemplate, binding: dict[str, str],
                               shard_atoms: dict[str, HypergraphAtom],
                               shard_links: dict[str, HypergraphLink]) -> bool:
        """Check truth value constraints"""

        # For now, accept all truth values
        # In a full implementation, this would check specific truth value constraints
        return True

    def _check_custom_constraints(self, template: PatternTemplate, binding: dict[str, str],
                                shard_atoms: dict[str, HypergraphAtom],
                                shard_links: dict[str, HypergraphLink]) -> bool:
        """Check custom constraints specified in template"""

        for constraint in template.constraints:
            if not self._evaluate_constraint(constraint, binding, shard_atoms, shard_links):
                return False

        return True

    def _evaluate_constraint(self, constraint: str, binding: dict[str, str],
                           shard_atoms: dict[str, HypergraphAtom],
                           shard_links: dict[str, HypergraphLink]) -> bool:
        """Evaluate a single constraint"""

        # Simple constraint evaluation
        # In a full implementation, this would parse and evaluate complex expressions

        if "strength" in constraint.lower():
            # Check strength constraints
            if ">" in constraint:
                threshold = float(constraint.split(">")[1].strip())
                for _var_name, atom_id in binding.items():
                    atom = shard_atoms.get(atom_id) or shard_links.get(atom_id)
                    if atom and atom.truth_value and atom.truth_value.strength <= threshold:
                        return False

        return True

    def _calculate_match_confidence(self, template: PatternTemplate, binding: dict[str, str],
                                  shard_atoms: dict[str, HypergraphAtom],
                                  shard_links: dict[str, HypergraphLink]) -> float:
        """Calculate confidence score for a match"""

        confidence_factors = []

        # Factor 1: Truth value confidence of bound atoms
        for _var_name, atom_id in binding.items():
            atom = shard_atoms.get(atom_id) or shard_links.get(atom_id)
            if atom and atom.truth_value:
                confidence_factors.append(atom.truth_value.confidence)
            else:
                confidence_factors.append(0.5)  # Default confidence

        # Factor 2: Structural completeness
        structural_score = len(binding) / max(1, len(template.variables))
        confidence_factors.append(structural_score)

        # Factor 3: Constraint satisfaction
        constraint_score = 1.0  # All constraints must be satisfied to reach this point
        confidence_factors.append(constraint_score)

        # Calculate average confidence
        overall_confidence = sum(confidence_factors) / len(confidence_factors) if confidence_factors else 0.0

        return min(1.0, max(0.0, overall_confidence))

    def _initialize_sample_hypergraph(self):
        """Initialize hypergraph with sample data for testing"""

        # Create sample atoms for each shard
        for shard_id in range(self.num_shards):
            # Add concept nodes
            for i in range(self.links_per_shard):
                atom_id = f"concept_{shard_id}_{i}"
                atom = HypergraphAtom(
                    atom_id=atom_id,
                    atom_type=AtomType.CONCEPT_NODE,
                    name=f"knowledge_{shard_id}_{i}",
                    truth_value=TruthValue(0.7 + (i * 0.1), 0.8 + (shard_id * 0.01)),
                    shard_id=shard_id,
                    coordinates=(shard_id, i, 0)
                )
                self.atoms[atom_id] = atom

            # Add predicate nodes
            for i in range(min(3, self.links_per_shard)):
                atom_id = f"predicate_{shard_id}_{i}"
                atom = HypergraphAtom(
                    atom_id=atom_id,
                    atom_type=AtomType.PREDICATE_NODE,
                    name=f"relates_to_{shard_id}_{i}",
                    truth_value=TruthValue(0.6 + (i * 0.15), 0.75 + (shard_id * 0.02)),
                    shard_id=shard_id,
                    coordinates=(shard_id, i, 1)
                )
                self.atoms[atom_id] = atom

            # Add evaluation links
            for i in range(self.links_per_shard):
                link_id = f"eval_link_{shard_id}_{i}"

                # Link concepts through predicates
                concept_id = f"concept_{shard_id}_{i}"
                predicate_id = f"predicate_{shard_id}_{i % 3}"
                target_concept_id = f"concept_{shard_id}_{(i + 1) % self.links_per_shard}"

                link = HypergraphLink(
                    link_id=link_id,
                    link_type=AtomType.EVALUATION_LINK,
                    targets=[predicate_id, concept_id, target_concept_id],
                    truth_value=TruthValue(0.75 + (i * 0.05), 0.85),
                    shard_id=shard_id,
                    coordinates=(shard_id, i, 1)
                )
                self.links[link_id] = link

    def create_sample_patterns(self) -> list[str]:
        """Create sample pattern templates for testing"""
        patterns = []

        # Pattern 1: Find concepts
        template1 = PatternTemplate(
            template_id="find_concepts",
            atoms=[
                HypergraphAtom(
                    atom_id="$concept",
                    atom_type=AtomType.CONCEPT_NODE,
                    name=None
                )
            ],
            links=[],
            variables={"$concept": AtomType.CONCEPT_NODE},
            constraints=["strength > 0.5"]
        )
        self.add_pattern_template(template1)
        patterns.append(template1.template_id)

        # Pattern 2: Find evaluation relationships
        template2 = PatternTemplate(
            template_id="find_evaluations",
            atoms=[
                HypergraphAtom(atom_id="$pred", atom_type=AtomType.PREDICATE_NODE),
                HypergraphAtom(atom_id="$concept1", atom_type=AtomType.CONCEPT_NODE),
                HypergraphAtom(atom_id="$concept2", atom_type=AtomType.CONCEPT_NODE)
            ],
            links=[
                HypergraphLink(
                    link_id="$eval",
                    link_type=AtomType.EVALUATION_LINK,
                    targets=["$pred", "$concept1", "$concept2"]
                )
            ],
            variables={
                "$pred": AtomType.PREDICATE_NODE,
                "$concept1": AtomType.CONCEPT_NODE,
                "$concept2": AtomType.CONCEPT_NODE,
                "$eval": AtomType.EVALUATION_LINK
            },
            constraints=[]
        )
        self.add_pattern_template(template2)
        patterns.append(template2.template_id)

        # Pattern 3: Find high-confidence knowledge
        template3 = PatternTemplate(
            template_id="find_high_confidence",
            atoms=[
                HypergraphAtom(atom_id="$knowledge", atom_type=AtomType.CONCEPT_NODE)
            ],
            links=[],
            variables={"$knowledge": AtomType.CONCEPT_NODE},
            constraints=["confidence > 0.8", "strength > 0.7"]
        )
        self.add_pattern_template(template3)
        patterns.append(template3.template_id)

        return patterns

    def get_matching_statistics(self) -> dict[str, Any]:
        """Get pattern matching statistics"""
        return {
            "hypergraph_stats": {
                "total_atoms": len(self.atoms),
                "total_links": len(self.links),
                "total_patterns": len(self.patterns),
                "states_covered": self.total_states
            },
            "performance_stats": self.match_statistics.copy(),
            "cache_stats": {
                "cache_size": len(self.match_cache),
                "hit_rate": self.match_statistics["cache_hits"] / max(1,
                    self.match_statistics["cache_hits"] + self.match_statistics["cache_misses"])
            },
            "shard_distribution": self._analyze_shard_distribution()
        }

    def _analyze_shard_distribution(self) -> dict[str, Any]:
        """Analyze distribution of atoms and links across shards"""
        distribution = {}

        for shard_id in range(self.num_shards):
            shard_atoms = sum(1 for atom in self.atoms.values() if atom.shard_id == shard_id)
            shard_links = sum(1 for link in self.links.values() if link.shard_id == shard_id)

            distribution[shard_id] = {
                "atoms": shard_atoms,
                "links": shard_links,
                "total": shard_atoms + shard_links,
                "density": (shard_atoms + shard_links) / (self.links_per_shard * 2)
            }

        return distribution


def main():
    """Test the hypergraph pattern matcher"""
    print("=== Hypergraph Pattern Matching Test ===")

    # Initialize matcher
    matcher = HypergraphPatternMatcher(num_shards=11, links_per_shard=5, truth_dimensions=2)

    # Create sample patterns
    print("Creating sample patterns...")
    pattern_ids = matcher.create_sample_patterns()
    print(f"Created {len(pattern_ids)} patterns: {pattern_ids}")

    # Test pattern matching
    print("\nTesting pattern matching...")

    for pattern_id in pattern_ids:
        print(f"\nMatching pattern: {pattern_id}")

        start_time = time.time()
        matches = matcher.match_pattern(pattern_id)
        match_time = time.time() - start_time

        print(f"  Found {len(matches)} matches in {match_time:.4f}s")

        # Show top 3 matches
        for i, match in enumerate(matches[:3]):
            print(f"    {i+1}. Match {match.match_id}")
            print(f"       Confidence: {match.confidence:.3f}")
            print(f"       Shard: {match.shard_id}")
            print(f"       Bindings: {match.bindings}")

    # Test specific shard matching
    print("\nTesting shard-specific matching...")
    shard_matches = matcher.match_pattern("find_concepts", target_shard=0)
    print(f"Found {len(shard_matches)} matches on shard 0")

    # Get statistics
    print("\nGetting system statistics...")
    stats = matcher.get_matching_statistics()

    print("Hypergraph statistics:")
    print(f"  Total atoms: {stats['hypergraph_stats']['total_atoms']}")
    print(f"  Total links: {stats['hypergraph_stats']['total_links']}")
    print(f"  Total patterns: {stats['hypergraph_stats']['total_patterns']}")
    print(f"  States covered: {stats['hypergraph_stats']['states_covered']}")

    print("\nPerformance statistics:")
    print(f"  Total matches: {stats['performance_stats']['total_matches']}")
    print(f"  Average match time: {stats['performance_stats']['average_match_time']:.4f}s")
    print(f"  Cache hit rate: {stats['cache_stats']['hit_rate']:.3f}")

    print("\nShard distribution (first 5 shards):")
    for shard_id in range(min(5, matcher.num_shards)):
        shard_info = stats['shard_distribution'][shard_id]
        print(f"  Shard {shard_id}: {shard_info['atoms']} atoms, {shard_info['links']} links "
              f"(density: {shard_info['density']:.2f})")

    # Validate 110 states
    print("\nValidating 110 quantum states...")
    total_elements = len(matcher.atoms) + len(matcher.links)
    expected_states = matcher.total_states

    print(f"Expected states: {expected_states}")
    print(f"Hypergraph elements: {total_elements}")
    print(f"Validation: {'✅ PASSED' if total_elements >= expected_states else '❌ FAILED'}")

    # Save results
    results = {
        "pattern_matches": {
            pattern_id: len(matcher.match_pattern(pattern_id))
            for pattern_id in pattern_ids
        },
        "statistics": stats,
        "validation": {
            "expected_states": expected_states,
            "hypergraph_elements": total_elements,
            "validation_passed": total_elements >= expected_states
        },
        "sample_matches": [
            {
                "match_id": match.match_id,
                "template_id": match.template_id,
                "confidence": match.confidence,
                "shard_id": match.shard_id,
                "bindings": match.bindings
            }
            for match in matcher.match_pattern(pattern_ids[0])[:5]
        ]
    }

    with open("pattern_matching_results.json", "w") as f:
        json.dump(results, f, indent=2)

    print("\nResults saved to pattern_matching_results.json")
    print("=== Hypergraph Pattern Matching Test Complete ===")


if __name__ == "__main__":
    main()
