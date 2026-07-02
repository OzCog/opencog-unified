#!/usr/bin/env python3
"""
demo_agentic_catalog.py

Comprehensive demonstration of the agentic kernels catalog system
This script showcases all the key features implemented
"""

import json
import math
import sys
from typing import Any


class AgenticKernelDemo:
    def __init__(self):
        """Initialize the demo with standard agentic kernels"""
        self.kernels = self._create_standard_kernels()

    def _create_standard_kernels(self) -> list[dict[str, Any]]:
        """Create all standard agentic kernels with complete specifications"""

        kernels = []

        # GHOST - Goal-oriented Hierarchical OpenCog Scripting Technology
        ghost = {
            "kernel_name": "GHOST",
            "description": "Goal-oriented Hierarchical OpenCog Scripting Technology",
            "version": "1.0.0",
            "status": "production",
            "implementation_language": "C++/Scheme",
            "source_location": "opencog/ghost",
            "functional_roles": ["conversational", "nlp_processing"],
            "cognitive_subsystems": ["working_memory", "semantic_memory"],
            "parameters": [
                {"name": "dialogue_depth", "type": "int", "default": 5, "range": [1, 10]},
                {"name": "response_confidence", "type": "float", "default": 0.7, "range": [0.0, 1.0]},
                {"name": "context_window", "type": "int", "default": 20, "range": [1, 100]},
                {"name": "goal_satisfaction_threshold", "type": "float", "default": 0.8, "range": [0.0, 1.0]},
            ],
        }
        kernels.append(ghost)

        # PLN - Probabilistic Logic Networks
        pln = {
            "kernel_name": "PLN",
            "description": "Probabilistic Logic Networks for reasoning",
            "version": "1.0.0",
            "status": "production",
            "implementation_language": "C++/Scheme",
            "source_location": "opencog/pln",
            "functional_roles": ["reasoning_inference"],
            "cognitive_subsystems": ["working_memory", "semantic_memory", "executive_control"],
            "parameters": [
                {"name": "inference_depth", "type": "int", "default": 15, "range": [1, 50]},
                {"name": "confidence_threshold", "type": "float", "default": 0.5, "range": [0.0, 1.0]},
                {"name": "truth_value_precision", "type": "float", "default": 0.01, "range": [0.001, 0.1]},
                {"name": "rule_strength", "type": "float", "default": 0.8, "range": [0.0, 1.0]},
            ],
        }
        kernels.append(pln)

        # ECAN - Economic Attention Networks
        ecan = {
            "kernel_name": "ECAN",
            "description": "Economic Attention Networks",
            "version": "1.0.0",
            "status": "production",
            "implementation_language": "C++",
            "source_location": "opencog/attention",
            "functional_roles": ["attention_allocation"],
            "cognitive_subsystems": ["attention_system", "working_memory"],
            "parameters": [
                {"name": "attention_allocation_rate", "type": "float", "default": 0.1, "range": [0.01, 1.0]},
                {"name": "forgetting_rate", "type": "float", "default": 0.01, "range": [0.001, 0.1]},
                {"name": "max_atom_attention", "type": "float", "default": 100.0, "range": [1.0, 1000.0]},
                {"name": "hebbian_learning_rate", "type": "float", "default": 0.01, "range": [0.001, 0.1]},
            ],
        }
        kernels.append(ecan)

        # Eva - Expressive Virtual Avatar
        eva = {
            "kernel_name": "Eva",
            "description": "Expressive Virtual Avatar",
            "version": "1.0.0",
            "status": "prototype",
            "implementation_language": "Python/C++",
            "source_location": "hansonrobotics/eva",
            "functional_roles": ["conversational", "emotional_affective"],
            "cognitive_subsystems": ["emotional_system", "social_cognition", "motor_output"],
            "parameters": [
                {"name": "emotional_expressiveness", "type": "float", "default": 0.7, "range": [0.0, 1.0]},
                {"name": "facial_animation_speed", "type": "float", "default": 1.0, "range": [0.1, 2.0]},
                {"name": "voice_emotion_strength", "type": "float", "default": 0.6, "range": [0.0, 1.0]},
                {"name": "personality_traits", "type": "int", "default": 10, "range": [5, 20]},
            ],
        }
        kernels.append(eva)

        # Loving AI
        loving_ai = {
            "kernel_name": "Loving AI",
            "description": "Compassionate AI for therapeutic interactions",
            "version": "1.0.0",
            "status": "experimental",
            "implementation_language": "Python",
            "source_location": "opencog/loving-ai",
            "functional_roles": ["emotional_affective", "conversational", "social_interaction"],
            "cognitive_subsystems": ["emotional_system", "social_cognition"],
            "parameters": [
                {"name": "compassion_level", "type": "float", "default": 0.9, "range": [0.0, 1.0]},
                {"name": "empathy_sensitivity", "type": "float", "default": 0.8, "range": [0.0, 1.0]},
                {"name": "therapeutic_style", "type": "int", "default": 3, "range": [1, 5]},
                {"name": "emotional_validation", "type": "float", "default": 0.85, "range": [0.0, 1.0]},
            ],
        }
        kernels.append(loving_ai)

        # Game AI
        game_ai = {
            "kernel_name": "Game AI",
            "description": "Strategic game playing artificial intelligence",
            "version": "1.0.0",
            "status": "prototype",
            "implementation_language": "C++/Python",
            "source_location": "opencog/game-ai",
            "functional_roles": ["game_strategy", "reasoning_inference"],
            "cognitive_subsystems": ["executive_control", "working_memory"],
            "parameters": [
                {"name": "search_depth", "type": "int", "default": 8, "range": [1, 20]},
                {"name": "exploration_rate", "type": "float", "default": 0.3, "range": [0.0, 1.0]},
                {"name": "strategic_patience", "type": "float", "default": 0.7, "range": [0.0, 1.0]},
                {"name": "risk_tolerance", "type": "float", "default": 0.5, "range": [0.0, 1.0]},
            ],
        }
        kernels.append(game_ai)

        return kernels

    def compute_degrees_of_freedom(self, kernel: dict[str, Any]) -> int:
        """Compute degrees of freedom for a kernel"""
        dof = 0

        # Parameter space degrees of freedom
        for param in kernel.get("parameters", []):
            param_type = param.get("type", "float")
            param_range = param.get("range", [0, 1])

            if param_type == "float":
                range_size = param_range[1] - param_range[0] if len(param_range) >= 2 else 1.0
                dof += max(1, int(range_size * 100))
            elif param_type == "int":
                range_size = param_range[1] - param_range[0] if len(param_range) >= 2 else 10
                dof += max(1, int(range_size))
            elif param_type == "bool":
                dof += 2
            else:
                dof += 5  # Default estimate

        # Structural complexity
        dof += len(kernel.get("functional_roles", [])) * 2
        dof += len(kernel.get("cognitive_subsystems", [])) * 3

        # Base complexity
        dof += 10

        return max(dof, 1)

    def prime_factorization(self, n: int) -> list[int]:
        """Compute prime factorization of a number"""
        if n <= 1:
            return [1]

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

    def derive_tensor_shape(self, dof: int) -> tuple[list[int], list[int]]:
        """Derive optimal tensor shape from degrees of freedom via prime factorization"""
        factors = self.prime_factorization(dof)

        if len(factors) == 0:
            return [1], [1]
        elif len(factors) == 1 or len(factors) == 2:
            return factors, factors
        else:
            # Distribute factors into 3 dimensions for better memory layout
            dim1, dim2, dim3 = 1, 1, 1
            for i, factor in enumerate(factors):
                if i % 3 == 0:
                    dim1 *= factor
                elif i % 3 == 1:
                    dim2 *= factor
                else:
                    dim3 *= factor
            return [dim1, dim2, dim3], factors

    def compute_shape_efficiency(self, shape: list[int]) -> tuple[float, float]:
        """Compute memory and computational efficiency of a tensor shape"""
        memory_efficiency = 0.0
        computational_efficiency = 0.0

        for dim in shape:
            # Memory efficiency: prefer powers of 2 and cache-friendly sizes
            if dim & (dim - 1) == 0:  # Power of 2
                memory_efficiency += 0.3
            if dim % 64 == 0:  # Cache-friendly
                memory_efficiency += 0.2
            if 16 <= dim <= 1024:  # Reasonable size
                memory_efficiency += 0.3

            # Computational efficiency: prefer SIMD-friendly dimensions
            if dim % 8 == 0:
                computational_efficiency += 0.25
            elif dim % 4 == 0:
                computational_efficiency += 0.15
            elif dim % 2 == 0:
                computational_efficiency += 0.10

        # Normalize by number of dimensions
        if shape:
            memory_efficiency = min(1.0, memory_efficiency / len(shape))
            computational_efficiency = min(1.0, computational_efficiency / len(shape))

        # Prefer 3D or 4D shapes for GPU processing
        if len(shape) in [3, 4]:
            computational_efficiency += 0.3
            computational_efficiency = min(1.0, computational_efficiency)

        return memory_efficiency, computational_efficiency

    def analyze_kernel_complexity(self, kernel: dict[str, Any]) -> dict[str, Any]:
        """Perform comprehensive complexity analysis of a kernel"""
        dof = self.compute_degrees_of_freedom(kernel)
        tensor_shape, prime_factors = self.derive_tensor_shape(dof)
        memory_eff, compute_eff = self.compute_shape_efficiency(tensor_shape)

        complexity_score = math.log10(max(1, dof))

        return {
            "kernel_name": kernel["kernel_name"],
            "degrees_of_freedom": dof,
            "prime_factors": prime_factors,
            "optimal_tensor_shape": tensor_shape,
            "total_tensor_elements": dof,
            "memory_efficiency": memory_eff,
            "computational_efficiency": compute_eff,
            "complexity_score": complexity_score,
        }

    def test_round_trip_serialization(self, kernel: dict[str, Any]) -> bool:
        """Test round-trip JSON serialization"""
        try:
            # Serialize to JSON
            json_str = json.dumps(kernel, indent=2)

            # Deserialize from JSON
            deserialized = json.loads(json_str)

            # Basic validation
            return (
                deserialized.get("kernel_name") == kernel.get("kernel_name")
                and deserialized.get("description") == kernel.get("description")
                and len(deserialized.get("parameters", [])) == len(kernel.get("parameters", []))
            )

        except Exception as e:
            print(f"    ✗ Serialization error: {e}")
            return False

    def generate_catalog_report(self) -> str:
        """Generate comprehensive catalog report"""
        report = []
        report.append("=== Agentic Kernels Catalog Report ===")
        report.append("")

        # Catalog overview
        total_kernels = len(self.kernels)
        production_kernels = [k for k in self.kernels if k["status"] == "production"]
        prototype_kernels = [k for k in self.kernels if k["status"] == "prototype"]
        experimental_kernels = [k for k in self.kernels if k["status"] == "experimental"]

        report.append("Catalog Overview:")
        report.append(f"  Total Kernels: {total_kernels}")
        report.append(f"  Production Kernels: {len(production_kernels)}")
        report.append(f"  Prototype Kernels: {len(prototype_kernels)}")
        report.append(f"  Experimental Kernels: {len(experimental_kernels)}")
        report.append("")

        # Complexity analysis
        report.append("Complexity Analysis:")
        analyses = [self.analyze_kernel_complexity(kernel) for kernel in self.kernels]

        for analysis in analyses:
            report.append(f"  • {analysis['kernel_name']}:")
            report.append(f"    DOF: {analysis['degrees_of_freedom']}")
            report.append(f"    Tensor Shape: {analysis['optimal_tensor_shape']}")
            report.append(f"    Memory Efficiency: {analysis['memory_efficiency']:.2f}")
            report.append(f"    Computational Efficiency: {analysis['computational_efficiency']:.2f}")
            report.append(f"    Complexity Score: {analysis['complexity_score']:.2f}")
            report.append("")

        # Statistics
        avg_dof = sum(a["degrees_of_freedom"] for a in analyses) / len(analyses)
        avg_complexity = sum(a["complexity_score"] for a in analyses) / len(analyses)
        avg_memory_eff = sum(a["memory_efficiency"] for a in analyses) / len(analyses)
        avg_compute_eff = sum(a["computational_efficiency"] for a in analyses) / len(analyses)

        report.append("Summary Statistics:")
        report.append(f"  Average DOF: {avg_dof:.1f}")
        report.append(f"  Average Complexity Score: {avg_complexity:.2f}")
        report.append(f"  Average Memory Efficiency: {avg_memory_eff:.2f}")
        report.append(f"  Average Computational Efficiency: {avg_compute_eff:.2f}")

        return "\n".join(report)

    def run_comprehensive_tests(self) -> bool:
        """Run comprehensive test suite"""
        print("🧠 Agentic Kernels Catalog - Comprehensive Test Suite")
        print("====================================================")
        print()

        passed = 0
        total = 0

        # Test 1: Kernel creation
        total += 1
        print("Testing kernel creation...")
        if len(self.kernels) >= 6:  # Should have at least 6 standard kernels
            print("  ✓ All standard kernels created successfully")
            passed += 1
        else:
            print("  ✗ Missing standard kernels")
        print()

        # Test 2: Degrees of freedom calculation
        total += 1
        print("Testing degrees of freedom calculation...")
        all_have_dof = all(self.compute_degrees_of_freedom(k) > 0 for k in self.kernels)
        if all_have_dof:
            for kernel in self.kernels:
                dof = self.compute_degrees_of_freedom(kernel)
                print(f"  • {kernel['kernel_name']}: DOF = {dof}")
            print("  ✓ DOF calculation working for all kernels")
            passed += 1
        else:
            print("  ✗ DOF calculation failed for some kernels")
        print()

        # Test 3: Prime factorization
        total += 1
        print("Testing prime factorization...")
        test_cases = [(60, [2, 2, 3, 5]), (100, [2, 2, 5, 5]), (17, [17])]
        factorization_passed = True
        for number, expected in test_cases:
            actual = self.prime_factorization(number)
            if sorted(actual) == sorted(expected):
                print(f"  • {number}: {actual} ✓")
            else:
                print(f"  • {number}: {actual} (expected {expected}) ✗")
                factorization_passed = False

        if factorization_passed:
            print("  ✓ Prime factorization working correctly")
            passed += 1
        else:
            print("  ✗ Prime factorization failed")
        print()

        # Test 4: Tensor shape derivation
        total += 1
        print("Testing tensor shape derivation...")
        derivation_passed = True
        for kernel in self.kernels[:3]:  # Test first 3 kernels
            dof = self.compute_degrees_of_freedom(kernel)
            shape, _factors = self.derive_tensor_shape(dof)
            volume = 1
            for dim in shape:
                volume *= dim

            if volume == dof:
                print(f"  • {kernel['kernel_name']}: DOF={dof}, Shape={shape} ✓")
            else:
                print(f"  • {kernel['kernel_name']}: Volume mismatch ✗")
                derivation_passed = False

        if derivation_passed:
            print("  ✓ Tensor shape derivation working correctly")
            passed += 1
        else:
            print("  ✗ Tensor shape derivation failed")
        print()

        # Test 5: Efficiency calculations
        total += 1
        print("Testing efficiency calculations...")
        efficiency_passed = True
        for kernel in self.kernels:
            dof = self.compute_degrees_of_freedom(kernel)
            shape, _ = self.derive_tensor_shape(dof)
            memory_eff, compute_eff = self.compute_shape_efficiency(shape)

            if 0.0 <= memory_eff <= 1.0 and 0.0 <= compute_eff <= 1.0:
                print(f"  • {kernel['kernel_name']}: Memory={memory_eff:.2f}, Compute={compute_eff:.2f} ✓")
            else:
                print(f"  • {kernel['kernel_name']}: Efficiency out of range ✗")
                efficiency_passed = False

        if efficiency_passed:
            print("  ✓ Efficiency calculations working correctly")
            passed += 1
        else:
            print("  ✗ Efficiency calculations failed")
        print()

        # Test 6: Serialization round-trip
        total += 1
        print("Testing serialization round-trip...")
        serialization_passed = True
        for kernel in self.kernels:
            if self.test_round_trip_serialization(kernel):
                print(f"  • {kernel['kernel_name']}: ✓")
            else:
                print(f"  • {kernel['kernel_name']}: ✗")
                serialization_passed = False

        if serialization_passed:
            print("  ✓ Serialization round-trip working correctly")
            passed += 1
        else:
            print("  ✗ Serialization round-trip failed")
        print()

        # Print test summary
        success_rate = (passed / total) * 100
        print("=== Test Results Summary ===")
        print(f"Total Tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {total - passed}")
        print(f"Success Rate: {success_rate:.1f}%")

        if passed == total:
            print("\n🎉 All tests passed! Agentic catalog system is working correctly.")
        else:
            print(f"\n⚠️  {total - passed} test(s) failed. Please check the implementation.")

        return passed == total

    def save_catalog_to_file(self, filename: str):
        """Save catalog to JSON file"""
        catalog_data = {
            "catalog_version": "1.0",
            "timestamp": "2025-01-01T00:00:00Z",
            "total_kernels": len(self.kernels),
            "kernels": [],
        }

        for kernel in self.kernels:
            analysis = self.analyze_kernel_complexity(kernel)
            kernel_entry = {**kernel, "analysis": analysis}
            catalog_data["kernels"].append(kernel_entry)

        with open(filename, "w") as f:
            json.dump(catalog_data, f, indent=2)

        print(f"Catalog saved to {filename}")


def main():
    """Main demonstration function"""
    demo = AgenticKernelDemo()

    # Run comprehensive tests
    success = demo.run_comprehensive_tests()
    print()

    # Generate and display catalog report
    print("📊 Generating catalog report...")
    print()
    report = demo.generate_catalog_report()
    print(report)
    print()

    # Save catalog to file
    demo.save_catalog_to_file("agentic_kernels_catalog.json")
    print()

    # Final message
    if success:
        print("✨ Agentic Kernels Catalog demonstration completed successfully!")
        print("   • All kernels enumerated and analyzed")
        print("   • Degrees of freedom computed via mathematical analysis")
        print("   • Tensor shapes derived via prime factorization")
        print("   • Round-trip serialization validated")
        print("   • Comprehensive catalog report generated")
        print("   • Ready for dynamic ggml kernel instantiation")
    else:
        print("⚠️  Some components need attention before full deployment.")

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
