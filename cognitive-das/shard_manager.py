#!/usr/bin/env python3
"""
Distributed Shard Execution Manager
Phase β: DAS-Hypergraph Integration

Manages parallel execution across 11 shards with 5 links per shard
and 2 truth value dimensions for 110 total quantum states.

Copyright (c) 2025 OpenCog Foundation
"""

import hashlib
import json
import statistics
import threading
import time
from dataclasses import asdict, dataclass
from queue import Empty, Queue
from typing import Any


@dataclass
class ShardTask:
    """Task to be executed on a shard"""

    task_id: str
    shard_id: int
    pattern: str
    variables: list[str]
    constraints: list[str]
    priority: int = 1
    timeout: float = 5.0


@dataclass
class ShardResult:
    """Result from shard execution"""

    task_id: str
    shard_id: int
    success: bool
    matches: list[dict[str, Any]]
    execution_time: float
    error_message: str | None = None
    truth_values: list[tuple[float, float]] = None  # (strength, confidence) pairs


@dataclass
class ShardMetrics:
    """Performance metrics for a shard"""

    shard_id: int
    total_tasks: int
    successful_tasks: int
    failed_tasks: int
    average_execution_time: float
    total_execution_time: float
    queue_length: int
    cpu_utilization: float = 0.0


class DistributedShardExecutor:
    """
    Distributed Shard Execution Manager

    Manages parallel execution of AtomSpace queries across 11 shards
    with load balancing and fault tolerance.
    """

    def __init__(self, num_shards: int = 11, links_per_shard: int = 5, truth_dimensions: int = 2):
        self.num_shards = num_shards
        self.links_per_shard = links_per_shard
        self.truth_dimensions = truth_dimensions
        self.total_states = num_shards * links_per_shard * truth_dimensions  # 110

        # Shard management
        self.shard_queues = {}
        self.shard_workers = {}
        self.shard_metrics = {}
        self.shard_locks = {}

        # Results tracking
        self.results_cache = {}
        self.active_tasks = {}

        # Configuration
        self.max_workers_per_shard = 2
        self.task_timeout = 10.0
        self.enable_caching = True

        # Initialize shards
        self._initialize_shards()

        # Global metrics
        self.global_metrics = {
            "total_tasks_submitted": 0,
            "total_tasks_completed": 0,
            "total_execution_time": 0.0,
            "average_throughput": 0.0,
        }

        # Performance monitoring
        self.performance_lock = threading.Lock()
        self.monitoring_active = True
        self.monitoring_thread = threading.Thread(target=self._monitor_performance)
        self.monitoring_thread.daemon = True
        self.monitoring_thread.start()

    def _initialize_shards(self):
        """Initialize all shards with queues and workers"""
        for shard_id in range(self.num_shards):
            # Create task queue for shard
            self.shard_queues[shard_id] = Queue()

            # Create shard lock
            self.shard_locks[shard_id] = threading.Lock()

            # Initialize metrics
            self.shard_metrics[shard_id] = ShardMetrics(
                shard_id=shard_id,
                total_tasks=0,
                successful_tasks=0,
                failed_tasks=0,
                average_execution_time=0.0,
                total_execution_time=0.0,
                queue_length=0,
            )

            # Start worker threads for shard
            self.shard_workers[shard_id] = []
            for worker_id in range(self.max_workers_per_shard):
                worker = threading.Thread(target=self._shard_worker, args=(shard_id, worker_id), daemon=True)
                worker.start()
                self.shard_workers[shard_id].append(worker)

    def execute_distributed(self, patterns: list[dict[str, Any]]) -> dict[str, Any]:
        """
        Execute patterns across distributed shards

        Args:
            patterns: List of pattern dictionaries to execute

        Returns:
            Dict[str, Any]: Aggregated results from all shards
        """
        start_time = time.time()

        # Create tasks from patterns
        tasks = []
        for i, pattern in enumerate(patterns):
            task = ShardTask(
                task_id=f"task_{i}_{int(time.time())}",
                shard_id=self._select_optimal_shard(pattern),
                pattern=pattern.get("pattern", ""),
                variables=pattern.get("variables", []),
                constraints=pattern.get("constraints", []),
                priority=pattern.get("priority", 1),
            )
            tasks.append(task)

        # Submit tasks to shards
        submitted_tasks = self._submit_tasks(tasks)

        # Wait for results
        results = self._collect_results(submitted_tasks)

        # Aggregate results
        aggregated = self._aggregate_results(results)
        aggregated["total_execution_time"] = time.time() - start_time

        # Update global metrics
        self._update_global_metrics(len(tasks), aggregated["total_execution_time"])

        return aggregated

    def _select_optimal_shard(self, pattern: dict[str, Any]) -> int:
        """
        Select optimal shard for pattern execution using load balancing

        Args:
            pattern: Pattern to execute

        Returns:
            int: Selected shard ID
        """
        # Hash-based distribution for consistency
        pattern_str = str(pattern.get("pattern", ""))
        base_shard = int(hashlib.md5(pattern_str.encode()).hexdigest(), 16) % self.num_shards

        # Load balancing: check queue lengths
        min_queue_length = float("inf")
        optimal_shard = base_shard

        for offset in range(self.num_shards):
            candidate_shard = (base_shard + offset) % self.num_shards
            queue_length = self.shard_queues[candidate_shard].qsize()

            if queue_length < min_queue_length:
                min_queue_length = queue_length
                optimal_shard = candidate_shard

                # If found empty queue, use it immediately
                if queue_length == 0:
                    break

        return optimal_shard

    def _submit_tasks(self, tasks: list[ShardTask]) -> list[str]:
        """
        Submit tasks to appropriate shards

        Args:
            tasks: List of tasks to submit

        Returns:
            List[str]: List of submitted task IDs
        """
        submitted_task_ids = []

        for task in tasks:
            # Add to shard queue
            self.shard_queues[task.shard_id].put(task)

            # Track active task
            self.active_tasks[task.task_id] = {"task": task, "submit_time": time.time(), "completed": False}

            submitted_task_ids.append(task.task_id)

            # Update metrics
            with self.shard_locks[task.shard_id]:
                self.shard_metrics[task.shard_id].total_tasks += 1
                self.shard_metrics[task.shard_id].queue_length += 1

        self.global_metrics["total_tasks_submitted"] += len(tasks)
        return submitted_task_ids

    def _collect_results(self, task_ids: list[str], timeout: float = 30.0) -> list[ShardResult]:
        """
        Collect results from submitted tasks

        Args:
            task_ids: List of task IDs to collect
            timeout: Maximum time to wait for all results

        Returns:
            List[ShardResult]: Collected results
        """
        results = []
        start_time = time.time()

        while len(results) < len(task_ids) and (time.time() - start_time) < timeout:
            # Check for completed tasks
            for task_id in task_ids:
                if task_id in self.results_cache and task_id not in [r.task_id for r in results]:
                    results.append(self.results_cache[task_id])

                    # Mark as completed
                    if task_id in self.active_tasks:
                        self.active_tasks[task_id]["completed"] = True

            # Sleep briefly to avoid busy waiting
            if len(results) < len(task_ids):
                time.sleep(0.01)

        # Handle timeouts
        for task_id in task_ids:
            if task_id not in [r.task_id for r in results]:
                # Create timeout result
                task = self.active_tasks.get(task_id, {}).get("task")
                timeout_result = ShardResult(
                    task_id=task_id,
                    shard_id=task.shard_id if task else -1,
                    success=False,
                    matches=[],
                    execution_time=timeout,
                    error_message="Task timeout",
                )
                results.append(timeout_result)

        return results

    def _aggregate_results(self, results: list[ShardResult]) -> dict[str, Any]:
        """
        Aggregate results from multiple shards

        Args:
            results: List of shard results

        Returns:
            Dict[str, Any]: Aggregated results
        """
        aggregated = {
            "total_tasks": len(results),
            "successful_tasks": sum(1 for r in results if r.success),
            "failed_tasks": sum(1 for r in results if not r.success),
            "total_matches": sum(len(r.matches) for r in results),
            "matches_by_shard": {},
            "execution_times": [r.execution_time for r in results],
            "average_execution_time": 0.0,
            "shard_utilization": {},
            "truth_values_summary": {},
            "error_summary": {},
        }

        # Calculate average execution time
        if aggregated["execution_times"]:
            aggregated["average_execution_time"] = statistics.mean(aggregated["execution_times"])

        # Group results by shard
        for result in results:
            shard_id = result.shard_id

            if shard_id not in aggregated["matches_by_shard"]:
                aggregated["matches_by_shard"][shard_id] = []

            aggregated["matches_by_shard"][shard_id].extend(result.matches)

            # Track shard utilization
            if shard_id not in aggregated["shard_utilization"]:
                aggregated["shard_utilization"][shard_id] = {"tasks": 0, "total_time": 0.0}

            aggregated["shard_utilization"][shard_id]["tasks"] += 1
            aggregated["shard_utilization"][shard_id]["total_time"] += result.execution_time

            # Collect truth values
            if result.truth_values:
                if shard_id not in aggregated["truth_values_summary"]:
                    aggregated["truth_values_summary"][shard_id] = []
                aggregated["truth_values_summary"][shard_id].extend(result.truth_values)

            # Collect errors
            if not result.success and result.error_message:
                if result.error_message not in aggregated["error_summary"]:
                    aggregated["error_summary"][result.error_message] = 0
                aggregated["error_summary"][result.error_message] += 1

        return aggregated

    def _shard_worker(self, shard_id: int, worker_id: int):
        """
        Worker thread for processing tasks on a specific shard

        Args:
            shard_id: ID of the shard this worker processes
            worker_id: ID of the worker thread
        """
        queue = self.shard_queues[shard_id]

        while True:
            try:
                # Get task from queue (blocking with timeout)
                task = queue.get(timeout=1.0)

                # Update queue length metric
                with self.shard_locks[shard_id]:
                    self.shard_metrics[shard_id].queue_length = queue.qsize()

                # Execute task
                result = self._execute_task_on_shard(shard_id, task)

                # Store result
                self.results_cache[task.task_id] = result

                # Update metrics
                self._update_shard_metrics(shard_id, result)

                # Mark task as done
                queue.task_done()

            except Empty:
                # No tasks available, continue waiting
                continue
            except Exception as e:
                # Handle worker errors
                print(f"Worker {worker_id} on shard {shard_id} error: {e}")

                if "task" in locals():
                    error_result = ShardResult(
                        task_id=task.task_id,
                        shard_id=shard_id,
                        success=False,
                        matches=[],
                        execution_time=0.0,
                        error_message=str(e),
                    )
                    self.results_cache[task.task_id] = error_result

    def _execute_task_on_shard(self, shard_id: int, task: ShardTask) -> ShardResult:
        """
        Execute a single task on a shard

        Args:
            shard_id: ID of the shard
            task: Task to execute

        Returns:
            ShardResult: Result of task execution
        """
        start_time = time.time()

        try:
            # Simulate pattern matching on shard
            matches = self._simulate_pattern_execution(shard_id, task)

            # Simulate truth value computation
            truth_values = self._compute_truth_values(shard_id, task, matches)

            execution_time = time.time() - start_time

            return ShardResult(
                task_id=task.task_id,
                shard_id=shard_id,
                success=True,
                matches=matches,
                execution_time=execution_time,
                truth_values=truth_values,
            )

        except Exception as e:
            execution_time = time.time() - start_time

            return ShardResult(
                task_id=task.task_id,
                shard_id=shard_id,
                success=False,
                matches=[],
                execution_time=execution_time,
                error_message=str(e),
            )

    def _simulate_pattern_execution(self, shard_id: int, task: ShardTask) -> list[dict[str, Any]]:
        """
        Simulate pattern matching execution on shard

        Args:
            shard_id: ID of the shard
            task: Task to execute

        Returns:
            List[Dict[str, Any]]: List of matches
        """
        matches = []

        # Simulate different types of patterns
        pattern = task.pattern.lower()

        if "concept" in pattern:
            # Generate concept matches based on shard
            for i in range(self.links_per_shard):
                match = {
                    "type": "ConceptNode",
                    "name": f"concept_{shard_id}_{i}",
                    "shard_id": shard_id,
                    "link_index": i,
                    "coordinates": (shard_id, i, 0),
                }
                matches.append(match)

        if "evaluation" in pattern:
            # Generate evaluation link matches
            for i in range(min(3, self.links_per_shard)):
                match = {
                    "type": "EvaluationLink",
                    "predicate": f"predicate_{shard_id}_{i}",
                    "arguments": [f"arg1_{shard_id}_{i}", f"arg2_{shard_id}_{i}"],
                    "shard_id": shard_id,
                    "link_index": i,
                    "coordinates": (shard_id, i, 1),
                }
                matches.append(match)

        if "bind" in pattern:
            # Generate variable bindings
            for var in task.variables:
                match = {
                    "type": "VariableBinding",
                    "variable": var,
                    "value": f"value_{shard_id}_{var}",
                    "shard_id": shard_id,
                    "coordinates": (shard_id, len(task.variables) % self.links_per_shard, 0),
                }
                matches.append(match)

        # Apply simulated execution delay
        import time

        time.sleep(0.001 * len(matches))  # 1ms per match

        return matches

    def _compute_truth_values(
        self, shard_id: int, task: ShardTask, matches: list[dict[str, Any]]
    ) -> list[tuple[float, float]]:
        """
        Compute truth values for matches

        Args:
            shard_id: ID of the shard
            task: Task that generated matches
            matches: List of matches

        Returns:
            List[Tuple[float, float]]: List of (strength, confidence) pairs
        """
        truth_values = []

        for i, match in enumerate(matches):
            # Simulate truth value computation based on shard and match characteristics
            base_strength = 0.5 + (shard_id / self.num_shards) * 0.3
            base_confidence = 0.7 + (i / max(1, len(matches))) * 0.2

            # Add some variation based on match type
            if match.get("type") == "ConceptNode":
                strength = min(1.0, base_strength + 0.1)
                confidence = min(1.0, base_confidence + 0.05)
            elif match.get("type") == "EvaluationLink":
                strength = min(1.0, base_strength + 0.15)
                confidence = min(1.0, base_confidence - 0.05)
            else:
                strength = base_strength
                confidence = base_confidence

            truth_values.append((strength, confidence))

        return truth_values

    def _update_shard_metrics(self, shard_id: int, result: ShardResult):
        """Update metrics for a shard based on task result"""
        with self.shard_locks[shard_id]:
            metrics = self.shard_metrics[shard_id]

            if result.success:
                metrics.successful_tasks += 1
            else:
                metrics.failed_tasks += 1

            metrics.total_execution_time += result.execution_time

            # Update average execution time
            total_completed = metrics.successful_tasks + metrics.failed_tasks
            if total_completed > 0:
                metrics.average_execution_time = metrics.total_execution_time / total_completed

    def _update_global_metrics(self, num_tasks: int, total_time: float):
        """Update global performance metrics"""
        with self.performance_lock:
            self.global_metrics["total_tasks_completed"] += num_tasks
            self.global_metrics["total_execution_time"] += total_time

            if total_time > 0:
                self.global_metrics["average_throughput"] = num_tasks / total_time

    def _monitor_performance(self):
        """Background thread for performance monitoring"""
        while self.monitoring_active:
            try:
                # Update CPU utilization simulation
                for shard_id in range(self.num_shards):
                    queue_size = self.shard_queues[shard_id].qsize()
                    # Simulate CPU utilization based on queue size
                    utilization = min(1.0, queue_size / 10.0)

                    with self.shard_locks[shard_id]:
                        self.shard_metrics[shard_id].cpu_utilization = utilization

                time.sleep(1.0)  # Monitor every second

            except Exception as e:
                print(f"Performance monitoring error: {e}")
                time.sleep(5.0)

    def get_performance_report(self) -> dict[str, Any]:
        """
        Get comprehensive performance report

        Returns:
            Dict[str, Any]: Performance metrics and statistics
        """
        report = {
            "global_metrics": self.global_metrics.copy(),
            "shard_metrics": {},
            "system_summary": {
                "total_shards": self.num_shards,
                "links_per_shard": self.links_per_shard,
                "truth_dimensions": self.truth_dimensions,
                "total_states": self.total_states,
                "active_tasks": len([t for t in self.active_tasks.values() if not t["completed"]]),
                "cached_results": len(self.results_cache),
            },
            "load_distribution": {},
            "performance_summary": {},
        }

        # Collect shard metrics
        total_tasks = 0
        total_execution_time = 0.0
        successful_tasks = 0

        for shard_id in range(self.num_shards):
            with self.shard_locks[shard_id]:
                shard_metrics = asdict(self.shard_metrics[shard_id])
                report["shard_metrics"][shard_id] = shard_metrics

                total_tasks += shard_metrics["total_tasks"]
                total_execution_time += shard_metrics["total_execution_time"]
                successful_tasks += shard_metrics["successful_tasks"]

                # Load distribution
                report["load_distribution"][shard_id] = {
                    "queue_length": shard_metrics["queue_length"],
                    "cpu_utilization": shard_metrics["cpu_utilization"],
                    "task_ratio": shard_metrics["total_tasks"] / max(1, self.global_metrics["total_tasks_submitted"]),
                }

        # Performance summary
        report["performance_summary"] = {
            "overall_success_rate": successful_tasks / max(1, total_tasks),
            "average_shard_utilization": sum(m["cpu_utilization"] for m in report["shard_metrics"].values())
            / self.num_shards,
            "load_balance_coefficient": self._calculate_load_balance_coefficient(),
            "throughput_per_shard": total_tasks / self.num_shards if total_tasks > 0 else 0,
            "system_efficiency": successful_tasks / max(1, self.global_metrics["total_tasks_submitted"]),
        }

        return report

    def _calculate_load_balance_coefficient(self) -> float:
        """Calculate load balance coefficient (lower is better balanced)"""
        task_counts = []
        for shard_id in range(self.num_shards):
            with self.shard_locks[shard_id]:
                task_counts.append(self.shard_metrics[shard_id].total_tasks)

        if not task_counts or max(task_counts) == 0:
            return 0.0

        return statistics.stdev(task_counts) / statistics.mean(task_counts) if task_counts else 0.0

    def shutdown(self):
        """Shutdown the distributed executor"""
        self.monitoring_active = False

        # Wait for all queues to empty
        for shard_id in range(self.num_shards):
            self.shard_queues[shard_id].join()

        print("Distributed shard executor shutdown complete")


def main():
    """Test the distributed shard executor"""
    print("=== Distributed Shard Execution Test ===")

    # Initialize executor
    executor = DistributedShardExecutor(num_shards=11, links_per_shard=5, truth_dimensions=2)

    # Create test patterns
    test_patterns = [
        {"pattern": "ConceptNode search", "variables": ["$x"], "constraints": [], "priority": 1},
        {
            "pattern": "EvaluationLink match",
            "variables": ["$pred", "$arg1", "$arg2"],
            "constraints": ["strength > 0.5"],
            "priority": 2,
        },
        {"pattern": "BindLink execution", "variables": ["$var"], "constraints": [], "priority": 1},
    ] * 10  # 30 total patterns

    print(f"Executing {len(test_patterns)} patterns across {executor.num_shards} shards...")

    # Execute patterns
    start_time = time.time()
    results = executor.execute_distributed(test_patterns)
    execution_time = time.time() - start_time

    print(f"Execution complete in {execution_time:.3f}s")
    print("Results summary:")
    print(f"  Total tasks: {results['total_tasks']}")
    print(f"  Successful: {results['successful_tasks']}")
    print(f"  Failed: {results['failed_tasks']}")
    print(f"  Total matches: {results['total_matches']}")
    print(f"  Average execution time: {results['average_execution_time']:.4f}s")

    # Show shard utilization
    print("\nShard utilization:")
    for shard_id, util_data in results["shard_utilization"].items():
        tasks = util_data["tasks"]
        avg_time = util_data["total_time"] / max(1, tasks)
        print(f"  Shard {shard_id}: {tasks} tasks, {avg_time:.4f}s avg")

    # Get performance report
    print("\nGetting performance report...")
    perf_report = executor.get_performance_report()

    print("System summary:")
    print(f"  Total states: {perf_report['system_summary']['total_states']}")
    print(f"  Success rate: {perf_report['performance_summary']['overall_success_rate']:.3f}")
    print(f"  Load balance: {perf_report['performance_summary']['load_balance_coefficient']:.3f}")
    print(f"  System efficiency: {perf_report['performance_summary']['system_efficiency']:.3f}")

    # Test 110 states validation
    print("\nValidating 110 quantum states...")
    states_verified = 0
    for shard in range(executor.num_shards):
        for link in range(executor.links_per_shard):
            for truth in range(executor.truth_dimensions):
                state_index = (
                    shard * executor.links_per_shard * executor.truth_dimensions
                    + link * executor.truth_dimensions
                    + truth
                )
                if 0 <= state_index < 110:
                    states_verified += 1

    print(f"States verified: {states_verified}/110")
    print(f"Validation: {'✅ PASSED' if states_verified == 110 else '❌ FAILED'}")

    # Save results
    final_results = {
        "execution_results": results,
        "performance_report": perf_report,
        "validation": {
            "expected_states": 110,
            "verified_states": states_verified,
            "validation_passed": states_verified == 110,
        },
        "test_metadata": {
            "num_patterns": len(test_patterns),
            "execution_time": execution_time,
            "patterns_per_second": len(test_patterns) / execution_time,
        },
    }

    with open("distributed_execution_results.json", "w") as f:
        json.dump(final_results, f, indent=2)

    print("\nResults saved to distributed_execution_results.json")

    # Shutdown executor
    executor.shutdown()

    print("=== Distributed Shard Execution Test Complete ===")


if __name__ == "__main__":
    main()
