# Agent-Zero Communication Examples CMakeLists.txt

cmake_minimum_required(VERSION 3.16)

# Example programs
set(COMMUNICATION_EXAMPLES
    basic_communication_example
    agent_messaging_demo
)

# Basic communication example
add_executable(basic_communication_example basic_communication_example.cpp)
target_link_libraries(basic_communication_example
    agentzero-communication
    ${COGUTIL_LIBRARIES}
    ${ATOMSPACE_LIBRARIES}
)
target_include_directories(basic_communication_example PRIVATE
# Agent-Zero Communication Module Examples

cmake_minimum_required(VERSION 3.16)

# Example source files
set(DIALOGUE_EXAMPLE_SOURCES
    dialogue_manager_example.cpp
)

# Build dialogue manager example
add_executable(dialogue_manager_example ${DIALOGUE_EXAMPLE_SOURCES})
target_link_libraries(dialogue_manager_example
# Examples for Agent-Zero Communication Module
# Part of AZ-HUMAN-001: Create HumanInterface layer

# Basic HumanInterface demonstration
add_executable(human_interface_demo
    HumanInterfaceDemo.cpp
)

target_link_libraries(human_interface_demo
    agentzero-communication
    ${COGUTIL_LIBRARIES}
    ${ATOMSPACE_LIBRARIES}
    ${Boost_LIBRARIES}
    pthread
)

target_include_directories(human_interface_demo PRIVATE
    ${CMAKE_SOURCE_DIR}/include

cmake_minimum_required(VERSION 3.16)

# Find required packages
find_package(PkgConfig REQUIRED)

# Find cogutil and atomspace
pkg_check_modules(COGUTIL cogutil)
pkg_check_modules(ATOMSPACE atomspace)
if (NOT ATOMSPACE_FOUND)
    # Find atomspace manually
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
        set(ATOMSPACE_INCLUDE_DIRS ${ATOMSPACE_INCLUDE_DIR})
    endif()
endif()

# Include directories
include_directories(
    ${CMAKE_CURRENT_SOURCE_DIR}/../include
    ${COGUTIL_INCLUDE_DIRS}
    ${ATOMSPACE_INCLUDE_DIRS}
)

# Agent messaging demo
add_executable(agent_messaging_demo agent_messaging_demo.cpp)
target_link_libraries(agent_messaging_demo
    agentzero-communication
    ${COGUTIL_LIBRARIES}
    ${ATOMSPACE_LIBRARIES}
)
target_include_directories(agent_messaging_demo PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}/../include
# Interactive conversation example
add_executable(conversation_example
    ConversationExample.cpp
)

target_link_libraries(conversation_example
    agentzero-communication
    ${COGUTIL_LIBRARIES}
    ${ATOMSPACE_LIBRARIES}
    ${Boost_LIBRARIES}
)

# Installation (optional)
install(TARGETS dialogue_manager_example
    RUNTIME DESTINATION bin/examples
)

message(STATUS "Communication module examples configured")
    pthread
)

target_include_directories(conversation_example PRIVATE
    ${CMAKE_SOURCE_DIR}/include
    ${COGUTIL_INCLUDE_DIRS}
    ${ATOMSPACE_INCLUDE_DIRS}
)

message(STATUS "Communication examples configured")
# Install examples
install(TARGETS human_interface_demo conversation_example
    DESTINATION ${CMAKE_INSTALL_BINDIR}/examples
)
# Link directories
link_directories(
    ${COGUTIL_LIBRARY_DIRS}
    ${ATOMSPACE_LIBRARY_DIRS}
)

# Example: Basic LanguageProcessor usage
add_executable(language_processor_example
    language_processor_example.cpp
)

target_link_libraries(language_processor_example
    agentzero-communication
    ${COGUTIL_LIBRARIES}
    ${ATOMSPACE_LIBRARIES}
)

# Add OpenCog libraries that might be needed
find_library(ATOMBASE_LIBRARY NAMES atombase PATHS /usr/local/lib/opencog)
find_library(ATOMCORE_LIBRARY NAMES atomcore PATHS /usr/local/lib/opencog)
find_library(VALUE_LIBRARY NAMES value PATHS /usr/local/lib/opencog)

# Link additional OpenCog libraries to both examples
if(ATOMBASE_LIBRARY)
    target_link_libraries(language_processor_example ${ATOMBASE_LIBRARY})
endif()
if(ATOMCORE_LIBRARY)
    target_link_libraries(language_processor_example ${ATOMCORE_LIBRARY})
endif()
if(VALUE_LIBRARY)
    target_link_libraries(language_processor_example ${VALUE_LIBRARY})
endif()

# Example: Batch processing
add_executable(batch_processing_example
    batch_processing_example.cpp
)

target_link_libraries(batch_processing_example
    agentzero-communication
    ${COGUTIL_LIBRARIES}
    ${ATOMSPACE_LIBRARIES}
)

# Link libraries to batch processing example too
if(ATOMBASE_LIBRARY)
    target_link_libraries(batch_processing_example ${ATOMBASE_LIBRARY})
endif()
if(ATOMCORE_LIBRARY)
    target_link_libraries(batch_processing_example ${ATOMCORE_LIBRARY})
endif()
if(VALUE_LIBRARY)
    target_link_libraries(batch_processing_example ${VALUE_LIBRARY})
endif()

# Example: Multi-Agent Coordination
add_executable(multi_agent_coordination_example
    multi_agent_coordination_example.cpp
)

target_link_libraries(multi_agent_coordination_example
    agentzero-communication
    ${COGUTIL_LIBRARIES}
    ${ATOMSPACE_LIBRARIES}
)

# Link libraries to multi-agent coordination example too
if(ATOMBASE_LIBRARY)
    target_link_libraries(multi_agent_coordination_example ${ATOMBASE_LIBRARY})
endif()
if(ATOMCORE_LIBRARY)
    target_link_libraries(multi_agent_coordination_example ${ATOMCORE_LIBRARY})
endif()
if(VALUE_LIBRARY)
    target_link_libraries(multi_agent_coordination_example ${VALUE_LIBRARY})
endif()
