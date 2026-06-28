# Agent-Zero Distributed Computing Module CMakeLists.txt
# Part of the AGENT-ZERO-GENESIS project (AZ-SCALE-001)

cmake_minimum_required(VERSION 3.16)

project(AgentZeroDistributed
    VERSION 0.1.0
    DESCRIPTION "Distributed Computing Integration for Agent-Zero"
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
    include_directories(${COGUTIL_INCLUDE_DIRS})
    link_directories(${COGUTIL_LIBRARY_DIRS})
endif()

# Find atomspace  
pkg_check_modules(ATOMSPACE atomspace)
if (ATOMSPACE_FOUND)
    message(STATUS "Found atomspace version ${ATOMSPACE_VERSION}")
    include_directories(${ATOMSPACE_INCLUDE_DIRS})
    link_directories(${ATOMSPACE_LIBRARY_DIRS})
endif()

# Find optional distributed storage backends
pkg_check_modules(ATOMSPACE_RPC atomspace-rpc)
if (ATOMSPACE_RPC_FOUND)
    message(STATUS "Found atomspace-rpc version ${ATOMSPACE_RPC_VERSION}")
    include_directories(${ATOMSPACE_RPC_INCLUDE_DIRS})
    link_directories(${ATOMSPACE_RPC_LIBRARY_DIRS})
    add_compile_definitions(HAVE_ATOMSPACE_RPC=1)
else()
    message(STATUS "atomspace-rpc not found - RPC features will be disabled")
endif()

pkg_check_modules(ATOMSPACE_DHT atomspace-dht)
if (ATOMSPACE_DHT_FOUND)
    message(STATUS "Found atomspace-dht version ${ATOMSPACE_DHT_VERSION}")
    include_directories(${ATOMSPACE_DHT_INCLUDE_DIRS})
    link_directories(${ATOMSPACE_DHT_LIBRARY_DIRS})
    add_compile_definitions(HAVE_ATOMSPACE_DHT=1)
else()
    message(STATUS "atomspace-dht not found - DHT features will be disabled")
endif()

# Include directories
include_directories(
    ${CMAKE_CURRENT_SOURCE_DIR}/include
    ${CMAKE_CURRENT_SOURCE_DIR}/../agentzero-core/include
)

# Source files
set(AGENTZERO_DISTRIBUTED_SOURCES
    src/DistributedCoordinator.cpp
    src/ClusterManager.cpp
    src/LoadBalancer.cpp
)

# Header files
set(AGENTZERO_DISTRIBUTED_HEADERS
    include/opencog/agentzero/distributed/DistributedCoordinator.h
    include/opencog/agentzero/distributed/ClusterManager.h
    include/opencog/agentzero/distributed/LoadBalancer.h
)

# Create library
add_library(agentzero-distributed SHARED
    ${AGENTZERO_DISTRIBUTED_SOURCES}
    ${AGENTZERO_DISTRIBUTED_HEADERS}
)

target_link_libraries(agentzero-distributed
    ${COGUTIL_LIBRARIES}
    ${ATOMSPACE_LIBRARIES}
    ${Boost_LIBRARIES}
)

# Link optional backends if available
if(ATOMSPACE_RPC_FOUND AND ATOMSPACE_RPC_LIBRARIES)
    target_link_libraries(agentzero-distributed ${ATOMSPACE_RPC_LIBRARIES})
    message(STATUS "Linking atomspace-rpc libraries")
endif()

if(ATOMSPACE_DHT_FOUND AND ATOMSPACE_DHT_LIBRARIES)
    target_link_libraries(agentzero-distributed ${ATOMSPACE_DHT_LIBRARIES})
    message(STATUS "Linking atomspace-dht libraries")
endif()

target_include_directories(agentzero-distributed PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
    $<INSTALL_INTERFACE:include>
)

# Installation
install(TARGETS agentzero-distributed
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

# Tests
if(BUILD_TESTING)
    enable_testing()
    add_subdirectory(tests)
endif()

# Examples
if(BUILD_EXAMPLES)
    add_subdirectory(examples)
endif()

# Status message
message(STATUS "Agent-Zero Distributed Computing module configured")
message(STATUS "  RPC support: ${ATOMSPACE_RPC_FOUND}")
message(STATUS "  DHT support: ${ATOMSPACE_DHT_FOUND}")
