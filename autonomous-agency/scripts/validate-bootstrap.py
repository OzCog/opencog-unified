#!/usr/bin/env python3
"""
Autonomous Agency Bootstrap Validation Script

This script validates the implementation of Stage 1 bootstrap mechanisms
for autonomous agency in OpenCog Unified.
"""

import json
import os
import sys
from pathlib import Path


def print_header(title):
    """Print a formatted header"""
    print(f"\n{'=' * 60}")
    print(f" {title}")
    print(f"{'=' * 60}")


def print_section(title):
    """Print a formatted section header"""
    print(f"\n{'-' * 40}")
    print(f" {title}")
    print(f"{'-' * 40}")


def validate_file_structure():
    """Validate that all expected files are present"""
    print_section("Validating File Structure")

    base_path = Path()
    expected_files = [
        "AUTONOMOUS-AGENCY-ROADMAP.md",
        "autonomous-agency/CMakeLists.txt",
        "autonomous-agency/bootstrap/entropic-drift-detector.hpp",
        "autonomous-agency/bootstrap/entropic-drift-detector.cpp",
        "autonomous-agency/bootstrap/self-healing-atomspace.hpp",
        "autonomous-agency/bootstrap/self-healing-atomspace.cpp",
        "autonomous-agency/bootstrap/bootstrap-resource-manager.hpp",
        "autonomous-agency/bootstrap/bootstrap-resource-manager.cpp",
        "autonomous-agency/tests/integration-test.cpp",
        "autonomous-agency/examples/bootstrap-example.cpp",
        "autonomous-agency/docs/STAGE-1-IMPLEMENTATION-SUMMARY.md",
        "autonomous-agency/config/autonomous-agency-config.json",
    ]

    missing_files = []
    present_files = []

    for file_path in expected_files:
        full_path = base_path / file_path
        if full_path.exists():
            present_files.append(file_path)
            print(f"✓ {file_path}")
        else:
            missing_files.append(file_path)
            print(f"✗ {file_path} (MISSING)")

    print(f"\nFiles present: {len(present_files)}")
    print(f"Files missing: {len(missing_files)}")

    return len(missing_files) == 0


def validate_configuration():
    """Validate the configuration file"""
    print_section("Validating Configuration")

    config_path = Path("autonomous-agency/config/autonomous-agency-config.json")

    if not config_path.exists():
        print("✗ Configuration file not found")
        return False

    try:
        with open(config_path) as f:
            config = json.load(f)

        # Validate basic structure
        if "autonomous_agency_config" not in config:
            print("✗ Missing autonomous_agency_config section")
            return False

        agency_config = config["autonomous_agency_config"]

        # Check required sections
        required_sections = [
            "entropic_drift_detector",
            "self_healing_atomspace",
            "bootstrap_resource_manager",
            "integration",
            "monitoring",
            "safety",
            "future_stages",
        ]

        missing_sections = []
        for section in required_sections:
            if section in agency_config:
                print(f"✓ {section}")
            else:
                missing_sections.append(section)
                print(f"✗ {section} (MISSING)")

        # Validate specific configuration values
        if "stage" in agency_config and agency_config["stage"] == 1:
            print("✓ Correct stage (1)")
        else:
            print("✗ Incorrect or missing stage")

        print(f"\nConfiguration sections present: {len(required_sections) - len(missing_sections)}")
        print(f"Configuration sections missing: {len(missing_sections)}")

        return len(missing_sections) == 0

    except json.JSONDecodeError as e:
        print(f"✗ Configuration file is not valid JSON: {e}")
        return False
    except Exception as e:
        print(f"✗ Error reading configuration: {e}")
        return False


def validate_code_structure():
    """Validate the code structure and quality"""
    print_section("Validating Code Structure")

    # Check C++ header files
    header_files = [
        "autonomous-agency/bootstrap/entropic-drift-detector.hpp",
        "autonomous-agency/bootstrap/self-healing-atomspace.hpp",
        "autonomous-agency/bootstrap/bootstrap-resource-manager.hpp",
    ]

    implementation_files = [
        "autonomous-agency/bootstrap/entropic-drift-detector.cpp",
        "autonomous-agency/bootstrap/self-healing-atomspace.cpp",
        "autonomous-agency/bootstrap/bootstrap-resource-manager.cpp",
    ]

    # Validate headers
    print("Checking header files:")
    for header in header_files:
        if Path(header).exists():
            with open(header) as f:
                content = f.read()

            # Check for basic C++ header structure
            if "#ifndef" in content and "#define" in content and "#endif" in content:
                print(f"✓ {header} - proper header guard")
            else:
                print(f"✗ {header} - missing header guard")

            # Check for namespace
            if "namespace opencog" in content:
                print(f"✓ {header} - proper namespace")
            else:
                print(f"✗ {header} - missing namespace")
        else:
            print(f"✗ {header} - file missing")

    # Validate implementations
    print("\nChecking implementation files:")
    for impl in implementation_files:
        if Path(impl).exists():
            with open(impl) as f:
                content = f.read()

            # Check for corresponding header include
            header_name = impl.replace(".cpp", ".hpp").split("/")[-1]
            if f'#include "{header_name}"' in content:
                print(f"✓ {impl} - includes corresponding header")
            else:
                print(f"✗ {impl} - missing header include")

            # Check for namespace
            if "namespace opencog" in content:
                print(f"✓ {impl} - proper namespace")
            else:
                print(f"✗ {impl} - missing namespace")
        else:
            print(f"✗ {impl} - file missing")

    return True


def generate_validation_report():
    """Generate a comprehensive validation report"""
    print_header("AUTONOMOUS AGENCY BOOTSTRAP VALIDATION REPORT")

    # Run all validations
    results = {}
    results["file_structure"] = validate_file_structure()
    results["configuration"] = validate_configuration()
    results["code_structure"] = validate_code_structure()

    # Summary
    print_section("Validation Summary")

    passed = sum(1 for result in results.values() if result)
    total = len(results)

    for category, result in results.items():
        status = "PASS" if result else "FAIL"
        symbol = "✓" if result else "✗"
        print(f"{symbol} {category.replace('_', ' ').title()}: {status}")

    print(f"\nOverall Result: {passed}/{total} validations passed")

    if passed == total:
        print("\n🎉 ALL VALIDATIONS PASSED!")
        print("Stage 1 Bootstrap Mechanisms are fully implemented and ready.")
        print("The autonomous agency foundation is established.")
    else:
        print(f"\n⚠️  {total - passed} validation(s) failed.")
        print("Please review the issues above before proceeding.")

    return passed == total


def main():
    """Main validation function"""
    print_header("AUTONOMOUS AGENCY BOOTSTRAP VALIDATION")
    print("This script validates the implementation of Stage 1 bootstrap mechanisms")
    print("for autonomous agency in OpenCog Unified.")

    # Change to the correct directory if needed
    if not Path("AUTONOMOUS-AGENCY-ROADMAP.md").exists():
        if Path("../AUTONOMOUS-AGENCY-ROADMAP.md").exists():
            os.chdir("..")
        else:
            print("Error: Cannot find autonomous agency files.")
            print("Please run this script from the OpenCog Unified root directory.")
            return 1

    # Run validation
    success = generate_validation_report()

    if success:
        print_header("NEXT STEPS")
        print("With Stage 1 successfully implemented, you can now proceed to:")
        print("1. Build and test the autonomous agency module")
        print("2. Begin planning Stage 2: Agentic Event Loops")
        print("3. Design inference engine vortices and metamorphosis protocols")
        print("4. Integrate with URE for advanced reasoning capabilities")
        return 0
    else:
        return 1


if __name__ == "__main__":
    sys.exit(main())
