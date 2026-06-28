# Simple build for TaskManager testing
cmake_minimum_required(VERSION 3.16)
project(TaskManagerTest)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Find dependencies
find_package(PkgConfig REQUIRED)
pkg_check_modules(COGUTIL cogutil)

# Manually specify atomspace paths
set(ATOMSPACE_INCLUDE_DIRS "/usr/local/include")
set(ATOMSPACE_LIBRARY_DIRS "/usr/local/lib/opencog")
set(ATOMSPACE_LIBRARIES "atomspace;atombase;truthvalue;value;atom_types;cogutil")

# Include directories
include_directories(${COGUTIL_INCLUDE_DIRS})
include_directories(${ATOMSPACE_INCLUDE_DIRS})
include_directories(../../include)

# Link directories
link_directories(${COGUTIL_LIBRARY_DIRS})
link_directories(${ATOMSPACE_LIBRARY_DIRS})

# Create executable
add_executable(task_manager_test 
    ../TaskManagerGoalTest.cpp
    ../../src/TaskManager.cpp
)

target_link_libraries(task_manager_test
    ${COGUTIL_LIBRARIES}
    ${ATOMSPACE_LIBRARIES}
)