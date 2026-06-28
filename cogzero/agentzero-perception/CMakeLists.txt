# <<<<<<< copilot/fix-26
#
# CMakeLists.txt for agentzero-perception module
# Part of the AGENT-ZERO-GENESIS project - Task AZ-PERC-002
#

cmake_minimum_required(VERSION 3.16)
project(agentzero-perception)

# ===================================================================
# Component Information
# ===================================================================

set(COMPONENT_NAME "agentzero-perception")
set(COMPONENT_DESCRIPTION "Agent-Zero Perception & Sensory Integration")
set(COMPONENT_VERSION "1.0.0")

# ===================================================================
# Dependencies
# ===================================================================

# Find OpenCog components (required)
find_package(PkgConfig REQUIRED)

# CogUtil (required for logging and utilities)
pkg_check_modules(COGUTIL cogutil)
if(NOT COGUTIL_FOUND)
    message(STATUS "CogUtil not found via pkg-config - using monorepo build")
endif()

# AtomSpace (required for knowledge representation)
pkg_check_modules(ATOMSPACE atomspace)
if(NOT ATOMSPACE_FOUND)
    message(STATUS "AtomSpace not found via pkg-config - using monorepo build")
endif()

# Optional OpenCog perception components
pkg_check_modules(PERCEPTION perception)
pkg_check_modules(SENSORY sensory)
pkg_check_modules(VISION vision)
pkg_check_modules(ATTENTION attention)

# Boost (required)
find_package(Boost REQUIRED COMPONENTS system thread)

# ===================================================================
# Include Directories
# ===================================================================

include_directories(
    ${CMAKE_CURRENT_SOURCE_DIR}/include
    ${COGUTIL_INCLUDE_DIRS}
    ${ATOMSPACE_INCLUDE_DIRS}
    ${Boost_INCLUDE_DIRS}
)

if(PERCEPTION_FOUND)
    include_directories(${PERCEPTION_INCLUDE_DIRS})
    add_definitions(-DHAVE_PERCEPTION)
endif()

if(SENSORY_FOUND)
    include_directories(${SENSORY_INCLUDE_DIRS})
    add_definitions(-DHAVE_SENSORY)
endif()

if(VISION_FOUND)
    include_directories(${VISION_INCLUDE_DIRS})
    add_definitions(-DHAVE_VISION)
endif()

if(ATTENTION_FOUND)
    include_directories(${ATTENTION_INCLUDE_DIRS})
    add_definitions(-DHAVE_ATTENTION)
endif()

# ===================================================================
# Compiler Flags
# ===================================================================

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Compiler-specific flags
if(CMAKE_COMPILER_IS_GNUCXX)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -Wextra -Wno-unused-parameter")
endif()

# ===================================================================
# Source Files
# ===================================================================

set(AGENTZERO_PERCEPTION_SOURCES
    src/PerceptualProcessor.cpp
    src/MultiModalSensor.cpp
)

set(AGENTZERO_PERCEPTION_HEADERS
    include/opencog/agentzero/PerceptualProcessor.h
    include/opencog/agentzero/MultiModalSensor.h
)

# ===================================================================
# Library Target
# ===================================================================

add_library(agentzero-perception SHARED ${AGENTZERO_PERCEPTION_SOURCES})

# Link libraries
target_link_libraries(agentzero-perception
    ${COGUTIL_LIBRARIES}
    ${ATOMSPACE_LIBRARIES}
    ${Boost_LIBRARIES}
)

# Link optional perception libraries if available
if(PERCEPTION_FOUND)
    target_link_libraries(agentzero-perception ${PERCEPTION_LIBRARIES})
endif()

if(SENSORY_FOUND)
    target_link_libraries(agentzero-perception ${SENSORY_LIBRARIES})
endif()

if(VISION_FOUND)
    target_link_libraries(agentzero-perception ${VISION_LIBRARIES})
endif()

if(ATTENTION_FOUND)
    target_link_libraries(agentzero-perception ${ATTENTION_LIBRARIES})
endif()

# Set library properties
set_target_properties(agentzero-perception PROPERTIES
    VERSION ${COMPONENT_VERSION}
    SOVERSION 1
    EXPORT_NAME AgentZeroPerception
)

# ===================================================================
# Installation
# ===================================================================

# Install library
install(TARGETS agentzero-perception
    EXPORT AgentZeroPerceptionTargets
    LIBRARY DESTINATION lib
    ARCHIVE DESTINATION lib
    RUNTIME DESTINATION bin
    INCLUDES DESTINATION include
)

# Install headers
install(FILES ${AGENTZERO_PERCEPTION_HEADERS}
    DESTINATION include/opencog/agentzero
)

# Install CMake config
install(EXPORT AgentZeroPerceptionTargets
    FILE AgentZeroPerceptionTargets.cmake
    NAMESPACE AgentZero::
    DESTINATION lib/cmake/AgentZeroPerception
)

# ===================================================================
# Testing
# ===================================================================

# Enable testing if requested
if(BUILD_TESTING)
    enable_testing()
    add_subdirectory(tests)
endif()

# ===================================================================
# Status Information
# ===================================================================

message(STATUS "")
message(STATUS "========================================")
message(STATUS "Agent-Zero Perception Module Configuration")
message(STATUS "========================================")
message(STATUS "Component: ${COMPONENT_NAME}")
message(STATUS "Description: ${COMPONENT_DESCRIPTION}")
message(STATUS "Version: ${COMPONENT_VERSION}")
message(STATUS "")
message(STATUS "Required Dependencies:")
message(STATUS "  CogUtil: ${COGUTIL_FOUND}")
message(STATUS "  AtomSpace: ${ATOMSPACE_FOUND}")
message(STATUS "  Boost: ${Boost_FOUND}")
message(STATUS "")
message(STATUS "Optional Dependencies:")
message(STATUS "  Perception: ${PERCEPTION_FOUND}")
message(STATUS "  Sensory: ${SENSORY_FOUND}")
message(STATUS "  Vision: ${VISION_FOUND}")
message(STATUS "  Attention: ${ATTENTION_FOUND}")
message(STATUS "")
message(STATUS "Build Configuration:")
message(STATUS "  Testing: ${BUILD_TESTING}")
message(STATUS "  C++ Standard: ${CMAKE_CXX_STANDARD}")
message(STATUS "========================================")
