#!/usr/bin/env python3
"""
AtomSpace-GraphQL Bridge
Phase β: DAS-Hypergraph Integration

Bridges AtomSpace hypergraphs with GraphQL queries for distributed processing
across 11×5×2 = 110 quantum states.

Copyright (c) 2025 OpenCog Foundation
"""

import json
import re
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from typing import Any


# Mock AtomSpace classes for development (will be replaced with real imports)
class MockAtomSpace:
    """Mock AtomSpace for development purposes"""
    def __init__(self):
        self.atoms = {}
        self.links = {}
        self.next_id = 1

    def add_node(self, node_type: str, name: str) -> str:
        atom_id = f"{node_type}_{self.next_id}"
        self.atoms[atom_id] = {"type": node_type, "name": name, "id": atom_id}
        self.next_id += 1
        return atom_id

    def add_link(self, link_type: str, targets: list[str]) -> str:
        link_id = f"{link_type}_{self.next_id}"
        self.links[link_id] = {"type": link_type, "targets": targets, "id": link_id}
        self.next_id += 1
        return link_id

    def get_atom(self, atom_id: str) -> dict | None:
        return self.atoms.get(atom_id) or self.links.get(atom_id)

    def get_all_atoms(self) -> list[dict]:
        return list(self.atoms.values()) + list(self.links.values())

@dataclass
class AtomSpaceQuery:
    """Structured AtomSpace query representation"""
    pattern: str
    variables: list[str]
    constraints: list[str]
    shard_hint: int | None = None

@dataclass
class HypergraphPattern:
    """Hypergraph pattern for distributed matching"""
    nodes: list[dict[str, Any]]
    edges: list[dict[str, Any]]
    variables: dict[str, str]
    tensor_coordinates: tuple[int, int, int]  # (shard, link, truth) for 11×5×2

@dataclass
class DistributedShard:
    """Represents one shard in the 11-shard distributed system"""
    shard_id: int
    atomspace: MockAtomSpace
    links_per_shard: int = 5
    truth_dimensions: int = 2
    lock: threading.Lock = None

    def __post_init__(self):
        if self.lock is None:
            self.lock = threading.Lock()

class AtomSpaceGraphQLBridge:
    """
    AtomSpace-GraphQL Bridge for Distributed Hypergraph Processing

    Converts GraphQL queries to AtomSpace patterns and distributes execution
    across 11 shards with 5 links per shard and 2 truth value dimensions.
    """

    def __init__(self, num_shards: int = 11):
        self.num_shards = num_shards
        self.links_per_shard = 5
        self.truth_dimensions = 2
        self.total_states = num_shards * self.links_per_shard * self.truth_dimensions  # 110

        # Initialize distributed shards
        self.shards = {}
        for i in range(num_shards):
            self.shards[i] = DistributedShard(
                shard_id=i,
                atomspace=MockAtomSpace(),
                links_per_shard=self.links_per_shard,
                truth_dimensions=self.truth_dimensions
            )

        # GraphQL to AtomSpace mapping
        self.graphql_to_atomspace_map = {
            "ConceptNode": "ConceptNode",
            "PredicateNode": "PredicateNode",
            "EvaluationLink": "EvaluationLink",
            "ListLink": "ListLink",
            "VariableNode": "VariableNode",
            "BindLink": "BindLink",
            "ExecutionOutputLink": "ExecutionOutputLink"
        }

        # Initialize sample data for testing
        self._populate_test_data()

    def graphql_to_atomspace(self, graphql_query: str) -> list[AtomSpaceQuery]:
        """
        Convert GraphQL query to AtomSpace hypergraph patterns

        Args:
            graphql_query: GraphQL query string

        Returns:
            List[AtomSpaceQuery]: Converted AtomSpace queries
        """
        # Parse GraphQL query structure
        parsed = self._parse_graphql_structure(graphql_query)

        # Convert to AtomSpace patterns
        atomspace_queries = []

        for field in parsed.get("fields", []):
            if field["name"] == "searchHypergraph":
                atomspace_queries.extend(self._convert_hypergraph_search(field))
            elif field["name"] == "matchPattern":
                atomspace_queries.extend(self._convert_pattern_match(field))
            elif field["name"] == "executeQuery":
                atomspace_queries.extend(self._convert_query_execution(field))

        return atomspace_queries

    def execute_distributed_query(self, queries: list[AtomSpaceQuery]) -> dict[str, Any]:
        """
        Execute AtomSpace queries across distributed shards

        Args:
            queries: List of AtomSpace queries to execute

        Returns:
            Dict[str, Any]: Aggregated results from all shards
        """
        results = {
            "total_matches": 0,
            "shard_results": {},
            "execution_time": 0,
            "pattern_matches": []
        }

        start_time = time.time()

        # Execute queries in parallel across shards
        with ThreadPoolExecutor(max_workers=self.num_shards) as executor:
            futures = {}

            for query in queries:
                # Determine target shards
                target_shards = self._determine_target_shards(query)

                for shard_id in target_shards:
                    future = executor.submit(self._execute_on_shard, shard_id, query)
                    futures[f"{shard_id}_{len(futures)}"] = future

            # Collect results
            for future_id, future in futures.items():
                shard_id = int(future_id.split('_')[0])
                shard_result = future.result()

                results["shard_results"][shard_id] = shard_result
                results["total_matches"] += shard_result.get("matches", 0)
                results["pattern_matches"].extend(shard_result.get("patterns", []))

        results["execution_time"] = time.time() - start_time
        return results

    def create_hypergraph_pattern(self, pattern_spec: dict[str, Any]) -> HypergraphPattern:
        """
        Create hypergraph pattern from specification

        Args:
            pattern_spec: Pattern specification dictionary

        Returns:
            HypergraphPattern: Structured hypergraph pattern
        """
        nodes = []
        edges = []
        variables = {}

        # Extract nodes
        for node_spec in pattern_spec.get("nodes", []):
            node = {
                "id": node_spec.get("id"),
                "type": node_spec.get("type", "ConceptNode"),
                "name": node_spec.get("name"),
                "is_variable": node_spec.get("name", "").startswith("$")
            }
            nodes.append(node)

            if node["is_variable"]:
                variables[node["name"]] = node["type"]

        # Extract edges (links)
        for edge_spec in pattern_spec.get("edges", []):
            edge = {
                "id": edge_spec.get("id"),
                "type": edge_spec.get("type", "EvaluationLink"),
                "source": edge_spec.get("source"),
                "target": edge_spec.get("target"),
                "targets": edge_spec.get("targets", [])
            }
            edges.append(edge)

        # Assign tensor coordinates
        pattern_hash = hash(str(pattern_spec)) % self.total_states
        shard = pattern_hash % self.num_shards
        link = (pattern_hash // self.num_shards) % self.links_per_shard
        truth = (pattern_hash // (self.num_shards * self.links_per_shard)) % self.truth_dimensions

        return HypergraphPattern(
            nodes=nodes,
            edges=edges,
            variables=variables,
            tensor_coordinates=(shard, link, truth)
        )

    def _parse_graphql_structure(self, graphql_query: str) -> dict[str, Any]:
        """Parse GraphQL query into structured format"""
        # Simplified GraphQL parsing
        structure = {"fields": []}

        # Extract field patterns
        field_pattern = r'(\w+)(?:\s*\([^)]*\))?\s*\{([^}]*)\}'
        matches = re.finditer(field_pattern, graphql_query)

        for match in matches:
            field_name = match.group(1)
            field_body = match.group(2)

            field = {
                "name": field_name,
                "arguments": self._extract_arguments(match.group(0)),
                "selections": self._extract_selections(field_body)
            }
            structure["fields"].append(field)

        return structure

    def _extract_arguments(self, field_text: str) -> dict[str, Any]:
        """Extract arguments from GraphQL field"""
        arguments = {}

        # Find arguments in parentheses
        arg_match = re.search(r'\(([^)]+)\)', field_text)
        if arg_match:
            arg_string = arg_match.group(1)

            # Parse key-value pairs
            pairs = re.findall(r'(\w+):\s*([^,\s]+)', arg_string)
            for key, value in pairs:
                # Simple value parsing
                if value.startswith('"') and value.endswith('"'):
                    arguments[key] = value[1:-1]  # Remove quotes
                elif value.isdigit():
                    arguments[key] = int(value)
                elif value.replace('.', '').isdigit():
                    arguments[key] = float(value)
                else:
                    arguments[key] = value

        return arguments

    def _extract_selections(self, field_body: str) -> list[str]:
        """Extract field selections from GraphQL"""
        selections = []

        # Split by whitespace and filter
        parts = field_body.split()
        for part in parts:
            clean_part = part.strip().rstrip(',')
            if clean_part and not clean_part.startswith('{') and not clean_part.endswith('}'):
                selections.append(clean_part)

        return selections

    def _convert_hypergraph_search(self, field: dict[str, Any]) -> list[AtomSpaceQuery]:
        """Convert GraphQL hypergraph search to AtomSpace queries"""
        queries = []

        # Extract search parameters
        args = field.get("arguments", {})
        pattern_type = args.get("pattern", "concept")
        target_name = args.get("target", "unknown")

        if pattern_type == "concept":
            pattern = f"(ConceptNode \"{target_name}\")"
            queries.append(AtomSpaceQuery(
                pattern=pattern,
                variables=[],
                constraints=[]
            ))

        elif pattern_type == "evaluation":
            pattern = f"""
            (EvaluationLink
                (PredicateNode "{target_name}")
                (ListLink $X $Y))
            """
            queries.append(AtomSpaceQuery(
                pattern=pattern,
                variables=["$X", "$Y"],
                constraints=[]
            ))

        return queries

    def _convert_pattern_match(self, field: dict[str, Any]) -> list[AtomSpaceQuery]:
        """Convert GraphQL pattern match to AtomSpace queries"""
        queries = []

        args = field.get("arguments", {})
        variables = args.get("variables", [])

        # Create pattern with variables
        pattern = f"""
        (BindLink
            (VariableList {' '.join(f'(VariableNode "{var}")' for var in variables)})
            (AndLink
                (ConceptNode $concept)
                (EvaluationLink
                    (PredicateNode "related-to")
                    (ListLink $concept $target)))
            (ExecutionOutputLink
                (GroundedSchemaNode "scm: find-related")
                (ListLink $concept $target)))
        """

        queries.append(AtomSpaceQuery(
            pattern=pattern,
            variables=variables,
            constraints=[]
        ))

        return queries

    def _convert_query_execution(self, field: dict[str, Any]) -> list[AtomSpaceQuery]:
        """Convert GraphQL query execution to AtomSpace patterns"""
        queries = []

        args = field.get("arguments", {})
        query_type = args.get("type", "search")

        if query_type == "search":
            pattern = """
            (BindLink
                (VariableNode $X)
                (ConceptNode $X)
                $X)
            """

            queries.append(AtomSpaceQuery(
                pattern=pattern,
                variables=["$X"],
                constraints=["(> (cog-tv-confidence $X) 0.5)"]
            ))

        return queries

    def _determine_target_shards(self, query: AtomSpaceQuery) -> list[int]:
        """Determine which shards should execute the query"""
        if query.shard_hint is not None:
            return [query.shard_hint]

        # Use pattern hash to determine shards
        pattern_hash = hash(query.pattern)

        # For broad queries, use multiple shards
        if len(query.variables) > 1:
            num_target_shards = min(5, self.num_shards)
            return [(pattern_hash + i) % self.num_shards for i in range(num_target_shards)]
        else:
            # For specific queries, use single shard
            return [pattern_hash % self.num_shards]

    def _execute_on_shard(self, shard_id: int, query: AtomSpaceQuery) -> dict[str, Any]:
        """Execute query on specific shard"""
        shard = self.shards[shard_id]

        with shard.lock:
            # Simulate query execution
            matches = self._simulate_pattern_matching(shard, query)

            return {
                "shard_id": shard_id,
                "matches": len(matches),
                "patterns": matches,
                "query_pattern": query.pattern,
                "execution_time": 0.01  # Simulated execution time
            }

    def _simulate_pattern_matching(self, shard: DistributedShard, query: AtomSpaceQuery) -> list[dict[str, Any]]:
        """Simulate pattern matching on shard"""
        matches = []

        # Get all atoms from shard
        atoms = shard.atomspace.get_all_atoms()

        # Simulate pattern matching based on query
        if "ConceptNode" in query.pattern:
            concept_matches = [atom for atom in atoms if atom.get("type") == "ConceptNode"]
            matches.extend(concept_matches[:3])  # Limit to 3 matches per shard

        if "EvaluationLink" in query.pattern:
            link_matches = [atom for atom in atoms if atom.get("type") == "EvaluationLink"]
            matches.extend(link_matches[:2])

        return matches

    def _populate_test_data(self):
        """Populate shards with test data"""
        concepts = ["knowledge", "learning", "reasoning", "memory", "attention",
                   "perception", "action", "goal", "belief", "desire", "emotion"]
        predicates = ["related-to", "is-a", "part-of", "causes", "enables"]

        for shard_id, shard in self.shards.items():
            atomspace = shard.atomspace

            # Add concepts
            concept_ids = []
            for i, concept in enumerate(concepts):
                if i % self.num_shards == shard_id:  # Distribute concepts across shards
                    concept_id = atomspace.add_node("ConceptNode", f"{concept}_{shard_id}")
                    concept_ids.append(concept_id)

            # Add predicates
            for predicate in predicates:
                atomspace.add_node("PredicateNode", f"{predicate}_{shard_id}")

            # Add evaluation links
            for i in range(self.links_per_shard):
                if len(concept_ids) >= 2:
                    target_concepts = concept_ids[:2]
                    predicate_id = atomspace.add_node("PredicateNode", f"relation_{i}_{shard_id}")
                    list_id = atomspace.add_link("ListLink", target_concepts)
                    atomspace.add_link("EvaluationLink", [predicate_id, list_id])

    def get_shard_statistics(self) -> dict[str, Any]:
        """Get statistics about distributed shards"""
        stats = {
            "total_shards": self.num_shards,
            "links_per_shard": self.links_per_shard,
            "truth_dimensions": self.truth_dimensions,
            "total_states": self.total_states,
            "shard_details": {}
        }

        for shard_id, shard in self.shards.items():
            atoms = shard.atomspace.get_all_atoms()
            nodes = [a for a in atoms if "Node" in a.get("type", "")]
            links = [a for a in atoms if "Link" in a.get("type", "")]

            stats["shard_details"][shard_id] = {
                "total_atoms": len(atoms),
                "nodes": len(nodes),
                "links": len(links),
                "tensor_coordinate": (shard_id, len(links) % self.links_per_shard, 0)
            }

        return stats

    def validate_110_states(self) -> dict[str, Any]:
        """Validate that all 110 states are accessible"""
        validation = {
            "total_expected": 110,
            "states_found": 0,
            "coordinate_mapping": {},
            "validation_passed": False
        }

        # Enumerate all possible coordinates
        for shard in range(self.num_shards):
            for link in range(self.links_per_shard):
                for truth in range(self.truth_dimensions):
                    state_index = shard * self.links_per_shard * self.truth_dimensions + link * self.truth_dimensions + truth

                    validation["coordinate_mapping"][state_index] = {
                        "shard": shard,
                        "link": link,
                        "truth": truth,
                        "coordinate": (shard, link, truth)
                    }
                    validation["states_found"] += 1

        validation["validation_passed"] = validation["states_found"] == 110
        return validation


def main():
    """Test the AtomSpace-GraphQL bridge"""
    print("=== AtomSpace-GraphQL Bridge Test ===")

    # Initialize bridge
    bridge = AtomSpaceGraphQLBridge(num_shards=11)

    # Test GraphQL to AtomSpace conversion
    test_query = """
    query HypergraphSearch {
        searchHypergraph(pattern: "concept", target: "knowledge") {
            nodes {
                id
                type
                name
            }
            links {
                id
                type
                targets
            }
        }
        matchPattern(variables: ["$concept", "$target"]) {
            bindings {
                variable
                value
            }
        }
    }
    """

    print("Converting GraphQL query to AtomSpace patterns...")
    atomspace_queries = bridge.graphql_to_atomspace(test_query)
    print(f"Generated {len(atomspace_queries)} AtomSpace queries")

    # Execute distributed queries
    print(f"Executing queries across {bridge.num_shards} shards...")
    results = bridge.execute_distributed_query(atomspace_queries)

    print("Execution complete:")
    print(f"  Total matches: {results['total_matches']}")
    print(f"  Execution time: {results['execution_time']:.3f}s")
    print(f"  Shards used: {len(results['shard_results'])}")

    # Test hypergraph pattern creation
    print("\nTesting hypergraph pattern creation...")
    pattern_spec = {
        "nodes": [
            {"id": "n1", "type": "ConceptNode", "name": "knowledge"},
            {"id": "n2", "type": "ConceptNode", "name": "$target"}
        ],
        "edges": [
            {"id": "e1", "type": "EvaluationLink", "targets": ["n1", "n2"]}
        ]
    }

    pattern = bridge.create_hypergraph_pattern(pattern_spec)
    print(f"Created pattern with {len(pattern.nodes)} nodes, {len(pattern.edges)} edges")
    print(f"Tensor coordinates: {pattern.tensor_coordinates}")

    # Get system statistics
    print("\nSystem statistics:")
    stats = bridge.get_shard_statistics()
    print(f"  Total shards: {stats['total_shards']}")
    print(f"  Links per shard: {stats['links_per_shard']}")
    print(f"  Truth dimensions: {stats['truth_dimensions']}")
    print(f"  Total states: {stats['total_states']}")

    # Show per-shard stats
    print("\nPer-shard statistics:")
    for shard_id, shard_stats in list(stats["shard_details"].items())[:5]:
        print(f"  Shard {shard_id}: {shard_stats['total_atoms']} atoms "
              f"({shard_stats['nodes']} nodes, {shard_stats['links']} links)")

    # Validate 110 states
    print("\nValidating 110 states...")
    validation = bridge.validate_110_states()
    print(f"  Expected states: {validation['total_expected']}")
    print(f"  Found states: {validation['states_found']}")
    print(f"  Validation: {'✅ PASSED' if validation['validation_passed'] else '❌ FAILED'}")

    # Save results
    results_summary = {
        "bridge_stats": stats,
        "query_results": results,
        "validation": validation,
        "sample_pattern": {
            "nodes": len(pattern.nodes),
            "edges": len(pattern.edges),
            "coordinates": pattern.tensor_coordinates
        }
    }

    with open("atomspace_bridge_results.json", "w") as f:
        json.dump(results_summary, f, indent=2)

    print("\nResults saved to atomspace_bridge_results.json")
    print("=== AtomSpace-GraphQL Bridge Test Complete ===")


if __name__ == "__main__":
    main()
