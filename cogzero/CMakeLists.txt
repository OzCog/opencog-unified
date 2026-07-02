# CogZero: Agent-Zero C++ Implementation for OpenCog Integration
# Integrated into OpenCog Unified monorepo
# Original source: https://github.com/o9nn/cogzero

cmake_minimum_required(VERSION 3.16)

# When building as part of opencog-unified, project is already set
if(NOT PROJECT_NAME)
    project(CogZero
        VERSION 0.1.0
        DESCRIPTION "C++ Agent-Zero Implementation Optimized for OpenCog Integration"
        LANGUAGES CXX
    )
endif()

# Set C++ standard (inherit from parent if set)
if(NOT CMAKE_CXX_STANDARD)
    set(CMAKE_CXX_STANDARD 17)
    set(CMAKE_CXX_STANDARD_REQUIRED ON)
endif()

# Build options
option(COGZERO_BUILD_TESTING "Build CogZero tests" ON)
option(COGZERO_BUILD_EXAMPLES "Build CogZero example applications" ON)
option(COGZERO_BUILD_DOCS "Build CogZero documentation" OFF)

message(STATUS "")
message(STATUS "=== CogZero: Agent-Zero C++ for OpenCog ===")
message(STATUS "Build type: ${CMAKE_BUILD_TYPE}")

# Compiler settings for this module
if(CMAKE_BUILD_TYPE STREQUAL "Debug")
    add_compile_options(-g -O0)
else()
    add_compile_options(-O3 -DNDEBUG)
endif()

# ----------------------------------------------------------
# OpenCog Monorepo Integration
# When part of opencog-unified, use local targets instead of pkg-config
# ----------------------------------------------------------

# Check if we're building as part of opencog-unified
if(TARGET cogutil)
    message(STATUS "CogZero: Using monorepo cogutil target")
    set(COGZERO_COGUTIL_TARGET cogutil)
    set(COGUTIL_FOUND TRUE)
else()
    find_package(PkgConfig REQUIRED)
    pkg_check_modules(COGUTIL cogutil)
    if(COGUTIL_FOUND)
        set(COGZERO_COGUTIL_LIBS ${COGUTIL_LIBRARIES})
        include_directories(${COGUTIL_INCLUDE_DIRS})
        link_directories(${COGUTIL_LIBRARY_DIRS})
    endif()
endif()

if(TARGET atomspace)
    message(STATUS "CogZero: Using monorepo atomspace target")
    set(COGZERO_ATOMSPACE_TARGET atomspace)
    set(ATOMSPACE_FOUND TRUE)
else()
    pkg_check_modules(ATOMSPACE atomspace)
    if(ATOMSPACE_FOUND)
        set(COGZERO_ATOMSPACE_LIBS ${ATOMSPACE_LIBRARIES})
        include_directories(${ATOMSPACE_INCLUDE_DIRS})
        link_directories(${ATOMSPACE_LIBRARY_DIRS})
    endif()
endif()

if(TARGET server)
    message(STATUS "CogZero: Using monorepo cogserver target")
    set(COGZERO_COGSERVER_TARGET server)
    set(COGSERVER_FOUND TRUE)
else()
    pkg_check_modules(COGSERVER cogserver)
    if(COGSERVER_FOUND)
        set(COGZERO_COGSERVER_LIBS ${COGSERVER_LIBRARIES})
        include_directories(${COGSERVER_INCLUDE_DIRS})
        link_directories(${COGSERVER_LIBRARY_DIRS})
    endif()
endif()

# Check for required dependencies
if(NOT COGUTIL_FOUND)
    message(WARNING "CogZero: cogutil not found via pkg-config - using monorepo targets")
endif()

if(NOT ATOMSPACE_FOUND)
    message(WARNING "CogZero: atomspace not found via pkg-config - using monorepo targets")
endif()

if(NOT COGSERVER_FOUND)
    message(WARNING "CogZero: cogserver not found - some features may be disabled")
endif()

# Optional OpenCog dependencies (check for monorepo targets first)
if(TARGET pln)
    set(PLN_FOUND TRUE)
    set(COGZERO_PLN_TARGET pln)
    message(STATUS "CogZero: Using monorepo pln target")
endif()

if(TARGET ure)
    set(URE_FOUND TRUE)
    set(COGZERO_URE_TARGET ure)
    message(STATUS "CogZero: Using monorepo ure target")
endif()

if(TARGET miner)
    set(MINER_FOUND TRUE)
    set(COGZERO_MINER_TARGET miner)
    message(STATUS "CogZero: Using monorepo miner target")
endif()

if(TARGET moses)
    set(MOSES_FOUND TRUE)
    set(COGZERO_MOSES_TARGET moses)
    message(STATUS "CogZero: Using monorepo moses target")
endif()

if(TARGET attention)
    set(ATTENTION_FOUND TRUE)
    set(COGZERO_ATTENTION_TARGET attention)
    message(STATUS "CogZero: Using monorepo attention target")
endif()

if(TARGET spacetime)
    set(SPACETIME_FOUND TRUE)
    set(COGZERO_SPACETIME_TARGET spacetime)
    message(STATUS "CogZero: Using monorepo spacetime target")
endif()

if(TARGET lg-atomese)
    set(LG_ATOMESE_FOUND TRUE)
    set(COGZERO_LG_ATOMESE_TARGET lg-atomese)
    message(STATUS "CogZero: Using monorepo lg-atomese target")
endif()

# Report found dependencies
message(STATUS "CogZero OpenCog Dependencies:")
message(STATUS "  cogutil: ${COGUTIL_FOUND}")
message(STATUS "  atomspace: ${ATOMSPACE_FOUND}")
message(STATUS "  cogserver: ${COGSERVER_FOUND}")
message(STATUS "  pln: ${PLN_FOUND}")
message(STATUS "  ure: ${URE_FOUND}")
message(STATUS "  moses: ${MOSES_FOUND}")
message(STATUS "  attention: ${ATTENTION_FOUND}")
message(STATUS "  spacetime: ${SPACETIME_FOUND}")

# Global include directories for cogzero
include_directories(
    ${CMAKE_CURRENT_SOURCE_DIR}/include
    ${CMAKE_CURRENT_SOURCE_DIR}/agentzero-core/include
    ${CMAKE_CURRENT_SOURCE_DIR}/agentzero-perception/include
    ${CMAKE_CURRENT_SOURCE_DIR}/agentzero-planning/include
    ${CMAKE_CURRENT_SOURCE_DIR}/agentzero-learning/include
    ${CMAKE_CURRENT_SOURCE_DIR}/agentzero-communication/include
    ${CMAKE_CURRENT_SOURCE_DIR}/agentzero-memory/include
    ${CMAKE_CURRENT_SOURCE_DIR}/agentzero-tools/include
    ${CMAKE_CURRENT_SOURCE_DIR}/agentzero-distributed/include
)

# ----------------------------------------------------------
# Add subdirectories for each Agent-Zero module
# These are added in dependency order
# ----------------------------------------------------------

# Phase 1: Foundation Layer (always built)
add_subdirectory(agentzero-core)

# Phase 2: Perception & Action (depends on core)
add_subdirectory(agentzero-perception)

# Phase 3: Knowledge & Reasoning (depends on core, PLN, URE)
if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/agentzero-knowledge/CMakeLists.txt")
    if(PLN_FOUND AND URE_FOUND)
        add_subdirectory(agentzero-knowledge)
    else()
        message(STATUS "CogZero: Skipping agentzero-knowledge (PLN/URE not found)")
    endif()
endif()

# Phase 4: Planning & Goals (depends on core, spacetime)
if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/agentzero-planning/CMakeLists.txt")
    add_subdirectory(agentzero-planning)
    if(NOT SPACETIME_FOUND)
        message(STATUS "CogZero: agentzero-planning built with limited features (spacetime not found)")
    endif()
endif()

# Phase 5: Learning & Adaptation (depends on core, MOSES)
if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/agentzero-learning/CMakeLists.txt")
    add_subdirectory(agentzero-learning)
    if(NOT MOSES_FOUND)
        message(STATUS "CogZero: agentzero-learning built with limited features (MOSES not found)")
    endif()
endif()

# Phase 6: Communication & NLP (depends on core)
# NOTE: Fixed duplicate add_subdirectory from original
if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/agentzero-communication/CMakeLists.txt")
    add_subdirectory(agentzero-communication)
    if(NOT LG_ATOMESE_FOUND)
        message(STATUS "CogZero: agentzero-communication built with basic NLP (lg-atomese not found)")
    endif()
endif()

# Phase 7: Memory & Context (depends on core, attention)
if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/agentzero-memory/CMakeLists.txt")
    add_subdirectory(agentzero-memory)
    if(NOT ATTENTION_FOUND)
        message(STATUS "CogZero: agentzero-memory built with limited features (attention not found)")
    endif()
endif()

# Phase 8: Tool Integration (depends on core)
if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/agentzero-tools/CMakeLists.txt")
    add_subdirectory(agentzero-tools)
endif()

# Phase 9: Profiling Infrastructure
if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/profiling/CMakeLists.txt")
    add_subdirectory(profiling)
endif()

# Phase 10: Distributed Computing
if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/agentzero-distributed/CMakeLists.txt")
    add_subdirectory(agentzero-distributed)
endif()

# Phase 11: Python Bridge
if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/agentzero-python-bridge/CMakeLists.txt")
    add_subdirectory(agentzero-python-bridge)
endif()

# Examples
if(COGZERO_BUILD_EXAMPLES AND EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/examples/CMakeLists.txt")
    add_subdirectory(examples)
endif()

# Tests
if(COGZERO_BUILD_TESTING AND EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/tests/CMakeLists.txt")
    enable_testing()
    add_subdirectory(tests)
endif()

# Documentation
if(COGZERO_BUILD_DOCS)
    find_package(Doxygen)
    if(DOXYGEN_FOUND AND EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/docs/CMakeLists.txt")
        add_subdirectory(docs)
    else()
        message(STATUS "CogZero: Doxygen not found, documentation will not be built")
    endif()
endif()

# ----------------------------------------------------------
# Create unified cogzero target for easy dependency management
# ----------------------------------------------------------
add_custom_target(cogzero
    COMMENT "Building all CogZero modules"
)

# Add dependencies based on what's available
if(TARGET agentzero-core)
    add_dependencies(cogzero agentzero-core)
endif()
if(TARGET agentzero-perception)
    add_dependencies(cogzero agentzero-perception)
endif()
if(TARGET agentzero-planning)
    add_dependencies(cogzero agentzero-planning)
endif()
if(TARGET agentzero-learning)
    add_dependencies(cogzero agentzero-learning)
endif()
if(TARGET agentzero-communication)
    add_dependencies(cogzero agentzero-communication)
endif()
if(TARGET agentzero-memory)
    add_dependencies(cogzero agentzero-memory)
endif()
if(TARGET agentzero-tools)
    add_dependencies(cogzero agentzero-tools)
endif()
if(TARGET agentzero-distributed)
    add_dependencies(cogzero agentzero-distributed)
endif()

# Status summary
message(STATUS "")
message(STATUS "CogZero Configuration Summary:")
message(STATUS "  Version: 0.1.0")
message(STATUS "  Build testing: ${COGZERO_BUILD_TESTING}")
message(STATUS "  Build examples: ${COGZERO_BUILD_EXAMPLES}")
message(STATUS "  Build documentation: ${COGZERO_BUILD_DOCS}")
message(STATUS "=== CogZero configuration complete ===")
message(STATUS "")
