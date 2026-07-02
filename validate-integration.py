#!/usr/bin/env python3
"""
OpenCog Unified Integration Validator
Validates component integration and dependency resolution
"""

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path


class IntegrationValidator:
    """Validates OpenCog component integration"""

    def __init__(self, root_dir: str = "."):
        self.root_dir = Path(root_dir).resolve()
        self.components_dir = self.root_dir / "components"
        self.results = {
            "timestamp": time.time(),
            "validations": {},
            "summary": {},
            "errors": []
        }

        # Component dependency map
        self.dependency_map = {
            "atomspace-storage": ["atomspace"],
            "atomspace-rocks": ["atomspace"],
            "atomspace-restful": ["atomspace"],
            "unify": ["atomspace"],
            "ure": ["atomspace", "unify"],
            "attention": ["atomspace", "cogserver"],
            "spacetime": ["atomspace"],
            "pln": ["atomspace", "ure", "spacetime"],
            "miner": ["atomspace", "ure"],
            "moses": ["cogutil"],
            "asmoses": ["atomspace", "ure"],
            "lg-atomese": ["atomspace"],
            "learn": ["atomspace", "cogserver"],
            "language-learning": ["cogutil"],
            "opencog": ["atomspace", "cogserver", "attention", "ure", "lg-atomese"]
        }

        # Phase organization
        self.phases = {
            1: ["atomspace-storage", "atomspace-rocks", "atomspace-restful", "moses"],
            2: ["unify", "ure", "language-learning"],
            3: ["attention", "spacetime"],
            4: ["pln", "miner", "asmoses"],
            5: ["lg-atomese", "learn", "opencog"]
        }

    def log(self, level: str, message: str):
        """Log message with timestamp"""
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        color_codes = {
            "INFO": "\033[0;34m",
            "SUCCESS": "\033[0;32m",
            "WARNING": "\033[1;33m",
            "ERROR": "\033[0;31m",
            "RESET": "\033[0m"
        }

        color = color_codes.get(level, "")
        reset = color_codes["RESET"]
        print(f"{color}[{level}]{reset} {timestamp} - {message}")

    def validate_directory_structure(self) -> bool:
        """Validate expected directory structure exists"""
        self.log("INFO", "Validating directory structure...")

        required_dirs = [
            "components/core",
            "components/logic",
            "components/cognitive",
            "components/advanced",
            "components/learning",
            "components/language",
            "components/integration",
            "tests/integration",
            "tests/performance",
            "tests/end_to_end"
        ]

        missing_dirs = []
        for dir_path in required_dirs:
            full_path = self.root_dir / dir_path
            if not full_path.exists():
                missing_dirs.append(dir_path)

        if missing_dirs:
            self.log("ERROR", f"Missing directories: {', '.join(missing_dirs)}")
            self.results["errors"].append(f"Missing directories: {missing_dirs}")
            return False

        self.log("SUCCESS", "Directory structure validation passed")
        return True

    def check_component_presence(self, component: str) -> tuple[bool, str]:
        """Check if component is present in repository"""
        # Check in root directory first (for existing components)
        root_component = self.root_dir / component
        if root_component.exists():
            return True, str(root_component)

        # Check in components subdirectories
        for category in ["core", "logic", "cognitive", "advanced", "learning", "language", "integration"]:
            component_path = self.components_dir / category / component
            if component_path.exists():
                return True, str(component_path)

        return False, ""

    def validate_dependencies(self, component: str) -> dict:
        """Validate component dependencies are satisfied"""
        self.log("INFO", f"Validating dependencies for {component}...")

        result = {
            "component": component,
            "dependencies": self.dependency_map.get(component, []),
            "satisfied": [],
            "missing": [],
            "status": "unknown"
        }

        for dep in result["dependencies"]:
            is_present, path = self.check_component_presence(dep)
            if is_present:
                result["satisfied"].append({"dependency": dep, "path": path})
            else:
                result["missing"].append(dep)

        if not result["missing"]:
            result["status"] = "satisfied"
            self.log("SUCCESS", f"All dependencies satisfied for {component}")
        else:
            result["status"] = "missing_dependencies"
            self.log("ERROR", f"Missing dependencies for {component}: {result['missing']}")

        return result

    def validate_cmake_integration(self, component: str) -> dict:
        """Validate CMake integration for component"""
        self.log("INFO", f"Validating CMake integration for {component}...")

        result = {
            "component": component,
            "cmake_file_exists": False,
            "integrated_in_main": False,
            "status": "unknown"
        }

        # Check if component has CMakeLists.txt
        is_present, component_path = self.check_component_presence(component)
        if is_present:
            cmake_file = Path(component_path) / "CMakeLists.txt"
            result["cmake_file_exists"] = cmake_file.exists()

        # Check if component is referenced in main CMakeLists.txt
        main_cmake = self.root_dir / "CMakeLists.txt"
        if main_cmake.exists():
            content = main_cmake.read_text()
            result["integrated_in_main"] = component in content

        if result["cmake_file_exists"] and result["integrated_in_main"]:
            result["status"] = "integrated"
            self.log("SUCCESS", f"CMake integration validated for {component}")
        else:
            result["status"] = "not_integrated"
            issues = []
            if not result["cmake_file_exists"]:
                issues.append("no CMakeLists.txt")
            if not result["integrated_in_main"]:
                issues.append("not in main CMakeLists.txt")
            self.log("WARNING", f"CMake integration issues for {component}: {', '.join(issues)}")

        return result

    def validate_build_capability(self) -> dict:
        """Test if the unified system can be built"""
        self.log("INFO", "Validating build capability...")

        result = {
            "build_attempted": False,
            "build_successful": False,
            "cmake_successful": False,
            "errors": [],
            "status": "unknown"
        }

        build_dir = self.root_dir / "build_test"
        try:
            # Create clean build directory
            if build_dir.exists():
                import shutil
                shutil.rmtree(build_dir)
            build_dir.mkdir()

            # Run cmake
            self.log("INFO", "Running cmake configuration...")
            cmake_process = subprocess.run(
                ["cmake", ".."],
                cwd=build_dir,
                capture_output=True,
                text=True,
                timeout=120
            )

            result["build_attempted"] = True
            result["cmake_successful"] = cmake_process.returncode == 0

            if cmake_process.returncode != 0:
                result["errors"].append(f"CMake failed: {cmake_process.stderr}")
                result["status"] = "cmake_failed"
                self.log("ERROR", "CMake configuration failed")
                return result

            # Run make (limited time)
            self.log("INFO", "Running build (limited time test)...")
            make_process = subprocess.run(
                ["make", "-j2"],
                cwd=build_dir,
                capture_output=True,
                text=True,
                timeout=300  # 5 minutes timeout
            )

            result["build_successful"] = make_process.returncode == 0

            if make_process.returncode == 0:
                result["status"] = "build_successful"
                self.log("SUCCESS", "Build test successful")
            else:
                result["errors"].append(f"Build failed: {make_process.stderr}")
                result["status"] = "build_failed"
                self.log("ERROR", "Build test failed")

        except subprocess.TimeoutExpired:
            result["status"] = "build_timeout"
            result["errors"].append("Build timed out after 5 minutes")
            self.log("WARNING", "Build test timed out")
        except Exception as e:
            result["status"] = "build_error"
            result["errors"].append(f"Build test error: {e!s}")
            self.log("ERROR", f"Build test error: {e}")
        finally:
            # Clean up build directory
            if build_dir.exists():
                import shutil
                shutil.rmtree(build_dir)

        return result

    def validate_integration_tests(self) -> dict:
        """Run integration tests if they exist"""
        self.log("INFO", "Validating integration tests...")

        result = {
            "tests_found": [],
            "tests_run": [],
            "tests_passed": [],
            "tests_failed": [],
            "status": "unknown"
        }

        test_dir = self.root_dir / "tests" / "integration"
        if test_dir.exists():
            test_files = list(test_dir.glob("test_*.py"))
            result["tests_found"] = [t.name for t in test_files]

            for test_file in test_files:
                try:
                    self.log("INFO", f"Running test: {test_file.name}")
                    test_process = subprocess.run(
                        [sys.executable, str(test_file)],
                        capture_output=True,
                        text=True,
                        timeout=60
                    )

                    result["tests_run"].append(test_file.name)

                    if test_process.returncode == 0:
                        result["tests_passed"].append(test_file.name)
                        self.log("SUCCESS", f"Test passed: {test_file.name}")
                    else:
                        result["tests_failed"].append({
                            "test": test_file.name,
                            "error": test_process.stderr
                        })
                        self.log("ERROR", f"Test failed: {test_file.name}")

                except subprocess.TimeoutExpired:
                    result["tests_failed"].append({
                        "test": test_file.name,
                        "error": "Test timed out"
                    })
                    self.log("WARNING", f"Test timed out: {test_file.name}")
                except Exception as e:
                    result["tests_failed"].append({
                        "test": test_file.name,
                        "error": str(e)
                    })
                    self.log("ERROR", f"Test error: {test_file.name} - {e}")

        if result["tests_found"]:
            if result["tests_failed"]:
                result["status"] = "some_tests_failed"
            else:
                result["status"] = "all_tests_passed"
        else:
            result["status"] = "no_tests_found"
            self.log("WARNING", "No integration tests found")

        return result

    def validate_phase(self, phase_num: int) -> dict:
        """Validate a specific integration phase"""
        self.log("INFO", f"Validating Phase {phase_num}...")

        phase_components = self.phases.get(phase_num, [])
        result = {
            "phase": phase_num,
            "components": phase_components,
            "validations": {},
            "status": "unknown"
        }

        all_valid = True
        for component in phase_components:
            component_result = {
                "dependencies": self.validate_dependencies(component),
                "cmake": self.validate_cmake_integration(component)
            }

            result["validations"][component] = component_result

            if (component_result["dependencies"]["status"] != "satisfied" or
                component_result["cmake"]["status"] != "integrated"):
                all_valid = False

        result["status"] = "valid" if all_valid else "invalid"

        if all_valid:
            self.log("SUCCESS", f"Phase {phase_num} validation passed")
        else:
            self.log("ERROR", f"Phase {phase_num} validation failed")

        return result

    def run_full_validation(self) -> dict:
        """Run complete validation suite"""
        self.log("INFO", "Starting full integration validation...")

        # Validate directory structure
        structure_valid = self.validate_directory_structure()
        self.results["validations"]["directory_structure"] = {
            "status": "valid" if structure_valid else "invalid"
        }

        # Validate each phase
        for phase_num in range(1, 6):
            phase_result = self.validate_phase(phase_num)
            self.results["validations"][f"phase_{phase_num}"] = phase_result

        # Validate build capability
        build_result = self.validate_build_capability()
        self.results["validations"]["build"] = build_result

        # Validate integration tests
        test_result = self.validate_integration_tests()
        self.results["validations"]["integration_tests"] = test_result

        # Generate summary
        self.generate_summary()

        return self.results

    def generate_summary(self):
        """Generate validation summary"""
        validations = self.results["validations"]

        summary = {
            "total_phases": 5,
            "phases_valid": 0,
            "build_status": validations.get("build", {}).get("status", "unknown"),
            "test_status": validations.get("integration_tests", {}).get("status", "unknown"),
            "overall_status": "unknown"
        }

        # Count valid phases
        for phase_num in range(1, 6):
            phase_key = f"phase_{phase_num}"
            if validations.get(phase_key, {}).get("status") == "valid":
                summary["phases_valid"] += 1

        # Determine overall status
        structure_valid = validations.get("directory_structure", {}).get("status") == "valid"
        all_phases_valid = summary["phases_valid"] == summary["total_phases"]
        build_ok = summary["build_status"] in ["build_successful", "cmake_successful"]

        if structure_valid and all_phases_valid and build_ok:
            summary["overall_status"] = "excellent"
        elif structure_valid and summary["phases_valid"] >= 3:
            summary["overall_status"] = "good"
        elif summary["phases_valid"] >= 1:
            summary["overall_status"] = "partial"
        else:
            summary["overall_status"] = "poor"

        self.results["summary"] = summary

    def save_results(self, output_file: str = "integration_validation.json"):
        """Save validation results to file"""
        output_path = self.root_dir / output_file
        with open(output_path, 'w') as f:
            json.dump(self.results, f, indent=2)

        self.log("INFO", f"Validation results saved to {output_path}")

    def print_summary(self):
        """Print validation summary"""
        summary = self.results["summary"]

        print("\n" + "="*60)
        print("OPENCOG UNIFIED INTEGRATION VALIDATION SUMMARY")
        print("="*60)

        print(f"Overall Status: {summary['overall_status'].upper()}")
        print(f"Phases Valid: {summary['phases_valid']}/{summary['total_phases']}")
        print(f"Build Status: {summary['build_status']}")
        print(f"Test Status: {summary['test_status']}")

        print("\nPhase Details:")
        for phase_num in range(1, 6):
            phase_key = f"phase_{phase_num}"
            phase_data = self.results["validations"].get(phase_key, {})
            status = phase_data.get("status", "unknown")
            components = phase_data.get("components", [])
            print(f"  Phase {phase_num}: {status.upper()} - {', '.join(components)}")

        if self.results["errors"]:
            print("\nErrors:")
            for error in self.results["errors"]:
                print(f"  - {error}")

        print("="*60)

def main():
    parser = argparse.ArgumentParser(description="Validate OpenCog Unified integration")
    parser.add_argument("--phase", type=int, choices=[1,2,3,4,5],
                       help="Validate specific phase only")
    parser.add_argument("--output", default="integration_validation.json",
                       help="Output file for results")
    parser.add_argument("--no-build", action="store_true",
                       help="Skip build validation")
    parser.add_argument("--root-dir", default=".",
                       help="Root directory of OpenCog Unified repository")

    args = parser.parse_args()

    validator = IntegrationValidator(args.root_dir)

    if args.phase:
        # Validate specific phase
        result = validator.validate_phase(args.phase)
        print(json.dumps(result, indent=2))
    else:
        # Run full validation
        validator.run_full_validation()
        validator.print_summary()
        validator.save_results(args.output)

if __name__ == "__main__":
    main()
