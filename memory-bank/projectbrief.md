# Project Brief — OpenCog Unified

## What Is This?
OpenCog Unified is a monorepo integrating 14+ components of the OpenCog cognitive architecture framework for Artificial General Intelligence (AGI) research and development.

## Core Goal
Provide a single, buildable, testable repository containing the complete OpenCog cognitive stack — from low-level utilities through reasoning engines to language processing.

## Target Users
- AGI researchers implementing cognitive architectures
- Developers building on the OpenCog framework
- Scientists exploring hypergraph-based knowledge representation

## Key Technical Facts
- **Language**: C++ (core) + Guile/Scheme (scripting/rules) + Python (tests/bindings)
- **Build**: CMake, requires Boost + Guile + RocksDB
- **Build time**: 30-60 minutes full, 5-10 min per phase
- **Components**: 14+ with strict dependency ordering
- **Central structure**: AtomSpace (typed hypergraph)
