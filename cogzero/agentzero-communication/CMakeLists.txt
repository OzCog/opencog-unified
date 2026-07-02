# Agent-Zero Communication Module CMakeLists.txt
# Part of the AGENT-ZERO-GENESIS project
# Includes AZ-COMM-001, AZ-NLP-001, AZ-NLP-002, AZ-HUMAN-001, AZ-MULTI-001

cmake_minimum_required(VERSION 3.16)

project(AgentZeroCommunication
    VERSION 0.1.0
    DESCRIPTION "Agent-Zero Communication & NLP Module for OpenCog Integration"
    LANGUAGES CXX
)

# Set C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

message(STATUS "Configuring Agent-Zero Communication Module...")

# Find required dependencies
find_package(PkgConfig REQUIRED)

# Core OpenCog dependencies (required)
pkg_check_modules(COGUTIL cogutil)
if (COGUTIL_FOUND)
    message(STATUS "Found cogutil version ${COGUTIL_VERSION}")
    include_directories(${COGUTIL_INCLUDE_DIRS})
    link_directories(${COGUTIL_LIBRARY_DIRS})
endif()

pkg_check_modules(ATOMSPACE atomspace)
if (ATOMSPACE_FOUND)
    message(STATUS "Found atomspace version ${ATOMSPACE_VERSION}")
    include_directories(${ATOMSPACE_INCLUDE_DIRS})
    link_directories(${ATOMSPACE_LIBRARY_DIRS})
else()
    message(STATUS "atomspace not found via pkg-config, looking for system installation")
    find_path(ATOMSPACE_INCLUDE_DIR
        NAMES opencog/atomspace/AtomSpace.h
        PATHS /usr/local/include /usr/include
    )
    find_library(ATOMSPACE_LIBRARY
        NAMES atomspace
        PATHS /usr/local/lib/opencog /usr/local/lib /usr/lib
    )
    if(ATOMSPACE_INCLUDE_DIR AND ATOMSPACE_LIBRARY)
        set(ATOMSPACE_FOUND TRUE)
        set(ATOMSPACE_LIBRARIES ${ATOMSPACE_LIBRARY})
        message(STATUS "Found atomspace at ${ATOMSPACE_INCLUDE_DIR} and ${ATOMSPACE_LIBRARY}")
        include_directories(${ATOMSPACE_INCLUDE_DIR})
    else()
        message(STATUS "atomspace not found via pkg-config - using monorepo build")
    endif()
endif()

# Optional OpenCog dependencies
pkg_check_modules(COGSERVER cogserver)
if (COGSERVER_FOUND)
    message(STATUS "Found cogserver version ${COGSERVER_VERSION}")
    include_directories(${COGSERVER_INCLUDE_DIRS})
    link_directories(${COGSERVER_LIBRARY_DIRS})
    add_definitions(-DHAVE_COGSERVER)
else()
    message(STATUS "CogServer not found - network communication features will be disabled")
endif()

pkg_check_modules(LG_ATOMESE lg-atomese)
if (LG_ATOMESE_FOUND)
    message(STATUS "Found lg-atomese version ${LG_ATOMESE_VERSION}")
    include_directories(${LG_ATOMESE_INCLUDE_DIRS})
    link_directories(${LG_ATOMESE_LIBRARY_DIRS})
    add_definitions(-DHAVE_LG_ATOMESE)
else()
    message(STATUS "lg-atomese not found - NLP features will be basic")
endif()

find_path(LINK_GRAMMAR_INCLUDE_DIR
    NAMES link-grammar/link-includes.h
    PATHS /usr/include /usr/local/include
)

find_library(LINK_GRAMMAR_LIBRARY
    NAMES link-grammar linkgrammar
    PATHS /usr/lib /usr/local/lib
)

if(LINK_GRAMMAR_INCLUDE_DIR AND LINK_GRAMMAR_LIBRARY)
    set(LINK_GRAMMAR_FOUND TRUE)
    message(STATUS "Found link-grammar at ${LINK_GRAMMAR_INCLUDE_DIR} and ${LINK_GRAMMAR_LIBRARY}")
    include_directories(${LINK_GRAMMAR_INCLUDE_DIR})
else()
    message(STATUS "link-grammar not found - some NLP features will be limited")
endif()

pkg_check_modules(OPENCOG opencog)
if (OPENCOG_FOUND)
    message(STATUS "Found opencog version ${OPENCOG_VERSION}")
    include_directories(${OPENCOG_INCLUDE_DIRS})
    link_directories(${OPENCOG_LIBRARY_DIRS})
else()
    message(STATUS "OpenCog main package not found - basic functionality available")
endif()

# Find Boost (required by OpenCog)
find_package(Boost REQUIRED COMPONENTS
    system
    filesystem
    thread
    date_time
)

if(Boost_FOUND)
    message(STATUS "Found Boost ${Boost_VERSION}: ${Boost_INCLUDE_DIRS}")
    include_directories(${Boost_INCLUDE_DIRS})
    link_directories(${Boost_LIBRARY_DIRS})
endif()

# Include directories
include_directories(
    ${CMAKE_CURRENT_SOURCE_DIR}/include
    ${CMAKE_CURRENT_SOURCE_DIR}/src
    ${CMAKE_CURRENT_SOURCE_DIR}/../agentzero-core/include
)

# Source files
set(AGENTZERO_COMMUNICATION_SOURCES
    src/AgentComms.cpp
    src/MessageRouter.cpp
    src/ProtocolManager.cpp
    src/MessageSerializer.cpp
    src/DialogueManager.cpp
    src/ConversationState.cpp
    src/LanguageProcessor.cpp
    src/MessageHandler.cpp
    src/HumanInterface.cpp
    src/CommunicationUtils.cpp
    src/MultiAgentCoordinator.cpp
)

# Header files
set(AGENTZERO_COMMUNICATION_HEADERS
    include/opencog/agentzero/communication/AgentComms.h
    include/opencog/agentzero/communication/MessageRouter.h
    include/opencog/agentzero/communication/ProtocolManager.h
    include/opencog/agentzero/communication/MessageSerializer.h
    include/opencog/agentzero/communication/CommTypes.h
    include/opencog/agentzero/communication/MultiAgentCoordinator.h
    include/opencog/agentzero/DialogueManager.h
    include/opencog/agentzero/ConversationState.h
    include/opencog/agentzero/LanguageProcessor.h
    include/opencog/agentzero/MessageHandler.h
)

# Create library
add_library(agentzero-communication SHARED
    ${AGENTZERO_COMMUNICATION_SOURCES}
    ${AGENTZERO_COMMUNICATION_HEADERS}
)

# Set library properties
set_target_properties(agentzero-communication PROPERTIES
    VERSION ${PROJECT_VERSION}
    SOVERSION 0
    POSITION_INDEPENDENT_CODE ON
)

target_include_directories(agentzero-communication PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
    $<INSTALL_INTERFACE:include>
)

# Link required libraries
target_link_libraries(agentzero-communication
    ${COGUTIL_LIBRARIES}
    ${ATOMSPACE_LIBRARIES}
    ${Boost_LIBRARIES}
    pthread
)

# Link optional libraries with proper feature flags
if(COGSERVER_FOUND AND COGSERVER_LIBRARIES)
    target_link_libraries(agentzero-communication ${COGSERVER_LIBRARIES})
    target_compile_definitions(agentzero-communication PRIVATE HAVE_COGSERVER=1)
    message(STATUS "Linking cogserver libraries: ${COGSERVER_LIBRARIES}")
endif()

# Find additional required libraries
find_library(ATOMBASE_LIBRARY
    NAMES atombase
    PATHS /usr/local/lib/opencog /usr/local/lib /usr/lib
)

find_library(ATOMCORE_LIBRARY
    NAMES atomcore
    PATHS /usr/local/lib/opencog /usr/local/lib /usr/lib
)

find_library(VALUE_LIBRARY
    NAMES value
    PATHS /usr/local/lib/opencog /usr/local/lib /usr/lib
)

if(ATOMBASE_LIBRARY)
    target_link_libraries(agentzero-communication ${ATOMBASE_LIBRARY})
    message(STATUS "Linking atombase library: ${ATOMBASE_LIBRARY}")
endif()

if(ATOMCORE_LIBRARY)
    target_link_libraries(agentzero-communication ${ATOMCORE_LIBRARY})
    message(STATUS "Linking atomcore library: ${ATOMCORE_LIBRARY}")
endif()

if(VALUE_LIBRARY)
    target_link_libraries(agentzero-communication ${VALUE_LIBRARY})
    message(STATUS "Linking value library: ${VALUE_LIBRARY}")
endif()

# Link lg-atomese libraries if available
if(LG_ATOMESE_FOUND AND LG_ATOMESE_LIBRARIES)
    target_link_libraries(agentzero-communication ${LG_ATOMESE_LIBRARIES})
    target_compile_definitions(agentzero-communication PRIVATE HAVE_LG_ATOMESE=1)
    message(STATUS "Linking lg-atomese libraries: ${LG_ATOMESE_LIBRARIES}")
endif()

# Link link-grammar libraries if available
if(LINK_GRAMMAR_FOUND AND LINK_GRAMMAR_LIBRARY)
    target_link_libraries(agentzero-communication ${LINK_GRAMMAR_LIBRARY})
    target_compile_definitions(agentzero-communication PRIVATE HAVE_LINK_GRAMMAR=1)
    message(STATUS "Linking link-grammar library: ${LINK_GRAMMAR_LIBRARY}")
endif()

# Link opencog libraries if available
if(OPENCOG_FOUND AND OPENCOG_LIBRARIES)
    target_link_libraries(agentzero-communication ${OPENCOG_LIBRARIES})
    target_compile_definitions(agentzero-communication PRIVATE HAVE_OPENCOG=1)
    message(STATUS "Linking opencog libraries: ${OPENCOG_LIBRARIES}")
endif()

# Compiler flags
target_compile_definitions(agentzero-communication PRIVATE
    AGENTZERO_COMMUNICATION_VERSION="${PROJECT_VERSION}"
)

# Installation
include(GNUInstallDirs)

install(TARGETS agentzero-communication
    EXPORT AgentZeroCommunicationTargets
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
    INCLUDES DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}
)

# Install all headers
install(DIRECTORY include/
    DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}
    FILES_MATCHING PATTERN "*.h"
)

# Install export targets
install(EXPORT AgentZeroCommunicationTargets
    FILE AgentZeroCommunicationTargets.cmake
    NAMESPACE AgentZero::
    DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/AgentZeroCommunication
)

# Generate pkgconfig file
configure_file(
    ${CMAKE_CURRENT_SOURCE_DIR}/agentzero-communication.pc.in
    ${CMAKE_CURRENT_BINARY_DIR}/agentzero-communication.pc
    @ONLY
)

install(FILES ${CMAKE_CURRENT_BINARY_DIR}/agentzero-communication.pc
    DESTINATION lib/pkgconfig
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
message(STATUS "Agent-Zero Communication module configuration complete")
message(STATUS "Available features:")
message(STATUS "  - CogServer integration: ${COGSERVER_FOUND}")
message(STATUS "  - lg-atomese integration: ${LG_ATOMESE_FOUND}")
message(STATUS "  - Link Grammar parsing: ${LINK_GRAMMAR_FOUND}")
message(STATUS "  - OpenCog NLP integration: ${OPENCOG_FOUND}")
message(STATUS "Dependencies found: cogutil=${COGUTIL_FOUND}, atomspace=${ATOMSPACE_FOUND}")
