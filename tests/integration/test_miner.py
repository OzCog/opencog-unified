#!/usr/bin/env python3
"""
Test integration of miner component with atomspace and ure dependencies.
Tests that miner properly depends on both atomspace and ure components.
"""

import os
import unittest


class TestMinerIntegration(unittest.TestCase):
    """Test suite for miner component dependency validation."""

    def setUp(self):
        """Set up test environment."""
        self.root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.miner_dir = os.path.join(self.root_dir, "miner")

    def test_miner_directory_exists(self):
        """Test that miner directory exists."""
        self.assertTrue(os.path.exists(self.miner_dir), f"Miner directory should exist at {self.miner_dir}")

    def test_miner_cmakelists_exists(self):
        """Test that miner CMakeLists.txt exists."""
        cmake_file = os.path.join(self.miner_dir, "CMakeLists.txt")
        self.assertTrue(os.path.exists(cmake_file), f"Miner CMakeLists.txt should exist at {cmake_file}")

    def test_miner_dependencies_declared(self):
        """Test that miner declares atomspace and ure dependencies."""
        cmake_file = os.path.join(self.miner_dir, "CMakeLists.txt")

        with open(cmake_file) as f:
            content = f.read()

        # Check for atomspace dependency
        self.assertIn("find_package(AtomSpace REQUIRED)", content, "Miner should declare AtomSpace dependency")

        # Check for ure dependency
        self.assertIn("find_package(URE REQUIRED)", content, "Miner should declare URE dependency")

        # Check for ure linking
        self.assertIn("${URE_LIBRARY}", content, "Miner should link URE library")

    def test_miner_source_files_exist(self):
        """Test that miner source files exist."""
        config_header = os.path.join(self.miner_dir, "opencog", "miner", "MinerConfig.h")
        config_source = os.path.join(self.miner_dir, "opencog", "miner", "MinerConfig.cc")

        self.assertTrue(os.path.exists(config_header), f"MinerConfig.h should exist at {config_header}")
        self.assertTrue(os.path.exists(config_source), f"MinerConfig.cc should exist at {config_source}")

    def test_miner_includes_ure(self):
        """Test that miner source files include ure headers."""
        config_header = os.path.join(self.miner_dir, "opencog", "miner", "MinerConfig.h")
        config_source = os.path.join(self.miner_dir, "opencog", "miner", "MinerConfig.cc")

        with open(config_header) as f:
            header_content = f.read()

        with open(config_source) as f:
            source_content = f.read()

        # Check for ure includes
        self.assertIn("#include <opencog/ure/Rule.h>", header_content, "MinerConfig.h should include URE Rule header")
        self.assertIn("#include <opencog/ure/Rule.h>", source_content, "MinerConfig.cc should include URE Rule header")

    def test_miner_main_cmake_integration(self):
        """Test that miner is integrated in main CMakeLists.txt."""
        main_cmake = os.path.join(self.root_dir, "CMakeLists.txt")

        with open(main_cmake) as f:
            content = f.read()

        # Check that miner is included as subdirectory
        self.assertIn("add_subdirectory(miner)", content, "Main CMakeLists.txt should include miner as subdirectory")

        # Check that miner dependencies are declared
        self.assertIn(
            "add_dependencies(miner atomspace ure)",
            content,
            "Main CMakeLists.txt should declare miner dependencies on atomspace and ure",
        )


def run_tests():
    """Run the test suite."""
    unittest.main()


if __name__ == "__main__":
    run_tests()
