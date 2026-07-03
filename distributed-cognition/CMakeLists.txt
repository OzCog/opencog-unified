# Phase II.3: Distributed Cognition Engine
# Multi-agent Scheme modules for parallel cognitive cycles

cmake_minimum_required(VERSION 3.10)
project(distributed-cognition)

# Set C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Include directories from parent modules
include_directories(${CMAKE_SOURCE_DIR}/cogutil/opencog)
include_directories(${CMAKE_SOURCE_DIR}/atomspace/opencog)
include_directories(${CMAKE_SOURCE_DIR}/cogserver/opencog)
include_directories(${CMAKE_SOURCE_DIR}/cognitive-patterns/include)
include_directories(${CMAKE_CURRENT_SOURCE_DIR}/include)

# Source files for distributed cognition
set(DISTRIBUTED_SOURCES
    src/CognitiveAgent.cc
    src/AgentCoordinator.cc
    src/SharedHypergraphContext.cc
    src/DistributedCognitionEngine.cc
    src/ECANResourceManager.cc
    src/TensorHypergraphProtocol.cc
    src/DistributedAtomSpaceSync.cc
    src/MultiAgentStressTest.cc
)

# Header files
set(DISTRIBUTED_HEADERS
    include/CognitiveAgent.h
    include/AgentCoordinator.h
    include/SharedHypergraphContext.h
    include/DistributedCognitionEngine.h
    include/ECANResourceManager.h
    include/TensorHypergraphProtocol.h
    include/DistributedAtomSpaceSync.h
    include/MultiAgentStressTest.h
)

# Create include directory
file(MAKE_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/include)
file(MAKE_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/src)
file(MAKE_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/scheme)

# Create the distributed cognition library
add_library(distributed-cognition SHARED ${DISTRIBUTED_SOURCES})
ADD_DEPENDENCIES(distributed-cognition atombase atomcore atomspace atomvalue cogutil truthvalue)


# Link with parent modules (when they're available)
# target_link_libraries(distributed-cognition cogutil atomspace cognitive-patterns)

# Install headers
install(FILES ${DISTRIBUTED_HEADERS} DESTINATION include/opencog/distributed-cognition)

# Install library
install(TARGETS distributed-cognition DESTINATION lib)

# Install Scheme files
install(DIRECTORY scheme/ DESTINATION share/opencog/scm/distributed-cognition/)