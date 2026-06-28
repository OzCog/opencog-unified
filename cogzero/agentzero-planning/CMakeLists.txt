#<<<<<<< copilot/fix-38
cmake_minimum_required(VERSION 3.16)
project(agentzero-planning VERSION 0.1.0 DESCRIPTION "Agent-Zero Planning Module with Spatial-Temporal Integration")
#=======
# Agent-Zero Planning Module CMakeLists.txt

cmake_minimum_required(VERSION 3.16)

project(AgentZeroPlanning
    VERSION 0.1.0
    DESCRIPTION "Agent-Zero Planning Engine with temporal reasoning for OpenCog Integration"
    LANGUAGES CXX
)
#>>>>>>> main

# Set C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

#<<<<<<< copilot/fix-38
message(STATUS "Configuring Agent-Zero Planning Module (AZ-SPATIAL-001)")

# Dependencies
find_package(PkgConfig REQUIRED)
find_package(CogUtil REQUIRED)
find_package(AtomSpace REQUIRED)

# Find spacetime - it should be available as it's in the cognitive layer
find_path(SPACETIME_INCLUDE_DIR
    NAMES opencog/spacetime/octomap/TimeOctomap.h
    PATHS
        /usr/local/include
        /usr/include
        ${CMAKE_PREFIX_PATH}/include
    NO_DEFAULT_PATH
)

find_library(SPACETIME_LIBRARY
    NAMES spacetime
    PATHS
        /usr/local/lib
        /usr/lib
        ${CMAKE_PREFIX_PATH}/lib
    NO_DEFAULT_PATH
)

if(SPACETIME_INCLUDE_DIR AND SPACETIME_LIBRARY)
    message(STATUS "Found spacetime library: ${SPACETIME_LIBRARY}")
    message(STATUS "Found spacetime includes: ${SPACETIME_INCLUDE_DIR}")
    set(SPACETIME_FOUND TRUE)
else()
    message(WARNING "Spacetime library not found - building without spacetime integration")
    set(SPACETIME_FOUND FALSE)
endif()

# Find octomap
find_package(PkgConfig QUIET)
if(PKG_CONFIG_FOUND)
    pkg_check_modules(OCTOMAP octomap)
endif()

if(NOT OCTOMAP_FOUND)
    find_path(OCTOMAP_INCLUDE_DIR 
        NAMES octomap/octomap.h
        PATHS /usr/local/include /usr/include
    )
    find_library(OCTOMAP_LIBRARY 
        NAMES octomap
        PATHS /usr/local/lib /usr/lib
    )
    if(OCTOMAP_INCLUDE_DIR AND OCTOMAP_LIBRARY)
        set(OCTOMAP_FOUND TRUE)
        set(OCTOMAP_INCLUDE_DIRS ${OCTOMAP_INCLUDE_DIR})
        set(OCTOMAP_LIBRARIES ${OCTOMAP_LIBRARY})
    endif()
endif()

if(NOT OCTOMAP_FOUND)
    message(FATAL_ERROR "Octomap library is required for spatial-temporal planning")
#=======
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

# Find spacetime (optional for enhanced temporal reasoning)
pkg_check_modules(SPACETIME spacetime)
if (SPACETIME_FOUND)
    message(STATUS "Found spacetime version ${SPACETIME_VERSION}")
    include_directories(${SPACETIME_INCLUDE_DIRS})
    link_directories(${SPACETIME_LIBRARY_DIRS})
else()
    message(STATUS "Spacetime module not found - using basic temporal reasoning")
    set(SPACETIME_FOUND FALSE)
endif()

# Find cogserver (optional but preferred)
pkg_check_modules(COGSERVER cogserver)
if (COGSERVER_FOUND)
    message(STATUS "Found cogserver version ${COGSERVER_VERSION}")
    include_directories(${COGSERVER_INCLUDE_DIRS})
    link_directories(${COGSERVER_LIBRARY_DIRS})
else()
    message(STATUS "CogServer not found - some features will be disabled")
    set(COGSERVER_FOUND FALSE)
#>>>>>>> main
endif()

# Include directories
include_directories(
    ${CMAKE_CURRENT_SOURCE_DIR}/include
#<<<<<<< copilot/fix-38
    ${COGUTIL_INCLUDE_DIR}
    ${ATOMSPACE_INCLUDE_DIR}
    ${OCTOMAP_INCLUDE_DIRS}
)

if(SPACETIME_FOUND)
    include_directories(${SPACETIME_INCLUDE_DIR})
    add_definitions(-DHAVE_SPACETIME)
endif()

# Source files
set(SOURCES
    src/SpaceTimeIntegrator.cpp
)

set(HEADERS
    include/opencog/agentzero/SpaceTimeIntegrator.h
)

# Create the library
add_library(agentzero-planning SHARED ${SOURCES})

# Link libraries
target_link_libraries(agentzero-planning
    ${COGUTIL_LIBRARY}
    ${ATOMSPACE_LIBRARY}
    ${OCTOMAP_LIBRARIES}
)

if(SPACETIME_FOUND)
    target_link_libraries(agentzero-planning ${SPACETIME_LIBRARY})
endif()

# Install targets
install(TARGETS agentzero-planning
    LIBRARY DESTINATION lib
    ARCHIVE DESTINATION lib
    RUNTIME DESTINATION bin
)

install(DIRECTORY include/opencog
    DESTINATION include
    FILES_MATCHING PATTERN "*.h"
)

# Tests
if(BUILD_TESTING)
#=======
    ${CMAKE_CURRENT_SOURCE_DIR}/src
)

# Source files
set(AGENTZERO_PLANNING_SOURCES
    src/PlanningEngine.cpp
    src/GoalHierarchy.cpp
    src/TemporalReasoner.cpp
)

# Header files
set(AGENTZERO_PLANNING_HEADERS
    include/opencog/agentzero/PlanningEngine.h
    include/opencog/agentzero/GoalHierarchy.h
    include/opencog/agentzero/TemporalReasoner.h
)

# Create library (when source files exist)
if(AGENTZERO_PLANNING_SOURCES)
    add_library(agentzero-planning SHARED
        ${AGENTZERO_PLANNING_SOURCES}
        ${AGENTZERO_PLANNING_HEADERS}
    )

    target_link_libraries(agentzero-planning
        ${COGUTIL_LIBRARIES}
        ${ATOMSPACE_LIBRARIES}
        ${Boost_LIBRARIES}
    )
    
    # Link spacetime libraries if available
    if(SPACETIME_FOUND AND SPACETIME_LIBRARIES)
        target_link_libraries(agentzero-planning ${SPACETIME_LIBRARIES})
        target_compile_definitions(agentzero-planning PRIVATE HAVE_SPACETIME=1)
        message(STATUS "Linking spacetime libraries: ${SPACETIME_LIBRARIES}")
    endif()
    
    # Link cogserver libraries if available
    if(COGSERVER_FOUND AND COGSERVER_LIBRARIES)
        target_link_libraries(agentzero-planning ${COGSERVER_LIBRARIES})
        target_compile_definitions(agentzero-planning PRIVATE HAVE_COGSERVER=1)
        message(STATUS "Linking cogserver libraries: ${COGSERVER_LIBRARIES}")
    endif()

    target_include_directories(agentzero-planning PUBLIC
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
        $<INSTALL_INTERFACE:include>
    )

    # Installation
    install(TARGETS agentzero-planning
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
endif()

# Tests (when implemented)
if(BUILD_TESTING)
    enable_testing()
#>>>>>>> main
    add_subdirectory(tests)
endif()

# Examples
add_subdirectory(examples)

# Status message
message(STATUS "Agent-Zero Planning module configuration complete")
message(STATUS "Ready for PlanningEngine implementation with temporal reasoning")

