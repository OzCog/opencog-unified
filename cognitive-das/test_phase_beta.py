#!/usr/bin/env python3
"""
Phase β Integration Test: DAS-Hypergraph Integration
Tests the 110-state (11×5×2) distributed AtomSpace system

Copyright (c) 2025 OpenCog Foundation
"""

import json
import sys
import time
import unittest

# Import our Phase β implementations
from atomspace_bridge import AtomSpaceGraphQLBridge
from pattern_matcher import HypergraphPatternMatcher
from shard_manager import DistributedShardExecutor


class PhaseBetaIntegrationTest(unittest.TestCase):
    """Integration tests for Phase β: DAS-Hypergraph Integration"""

    def setUp(self):
        """Set up test components"""
        self.bridge = AtomSpaceGraphQLBridge(num_shards=11)
        self.executor = DistributedShardExecutor(num_shards=11, links_per_shard=5, truth_dimensions=2)
        self.matcher = HypergraphPatternMatcher(num_shards=11, links_per_shard=5, truth_dimensions=2)

        self.test_results = {}

    def test_110_states_validation(self):
        """Test that we can access all 110 states in 11×5×2 tensor"""
        print("\n=== Testing 110 State Validation ===")

        # Test bridge validation
        bridge_validation = self.bridge.validate_110_states()
        self.assertTrue(bridge_validation["validation_passed"], "Bridge should validate 110 states")
        self.assertEqual(bridge_validation["states_found"], 110, "Should find exactly 110 states")

        # Test executor state coverage
        total_executor_states = self.executor.total_states
        self.assertEqual(total_executor_states, 110, "Executor should have 110 total states")

        # Test matcher state coverage
        total_matcher_states = self.matcher.total_states
        self.assertEqual(total_matcher_states, 110, "Matcher should have 110 total states")

        self.test_results['state_validation'] = {
            'bridge_states': bridge_validation["states_found"],
            'executor_states': total_executor_states,
            'matcher_states': total_matcher_states,
            'all_valid': all([
                bridge_validation["validation_passed"],
                total_executor_states == 110,
                total_matcher_states == 110
            ]),
            'passed': True
        }

        print(f"✅ State validation: {bridge_validation['states_found']}/110 states accessible")

    def test_prime_factorization_110(self):
        """Test prime factorization of 110 = 2×5×11"""
        print("\n=== Testing Prime Factorization of 110 ===")

        def prime_factorize(n):
            factors = []
            d = 2
            while d * d <= n:
                while n % d == 0:
                    factors.append(d)
                    n //= d
                d += 1
            if n > 1:
                factors.append(n)
            return factors

        factors = prime_factorize(110)
        expected_factors = [2, 5, 11]

        self.assertEqual(sorted(factors), sorted(expected_factors),
                        f"110 should factor as 2×5×11, got {factors}")

        # Verify the tensor dimensions
        self.assertEqual(self.bridge.num_shards, 11, "Should have 11 shards")
        self.assertEqual(self.bridge.links_per_shard, 5, "Should have 5 links per shard")
        self.assertEqual(self.bridge.truth_dimensions, 2, "Should have 2 truth dimensions")

        product = self.bridge.num_shards * self.bridge.links_per_shard * self.bridge.truth_dimensions
        self.assertEqual(product, 110, "Product should equal 110")

        self.test_results['prime_factorization'] = {
            'target': 110,
            'factors': factors,
            'expected': expected_factors,
            'tensor_dimensions': (11, 5, 2),
            'product': product,
            'passed': factors == expected_factors and product == 110
        }

        print(f"✅ Prime factorization: 110 = {' × '.join(map(str, factors))}")

    def test_atomspace_bridge_conversion(self):
        """Test GraphQL to AtomSpace conversion"""
        print("\n=== Testing AtomSpace Bridge Conversion ===")

        test_query = """
        query HypergraphTest {
            searchHypergraph(pattern: "concept", target: "knowledge") {
                nodes { id type name }
                links { id type targets }
            }
            matchPattern(variables: ["$concept", "$relation"]) {
                bindings { variable value }
            }
        }
        """

        # Convert GraphQL to AtomSpace
        atomspace_queries = self.bridge.graphql_to_atomspace(test_query)

        self.assertGreater(len(atomspace_queries), 0, "Should generate AtomSpace queries")

        # Execute distributed queries
        results = self.bridge.execute_distributed_query(atomspace_queries)

        self.assertGreater(results["total_matches"], 0, "Should find matches")
        self.assertLess(results["execution_time"], 5.0, "Should execute within 5 seconds")

        # Test shard statistics
        stats = self.bridge.get_shard_statistics()
        self.assertEqual(stats["total_shards"], 11, "Should have 11 shards")
        self.assertEqual(stats["total_states"], 110, "Should have 110 total states")

        self.test_results['atomspace_bridge'] = {
            'queries_generated': len(atomspace_queries),
            'total_matches': results["total_matches"],
            'execution_time': results["execution_time"],
            'shards_used': len(results["shard_results"]),
            'stats_valid': stats["total_states"] == 110,
            'passed': True
        }

        print(f"✅ AtomSpace bridge: {len(atomspace_queries)} queries, {results['total_matches']} matches")

    def test_distributed_shard_execution(self):
        """Test distributed execution across shards"""
        print("\n=== Testing Distributed Shard Execution ===")

        # Create test patterns
        test_patterns = [
            {
                "pattern": "ConceptNode search",
                "variables": ["$concept"],
                "constraints": [],
                "priority": 1
            },
            {
                "pattern": "EvaluationLink match",
                "variables": ["$pred", "$arg1", "$arg2"],
                "constraints": ["strength > 0.5"],
                "priority": 2
            }
        ] * 5  # 10 total patterns

        # Execute patterns
        start_time = time.time()
        results = self.executor.execute_distributed(test_patterns)
        execution_time = time.time() - start_time

        # Validate results
        self.assertEqual(results["total_tasks"], len(test_patterns), "Should process all tasks")
        self.assertGreater(results["successful_tasks"], 0, "Should have successful tasks")
        self.assertLess(execution_time, 10.0, "Should complete within 10 seconds")

        # Check shard utilization
        self.assertGreater(len(results["shard_utilization"]), 0, "Should utilize shards")

        # Get performance report
        perf_report = self.executor.get_performance_report()
        self.assertEqual(perf_report["system_summary"]["total_states"], 110, "Should track 110 states")

        self.test_results['distributed_execution'] = {
            'total_patterns': len(test_patterns),
            'successful_tasks': results["successful_tasks"],
            'execution_time': execution_time,
            'shards_utilized': len(results["shard_utilization"]),
            'system_efficiency': perf_report["performance_summary"]["system_efficiency"],
            'passed': True
        }

        print(f"✅ Distributed execution: {results['successful_tasks']}/{len(test_patterns)} tasks completed")

    def test_hypergraph_pattern_matching(self):
        """Test hypergraph pattern matching"""
        print("\n=== Testing Hypergraph Pattern Matching ===")

        # Create sample patterns
        pattern_ids = self.matcher.create_sample_patterns()
        self.assertGreater(len(pattern_ids), 0, "Should create sample patterns")

        # Test pattern matching
        total_matches = 0
        for pattern_id in pattern_ids:
            matches = self.matcher.match_pattern(pattern_id)
            self.assertIsInstance(matches, list, "Should return list of matches")
            total_matches += len(matches)

        self.assertGreater(total_matches, 0, "Should find pattern matches")

        # Test shard-specific matching
        shard_matches = self.matcher.match_pattern(pattern_ids[0], target_shard=0)
        self.assertIsInstance(shard_matches, list, "Should return shard-specific matches")

        # Get statistics
        stats = self.matcher.get_matching_statistics()
        self.assertEqual(stats["hypergraph_stats"]["states_covered"], 110, "Should cover 110 states")
        self.assertGreater(stats["hypergraph_stats"]["total_atoms"], 0, "Should have atoms")
        self.assertGreater(stats["hypergraph_stats"]["total_links"], 0, "Should have links")

        self.test_results['pattern_matching'] = {
            'patterns_created': len(pattern_ids),
            'total_matches': total_matches,
            'atoms_count': stats["hypergraph_stats"]["total_atoms"],
            'links_count': stats["hypergraph_stats"]["total_links"],
            'states_covered': stats["hypergraph_stats"]["states_covered"],
            'cache_hit_rate': stats["cache_stats"]["hit_rate"],
            'passed': True
        }

        print(f"✅ Pattern matching: {total_matches} matches across {len(pattern_ids)} patterns")

    def test_tensor_coordinates_mapping(self):
        """Test 11×5×2 tensor coordinate mapping"""
        print("\n=== Testing Tensor Coordinate Mapping ===")

        # Test coordinate generation for all 110 states
        coordinates_found = set()

        for shard in range(11):
            for link in range(5):
                for truth in range(2):
                    coord = (shard, link, truth)
                    coordinates_found.add(coord)

        self.assertEqual(len(coordinates_found), 110, "Should generate 110 unique coordinates")

        # Test coordinate to state index mapping
        state_indices = set()
        for shard in range(11):
            for link in range(5):
                for truth in range(2):
                    state_index = shard * 5 * 2 + link * 2 + truth
                    state_indices.add(state_index)

        self.assertEqual(len(state_indices), 110, "Should generate 110 unique state indices")
        self.assertEqual(min(state_indices), 0, "Minimum state index should be 0")
        self.assertEqual(max(state_indices), 109, "Maximum state index should be 109")

        # Test reverse mapping
        reverse_coords = []
        for state_idx in range(110):
            shard = state_idx // (5 * 2)
            link = (state_idx % (5 * 2)) // 2
            truth = state_idx % 2
            reverse_coords.append((shard, link, truth))

        self.assertEqual(len(set(reverse_coords)), 110, "Reverse mapping should be unique")

        self.test_results['tensor_coordinates'] = {
            'coordinates_generated': len(coordinates_found),
            'state_indices_generated': len(state_indices),
            'min_state_index': min(state_indices),
            'max_state_index': max(state_indices),
            'reverse_mapping_unique': len(set(reverse_coords)) == 110,
            'passed': True
        }

        print("✅ Tensor coordinates: 110 unique mappings validated")

    def test_performance_benchmarks(self):
        """Test performance benchmarks for Phase β"""
        print("\n=== Testing Performance Benchmarks ===")

        # Benchmark 1: AtomSpace query conversion time
        test_query = "query { searchHypergraph(pattern: \"test\") { nodes { id } } }"

        start_time = time.time()
        for _ in range(100):
            self.bridge.graphql_to_atomspace(test_query)
        conversion_time = (time.time() - start_time) / 100

        self.assertLess(conversion_time, 0.01, "Query conversion should be < 10ms")

        # Benchmark 2: Distributed execution throughput
        small_patterns = [{"pattern": "test", "variables": [], "constraints": []}] * 20

        start_time = time.time()
        self.executor.execute_distributed(small_patterns)
        exec_time = time.time() - start_time

        throughput = len(small_patterns) / exec_time
        self.assertGreater(throughput, 10, "Should process > 10 patterns/sec")

        # Benchmark 3: Pattern matching speed
        start_time = time.time()
        for _ in range(10):
            self.matcher.match_pattern("find_concepts")
        match_time = (time.time() - start_time) / 10

        self.assertLess(match_time, 0.1, "Pattern matching should be < 100ms")

        self.test_results['performance_benchmarks'] = {
            'query_conversion_time': conversion_time,
            'execution_throughput': throughput,
            'pattern_match_time': match_time,
            'all_benchmarks_passed': all([
                conversion_time < 0.01,
                throughput > 10,
                match_time < 0.1
            ]),
            'passed': True
        }

        print(f"✅ Performance: {conversion_time*1000:.1f}ms conversion, {throughput:.1f} patterns/s, {match_time*1000:.1f}ms matching")

    def test_integration_end_to_end(self):
        """Test complete end-to-end Phase β integration"""
        print("\n=== Testing End-to-End Integration ===")

        # 1. Create GraphQL query
        graphql_query = """
        query IntegrationTest {
            searchHypergraph(pattern: "concept", target: "knowledge") {
                nodes { id type name }
                links { type targets }
            }
            matchPattern(variables: ["$concept"]) {
                bindings { variable value }
            }
        }
        """

        # 2. Convert to AtomSpace queries
        atomspace_queries = self.bridge.graphql_to_atomspace(graphql_query)
        self.assertGreater(len(atomspace_queries), 0, "Should generate queries")

        # 3. Execute through distributed system
        patterns = [{"pattern": q.pattern, "variables": q.variables, "constraints": q.constraints}
                   for q in atomspace_queries]
        dist_results = self.executor.execute_distributed(patterns)

        # 4. Perform pattern matching
        pattern_ids = self.matcher.create_sample_patterns()
        pattern_results = []
        for pattern_id in pattern_ids:
            matches = self.matcher.match_pattern(pattern_id)
            pattern_results.extend(matches)

        # 5. Validate complete pipeline
        self.assertGreater(len(atomspace_queries), 0, "Pipeline step 2 should succeed")
        self.assertGreater(dist_results["successful_tasks"], 0, "Pipeline step 3 should succeed")
        self.assertGreater(len(pattern_results), 0, "Pipeline step 4 should succeed")

        # 6. Check state coverage across all components
        bridge_states = self.bridge.get_shard_statistics()["total_states"]
        executor_states = self.executor.total_states
        matcher_states = self.matcher.total_states

        self.assertTrue(all(s == 110 for s in [bridge_states, executor_states, matcher_states]),
                       "All components should cover 110 states")

        self.test_results['end_to_end_integration'] = {
            'graphql_parsed': len(graphql_query) > 0,
            'queries_generated': len(atomspace_queries),
            'distributed_execution_successful': dist_results["successful_tasks"] > 0,
            'pattern_matches_found': len(pattern_results),
            'state_coverage_consistent': all(s == 110 for s in [bridge_states, executor_states, matcher_states]),
            'pipeline_complete': True,
            'passed': True
        }

        print("✅ End-to-end integration: Complete pipeline working")

    def tearDown(self):
        """Clean up and save test results"""
        # Shutdown executor
        self.executor.shutdown()

        # Save results with proper serialization
        serializable_results = self._make_serializable(self.test_results)

        with open("phase_beta_test_results.json", "w") as f:
            json.dump(serializable_results, f, indent=2)

    def _make_serializable(self, obj):
        """Convert objects to JSON serializable format"""
        if isinstance(obj, dict):
            return {k: self._make_serializable(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._make_serializable(item) for item in obj]
        elif isinstance(obj, tuple):
            return list(obj)
        elif hasattr(obj, '__dict__'):
            return str(obj)
        else:
            return obj


def run_comprehensive_test():
    """Run comprehensive Phase β integration test"""
    print("🔮 Phase β: DAS-Hypergraph Integration Test")
    print("=" * 60)

    # Run unit tests
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(PhaseBetaIntegrationTest)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Summary
    print("\n" + "=" * 60)
    print("🎯 PHASE β INTEGRATION TEST SUMMARY")
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
        print("\n✅ ALL TESTS PASSED - Phase β Integration Ready!")
        print("🚀 110 quantum states operational")
        print("🧠 11×5×2 tensor architecture validated")
        print("📊 DAS-Hypergraph integration successful")
        print("⚡ Ready for Phase γ: ESN Reservoir Computing")
    else:
        print(f"\n❌ {failures + errors} tests failed")

    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_comprehensive_test()
    sys.exit(0 if success else 1)
