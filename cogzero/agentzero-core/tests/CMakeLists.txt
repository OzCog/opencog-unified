# Tests CMakeLists.txt for Agent-Zero Core
cmake_minimum_required(VERSION 3.16)

# Find CxxTest if available
find_package(CxxTest)

# Also try to find GTest for new tests
find_package(GTest QUIET)
find_package(Threads REQUIRED)

# Find OpenCog packages for tests
pkg_check_modules(COGUTIL cogutil)
pkg_check_modules(ATOMSPACE atomspace)

if(CXXTEST_FOUND)
    include_directories(${CXXTEST_INCLUDE_DIR})
    enable_testing()
    
    # Include the source directory for testing
    include_directories(${CMAKE_CURRENT_SOURCE_DIR}/../include)
    include_directories(${CMAKE_CURRENT_SOURCE_DIR}/../src)
    
    # AgentZeroCore unit tests
    if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/AgentZeroCoreUTest.cxxtest")
        cxxtest_add_test(AgentZeroCoreUTest AgentZeroCoreUTest.cpp 
                        "${CMAKE_CURRENT_SOURCE_DIR}/AgentZeroCoreUTest.cxxtest")
        
        target_link_libraries(AgentZeroCoreUTest
            agentzero-core
            ${COGUTIL_LIBRARIES}
            ${ATOMSPACE_LIBRARIES}
            ${COGSERVER_LIBRARIES}
            ${Boost_LIBRARIES}
        )
    endif()
    
    # ActionScheduler unit tests
    if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/ActionSchedulerTest.cpp")
        add_executable(ActionSchedulerTest ActionSchedulerTest.cpp)
        
        target_link_libraries(ActionSchedulerTest
            agentzero-core
            ${COGUTIL_LIBRARIES}
            ${ATOMSPACE_LIBRARIES}
            ${COGSERVER_LIBRARIES}
            ${Boost_LIBRARIES}
        )
        
        add_test(NAME ActionSchedulerTest COMMAND ActionSchedulerTest)
    endif()
    
    message(STATUS "Agent-Zero Core tests configured with CxxTest")
else()
    message(STATUS "CxxTest not found - CxxTest tests will not be built")
endif()

# GTest-based tests for action execution framework
if(GTEST_FOUND)
    enable_testing()
    
    # Include directories
    include_directories(
        ${CMAKE_CURRENT_SOURCE_DIR}/../include
        ${COGUTIL_INCLUDE_DIRS}
        ${ATOMSPACE_INCLUDE_DIRS}
        ${GTEST_INCLUDE_DIRS}
    )

    # Link directories  
    link_directories(
        ${COGUTIL_LIBRARY_DIRS}
        ${ATOMSPACE_LIBRARY_DIRS}
    )

    # Test source files for action framework
    set(ACTION_TEST_SOURCES
        test_action_executor.cpp
        test_action_scheduler.cpp
    )
    
    # ReasoningEngine tests
    if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/ReasoningEngineTest.cpp")
        add_executable(ReasoningEngineTest ReasoningEngineTest.cpp)
        
        target_link_libraries(ReasoningEngineTest
            agentzero-core
            ${COGUTIL_LIBRARIES}
            ${ATOMSPACE_LIBRARIES}
            ${PLN_LIBRARIES}
            ${URE_LIBRARIES}
            ${GTEST_LIBRARIES}
            ${GTEST_MAIN_LIBRARIES}
            Threads::Threads
        )
        
        target_compile_features(ReasoningEngineTest PRIVATE cxx_std_17)
        
        # Add the test to CTest
        add_test(NAME ReasoningEngineTest COMMAND ReasoningEngineTest)
        
        set_tests_properties(ReasoningEngineTest
            PROPERTIES
            TIMEOUT 120
            LABELS "reasoning;pln;ure"
        )
        
        message(STATUS "ReasoningEngine tests configured")
    endif()
    
    # SelfModification tests
    if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/SelfModificationTest.cpp")
        add_executable(SelfModificationTest SelfModificationTest.cpp)
        
        target_link_libraries(SelfModificationTest
            agentzero-core
            ${COGUTIL_LIBRARIES}
            ${ATOMSPACE_LIBRARIES}
            Threads::Threads
        )
        
        target_compile_features(SelfModificationTest PRIVATE cxx_std_17)
        
        # Add the test to CTest
        add_test(NAME SelfModificationTest COMMAND SelfModificationTest)
        
        set_tests_properties(SelfModificationTest
            PROPERTIES
            TIMEOUT 60
            LABELS "meta;selfmodification"
        )
        
        message(STATUS "SelfModification tests configured")
    endif()

    # Create test executable for action framework
    add_executable(test_agentzero_action_framework
        ${ACTION_TEST_SOURCES}
    )

    # Link libraries
    target_link_libraries(test_agentzero_action_framework
        agentzero-core
        ${COGUTIL_LIBRARIES}
        ${ATOMSPACE_LIBRARIES}
        ${GTEST_LIBRARIES}
        ${GTEST_MAIN_LIBRARIES}
        Threads::Threads
    )

    # Add compiler flags
    target_compile_features(test_agentzero_action_framework PRIVATE cxx_std_17)

    # Add tests
    add_test(
        NAME ActionExecutorTests
        COMMAND test_agentzero_action_framework --gtest_filter="ActionExecutorTest.*"
    )

    add_test(
        NAME ActionSchedulerTests  
        COMMAND test_agentzero_action_framework --gtest_filter="ActionSchedulerTest.*"
    )

    add_test(
        NAME AllActionFrameworkTests
        COMMAND test_agentzero_action_framework
    )

    # Set test properties
    set_tests_properties(ActionExecutorTests ActionSchedulerTests AllActionFrameworkTests
        PROPERTIES
        TIMEOUT 60
        LABELS "action_framework"
    )
    
    message(STATUS "Action execution framework tests configured with GTest")
else()
    message(STATUS "GTest not found - GTest tests will not be built")
    message(STATUS "Install GTest to enable action framework unit testing")
endif()

if(NOT CXXTEST_FOUND AND NOT GTEST_FOUND)
    message(STATUS "Neither CxxTest nor GTest found - no tests will be built")
    message(STATUS "Install CxxTest or GTest to enable unit testing")
endif()