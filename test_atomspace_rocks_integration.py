#!/usr/bin/env python3
"""
Integration test for Phase 1 Week 1: AtomSpace-Rocks storage backend
This test verifies that the RocksDB storage backend is functional.
"""

import os
import subprocess
import sys
import tempfile


def test_atomspace_rocks_guile():
    """Test basic RocksDB storage functionality using Guile"""

    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test.rdb")

        # Create a test Scheme script
        test_script = f"""
(use-modules (opencog))
(use-modules (opencog persist))
(use-modules (opencog persist-rocks))

; Create a test atom
(define test-atom (Concept "TestConcept"))

; Create RocksDB storage
(define storage (RocksStorageNode "rocks://{db_path}/"))

; Open storage and store atom
(cog-open storage)
(store-atom test-atom)
(cog-close storage)

; Re-open storage and load atom
(cog-open storage)
(load-atomspace)
(cog-close storage)

; Check if atom exists
(if (not (null? (cog-node 'Concept "TestConcept")))
    (display "SUCCESS: AtomSpace-Rocks integration test passed!\\n")
    (display "FAILED: AtomSpace-Rocks integration test failed!\\n"))
"""

        script_path = os.path.join(tmpdir, "test_rocks.scm")
        with open(script_path, "w") as f:
            f.write(test_script)

        try:
            # Run the test
            result = subprocess.run(["guile", "-l", script_path], capture_output=True, text=True, timeout=30)

            if result.returncode == 0 and "SUCCESS" in result.stdout:
                print("✓ AtomSpace-Rocks integration test PASSED")
                return True
            else:
                print("✗ AtomSpace-Rocks integration test FAILED")
                print("Return code: {result.returncode}")
                print("Stdout: {result.stdout}")
                print("Stderr: {result.stderr}")
                return False

        except subprocess.TimeoutExpired:
            print("✗ AtomSpace-Rocks integration test TIMED OUT")
            return False
        except FileNotFoundError:
            print("✗ Guile not found - cannot run AtomSpace-Rocks test")
            return False


def test_rocksdb_library():
    """Test that RocksDB library is accessible"""
    try:
        # Check if RocksDB library is installed
        result = subprocess.run(["pkg-config", "--exists", "rocksdb"], capture_output=True)
        if result.returncode == 0:
            print("✓ RocksDB library found")
            return True
        else:
            # Try alternative check
            result = subprocess.run(["ldconfig", "-p"], capture_output=True, text=True)
            if "rocksdb" in result.stdout:
                print("✓ RocksDB library found via ldconfig")
                return True
            else:
                print("✗ RocksDB library not found")
                return False
    except Exception:
        print("✗ Error checking RocksDB library")
        return False


def main():
    """Run integration tests for Week 1: AtomSpace-Rocks"""
    print("=== Phase 1 Week 1 Integration Test: AtomSpace-Rocks ===")

    tests_passed = 0
    total_tests = 2

    # Test 1: RocksDB library availability
    if test_rocksdb_library():
        tests_passed += 1

    # Test 2: AtomSpace-Rocks functionality
    if test_atomspace_rocks_guile():
        tests_passed += 1

    print("\n=== Results: {tests_passed}/{total_tests} tests passed ===")

    if tests_passed == total_tests:
        print("🎉 All integration tests PASSED!")
        sys.exit(0)
    else:
        print("❌ Some integration tests FAILED!")
        sys.exit(1)


if __name__ == "__main__":
    main()
