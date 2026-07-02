#!/usr/bin/env python3
"""
CMake Dependency Fixer for OpenCog Unified

This script analyzes CMakeLists.txt files and adds missing ADD_DEPENDENCIES
declarations based on TARGET_LINK_LIBRARIES usage.

Author: Claude Code Assistant
Date: 2026-01-02
"""

import re
from pathlib import Path


# Mapping of CMake variables to their target names
KNOWN_DEPENDENCIES = {
    # Core utilities
    '${COGUTIL_LIBRARY}': 'cogutil',
    '${COGUTIL_LIBRARIES}': 'cogutil',
    'cogutil': 'cogutil',

    # AtomSpace
    '${ATOMSPACE_LIBRARY}': 'atomspace',
    '${ATOMSPACE_LIBRARIES}': 'atomspace',
    '${ATOMSPACE_atombase_LIBRARY}': 'atombase',
    '${ATOMSPACE_atomcore_LIBRARY}': 'atomcore',
    '${ATOMSPACE_atomtypes_LIBRARY}': 'atomspace-types',
    '${ATOMSPACE_atomvalue_LIBRARY}': 'atomvalue',
    '${ATOMSPACE_atomproto_LIBRARY}': 'atomproto',
    '${ATOMSPACE_truthvalue_LIBRARY}': 'truthvalue',
    '${ATOMSPACE_attentionbank_LIBRARY}': 'attentionbank',
    '${ATOMSPACE_atom_types_LIBRARY}': 'atom_types',
    'atombase': 'atombase',
    'atomcore': 'atomcore',
    'atomspace': 'atomspace',
    'atomspace-types': 'atomspace-types',
    'atom_types': 'atom_types',
    'atomvalue': 'atomvalue',
    'atomproto': 'atomproto',
    'truthvalue': 'truthvalue',
    'attentionbank': 'attentionbank',

    # CogServer
    '${COGSERVER_LIBRARY}': 'server',
    '${COGSERVER_LIBRARIES}': 'server',
    '${COGSERVER_SERVER_LIBRARY}': 'server',
    '${COGSERVER_NETWORK_LIBRARY}': 'network',
    'server': 'server',
    'network': 'network',
    'builtinreqs': 'builtinreqs',

    # Unify
    '${UNIFY_LIBRARY}': 'unify',
    '${UNIFY_LIBRARIES}': 'unify',
    'unify': 'unify',
    'unify-types': 'unify-types',

    # URE
    '${URE_LIBRARY}': 'ure',
    '${URE_LIBRARIES}': 'ure',
    'ure': 'ure',
    'ure-types': 'ure-types',

    # Attention
    '${ATTENTION_LIBRARY}': 'attention',
    '${ATTENTION_LIBRARIES}': 'attention',
    'attention': 'attention',
    'attentionagents': 'attentionagents',
    'hebbiancreation': 'hebbiancreation',

    # Spacetime
    '${SPACETIME_LIBRARY}': 'spacetime',
    '${SPACETIME_LIBRARIES}': 'spacetime',
    'spacetime': 'spacetime',

    # PLN
    '${PLN_LIBRARY}': 'pln',
    '${PLN_LIBRARIES}': 'pln',
    'pln': 'pln',

    # Miner
    '${MINER_LIBRARY}': 'miner',
    '${MINER_LIBRARIES}': 'miner',
    'miner': 'miner',

    # MOSES
    '${MOSES_LIBRARY}': 'moses',
    '${MOSES_LIBRARIES}': 'moses',
    '${COMBOREDUCT_LIBRARY}': 'comboreduct',
    '${COMBOREDUCT_LIBRARIES}': 'comboreduct',
    'moses': 'moses',
    'comboreduct': 'comboreduct',
    'comboant': 'comboant',
    'comboreduct_complete': 'comboreduct_complete',

    # Persistence
    '${PERSIST_LIBRARY}': 'persist',
    '${PERSIST_LIBRARIES}': 'persist',
    'persist': 'persist',
    'persist-api': 'persist-api',
    'persist-rocks': 'persist-rocks',
    'persist-monospace': 'persist-monospace',
    'persist-sexpr': 'persist-sexpr',
    'persist-file': 'persist-file',
    'persist-json': 'persist-json',
    'persist-csv': 'persist-csv',
    'persist-flow': 'persist-flow',
    'persist-storage': 'persist-storage',
    'persist-sexcom': 'persist-sexcom',
    'persist-tlb': 'persist-tlb',
    'persist-prolog': 'persist-prolog',
    'persist-proxy': 'persist-proxy',

    # Language Learning
    '${LG_ATOMESE_LIBRARY}': 'lg-atomese',
    '${LEARN_LIBRARY}': 'learn',
    'lg-atomese': 'lg-atomese',
    'learn': 'learn',

    # Neural-symbolic integration
    'neural-symbolic': 'neural-symbolic',

    # Execution
    'execution': 'execution',
    'query': 'query',
    'clearbox': 'clearbox',

    # Pattern
    'pattern': 'pattern',

    # Value
    'value': 'value',

    # Smob
    'smob': 'smob',
}

# Build order dependencies (what each target depends on)
BUILD_ORDER = {
    # Level 0: No dependencies within opencog
    'cogutil': [],

    # Level 1: Depends on cogutil
    'atomspace-types': ['cogutil'],
    'atom_types': ['cogutil'],
    'atomvalue': ['cogutil'],
    'truthvalue': ['cogutil', 'atomvalue'],

    # Level 2: Depends on atomspace core types
    'atombase': ['cogutil', 'atomvalue', 'truthvalue'],
    'atomproto': ['cogutil', 'atomvalue', 'truthvalue'],
    'atomcore': ['cogutil', 'atombase', 'atomvalue', 'truthvalue'],

    # Level 3: Full atomspace
    'atomspace': ['cogutil', 'atombase', 'atomcore', 'atomvalue', 'truthvalue'],
    'execution': ['atomspace'],
    'query': ['atomspace'],
    'pattern': ['atomspace'],
    'clearbox': ['atomspace'],
    'smob': ['atomspace'],
    'value': ['atomspace'],

    # Level 4: Depends on atomspace
    'network': ['cogutil'],
    'server': ['cogutil', 'network', 'atomspace'],
    'builtinreqs': ['server', 'atomspace'],

    # Level 5: Persistence
    'persist': ['atomspace'],
    'persist-api': ['atomspace'],
    'persist-sexpr': ['atomspace'],
    'persist-file': ['atomspace', 'persist-sexpr'],
    'persist-json': ['atomspace'],
    'persist-csv': ['atomspace'],
    'persist-flow': ['atomspace'],
    'persist-storage': ['atomspace'],
    'persist-sexcom': ['atomspace', 'server'],
    'persist-tlb': ['atomspace'],
    'persist-prolog': ['atomspace'],
    'persist-proxy': ['atomspace'],
    'persist-rocks': ['atomspace'],
    'persist-monospace': ['atomspace'],

    # Level 6: Logic systems
    'unify': ['atomspace'],
    'unify-types': ['atomspace'],
    'ure': ['atomspace', 'unify'],
    'ure-types': ['atomspace'],

    # Level 7: Reasoning systems
    'pln': ['atomspace', 'ure'],
    'miner': ['atomspace', 'ure'],

    # Level 8: MOSES
    'comboreduct': ['cogutil'],
    'moses': ['cogutil', 'comboreduct'],

    # Level 9: Attention and Spacetime
    'attention': ['atomspace', 'cogutil'],
    'attentionagents': ['atomspace', 'attention'],
    'hebbiancreation': ['atomspace', 'attention'],
    'spacetime': ['atomspace'],

    # Level 10: Language
    'lg-atomese': ['atomspace'],
    'learn': ['atomspace'],
}


def find_add_library(content: str) -> list[str]:
    """Find all ADD_LIBRARY target names in content."""
    pattern = r'ADD_LIBRARY\s*\(\s*(\w+[-\w]*)'
    matches = re.findall(pattern, content, re.IGNORECASE)
    return matches


def find_target_link_libraries(content: str, target: str) -> list[str]:
    """Find all libraries linked to a target."""
    # Pattern to match TARGET_LINK_LIBRARIES(target ...)
    pattern = rf'TARGET_LINK_LIBRARIES\s*\(\s*{re.escape(target)}[\s\n]+([^)]+)\)'
    match = re.search(pattern, content, re.IGNORECASE | re.DOTALL)

    if not match:
        return []

    links_text = match.group(1)
    # Extract library references
    links = re.findall(r'\$\{[^}]+\}|\b\w+[-\w]*\b', links_text)
    return links


def find_existing_dependencies(content: str, target: str) -> set[str]:
    """Find existing ADD_DEPENDENCIES for a target."""
    pattern = rf'ADD_DEPENDENCIES\s*\(\s*{re.escape(target)}[\s\n]+([^)]+)\)'
    match = re.search(pattern, content, re.IGNORECASE | re.DOTALL)

    if not match:
        return set()

    deps_text = match.group(1)
    deps = set(re.findall(r'\b\w+[-\w]*\b', deps_text))
    return deps


def determine_required_dependencies(links: list[str]) -> set[str]:
    """Determine required dependencies based on linked libraries."""
    deps = set()

    for link in links:
        if link in KNOWN_DEPENDENCIES:
            dep = KNOWN_DEPENDENCIES[link]
            deps.add(dep)
            # Also add transitive dependencies from BUILD_ORDER
            if dep in BUILD_ORDER:
                for transitive_dep in BUILD_ORDER[dep]:
                    deps.add(transitive_dep)

    return deps


def add_dependency_declaration(content: str, target: str, deps: set[str]) -> str:
    """Add ADD_DEPENDENCIES declaration after ADD_LIBRARY."""
    if not deps:
        return content

    # Format dependencies - limit to direct dependencies, not all transitive
    deps_str = ' '.join(sorted(deps))
    new_line = f'\nADD_DEPENDENCIES({target} {deps_str})\n'

    # Find the ADD_LIBRARY line for this target
    pattern = rf'(ADD_LIBRARY\s*\(\s*{re.escape(target)}[^)]+\))'
    match = re.search(pattern, content, re.IGNORECASE)

    if match:
        # Insert after the ADD_LIBRARY statement
        insert_pos = match.end()
        content = content[:insert_pos] + new_line + content[insert_pos:]

    return content


def process_cmake_file(filepath: Path, dry_run: bool = False) -> tuple[bool, list[str]]:
    """Process a single CMakeLists.txt file."""
    changes = []

    try:
        content = filepath.read_text()
        original_content = content
    except Exception as e:
        return False, [f"Error reading {filepath}: {e}"]

    # Find all library targets
    targets = find_add_library(content)

    for target in targets:
        # Find what this target links to
        links = find_target_link_libraries(content, target)

        if not links:
            continue

        # Find existing dependencies
        existing_deps = find_existing_dependencies(content, target)

        # Determine required dependencies
        required_deps = determine_required_dependencies(links)

        # Filter to only direct OpenCog dependencies (not system libs)
        required_deps = {d for d in required_deps if d in KNOWN_DEPENDENCIES.values()}

        # Remove self-reference
        required_deps.discard(target)

        # Find missing dependencies
        missing_deps = required_deps - existing_deps

        if missing_deps:
            changes.append(f"  {target}: adding dependencies {missing_deps}")

            if not dry_run:
                if existing_deps:
                    # Update existing ADD_DEPENDENCIES
                    all_deps = existing_deps | missing_deps
                    deps_str = ' '.join(sorted(all_deps))

                    # Replace existing declaration
                    old_pattern = rf'ADD_DEPENDENCIES\s*\(\s*{re.escape(target)}[^)]+\)'
                    new_decl = f'ADD_DEPENDENCIES({target} {deps_str})'
                    content = re.sub(old_pattern, new_decl, content, flags=re.IGNORECASE)
                else:
                    # Add new declaration
                    content = add_dependency_declaration(content, target, missing_deps)

    if changes and not dry_run and content != original_content:
        try:
            filepath.write_text(content)
            return True, changes
        except Exception as e:
            return False, [f"Error writing {filepath}: {e}"]

    return bool(changes), changes


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Fix CMake dependencies for OpenCog Unified')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be changed without modifying files')
    parser.add_argument('--path', type=str, default='.', help='Root path to search for CMakeLists.txt files')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    args = parser.parse_args()

    root_path = Path(args.path).resolve()
    cmake_files = list(root_path.rglob('CMakeLists.txt'))

    # Filter to only process files in opencog directories
    cmake_files = [f for f in cmake_files if 'opencog' in str(f) and 'build' not in str(f)]

    print(f"Scanning {len(cmake_files)} CMakeLists.txt files...")

    total_changes = 0
    files_modified = 0

    for cmake_file in sorted(cmake_files):
        modified, changes = process_cmake_file(cmake_file, dry_run=args.dry_run)

        if changes:
            rel_path = cmake_file.relative_to(root_path)
            print(f"\n{rel_path}:")
            for change in changes:
                print(change)

            if modified:
                files_modified += 1
            total_changes += len(changes)

    print(f"\n{'Would modify' if args.dry_run else 'Modified'} {files_modified} files with {total_changes} dependency additions")

    if args.dry_run:
        print("\nRun without --dry-run to apply changes")


if __name__ == '__main__':
    main()
