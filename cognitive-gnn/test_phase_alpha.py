#!/usr/bin/env python3
"""
Phase α Integration Test: GraphQL-GNN Foundation
Tests the 343-state (7×7×7) neural graph network system

Copyright (c) 2025 OpenCog Foundation
"""

import json
import sys
import time
import unittest

import numpy as np
from message_passing import MessagePassingEngine
from query_parser import GraphQLQueryParser

# Import our implementations
from schema_generator import NeuralSchemaGenerator


class PhaseAlphaIntegrationTest(unittest.TestCase):
    """Integration tests for Phase α: GraphQL-GNN Foundation"""

    def setUp(self):
        """Set up test components"""
        self.schema_generator = NeuralSchemaGenerator()
        self.message_engine = MessagePassingEngine(embedding_dim=64)
        self.query_parser = GraphQLQueryParser()

        self.test_results = {}

    def test_343_states_enumeration(self):
        """Test that we can enumerate all 343 states in 7×7×7 tensor"""
        print("\n=== Testing 343 State Enumeration ===")

        states = self.schema_generator.enumerate_all_states()

        # Validate count
        self.assertEqual(len(states), 343, "Should have exactly 343 states")

        # Validate range
        self.assertEqual(min(states), 0, "Minimum state should be 0")
        self.assertEqual(max(states), 342, "Maximum state should be 342")

        # Validate uniqueness
        self.assertEqual(len(set(states)), 343, "All states should be unique")

        self.test_results["state_enumeration"] = {
            "total_states": len(states),
            "min_state": min(states),
            "max_state": max(states),
            "unique_states": len(set(states)),
            "passed": True,
        }

        print(f"✅ State enumeration: {len(states)} states")

    def test_prime_factorization(self):
        """Test prime factorization of 343 = 7³"""
        print("\n=== Testing Prime Factorization ===")

        factors = self.schema_generator.validate_prime_factorization(343)
        expected_factors = [7, 7, 7]  # 7³

        self.assertEqual(factors, expected_factors, f"343 should factor as 7³, got {factors}")

        # Test the product
        product = 1
        for factor in factors:
            product *= factor
        self.assertEqual(product, 343, "Product of factors should equal 343")

        self.test_results["prime_factorization"] = {
            "target": 343,
            "factors": factors,
            "expected": expected_factors,
            "product": product,
            "passed": factors == expected_factors,
        }

        print(f"✅ Prime factorization: 343 = {' × '.join(map(str, factors))}")

    def test_neural_graph_creation(self):
        """Test creation of 7×7×7 neural graph"""
        print("\n=== Testing Neural Graph Creation ===")

        graph = self.message_engine.create_test_graph()

        # Validate node count (7³ = 343)
        self.assertEqual(len(graph.nodes), 343, "Should have 343 nodes")

        # Validate tensor shape
        self.assertEqual(graph.tensor_shape, (7, 7, 7), "Tensor shape should be (7, 7, 7)")

        # Validate coordinates are within bounds
        for node in graph.nodes.values():
            x, y, z = node.coordinates
            self.assertTrue(0 <= x < 7, f"X coordinate {x} out of bounds")
            self.assertTrue(0 <= y < 7, f"Y coordinate {y} out of bounds")
            self.assertTrue(0 <= z < 7, f"Z coordinate {z} out of bounds")

        # Validate embeddings
        for node in graph.nodes.values():
            self.assertEqual(len(node.embedding), 64, "Embedding should be 64-dimensional")
            self.assertTrue(np.isfinite(node.embedding).all(), "Embedding should contain finite values")

        # Count edges (approximately 6 * 343 for 6-connectivity, minus boundary effects)
        edge_count = len(graph.edges)
        expected_min_edges = 300  # Conservative estimate accounting for boundaries
        expected_max_edges = 2500  # Liberal estimate

        self.assertTrue(
            expected_min_edges <= edge_count <= expected_max_edges, f"Edge count {edge_count} outside expected range"
        )

        self.test_results["neural_graph_creation"] = {
            "node_count": len(graph.nodes),
            "edge_count": edge_count,
            "tensor_shape": graph.tensor_shape,
            "embedding_dim": len(next(iter(graph.nodes.values())).embedding),
            "passed": True,
        }

        print(f"✅ Neural graph: {len(graph.nodes)} nodes, {edge_count} edges")

    def test_message_passing_performance(self):
        """Test message passing across 7 layers with performance benchmarks"""
        print("\n=== Testing Message Passing Performance ===")

        # Create test graph
        graph = self.message_engine.create_test_graph()

        # Time the message passing
        start_time = time.time()
        updated_graph = self.message_engine.neural_propagation(graph)
        end_time = time.time()

        processing_time = end_time - start_time

        # Validate processing completed
        self.assertIsNotNone(updated_graph, "Message passing should return updated graph")
        self.assertEqual(len(updated_graph.nodes), 343, "Node count should be preserved")

        # Validate attention scores were updated
        attention_scores = [node.attention_score for node in updated_graph.nodes.values()]
        self.assertTrue(
            all(0.0 <= score <= 1.0 for score in attention_scores), "Attention scores should be in [0, 1] range"
        )

        # Performance benchmark: should process 343 nodes in reasonable time
        max_allowed_time = 30.0  # 30 seconds
        self.assertTrue(
            processing_time <= max_allowed_time,
            f"Processing took {processing_time:.2f}s, should be <= {max_allowed_time}s",
        )

        # Benchmark: nodes per second
        nodes_per_second = 343 / processing_time
        min_throughput = 10  # At least 10 nodes per second
        self.assertTrue(
            nodes_per_second >= min_throughput,
            f"Throughput {nodes_per_second:.1f} nodes/s should be >= {min_throughput}",
        )

        self.test_results["message_passing_performance"] = {
            "processing_time": processing_time,
            "nodes_per_second": nodes_per_second,
            "attention_score_range": [min(attention_scores), max(attention_scores)],
            "final_state": updated_graph.current_state,
            "passed": True,
        }

        print(f"✅ Message passing: {processing_time:.2f}s, {nodes_per_second:.1f} nodes/s")

    def test_graphql_schema_generation(self):
        """Test GraphQL schema generation with neural directives"""
        print("\n=== Testing GraphQL Schema Generation ===")

        schema = self.schema_generator.generate_schema()

        # Validate schema contains required components
        required_types = ["NeuralNode", "NeuralEdge", "NeuralGraph", "AttentionHead"]
        for type_name in required_types:
            self.assertIn(f"type {type_name}", schema, f"Schema should contain {type_name} type")

        # Validate neural directives
        required_directives = ["@neural_attention", "@message_passing", "@tensor_reshape", "@cognitive_primitive"]
        for directive in required_directives:
            self.assertIn(directive, schema, f"Schema should contain {directive} directive")

        # Validate operations
        required_operations = ["Query", "Mutation", "Subscription"]
        for operation in required_operations:
            self.assertIn(f"type {operation}", schema, f"Schema should contain {operation} type")

        # Validate specific queries
        required_queries = ["getNeuralGraph", "getAttentionState", "performMessagePassing"]
        for query in required_queries:
            self.assertIn(query, schema, f"Schema should contain {query} query")

        self.test_results["graphql_schema"] = {
            "schema_length": len(schema),
            "types_found": len([t for t in required_types if f"type {t}" in schema]),
            "directives_found": len([d for d in required_directives if d in schema]),
            "operations_found": len([o for o in required_operations if f"type {o}" in schema]),
            "passed": True,
        }

        print(f"✅ GraphQL schema: {len(schema)} characters")

    def test_query_parsing_and_conversion(self):
        """Test GraphQL query parsing and conversion to neural graphs"""
        print("\n=== Testing Query Parsing and Conversion ===")

        test_query = """
        query TestQuery($nodeId: ID!) {
            getNeuralGraph(id: $nodeId) {
                nodes {
                    id
                    embedding
                    attention_score
                }
                edges {
                    source
                    target
                    weight
                }
            }
            getAttentionState(layer: 3, head: 4) @neural_attention(head: 4, weight: 0.8) {
                attention_weights
            }
        }
        """

        # Parse query
        parsed_query = self.query_parser.parse_query(test_query)

        # Validate parsing
        self.assertEqual(parsed_query.operation_type.value, "query", "Should be a query operation")
        self.assertEqual(parsed_query.operation_name, "TestQuery", "Should have correct name")
        self.assertGreater(len(parsed_query.fields), 0, "Should have fields")

        # Convert to neural graph
        neural_graph = self.query_parser.query_to_neural_graph(parsed_query)

        # Validate neural graph
        self.assertGreater(len(neural_graph.nodes), 0, "Should have nodes")
        self.assertGreater(len(neural_graph.edges), 0, "Should have edges")
        self.assertEqual(neural_graph.tensor_shape, (7, 7, 7), "Should have correct tensor shape")
        self.assertIsNotNone(neural_graph.query_embedding, "Should have query embedding")
        self.assertEqual(neural_graph.query_embedding.shape, (64,), "Query embedding should be 64-dimensional")

        # Validate attention weights
        self.assertEqual(neural_graph.attention_weights.shape, (7, 7), "Attention weights should be 7×7")

        self.test_results["query_parsing"] = {
            "operation_type": parsed_query.operation_type.value,
            "operation_name": parsed_query.operation_name,
            "field_count": len(parsed_query.fields),
            "node_count": len(neural_graph.nodes),
            "edge_count": len(neural_graph.edges),
            "embedding_shape": neural_graph.query_embedding.shape,
            "attention_shape": neural_graph.attention_weights.shape,
            "passed": True,
        }

        print(f"✅ Query parsing: {len(neural_graph.nodes)} nodes, {len(neural_graph.edges)} edges")

    def test_attention_encoding(self):
        """Test attention state encoding to 7×7×7 coordinates"""
        print("\n=== Testing Attention Encoding ===")

        # Test all valid layer/head combinations
        valid_encodings = 0
        for layer in range(7):
            for head in range(7):
                coords = self.schema_generator.encode_attention_state(layer, head)

                # Validate coordinates are in bounds
                self.assertEqual(len(coords), 3, "Should return 3D coordinates")
                self.assertTrue(
                    all(0 <= c < 7 for c in coords),
                    f"Coordinates {coords} out of bounds for layer={layer}, head={head}",
                )

                valid_encodings += 1

        # Should have tested 7×7 = 49 combinations
        self.assertEqual(valid_encodings, 49, "Should test 49 layer/head combinations")

        # Test invalid inputs
        with self.assertRaises(ValueError):
            self.schema_generator.encode_attention_state(-1, 0)

        with self.assertRaises(ValueError):
            self.schema_generator.encode_attention_state(0, 7)

        self.test_results["attention_encoding"] = {
            "valid_encodings": valid_encodings,
            "expected_encodings": 49,
            "bounds_checking": True,
            "passed": True,
        }

        print(f"✅ Attention encoding: {valid_encodings}/49 combinations valid")

    def test_tensor_shape_consistency(self):
        """Test that all components maintain 7×7×7 tensor shape consistency"""
        print("\n=== Testing Tensor Shape Consistency ===")

        # Schema generator
        metadata = self.schema_generator.get_state_metadata()
        self.assertEqual(metadata["tensor_shape"], (7, 7, 7), "Schema generator tensor shape")
        self.assertEqual(metadata["total_states"], 343, "Schema generator total states")

        # Message passing engine
        graph = self.message_engine.create_test_graph()
        self.assertEqual(graph.tensor_shape, (7, 7, 7), "Message engine tensor shape")

        # Query parser
        parser_shape = self.query_parser.tensor_shape
        self.assertEqual(parser_shape, (7, 7, 7), "Query parser tensor shape")

        # Test neural graph from query
        test_query = 'query { getNeuralGraph(id: "test") { nodes { id } } }'
        neural_graph = self.query_parser.query_to_neural_graph(test_query)
        self.assertEqual(neural_graph.tensor_shape, (7, 7, 7), "Neural graph tensor shape")

        self.test_results["tensor_consistency"] = {
            "schema_generator_shape": metadata["tensor_shape"],
            "message_engine_shape": graph.tensor_shape,
            "query_parser_shape": parser_shape,
            "neural_graph_shape": neural_graph.tensor_shape,
            "all_consistent": True,
            "passed": True,
        }

        print("✅ Tensor shape consistency: All components use (7, 7, 7)")

    def test_integration_end_to_end(self):
        """Test complete end-to-end integration"""
        print("\n=== Testing End-to-End Integration ===")

        # 1. Generate schema
        schema = self.schema_generator.generate_schema()
        self.assertGreater(len(schema), 1000, "Schema should be substantial")

        # 2. Parse a complex query
        complex_query = """
        query ComplexQuery {
            getNeuralGraph(id: "test") {
                nodes {
                    id
                    embedding
                    coordinates
                    attention_score
                }
                edges {
                    source
                    target
                    weight
                    message_vector
                }
                tensor_shape
                current_state
            }
            performMessagePassing(graph: "test", layers: 7) @message_passing(layers: 7, aggregation: "mean") {
                nodes {
                    attention_score
                }
            }
        }
        """

        parsed = self.query_parser.parse_query(complex_query)
        neural_graph = self.query_parser.query_to_neural_graph(parsed)

        # 3. Create actual neural graph for processing
        processing_graph = self.message_engine.create_test_graph()

        # 4. Execute message passing
        result_graph = self.message_engine.neural_propagation(processing_graph)

        # 5. Validate complete pipeline
        self.assertEqual(len(result_graph.nodes), 343, "Should preserve all 343 nodes")
        self.assertGreater(result_graph.current_state, 0, "Should have valid current state")
        self.assertTrue(0 <= result_graph.current_state < 343, "Current state should be in valid range")

        # 6. Validate attention allocation
        attention_scores = [node.attention_score for node in result_graph.nodes.values()]
        self.assertTrue(
            all(0.0 <= score <= 1.0 for score in attention_scores), "All attention scores should be normalized"
        )

        total_attention = sum(attention_scores)
        self.assertGreater(total_attention, 0, "Should have non-zero total attention")

        self.test_results["end_to_end_integration"] = {
            "schema_generated": len(schema) > 1000,
            "query_parsed": len(parsed.fields) > 0,
            "neural_graph_created": len(neural_graph.nodes) > 0,
            "processing_completed": len(result_graph.nodes) == 343,
            "attention_allocated": total_attention > 0,
            "current_state_valid": 0 <= result_graph.current_state < 343,
            "passed": True,
        }

        print("✅ End-to-end integration: Complete pipeline working")

    def tearDown(self):
        """Save test results"""

        # Convert numpy arrays and other non-serializable objects
        def make_serializable(obj):
            if hasattr(obj, "tolist"):  # numpy arrays
                return obj.tolist()
            elif isinstance(obj, np.integer | int):
                return int(obj)
            elif isinstance(obj, np.floating | float):
                return float(obj)
            elif isinstance(obj, bool):
                return bool(obj)
            elif isinstance(obj, tuple):
                return [make_serializable(item) for item in obj]
            elif isinstance(obj, dict):
                return {str(k): make_serializable(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [make_serializable(item) for item in obj]
            elif obj is None:
                return None
            else:
                return str(obj)  # Convert unknown types to string

        try:
            serializable_results = make_serializable(self.test_results)
            with open("phase_alpha_test_results.json", "w") as f:
                json.dump(serializable_results, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save test results: {e}")
            # Save simple summary instead
            summary = {"test_count": len(self.test_results), "tests_run": list(self.test_results.keys())}
            with open("phase_alpha_test_results.json", "w") as f:
                json.dump(summary, f, indent=2)


def run_comprehensive_test():
    """Run comprehensive Phase α integration test"""
    print("🌌 Phase α: GraphQL-GNN Foundation Integration Test")
    print("=" * 60)

    # Run unit tests
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(PhaseAlphaIntegrationTest)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Summary
    print("\n" + "=" * 60)
    print("🎯 PHASE α INTEGRATION TEST SUMMARY")
    print("=" * 60)

    total_tests = result.testsRun
    failures = len(result.failures)
    errors = len(result.errors)
    passed = total_tests - failures - errors

    print(f"Total Tests: {total_tests}")
    print(f"Passed: {passed}")
    print(f"Failed: {failures}")
    print(f"Errors: {errors}")

    if failures == 0 and errors == 0:
        print("\n✅ ALL TESTS PASSED - Phase α Foundation Ready!")
        print("🚀 343 quantum states operational")
        print("🧠 7×7×7 tensor architecture validated")
        print("📊 GraphQL-GNN integration successful")
    else:
        print(f"\n❌ {failures + errors} tests failed")

    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_comprehensive_test()
    sys.exit(0 if success else 1)
