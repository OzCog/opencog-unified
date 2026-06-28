# Agent-Zero Profiling Infrastructure CMakeLists.txt
# AZ-PERF-001: Performance optimization and profiling
# Provides comprehensive profiling tools integration

cmake_minimum_required(VERSION 3.16)
project(AgentZeroProfiler)

# Find required packages
find_package(PkgConfig REQUIRED)
pkg_check_modules(COGUTIL cogutil)
pkg_check_modules(ATOMSPACE atomspace)

# Check for profiling tools
find_program(GPROF_PATH gprof)
find_program(PERF_PATH perf)
find_program(VALGRIND_PATH valgrind)

if(GPROF_PATH)
    message(STATUS "gprof found: ${GPROF_PATH}")
else()
    message(STATUS "gprof not found - install with: sudo apt-get install binutils")
endif()

if(PERF_PATH)
    message(STATUS "perf found: ${PERF_PATH}")
else()
    message(STATUS "perf not found - install with: sudo apt-get install linux-tools-common")
endif()

if(VALGRIND_PATH)
    message(STATUS "valgrind found: ${VALGRIND_PATH}")
else()
    message(STATUS "valgrind not found - install with: sudo apt-get install valgrind")
endif()

# Build Agent-Zero Profiling Library
add_library(agentzero-profiler SHARED
    AgentZeroProfiler.cpp
)

target_link_libraries(agentzero-profiler
    ${COGUTIL_LIBRARIES}
    ${ATOMSPACE_LIBRARIES}
    atombase
    atomcore
)

target_include_directories(agentzero-profiler PUBLIC
    ${CMAKE_CURRENT_SOURCE_DIR}
    ${COGUTIL_INCLUDE_DIRS}
    ${ATOMSPACE_INCLUDE_DIRS}
)

target_link_directories(agentzero-profiler PUBLIC
    ${COGUTIL_LIBRARY_DIRS}
    ${ATOMSPACE_LIBRARY_DIRS}
    /usr/local/lib/opencog
)

# Install profiling library
install(TARGETS agentzero-profiler
    LIBRARY DESTINATION lib/opencog
    ARCHIVE DESTINATION lib/opencog
)

install(FILES
    AgentZeroProfiler.h
    DESTINATION include/opencog/agentzero/profiling
)

# Build profiling example application
add_executable(profiling-demo
    profiling_demo.cpp
)

target_link_libraries(profiling-demo
    agentzero-profiler
    ${COGUTIL_LIBRARIES}
    ${ATOMSPACE_LIBRARIES}
    atombase
    atomcore
)

target_link_directories(profiling-demo PUBLIC
    ${COGUTIL_LIBRARY_DIRS}
    ${ATOMSPACE_LIBRARY_DIRS}
    /usr/local/lib/opencog
)

# Install profiling demo
install(TARGETS profiling-demo
    RUNTIME DESTINATION bin
)

# Add profiling build configuration support
# Profile build type with gprof support
set(CMAKE_CXX_FLAGS_PROFILE "-O2 -g -pg" CACHE STRING
    "Flags used by the C++ compiler during profile builds." FORCE)
set(CMAKE_C_FLAGS_PROFILE "-O2 -g -pg" CACHE STRING
    "Flags used by the C compiler during profile builds." FORCE)
set(CMAKE_EXE_LINKER_FLAGS_PROFILE "-pg" CACHE STRING
    "Flags used for linking binaries during profile builds." FORCE)
set(CMAKE_SHARED_LINKER_FLAGS_PROFILE "-pg" CACHE STRING
    "Flags used by the shared libraries linker during profile builds." FORCE)
mark_as_advanced(
    CMAKE_CXX_FLAGS_PROFILE
    CMAKE_C_FLAGS_PROFILE
    CMAKE_EXE_LINKER_FLAGS_PROFILE
    CMAKE_SHARED_LINKER_FLAGS_PROFILE
)

# Add custom profiling targets

# Target: profile-with-gprof
# Builds with gprof instrumentation and runs the demo
if(GPROF_PATH)
    add_custom_target(profile-with-gprof
        COMMAND ${CMAKE_COMMAND} -E echo "Building with gprof instrumentation..."
        COMMAND ${CMAKE_COMMAND} -E echo "Run your application, then analyze with: gprof <binary> gmon.out > analysis.txt"
        COMMENT "Preparing gprof profiling setup"
    )
    
    add_custom_target(analyze-gprof
        COMMAND ${GPROF_PATH} profiling-demo gmon.out > ${CMAKE_CURRENT_BINARY_DIR}/gprof_report.txt
        COMMAND ${CMAKE_COMMAND} -E echo "gprof analysis saved to: ${CMAKE_CURRENT_BINARY_DIR}/gprof_report.txt"
        WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
        COMMENT "Analyzing gprof profiling data"
    )
endif()

# Target: profile-with-perf
# Uses Linux perf tool for CPU profiling
if(PERF_PATH)
    add_custom_target(profile-with-perf
        COMMAND ${CMAKE_COMMAND} -E echo "Recording performance data with perf..."
        COMMAND sudo ${PERF_PATH} record -F 99 -g ./profiling-demo
        COMMAND sudo ${PERF_PATH} report > ${CMAKE_CURRENT_BINARY_DIR}/perf_report.txt
        COMMAND ${CMAKE_COMMAND} -E echo "perf analysis saved to: ${CMAKE_CURRENT_BINARY_DIR}/perf_report.txt"
        DEPENDS profiling-demo
        WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
        COMMENT "Profiling with Linux perf tool"
    )
    
    add_custom_target(perf-flamegraph
        COMMAND ${CMAKE_COMMAND} -E echo "Generating flamegraph..."
        COMMAND sudo ${PERF_PATH} record -F 99 -g ./profiling-demo
        COMMAND sudo ${PERF_PATH} script > perf.data.script
        COMMAND ${CMAKE_COMMAND} -E echo "perf script data saved to: perf.data.script"
        COMMAND ${CMAKE_COMMAND} -E echo "Use flamegraph.pl to generate visualization"
        DEPENDS profiling-demo
        WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
        COMMENT "Generating perf flamegraph data"
    )
endif()

# Target: profile-with-valgrind
# Uses valgrind/callgrind for detailed profiling
if(VALGRIND_PATH)
    add_custom_target(profile-with-valgrind
        COMMAND ${CMAKE_COMMAND} -E echo "Profiling with valgrind/callgrind..."
        COMMAND ${VALGRIND_PATH} --tool=callgrind --callgrind-out-file=callgrind.out ./profiling-demo
        COMMAND ${CMAKE_COMMAND} -E echo "Callgrind data saved to: callgrind.out"
        COMMAND ${CMAKE_COMMAND} -E echo "Analyze with: kcachegrind callgrind.out (or callgrind_annotate callgrind.out)"
        DEPENDS profiling-demo
        WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
        COMMENT "Profiling with valgrind/callgrind"
    )
    
    add_custom_target(profile-memory-valgrind
        COMMAND ${CMAKE_COMMAND} -E echo "Memory profiling with valgrind/massif..."
        COMMAND ${VALGRIND_PATH} --tool=massif --massif-out-file=massif.out ./profiling-demo
        COMMAND ${CMAKE_COMMAND} -E echo "Massif data saved to: massif.out"
        COMMAND ${CMAKE_COMMAND} -E echo "Analyze with: ms_print massif.out"
        DEPENDS profiling-demo
        WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
        COMMENT "Memory profiling with valgrind/massif"
    )
endif()

# Target: run-profiling-demo
# Runs the profiling demo with internal profiler
add_custom_target(run-profiling-demo
    COMMAND ./profiling-demo
    DEPENDS profiling-demo
    WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
    COMMENT "Running Agent-Zero profiling demonstration"
)

# Print available profiling targets
message(STATUS "")
message(STATUS "Agent-Zero Profiling Infrastructure configured (AZ-PERF-001)")
message(STATUS "Available profiling targets:")
message(STATUS "  run-profiling-demo           - Run profiling demo with internal profiler")
if(GPROF_PATH)
    message(STATUS "  profile-with-gprof          - Profile with gprof (requires -pg build)")
    message(STATUS "  analyze-gprof               - Analyze gprof results")
endif()
if(PERF_PATH)
    message(STATUS "  profile-with-perf           - Profile with Linux perf")
    message(STATUS "  perf-flamegraph             - Generate perf flamegraph data")
endif()
if(VALGRIND_PATH)
    message(STATUS "  profile-with-valgrind       - Profile with valgrind/callgrind")
    message(STATUS "  profile-memory-valgrind     - Memory profile with valgrind/massif")
endif()
message(STATUS "")
