---
description: 'OpenCog C++ coding standards and patterns. Stacks with cmake-vcpkg and cpp-language-service-tools instructions.'
applyTo: '**/*.cc, **/*.cpp, **/*.h, **/*.hpp, **/*.cxx'
---

# OpenCog C++ Coding Standards

## Naming Conventions
- Classes: `CamelCase` (e.g., `AtomSpace`, `TruthValue`, `HandleSeq`)
- Functions: `snake_case` (e.g., `get_handle`, `add_atom`)
- Member variables: `_underscore_prefix` (e.g., `_atomspace`, `_name`)
- Constants: `ALL_CAPS` (e.g., `MAX_ARITY`, `DEFAULT_TV`)
- Namespaces: `opencog` (always)

## Include Guards
```cpp
#ifndef _OPENCOG_COMPONENT_CLASS_H
#define _OPENCOG_COMPONENT_CLASS_H
// ...
#endif // _OPENCOG_COMPONENT_CLASS_H
```

## Common Types
```cpp
using namespace opencog;

Handle h;                    // Atom reference
HandleSeq hs;               // std::vector<Handle>
HandleSet hset;             // std::unordered_set<Handle>
AtomSpace* as;              // AtomSpace pointer
TruthValuePtr tv;           // shared_ptr<TruthValue>
ValuePtr vp;                // shared_ptr<Value>
Type t;                     // Atom type ID
```

## Factory Functions (prefer over constructors)
```cpp
Handle h = as->add_node(CONCEPT_NODE, "name");
Handle l = as->add_link(INHERITANCE_LINK, {h1, h2});
TruthValuePtr tv = createSimpleTruthValue(0.9, 0.8);
```

## Error Handling
- Use `OC_ASSERT(condition, "message")` from cogutil
- Throw `InvalidParamException` for bad inputs
- Throw `RuntimeException` for unexpected states
- Never silently swallow exceptions

## Build Integration
- Every .cc file must be listed in component's `CMakeLists.txt`
- Headers go in `opencog/component-name/`
- Implementation goes alongside headers or in `src/`
- Tests in `tests/component-name/`
