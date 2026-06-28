# Performance Tests CMakeLists.txt
# AZ-TEST-001: Performance benchmarking and stress testing
# AZ-INT-002: Comprehensive benchmarking suite

cmake_minimum_required(VERSION 3.16)
project(AgentZeroBenchmark)

# Find required packages
find_package(PkgConfig REQUIRED)
pkg_check_modules(COGUTIL cogutil)
pkg_check_modules(ATOMSPACE atomspace)

# Build Agent-Zero Benchmarking Library
add_library(agentzero-benchmark SHARED
    AgentZeroBenchmark.cpp
)

target_link_libraries(agentzero-benchmark
    ${COGUTIL_LIBRARIES}
    ${ATOMSPACE_LIBRARIES}
    atombase
    atomcore
)

target_include_directories(agentzero-benchmark PUBLIC
    ${CMAKE_CURRENT_SOURCE_DIR}
    ${COGUTIL_INCLUDE_DIRS}
    ${ATOMSPACE_INCLUDE_DIRS}
)

target_link_directories(agentzero-benchmark PUBLIC
    ${COGUTIL_LIBRARY_DIRS}
    ${ATOMSPACE_LIBRARY_DIRS}
    /usr/local/lib/opencog
)

# Install benchmarking library
install(TARGETS agentzero-benchmark
    LIBRARY DESTINATION lib/opencog
    ARCHIVE DESTINATION lib/opencog
)

install(FILES
    AgentZeroBenchmark.h
    DESTINATION include/opencog/agentzero/benchmark
)

# Build benchmark executable
add_executable(agentzero-component-benchmarks
    AgentZeroComponentBenchmarks.cpp
)

target_link_libraries(agentzero-component-benchmarks
    agentzero-benchmark
    ${COGUTIL_LIBRARIES}
    ${ATOMSPACE_LIBRARIES}
    atom_types
    atombase
    atomcore
)

target_link_directories(agentzero-component-benchmarks PUBLIC
    ${COGUTIL_LIBRARY_DIRS}
    ${ATOMSPACE_LIBRARY_DIRS}
    /usr/local/lib/opencog
)

# Install benchmark executable
install(TARGETS agentzero-component-benchmarks
    RUNTIME DESTINATION bin
)

# Add custom target for running benchmarks
add_custom_target(run-benchmarks
    COMMAND agentzero-component-benchmarks
    DEPENDS agentzero-component-benchmarks
    WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
    COMMENT "Running Agent-Zero benchmarking suite"
)

if(CXXTEST_FOUND)
    # Performance Benchmark Tests
    if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/PerformanceBenchmarkTest.cxxtest")
        cxxtest_add_test(PerformanceBenchmarkTest PerformanceBenchmarkTest.cpp 
                        "${CMAKE_CURRENT_SOURCE_DIR}/PerformanceBenchmarkTest.cxxtest")
        
        target_link_libraries(PerformanceBenchmarkTest
            agentzero-test-framework
            agentzero-core
            ${COGUTIL_LIBRARIES}
            ${ATOMSPACE_LIBRARIES}
            ${COGSERVER_LIBRARIES}
        )
    endif()
    
    # Memory Usage Tests
    if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/MemoryUsageTest.cxxtest")
        cxxtest_add_test(MemoryUsageTest MemoryUsageTest.cpp 
                        "${CMAKE_CURRENT_SOURCE_DIR}/MemoryUsageTest.cxxtest")
        
        target_link_libraries(MemoryUsageTest
            agentzero-test-framework
            agentzero-core
            ${COGUTIL_LIBRARIES}
            ${ATOMSPACE_LIBRARIES}
            ${COGSERVER_LIBRARIES}
        )
    endif()
    
    message(STATUS "Agent-Zero performance tests configured")
endif()

message(STATUS "Agent-Zero benchmarking suite configured (AZ-INT-002)")