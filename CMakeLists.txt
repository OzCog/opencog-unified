cmake_minimum_required(VERSION 3.10)
project(opencog-unified)

# Include dependencies
add_subdirectory(deps)

# Include unified cognitive modules
add_subdirectory(cogutil)
add_subdirectory(atomspace)
add_subdirectory(cogserver)

# Define inter-module dependencies explicitly
add_dependencies(atomspace cogutil)
add_dependencies(cogserver atomspace)

# Global cognitive build targets
add_custom_target(cognitive ALL DEPENDS cogutil atomspace cogserver)