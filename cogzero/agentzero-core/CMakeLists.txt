# Agent-Zero Core Module CMakeLists.txt

cmake_minimum_required(VERSION 3.16)

project(AgentZeroCore
    VERSION 0.1.0
    DESCRIPTION "Agent-Zero Core Orchestration Engine for OpenCog Integration"
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
else()
    message(STATUS "CogUtil not found via pkg-config - using monorepo build")
endif()

# Find atomspace  
pkg_check_modules(ATOMSPACE atomspace)
if (ATOMSPACE_FOUND)
    message(STATUS "Found atomspace version ${ATOMSPACE_VERSION}")
    include_directories(${ATOMSPACE_INCLUDE_DIRS})
    link_directories(${ATOMSPACE_LIBRARY_DIRS})
else()
    message(STATUS "AtomSpace not found via pkg-config - using monorepo build")
endif()

# Find cogserver (optional)
pkg_check_modules(COGSERVER cogserver)
if (COGSERVER_FOUND)
    message(STATUS "Found cogserver version ${COGSERVER_VERSION}")
    include_directories(${COGSERVER_INCLUDE_DIRS})
    link_directories(${COGSERVER_LIBRARY_DIRS})
else()
    message(STATUS "CogServer not found - some features will be disabled")
    set(COGSERVER_FOUND FALSE)
endif()

# Find attention module
pkg_check_modules(ATTENTION attention)
if (ATTENTION_FOUND)
    message(STATUS "Found attention version ${ATTENTION_VERSION}")
    include_directories(${ATTENTION_INCLUDE_DIRS})
    link_directories(${ATTENTION_LIBRARY_DIRS})
else()
    message(STATUS "Attention module not found via pkg-config, looking for system includes")
    # Look for attention headers in system paths
    find_path(ATTENTION_INCLUDE_PATH
        NAMES opencog/attentionbank/bank/AttentionBank.h
        PATHS /usr/local/include /usr/include
        PATH_SUFFIXES opencog
    )
    if(ATTENTION_INCLUDE_PATH)
        message(STATUS "Found attention headers at ${ATTENTION_INCLUDE_PATH}")
        include_directories(${ATTENTION_INCLUDE_PATH})
        set(ATTENTION_FOUND TRUE)
    endif()
endif()

# Find PLN (Probabilistic Logic Networks) module
pkg_check_modules(PLN pln)
if (PLN_FOUND)
    message(STATUS "Found PLN version ${PLN_VERSION}")
    include_directories(${PLN_INCLUDE_DIRS})
    link_directories(${PLN_LIBRARY_DIRS})
else()
    message(STATUS "PLN module not found via pkg-config, looking for system includes")
    find_path(PLN_INCLUDE_PATH
        NAMES opencog/pln/PLN.h
        PATHS /usr/local/include /usr/include
        PATH_SUFFIXES opencog
    )
    if(PLN_INCLUDE_PATH)
        message(STATUS "Found PLN headers at ${PLN_INCLUDE_PATH}")
        include_directories(${PLN_INCLUDE_PATH})
        set(PLN_FOUND TRUE)
    endif()
endif()

# Find URE (Unified Rule Engine) module
pkg_check_modules(URE ure)
if (URE_FOUND)
    message(STATUS "Found URE version ${URE_VERSION}")
    include_directories(${URE_INCLUDE_DIRS})
    link_directories(${URE_LIBRARY_DIRS})
else()
    message(STATUS "URE module not found via pkg-config, looking for system includes")
    find_path(URE_INCLUDE_PATH
        NAMES opencog/ure/Rule.h
        PATHS /usr/local/include /usr/include
        PATH_SUFFIXES opencog
    )
    if(URE_INCLUDE_PATH)
        message(STATUS "Found URE headers at ${URE_INCLUDE_PATH}")
        include_directories(${URE_INCLUDE_PATH})
        set(URE_FOUND TRUE)
    endif()
endif()

# Find Miner module for pattern discovery
pkg_check_modules(MINER miner)
if (MINER_FOUND)
    message(STATUS "Found miner version ${MINER_VERSION}")
    include_directories(${MINER_INCLUDE_DIRS})
    link_directories(${MINER_LIBRARY_DIRS})
else()
    message(STATUS "Miner module not found - pattern discovery features may be limited")
    set(MINER_FOUND FALSE)
endif()

# Include directories
include_directories(
    ${CMAKE_CURRENT_SOURCE_DIR}/include
    ${CMAKE_CURRENT_SOURCE_DIR}/src
)

# Source files
set(AGENTZERO_CORE_SOURCES
    src/AgentZeroCore.cpp
    src/CognitiveLoop.cpp  
    src/TaskManager.cpp
    src/KnowledgeIntegrator.cpp
    src/ReasoningEngine.cpp
    src/ActionExecutor.cpp
    src/ActionScheduler.cpp
    src/MetaPlanner.cpp
    src/SelfModification.cpp
)

# Header files
set(AGENTZERO_CORE_HEADERS
    include/opencog/agentzero/AgentZeroCore.h
    include/opencog/agentzero/CognitiveLoop.h
    include/opencog/agentzero/TaskManager.h
    include/opencog/agentzero/KnowledgeIntegrator.h
    include/opencog/agentzero/ReasoningEngine.h
    include/opencog/agentzero/ActionExecutor.h
    include/opencog/agentzero/ActionScheduler.h
    include/opencog/agentzero/MetaPlanner.h
    include/opencog/agentzero/SelfModification.h
)

# Create library (when source files exist)
if(AGENTZERO_CORE_SOURCES)
    add_library(agentzero-core SHARED
        ${AGENTZERO_CORE_SOURCES}
        ${AGENTZERO_CORE_HEADERS}
    )

    target_link_libraries(agentzero-core
        ${COGUTIL_LIBRARIES}
        ${ATOMSPACE_LIBRARIES}
        ${Boost_LIBRARIES}
    )
    
    # Link cogserver libraries if available
    if(COGSERVER_FOUND AND COGSERVER_LIBRARIES)
        target_link_libraries(agentzero-core ${COGSERVER_LIBRARIES})
        target_compile_definitions(agentzero-core PRIVATE HAVE_COGSERVER=1)
        message(STATUS "Linking cogserver libraries: ${COGSERVER_LIBRARIES}")
    endif()
    
    # Link attention libraries if available
    if(ATTENTION_FOUND AND ATTENTION_LIBRARIES)
        target_link_libraries(agentzero-core ${ATTENTION_LIBRARIES})
        target_compile_definitions(agentzero-core PRIVATE HAVE_ATTENTION_BANK=1)
        message(STATUS "Linking attention libraries: ${ATTENTION_LIBRARIES}")
    elseif(ATTENTION_FOUND)
        target_compile_definitions(agentzero-core PRIVATE HAVE_ATTENTION_BANK=1) 
        message(STATUS "Attention headers found, compiling with attention support")
    endif()
    
    # Link PLN libraries if available
    if(PLN_FOUND AND PLN_LIBRARIES)
        target_link_libraries(agentzero-core ${PLN_LIBRARIES})
        target_compile_definitions(agentzero-core PRIVATE HAVE_PLN=1)
        message(STATUS "Linking PLN libraries: ${PLN_LIBRARIES}")
    elseif(PLN_FOUND)
        target_compile_definitions(agentzero-core PRIVATE HAVE_PLN=1)
        message(STATUS "PLN headers found, compiling with PLN support")
    endif()
    
    # Link URE libraries if available
    if(URE_FOUND AND URE_LIBRARIES)
        target_link_libraries(agentzero-core ${URE_LIBRARIES})
        target_compile_definitions(agentzero-core PRIVATE HAVE_URE=1)
        message(STATUS "Linking URE libraries: ${URE_LIBRARIES}")
    elseif(URE_FOUND)
        target_compile_definitions(agentzero-core PRIVATE HAVE_URE=1)
        message(STATUS "URE headers found, compiling with URE support")
    endif()
    
    # Link Miner libraries if available
    if(MINER_FOUND AND MINER_LIBRARIES)
        target_link_libraries(agentzero-core ${MINER_LIBRARIES})
        target_compile_definitions(agentzero-core PRIVATE HAVE_MINER=1)
        message(STATUS "Linking miner libraries: ${MINER_LIBRARIES}")
    endif()

    target_include_directories(agentzero-core PUBLIC
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
        $<INSTALL_INTERFACE:include>
    )

    # Installation
    install(TARGETS agentzero-core
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
    add_subdirectory(tests)
endif()

# Status message
message(STATUS "Agent-Zero Core module configuration complete")
message(STATUS "Source files implemented - ready for build and testing")