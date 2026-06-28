cmake_minimum_required(VERSION 3.16)

# Project metadata
project(agentzero-tools VERSION 0.1.0 DESCRIPTION "Agent-Zero Tool Integration Framework")

message(STATUS "Configuring Agent-Zero Tool Integration Framework...")

# Find required dependencies
find_package(CogUtil REQUIRED)
find_package(AtomSpace REQUIRED)
# Agent-Zero Tools Module CMakeLists.txt
# Phase 8: Tool Integration - AZ-TOOL-002

cmake_minimum_required(VERSION 3.16)

project(AgentZeroTools
    VERSION 0.1.0
    DESCRIPTION "Agent-Zero Tool Integration Framework for OpenCog"
    LANGUAGES CXX
)

# Set C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Find required OpenCog packages
find_package(PkgConfig REQUIRED)

# Find cogutil
pkg_check_modules(COGUTIL cogutil)
if (COGUTIL_FOUND)
    message(STATUS "Found cogutil version ${COGUTIL_VERSION}")
# Try to find cogutil
pkg_check_modules(COGUTIL cogutil)
if (NOT COGUTIL_FOUND)
    # Try CMake find_package as fallback
    find_package(CogUtil REQUIRED)
    set(COGUTIL_INCLUDE_DIRS ${COGUTIL_INCLUDE_DIR})
    set(COGUTIL_LIBRARIES ${COGUTIL_LIBRARY})
endif()

if (COGUTIL_FOUND OR CogUtil_FOUND)
    message(STATUS "Found cogutil")
    include_directories(${COGUTIL_INCLUDE_DIRS})
    link_directories(${COGUTIL_LIBRARY_DIRS})
endif()

# Find atomspace  
pkg_check_modules(ATOMSPACE atomspace)
if (ATOMSPACE_FOUND)
    message(STATUS "Found atomspace version ${ATOMSPACE_VERSION}")
# Try to find atomspace  
pkg_check_modules(ATOMSPACE atomspace)
if (NOT ATOMSPACE_FOUND)
    # Try CMake find_package as fallback
    find_package(AtomSpace REQUIRED)
    set(ATOMSPACE_INCLUDE_DIRS ${ATOMSPACE_INCLUDE_DIR})
    set(ATOMSPACE_LIBRARIES ${ATOMSPACE_LIBRARY})
endif()

if (ATOMSPACE_FOUND OR AtomSpace_FOUND)
    message(STATUS "Found atomspace")
    include_directories(${ATOMSPACE_INCLUDE_DIRS})
    link_directories(${ATOMSPACE_LIBRARY_DIRS})
endif()

# Include directories
include_directories(
    ${CMAKE_CURRENT_SOURCE_DIR}/include
    ${COGUTIL_INCLUDE_DIR}
    ${ATOMSPACE_INCLUDE_DIR}
)

# Library sources
set(TOOLS_SOURCES
    src/CapabilityComposer.cpp
    src/ToolWrapper.cpp
    src/ToolRegistry.cpp
    src/ResourceManager.cpp
)

# Create the agentzero-tools library
add_library(agentzero-tools SHARED ${TOOLS_SOURCES})

# Link dependencies
target_link_libraries(agentzero-tools
    ${COGUTIL_LIBRARY}
    ${ATOMSPACE_LIBRARY}
)

# Set library properties
set_target_properties(agentzero-tools PROPERTIES
    VERSION "1.0.0"
    SOVERSION "1"
)

# Install targets
install(TARGETS agentzero-tools
    LIBRARY DESTINATION lib
    ARCHIVE DESTINATION lib
)

# Install headers
install(DIRECTORY include/opencog
    DESTINATION include
    FILES_MATCHING PATTERN "*.h"
)

# Add tests if requested
option(BUILD_TESTS "Build tests" ON)
if(BUILD_TESTS)
    add_subdirectory(tests)
endif()

# Add examples
option(BUILD_EXAMPLES "Build examples" ON)
    ${CMAKE_CURRENT_SOURCE_DIR}/src
)

# Source files
set(AGENTZERO_TOOLS_SOURCES
    src/ToolWrapper.cpp
    src/ToolRegistry.cpp
)

# Header files
set(AGENTZERO_TOOLS_HEADERS
    include/opencog/agentzero/tools/ToolWrapper.h
)

# Create library
add_library(agentzero-tools SHARED
    ${AGENTZERO_TOOLS_SOURCES}
    ${AGENTZERO_TOOLS_HEADERS}
)

target_link_libraries(agentzero-tools
    ${COGUTIL_LIBRARIES}
    ${ATOMSPACE_LIBRARIES}
    ${Boost_LIBRARIES}
)

target_include_directories(agentzero-tools PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
    $<INSTALL_INTERFACE:include>
)

# Installation
install(TARGETS agentzero-tools
    EXPORT AgentZeroCppTargets
    LIBRARY DESTINATION lib
    ARCHIVE DESTINATION lib
    RUNTIME DESTINATION bin
    INCLUDES DESTINATION include
)

install(DIRECTORY include/
    DESTINATION include
    FILES_MATCHING PATTERN "*.h"
)
    include/opencog/agentzero/ToolRegistry.h
)

# Create library
if(AGENTZERO_TOOLS_SOURCES)
    add_library(agentzero-tools SHARED
        ${AGENTZERO_TOOLS_SOURCES}
        ${AGENTZERO_TOOLS_HEADERS}
    )

    target_link_libraries(agentzero-tools
        ${COGUTIL_LIBRARIES}
        ${ATOMSPACE_LIBRARIES}
        ${Boost_LIBRARIES}
    )

    target_include_directories(agentzero-tools PUBLIC
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
        $<INSTALL_INTERFACE:include>
    )

    # Installation
    install(TARGETS agentzero-tools
        EXPORT AgentZeroToolsTargets
        LIBRARY DESTINATION lib
        ARCHIVE DESTINATION lib
        RUNTIME DESTINATION bin
        INCLUDES DESTINATION include
    )

    install(DIRECTORY include/
        DESTINATION include
        FILES_MATCHING PATTERN "*.h"
    )
endif()

# Tests
if(BUILD_TESTING)
    enable_testing()
    add_subdirectory(tests)
endif()

# Examples
if(BUILD_EXAMPLES)
    add_subdirectory(examples)
endif()

message(STATUS "Agent-Zero Tools module configured successfully")
# Status message
message(STATUS "Agent-Zero Tools module configuration complete")
message(STATUS "AZ-TOOL-002: ToolWrapper unified interface implemented")
# Status message
message(STATUS "Agent-Zero Tools module configuration complete")
message(STATUS "ToolRegistry implementation ready for build and testing")
