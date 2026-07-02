# Agent-Zero Python Bridge CMakeLists.txt

cmake_minimum_required(VERSION 3.16)

project(AgentZeroPythonBridge
    VERSION 0.1.0
    DESCRIPTION "Python Bindings for Agent-Zero OpenCog Integration"
    LANGUAGES CXX
)

# Set C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Find Python
find_package(Python3 COMPONENTS Interpreter Development REQUIRED)
message(STATUS "Found Python ${Python3_VERSION}: ${Python3_EXECUTABLE}")
message(STATUS "Python include dirs: ${Python3_INCLUDE_DIRS}")
message(STATUS "Python libraries: ${Python3_LIBRARIES}")

# Find Cython
find_program(CYTHON_EXECUTABLE cython3
    NAMES cython3 cython
    DOC "Path to the cython executable")

if(NOT CYTHON_EXECUTABLE)
    message(WARNING "Cython not found - Python bindings will not be built")
    message(STATUS "Install cython: pip install cython")
    return()
endif()

message(STATUS "Found Cython: ${CYTHON_EXECUTABLE}")

# Check Cython version
execute_process(
    COMMAND ${CYTHON_EXECUTABLE} --version
    OUTPUT_VARIABLE CYTHON_VERSION_OUTPUT
    ERROR_VARIABLE CYTHON_VERSION_OUTPUT
    OUTPUT_STRIP_TRAILING_WHITESPACE
    ERROR_STRIP_TRAILING_WHITESPACE
)

if(CYTHON_VERSION_OUTPUT MATCHES "([0-9]+\\.[0-9]+)")
    set(CYTHON_VERSION "${CMAKE_MATCH_1}")
    message(STATUS "Cython version: ${CYTHON_VERSION}")
    
    # Check if version is 0.29 or higher
    if(CYTHON_VERSION VERSION_LESS "0.29")
        message(WARNING "Cython version ${CYTHON_VERSION} is too old (need 0.29+)")
        message(STATUS "Upgrade cython: pip install --upgrade cython")
        return()
    endif()
else()
    message(WARNING "Could not determine Cython version")
endif()

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

# Find agentzero-core (optional - may not be built yet)
pkg_check_modules(AGENTZERO_CORE agentzero-core)
if (AGENTZERO_CORE_FOUND)
    message(STATUS "Found agentzero-core version ${AGENTZERO_CORE_VERSION}")
    include_directories(${AGENTZERO_CORE_INCLUDE_DIRS})
    link_directories(${AGENTZERO_CORE_LIBRARY_DIRS})
else()
    message(STATUS "agentzero-core not found via pkg-config, looking for local build")
    # Look for local installation
    find_path(AGENTZERO_CORE_INCLUDE_PATH
        NAMES opencog/agentzero/AgentZeroCore.h
        PATHS /usr/local/include /usr/include
              ${CMAKE_SOURCE_DIR}/../agentzero-core/include
        PATH_SUFFIXES opencog
    )
    if(AGENTZERO_CORE_INCLUDE_PATH)
        message(STATUS "Found agentzero-core headers at ${AGENTZERO_CORE_INCLUDE_PATH}")
        include_directories(${AGENTZERO_CORE_INCLUDE_PATH})
        set(AGENTZERO_CORE_FOUND TRUE)
    else()
        message(WARNING "agentzero-core not found - bridge will build with stub implementations")
        set(AGENTZERO_CORE_FOUND FALSE)
    endif()
endif()

# Include directories
include_directories(
    ${CMAKE_CURRENT_SOURCE_DIR}/include
    ${Python3_INCLUDE_DIRS}
    ${CMAKE_CURRENT_SOURCE_DIR}/opencog
)

# Python site-packages directory
execute_process(
    COMMAND ${Python3_EXECUTABLE} -c "import site; print(site.getsitepackages()[0])"
    OUTPUT_VARIABLE Python3_SITELIB
    OUTPUT_STRIP_TRAILING_WHITESPACE
)
message(STATUS "Python site-packages: ${Python3_SITELIB}")

# Set Cython include path
set(CYTHON_INCLUDE_PATH ${CMAKE_CURRENT_SOURCE_DIR}/opencog)

# Helper function to compile Cython modules
function(cython_add_module module_name pyx_file)
    set(c_file "${CMAKE_CURRENT_BINARY_DIR}/${module_name}.cpp")
    
    # Generate C++ from Cython
    add_custom_command(
        OUTPUT ${c_file}
        COMMAND ${CYTHON_EXECUTABLE}
        ARGS --cplus -3
             -I ${CYTHON_INCLUDE_PATH}
             -o ${c_file}
             ${CMAKE_CURRENT_SOURCE_DIR}/${pyx_file}
        DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/${pyx_file}
        COMMENT "Cythonizing ${pyx_file}"
    )
    
    # Create Python extension module
    Python3_add_library(${module_name} MODULE ${c_file})
    
    # Link libraries
    target_link_libraries(${module_name} PRIVATE
        ${COGUTIL_LIBRARIES}
        ${ATOMSPACE_LIBRARIES}
        Python3::Python
    )
    
    # Link agentzero-core if available
    if(AGENTZERO_CORE_FOUND AND AGENTZERO_CORE_LIBRARIES)
        target_link_libraries(${module_name} PRIVATE ${AGENTZERO_CORE_LIBRARIES})
    endif()
    
    # Set module properties
    set_target_properties(${module_name} PROPERTIES
        PREFIX ""
        OUTPUT_NAME ${module_name}
        SUFFIX ".so"
    )
    
    # Installation
    install(TARGETS ${module_name}
        LIBRARY DESTINATION ${Python3_SITELIB}/opencog/agentzero
    )
endfunction()

# Build Cython modules
cython_add_module(agentzero_core opencog/agentzero/agentzero_core.pyx)
cython_add_module(cognitive_loop opencog/agentzero/cognitive_loop.pyx)
cython_add_module(task_manager opencog/agentzero/task_manager.pyx)
cython_add_module(knowledge_integrator opencog/agentzero/knowledge_integrator.pyx)

# Install Python wrapper modules
install(FILES
    opencog/agentzero/__init__.py
    opencog/agentzero/agent_zero.py
    opencog/agentzero/exceptions.py
    opencog/agentzero/utils.py
    DESTINATION ${Python3_SITELIB}/opencog/agentzero
)

# Install opencog package init if it doesn't exist
install(CODE "
    if(NOT EXISTS ${Python3_SITELIB}/opencog/__init__.py)
        file(WRITE ${Python3_SITELIB}/opencog/__init__.py
             \"# OpenCog Python Package\\n\")
    endif()
")

# Tests
if(BUILD_TESTING)
    enable_testing()
    add_subdirectory(tests)
endif()

# Examples
add_subdirectory(examples)

# Status message
message(STATUS "Agent-Zero Python Bridge configuration complete")
if(AGENTZERO_CORE_FOUND)
    message(STATUS "Python bindings will link against agentzero-core")
else()
    message(STATUS "Python bindings will use stub implementations (agentzero-core not found)")
endif()
