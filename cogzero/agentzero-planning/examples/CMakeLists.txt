#<<<<<<< copilot/fix-38
cmake_minimum_required(VERSION 3.16)

# Include directories
include_directories(
    ${CMAKE_CURRENT_SOURCE_DIR}/../include
    ${COGUTIL_INCLUDE_DIR}
    ${ATOMSPACE_INCLUDE_DIR}
    ${OCTOMAP_INCLUDE_DIRS}
)

if(SPACETIME_FOUND)
    include_directories(${SPACETIME_INCLUDE_DIR})
endif()

# Example executable
add_executable(spatial_temporal_example spatial_temporal_example.cpp)

# Link libraries
target_link_libraries(spatial_temporal_example
    agentzero-planning
    ${COGUTIL_LIBRARY}
    ${ATOMSPACE_LIBRARY}
    ${OCTOMAP_LIBRARIES}
)

if(SPACETIME_FOUND)
    target_link_libraries(spatial_temporal_example ${SPACETIME_LIBRARY})
endif()

# Install example
install(TARGETS spatial_temporal_example
    RUNTIME DESTINATION bin/examples
)
#=======
# Agent-Zero Planning Examples CMakeLists.txt

cmake_minimum_required(VERSION 3.16)

# Find required libraries
find_package(PkgConfig REQUIRED)
pkg_check_modules(COGUTIL cogutil)
pkg_check_modules(ATOMSPACE atomspace)

# Include directories
include_directories(
    ${CMAKE_CURRENT_SOURCE_DIR}/../include
    ${COGUTIL_INCLUDE_DIRS}
    ${ATOMSPACE_INCLUDE_DIRS}
)

# Link directories
link_directories(
    ${COGUTIL_LIBRARY_DIRS}
    ${ATOMSPACE_LIBRARY_DIRS}
)

# Simple planning demo
add_executable(simple_planning_demo
    simple_planning_demo.cpp
)

target_link_libraries(simple_planning_demo
    agentzero-planning
    ${ATOMSPACE_LIBRARIES}
    ${COGUTIL_LIBRARIES}
    atom_types
    atombase
)

message(STATUS "Agent-Zero Planning examples configured")
#>>>>>>> main
