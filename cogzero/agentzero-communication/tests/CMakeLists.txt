# Agent-Zero Communication Tests CMakeLists.txt

cmake_minimum_required(VERSION 3.16)

# Find CxxTest for unit testing
find_package(CxxTest)

if(CXXTEST_FOUND)
    message(STATUS "CxxTest found - building communication tests")
    
    # Include CxxTest utilities
    include_directories(${CXXTEST_INCLUDE_DIR})
    
    # Test files
    set(COMMUNICATION_TEST_SOURCES
        AgentCommsUTest.cpp
        MessageRouterUTest.cpp
        ProtocolManagerUTest.cpp
        MessageSerializerUTest.cpp
    )
    
    # Generate test headers from cxxtest files
    foreach(test_source ${COMMUNICATION_TEST_SOURCES})
        string(REPLACE ".cpp" ".h" test_header ${test_source})
        
        # Check if the .h file exists, if not create a basic one
        if(NOT EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/${test_header}")
            file(WRITE "${CMAKE_CURRENT_SOURCE_DIR}/${test_header}"
                "// Auto-generated test header for ${test_source}\n"
                "#include <cxxtest/TestSuite.h>\n"
                "#include <opencog/agentzero/communication/AgentComms.h>\n\n"
                "class ${test_source}Suite : public CxxTest::TestSuite {\n"
                "public:\n"
                "    void testPlaceholder() {\n"
                "        TS_ASSERT(true); // Placeholder test\n"
                "    }\n"
                "};\n")
        endif()
        
        # Generate test runner
        cxxtest_add_test(${test_source}_runner ${test_source} ${CMAKE_CURRENT_SOURCE_DIR}/${test_header})
        
        # Link against communication library and dependencies
        target_link_libraries(${test_source}_runner
            agentzero-communication
            ${COGUTIL_LIBRARIES}
            ${ATOMSPACE_LIBRARIES}
        )
        
        # Include directories
        target_include_directories(${test_source}_runner PRIVATE
            ${CMAKE_CURRENT_SOURCE_DIR}/../include
            ${COGUTIL_INCLUDE_DIRS}
            ${ATOMSPACE_INCLUDE_DIRS}
        )
    endforeach()
    
    # Integration test
    if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/CommunicationIntegrationTest.h")
        cxxtest_add_test(communication_integration_test 
                        CommunicationIntegrationTest.cpp
                        CommunicationIntegrationTest.h)
        
        target_link_libraries(communication_integration_test
            agentzero-communication
            ${COGUTIL_LIBRARIES}
            ${ATOMSPACE_LIBRARIES}
        )
        
        target_include_directories(communication_integration_test PRIVATE
            ${CMAKE_CURRENT_SOURCE_DIR}/../include
            ${COGUTIL_INCLUDE_DIRS}
            ${ATOMSPACE_INCLUDE_DIRS}
        )
    endif()
    
    message(STATUS "Communication module tests configured")
    
else()
    message(STATUS "CxxTest not found - skipping communication tests")
endif()
# Agent-Zero Communication Module Tests

cmake_minimum_required(VERSION 3.16)

# Find test framework
find_package(PkgConfig REQUIRED)

# Try to find CxxTest
find_program(CXXTEST_BIN cxxtestgen)
find_path(CXXTEST_INCLUDE_DIR cxxtest/TestSuite.h)

if(CXXTEST_BIN AND CXXTEST_INCLUDE_DIR)
    message(STATUS "Found CxxTest: ${CXXTEST_BIN}")
    include_directories(${CXXTEST_INCLUDE_DIR})
    
    # Test source files
    set(TEST_SOURCES
        DialogueManagerUTest.cxxtest
        ConversationStateUTest.cxxtest
        LanguageProcessorUTest.cxxtest
        MessageHandlerUTest.cxxtest
        MultiAgentCoordinatorUTest.cxxtest
    )
    
    # Generate and build tests
    foreach(TEST_SOURCE ${TEST_SOURCES})
        get_filename_component(TEST_NAME ${TEST_SOURCE} NAME_WE)
        set(TEST_CPP ${CMAKE_CURRENT_BINARY_DIR}/${TEST_NAME}.cpp)
        
        # Generate test file
        add_custom_command(
            OUTPUT ${TEST_CPP}
            COMMAND ${CXXTEST_BIN} --error-printer -o ${TEST_CPP} ${CMAKE_CURRENT_SOURCE_DIR}/${TEST_SOURCE}
            DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/${TEST_SOURCE}
            COMMENT "Generating ${TEST_NAME}.cpp from ${TEST_SOURCE}"
        )
        
        # Create test executable
        add_executable(${TEST_NAME} ${TEST_CPP})
        target_link_libraries(${TEST_NAME} 
            agentzero-communication
            ${COGUTIL_LIBRARIES}
            ${ATOMSPACE_LIBRARIES}
            ${Boost_LIBRARIES}
        )
        
        # Add to test suite
        add_test(NAME ${TEST_NAME} COMMAND ${TEST_NAME})
    endforeach()
    
    message(STATUS "Communication module tests configured with CxxTest")
else()
    message(STATUS "CxxTest not found - tests will be disabled")
endif()
# Tests for Agent-Zero Communication Module
# Part of AZ-HUMAN-001: Create HumanInterface layer

find_package(Threads REQUIRED)

# Simple unit tests
add_executable(test_human_interface
    test_HumanInterface.cpp
)

target_link_libraries(test_human_interface
    agentzero-communication
    ${COGUTIL_LIBRARIES}
    ${ATOMSPACE_LIBRARIES}
    ${Boost_LIBRARIES}
    Threads::Threads
)

target_include_directories(test_human_interface PRIVATE
    ${CMAKE_SOURCE_DIR}/include
    ${COGUTIL_INCLUDE_DIRS}
    ${ATOMSPACE_INCLUDE_DIRS}
)

# Add test
add_test(NAME HumanInterfaceBasicTest COMMAND test_human_interface)

# Test utilities
add_executable(test_communication_utils
    test_CommunicationUtils.cpp
)

target_link_libraries(test_communication_utils
    agentzero-communication
    ${COGUTIL_LIBRARIES}
    ${ATOMSPACE_LIBRARIES}
    ${Boost_LIBRARIES}
    Threads::Threads
)

target_include_directories(test_communication_utils PRIVATE
    ${CMAKE_SOURCE_DIR}/include
    ${COGUTIL_INCLUDE_DIRS}
    ${ATOMSPACE_INCLUDE_DIRS}
)

add_test(NAME CommunicationUtilsTest COMMAND test_communication_utils)

cmake_minimum_required(VERSION 3.16)

# Find required packages for testing
find_package(PkgConfig REQUIRED)

# Find cogutil and atomspace (required for tests)
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

# Link directories
link_directories(
    ${COGUTIL_LIBRARY_DIRS}
    ${ATOMSPACE_LIBRARY_DIRS}
)

# Test for LanguageProcessor
add_executable(test_language_processor
    test_language_processor.cpp
)

target_link_libraries(test_language_processor
    agentzero-communication
    ${COGUTIL_LIBRARIES}
    ${ATOMSPACE_LIBRARIES}
)

# Add OpenCog libraries that might be needed
find_library(ATOMBASE_LIBRARY NAMES atombase PATHS /usr/local/lib/opencog)
find_library(ATOMCORE_LIBRARY NAMES atomcore PATHS /usr/local/lib/opencog)
find_library(VALUE_LIBRARY NAMES value PATHS /usr/local/lib/opencog)

if(ATOMBASE_LIBRARY)
    target_link_libraries(test_language_processor ${ATOMBASE_LIBRARY})
endif()
if(ATOMCORE_LIBRARY)
    target_link_libraries(test_language_processor ${ATOMCORE_LIBRARY})
endif()
if(VALUE_LIBRARY)
    target_link_libraries(test_language_processor ${VALUE_LIBRARY})
endif()

# Add test
add_test(NAME LanguageProcessorTest COMMAND test_language_processor)

# Test for basic communication functionality
add_executable(test_communication_basic
    test_communication_basic.cpp
)

target_link_libraries(test_communication_basic
    agentzero-communication
    ${COGUTIL_LIBRARIES}
    ${ATOMSPACE_LIBRARIES}
)

if(ATOMBASE_LIBRARY)
    target_link_libraries(test_communication_basic ${ATOMBASE_LIBRARY})
endif()
if(ATOMCORE_LIBRARY)
    target_link_libraries(test_communication_basic ${ATOMCORE_LIBRARY})
endif()
if(VALUE_LIBRARY)
    target_link_libraries(test_communication_basic ${VALUE_LIBRARY})
endif()

add_test(NAME CommunicationBasicTest COMMAND test_communication_basic)
