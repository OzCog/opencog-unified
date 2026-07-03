cmake_minimum_required(VERSION 3.10)
project(opencog-unified VERSION 1.0.0)

# Set CMake policies to handle target conflicts
cmake_policy(SET CMP0002 NEW)  # Allow duplicate target names in subdirectories
if(POLICY CMP0167)
    cmake_policy(SET CMP0167 OLD)  # Use legacy FindBoost module
endif()

# Set C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Add cmake directory to module path
set(CMAKE_MODULE_PATH 
    ${CMAKE_CURRENT_SOURCE_DIR}/cmake
    ${CMAKE_CURRENT_SOURCE_DIR}/cogutil/cmake
    ${CMAKE_MODULE_PATH}
)

# Create deps directory if it doesn't exist
file(MAKE_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/deps)

# Include dependencies if directory exists and has CMakeLists.txt
if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/deps/CMakeLists.txt")
    add_subdirectory(deps)
endif()

# Include dependencies (commented out as deps directory doesn't exist)
# add_subdirectory(deps)

# Include unified cognitive modules
# Build cogutil first as it's a core dependency
add_subdirectory(cogutil)

# Export CogUtil configuration for other components
set(CogUtil_DIR "${CMAKE_CURRENT_BINARY_DIR}/cogutil" CACHE PATH "CogUtil build directory")
set(ENV{CogUtil_DIR} "${CMAKE_CURRENT_BINARY_DIR}/cogutil")

# Add atomspace (depends on cogutil)
add_subdirectory(atomspace)

# Add cogserver (depends on atomspace)
add_subdirectory(cogserver)

# Phase I: Core Extensions (Week 1)
# Add atomspace-storage if it exists and has CMakeLists.txt
if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/atomspace-storage/CMakeLists.txt")
    add_subdirectory(atomspace-storage)
endif()

# Add atomspace-rocks if it exists and has CMakeLists.txt
if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/atomspace-rocks/CMakeLists.txt")
    add_subdirectory(atomspace-rocks)
endif()

# Add atomspace-restful if it exists and has CMakeLists.txt
if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/atomspace-restful/CMakeLists.txt")
    add_subdirectory(atomspace-restful)
endif()

# Phase I: Core Extensions (Week 3)
# Add moses if it exists and has CMakeLists.txt
if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/moses/CMakeLists.txt")
    add_subdirectory(moses)
endif()

# Define inter-module dependencies explicitly
add_dependencies(atomspace cogutil)
add_dependencies(cogserver atomspace)
# atomspace-storage depends on atomspace
if(TARGET atomspace-storage)
    add_dependencies(atomspace-storage atomspace)
endif()
# atomspace-rocks depends on atomspace
if(TARGET atomspace-rocks)
    add_dependencies(atomspace-rocks atomspace)
endif()
# atomspace-restful depends on atomspace
if(TARGET atomspace-restful)
    add_dependencies(atomspace-restful atomspace)
endif()
# cogserver optionally depends on atomspace-rocks for RocksDB storage tests
if(TARGET atomspace-rocks)
    add_dependencies(cogserver atomspace-rocks)
endif()
# moses depends on cogutil
if(TARGET moses)
    add_dependencies(moses cogutil)
endif()

# Phase II: Recursive Cognitive Expansion modules
# Create directories for new components
file(MAKE_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/cognitive-patterns)
file(MAKE_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/distributed-cognition) 
file(MAKE_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/cognitive-visualization)
file(MAKE_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/tutorial-automation)

# Add Phase II modules if they have CMakeLists.txt
# Temporarily disabled due to empty source lists - will be fixed in future PR
# if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/cognitive-patterns/CMakeLists.txt")
#     add_subdirectory(cognitive-patterns)
# endif()
if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/distributed-cognition/CMakeLists.txt")
    add_subdirectory(distributed-cognition)
endif()
if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/cognitive-visualization/CMakeLists.txt")
    add_subdirectory(cognitive-visualization)
endif()
# Temporarily disabled due to empty source lists - will be fixed in future PR
# if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/tutorial-automation/CMakeLists.txt")
#     add_subdirectory(tutorial-automation)
# endif()

# Add unified GGML tensor kernel
if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/ggml-tensor-kernel/CMakeLists.txt")
    add_subdirectory(ggml-tensor-kernel)
endif()

# Add agentic kernels catalog
if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/agentic-kernels-catalog/CMakeLists.txt")
    add_subdirectory(agentic-kernels-catalog)
endif()

# Add autonomous agency module
if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/autonomous-agency/CMakeLists.txt")
    add_subdirectory(autonomous-agency)
    message(STATUS "Autonomous Agency module: ENABLED")
else()
    message(STATUS "Autonomous Agency module: NOT FOUND")
endif()

# Phase II: Logic Systems Integration (Weeks 5-8)
# Add unify if it exists and has CMakeLists.txt (depends on atomspace)
if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/unify/CMakeLists.txt")
    add_subdirectory(unify)
endif()

# Add ure (Unified Rule Engine) if it exists and has CMakeLists.txt (depends on unify)
if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/ure/CMakeLists.txt")
    add_subdirectory(ure)
endif()

# Add language-learning if it exists and has CMakeLists.txt (depends on cogutil)
if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/language-learning/CMakeLists.txt")
    add_subdirectory(language-learning)
endif()

# Global cognitive build targets
add_custom_target(cognitive ALL DEPENDS cogutil atomspace cogserver)

# Phase II Logic Systems target
add_custom_target(logic-systems
    COMMENT "Building Phase II logic systems components"
)

# Add dependencies for logic systems if targets exist
if(TARGET unify)
    add_dependencies(logic-systems unify)
    add_dependencies(unify atomspace)
endif()
if(TARGET ure)
    add_dependencies(logic-systems ure)
    add_dependencies(ure unify)
endif()
if(TARGET language-learning)
    add_dependencies(logic-systems language-learning)
    add_dependencies(language-learning cogutil)
endif()

# Phase III: Cognitive Systems Integration (Weeks 9-12)
# Add attention component (Week 9)
if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/attention/CMakeLists.txt")
    add_subdirectory(attention)
endif()

# Add spacetime component (Week 10) - will be created next
if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/spacetime/CMakeLists.txt")
    add_subdirectory(spacetime)
endif()

# Add Phase III cognitive systems target
add_custom_target(cognitive-systems
    COMMENT "Building Phase III cognitive systems components"
)

# Add dependencies for cognitive systems if targets exist
if(TARGET attention)
    add_dependencies(cognitive-systems attention)
    add_dependencies(attention atomspace cogserver)
endif()
if(TARGET spacetime)
    add_dependencies(cognitive-systems spacetime)
    add_dependencies(spacetime atomspace)
endif()

# Phase IV: Advanced & Learning Systems (Weeks 13-16)
# Add PLN (Probabilistic Logic Networks) - Week 13
if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/pln/CMakeLists.txt")
    add_subdirectory(pln)
endif()

# Add Miner (Pattern Mining) - Week 14
if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/miner/CMakeLists.txt")
    add_subdirectory(miner)
endif()

# Add ASMoses (AtomSpace MOSES) - Week 15
if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/asmoses/CMakeLists.txt")
    add_subdirectory(asmoses)
endif()

# Add Phase IV advanced systems target
add_custom_target(advanced-systems
    COMMENT "Building Phase IV advanced and learning systems"
)

# Add dependencies for advanced systems if targets exist
if(TARGET pln)
    add_dependencies(advanced-systems pln)
    add_dependencies(pln atomspace ure spacetime)
endif()
if(TARGET miner)
    add_dependencies(advanced-systems miner)
    add_dependencies(miner atomspace ure)
endif()
if(TARGET asmoses)
    add_dependencies(advanced-systems asmoses)
    add_dependencies(asmoses atomspace ure)
endif()

# Phase V: Language & Final Integration (Weeks 17-20)
# Add lg-atomese (Link Grammar to AtomSpace) - Week 17
if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/lg-atomese/CMakeLists.txt")
    add_subdirectory(lg-atomese)
endif()

# Add learn (Unsupervised Learning) - Week 18
if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/learn/CMakeLists.txt")
    add_subdirectory(learn)
endif()

# Add opencog main integration - Week 19
if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/opencog/CMakeLists.txt")
    add_subdirectory(opencog)
endif()

# Add Phase V language and final integration target
add_custom_target(language-integration
    COMMENT "Building Phase V language and final integration systems"
)

# Add dependencies for language integration if targets exist
if(TARGET lg-atomese)
    add_dependencies(language-integration lg-atomese)
    add_dependencies(lg-atomese atomspace)
endif()
if(TARGET learn)
    add_dependencies(language-integration learn)
    add_dependencies(learn atomspace cogserver)
endif()
if(TARGET opencog-main)
    add_dependencies(language-integration opencog-main)
    add_dependencies(opencog-main atomspace cogserver attention ure lg-atomese)
endif()

# Phase V Extended: Recursive Meta-Cognition & Evolutionary Optimization
if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/meta-cognition/CMakeLists.txt")
    add_subdirectory(meta-cognition)
endif()

if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/evolutionary-optimization/CMakeLists.txt")
    add_subdirectory(evolutionary-optimization)
endif()

# Add Phase V meta-cognitive optimization target
add_custom_target(meta-cognitive-optimization
    COMMENT "Building Phase V meta-cognitive and evolutionary optimization systems"
)

# Add dependencies for meta-cognitive optimization if targets exist
if(TARGET meta-cognition)
    add_dependencies(meta-cognitive-optimization meta-cognition)
endif()
if(TARGET evolutionary-optimization)
    add_dependencies(meta-cognitive-optimization evolutionary-optimization)
    if(TARGET meta-cognition)
        add_dependencies(evolutionary-optimization meta-cognition)
    endif()
endif()
# Phase 4: Distributed Cognitive Mesh API & Embodiment Layer
# Temporarily disabled due to empty source lists - will be fixed in future PR
# if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/distributed-cognitive-mesh/CMakeLists.txt")
#     add_subdirectory(distributed-cognitive-mesh)
# endif()

# Add Phase 4 distributed cognitive mesh target
add_custom_target(distributed-cognitive-mesh-phase4
    COMMENT "Building Phase 4: Distributed Cognitive Mesh API & Embodiment Layer"
)

# Add dependencies for distributed cognitive mesh if targets exist
if(TARGET distributed-cognitive-mesh)
    add_dependencies(distributed-cognitive-mesh-phase4 distributed-cognitive-mesh)
    add_dependencies(distributed-cognitive-mesh distributed-cognition cognitive-visualization)
endif()

# Phase VI: CogZero - Agent-Zero C++ Implementation
# High-performance autonomous agent framework optimized for OpenCog
# Requires CogUtil and AtomSpace to be installed as system packages.
# Set BUILD_COGZERO=ON to enable when deps are available.
option(BUILD_COGZERO "Build the CogZero Agent-Zero framework (requires installed OpenCog packages)" OFF)
if(BUILD_COGZERO AND EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/cogzero/CMakeLists.txt")
    add_subdirectory(cogzero)
    message(STATUS "CogZero Agent Framework: ENABLED")
else()
    message(STATUS "CogZero Agent Framework: DISABLED (set BUILD_COGZERO=ON to enable)")
endif()

# Add Phase VI CogZero target
add_custom_target(cogzero-phase6
    COMMENT "Building Phase VI: CogZero Agent-Zero Framework"
)

# Add dependencies for CogZero if targets exist
if(TARGET cogzero)
    add_dependencies(cogzero-phase6 cogzero)
endif()
if(TARGET agentzero-core)
    add_dependencies(agentzero-core atomspace cogutil)
    if(TARGET server)
        add_dependencies(agentzero-core server)
    endif()
endif()
if(TARGET agentzero-learning AND TARGET moses)
    add_dependencies(agentzero-learning moses)
endif()
if(TARGET agentzero-planning AND TARGET spacetime)
    add_dependencies(agentzero-planning spacetime)
endif()
if(TARGET agentzero-memory AND TARGET attention)
    add_dependencies(agentzero-memory attention)
endif()
if(TARGET agentzero-communication AND TARGET lg-atomese)
    add_dependencies(agentzero-communication lg-atomese)
endif()

# Phase VII: ATenSpace - Tensor-based AtomSpace
# ATen/PyTorch tensor-based adaptation of AtomSpace with GPU acceleration
if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/atenspace/CMakeLists.txt")
    add_subdirectory(atenspace)
    message(STATUS "ATenSpace Tensor Backend: ENABLED")
else()
    message(STATUS "ATenSpace Tensor Backend: NOT FOUND")
endif()

# Add Phase VII ATenSpace target
add_custom_target(atenspace-phase7
    COMMENT "Building Phase VII: ATenSpace Tensor-based AtomSpace"
)

# Add dependencies for ATenSpace if targets exist
if(TARGET atenspace)
    add_dependencies(atenspace-phase7 atenspace)
endif()
if(TARGET atenspace-headers)
    add_dependencies(atenspace-phase7 atenspace-headers)
endif()

# Phase VIII: HyperMind - Distributed Neural Network Framework
# Actor-based concurrency and reactive streams for high-performance deep learning
if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/hypermind/CMakeLists.txt")
    add_subdirectory(hypermind)
    message(STATUS "HyperMind Neural Framework: ENABLED")
else()
    message(STATUS "HyperMind Neural Framework: NOT FOUND")
endif()

# Add Phase VIII HyperMind target
add_custom_target(hypermind-phase8
    COMMENT "Building Phase VIII: HyperMind Distributed Neural Network Framework"
)

# Add dependencies for HyperMind if targets exist
if(TARGET hypermind)
    add_dependencies(hypermind-phase8 hypermind)
    # HyperMind can optionally integrate with ATenSpace for tensor operations
    if(TARGET atenspace)
        add_dependencies(hypermind atenspace)
    endif()
endif()

# Add comprehensive target that includes all phases
add_custom_target(cognitive-complete
    DEPENDS cognitive agentic-kernels-catalog logic-systems cognitive-systems advanced-systems language-integration meta-cognitive-optimization distributed-cognitive-mesh-phase4 cogzero-phase6 atenspace-phase7 hypermind-phase8
    COMMENT "Building complete cognitive system with all phases: core, logic, cognitive, advanced, language, meta-cognitive, distributed cognitive mesh, CogZero agent, ATenSpace tensor, and HyperMind neural network systems"
)