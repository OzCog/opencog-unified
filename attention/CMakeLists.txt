cmake_minimum_required(VERSION 3.10)
project(attention VERSION 1.0.0)

# Set C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Find required dependencies
find_package(PkgConfig REQUIRED)

# Find CogUtil (required by atomspace)
find_package(CogUtil CONFIG)
if(CogUtil_FOUND)
    message(STATUS "CogUtil found.")
    set(HAVE_COGUTIL 1)
else()
    message(STATUS "CogUtil not found, using relative path")
    set(COGUTIL_INCLUDE_DIR ${CMAKE_CURRENT_SOURCE_DIR}/../cogutil)
endif()

# Find AtomSpace (required)
find_package(AtomSpace CONFIG)
if(AtomSpace_FOUND)
    message(STATUS "AtomSpace found.")
    set(HAVE_ATOMSPACE 1)
    add_definitions(-DHAVE_ATOMSPACE)
else()
    message(STATUS "AtomSpace not found, using relative path")
    set(ATOMSPACE_INCLUDE_DIR ${CMAKE_CURRENT_SOURCE_DIR}/../atomspace)
endif()

# Find CogServer (required)  
find_package(CogServer CONFIG)
if(CogServer_FOUND)
    message(STATUS "CogServer found.")
    set(HAVE_COGSERVER 1)
    add_definitions(-DHAVE_COGSERVER)
else()
    message(STATUS "CogServer not found, using relative path")
    set(COGSERVER_INCLUDE_DIR ${CMAKE_CURRENT_SOURCE_DIR}/../cogserver)
endif()

# Include directories
include_directories(
    ${CMAKE_CURRENT_SOURCE_DIR}
)

# Add include directories based on what was found
if(HAVE_COGUTIL)
    include_directories(${COGUTIL_INCLUDE_DIR})
else()
    include_directories(${CMAKE_CURRENT_SOURCE_DIR}/../cogutil)
endif()

if(HAVE_ATOMSPACE)
    include_directories(${ATOMSPACE_INCLUDE_DIR})
else()
    include_directories(${ATOMSPACE_INCLUDE_DIR})
endif()

if(HAVE_COGSERVER)
    include_directories(${COGSERVER_INCLUDE_DIR})
else()
    include_directories(${COGSERVER_INCLUDE_DIR})
endif()

# Attention library sources
set(ATTENTION_SOURCES
    src/AttentionValue.cc
    src/AttentionBank.cc
    src/ECANAgent.cc
    src/AttentionModule.cc
    src/ImportanceSpreadingAgent.cc
    src/ForgettingAgent.cc
    src/OscillationDetector.cc
)

# Create attention library
add_library(attention SHARED ${ATTENTION_SOURCES})

# Link dependencies
set(ATTENTION_LINK_LIBRARIES "")

# Link with proper targets or fallback libraries
if(HAVE_ATOMSPACE AND TARGET atomspace)
    list(APPEND ATTENTION_LINK_LIBRARIES atomspace)
elseif(ATOMSPACE_LIBRARIES)
    list(APPEND ATTENTION_LINK_LIBRARIES ${ATOMSPACE_LIBRARIES})
endif()

if(HAVE_COGSERVER AND TARGET cogserver)
    list(APPEND ATTENTION_LINK_LIBRARIES cogserver)
elseif(COGSERVER_LIBRARIES)
    list(APPEND ATTENTION_LINK_LIBRARIES ${COGSERVER_LIBRARIES})
endif()

if(HAVE_COGUTIL AND TARGET cogutil)
    list(APPEND ATTENTION_LINK_LIBRARIES cogutil)
elseif(COGUTIL_LIBRARIES)
    list(APPEND ATTENTION_LINK_LIBRARIES ${COGUTIL_LIBRARIES})
endif()

target_link_libraries(attention ${ATTENTION_LINK_LIBRARIES})

# Install targets
install(TARGETS attention
    LIBRARY DESTINATION lib
    ARCHIVE DESTINATION lib
    RUNTIME DESTINATION bin
)

# Install headers
install(DIRECTORY opencog/attention/
    DESTINATION include/opencog/attention
    FILES_MATCHING PATTERN "*.h"
)

# Add tests if BUILD_TESTS is enabled
option(BUILD_TESTS "Build attention tests" ON)
if(BUILD_TESTS)
    add_subdirectory(tests)
endif()

# Explicit dependency declarations for documentation and validation
# The attention module requires:
# - atomspace: For knowledge representation and atom management
# - cogserver: For distributed server integration and management
if(NOT HAVE_ATOMSPACE)
    message(WARNING "AtomSpace is required for attention module but was not found using CONFIG. Using fallback include path.")
endif()

if(NOT HAVE_COGSERVER)
    message(WARNING "CogServer is required for attention module but was not found using CONFIG. Using fallback include path.")
endif()

# Summary
message(STATUS "Attention module configuration:")
message(STATUS "  - AtomSpace dependency: ${HAVE_ATOMSPACE}")
message(STATUS "  - CogServer dependency: ${HAVE_COGSERVER}")
message(STATUS "  - CogUtil dependency: ${HAVE_COGUTIL}")
message(STATUS "  - Link libraries: ${ATTENTION_LINK_LIBRARIES}")