#!/usr/bin/env python3
"""
OpenCog Optimal Build Summary Generator
Creates a comprehensive summary of the optimal build sequence analysis
"""

import json
import sys
from pathlib import Path


def load_reports() -> dict:
    """Load all generated analysis reports"""
    reports = {}

    files_to_load = [
        ("dependency_analysis", "dependency_analysis_report.json"),
        ("build_optimization", "build_optimization_report.json"),
    ]

    for name, filename in files_to_load:
        try:
            with open(filename) as f:
                reports[name] = json.load(f)
        except FileNotFoundError:
            print(f"Warning: {filename} not found")
            reports[name] = {}

    return reports


def generate_summary_report() -> str:
    """Generate comprehensive summary report"""
    reports = load_reports()

    lines = [
        "# OpenCog Complete Dependency Analysis & Build Optimization",
        "## Generated from Issue #85 Dependency Diagram",
        "",
        "### Executive Summary",
        "",
    ]

    # Get analysis data
    dep_analysis = reports.get("dependency_analysis", {})
    build_opt = reports.get("build_optimization", {})

    if dep_analysis:
        summary = dep_analysis.get("analysis_summary", {})
        lines.extend(
            [
                f"- **Total Components Analyzed**: {summary.get('total_components', 'N/A')}",
                f"- **Available Components**: {build_opt.get('total_available', 'N/A')}",
                f"- **External Dependencies**: {summary.get('external_dependencies', 'N/A')}",
                f"- **Critical Path Length**: {summary.get('critical_path_length', 'N/A')}",
                f"- **Parallelization Levels**: {summary.get('parallelization_levels', 'N/A')}",
                f"- **Dependency Cycles**: {'None detected' if not summary.get('has_cycles', True) else 'Found'}",
                "",
            ]
        )

    # Critical path analysis
    if dep_analysis and "build_sequence" in dep_analysis:
        critical_path = dep_analysis["build_sequence"].get("critical_path", [])
        lines.extend(
            [
                "### Critical Path Analysis",
                "",
                f"**Complete Critical Path** ({len(critical_path)} components):",
                "```",
                f"{' → '.join(critical_path)}",
                "```",
                "",
            ]
        )

        if build_opt and "critical_path" in build_opt:
            available_critical = build_opt["critical_path"]
            lines.extend(
                [
                    f"**Available Critical Path** ({len(available_critical)} components):",
                    "```",
                    f"{' → '.join(available_critical)}",
                    "```",
                    "",
                ]
            )

    # Parallelization opportunities
    if build_opt and "parallel_groups" in build_opt:
        parallel_groups = build_opt["parallel_groups"]
        lines.extend(
            [
                "### Parallelization Analysis",
                "",
            ]
        )

        max_parallel = max(len(comps) for comps in parallel_groups.values()) if parallel_groups else 0
        lines.append(f"**Maximum Parallel Jobs**: {max_parallel} components simultaneously")
        lines.append("")

        for level, components in parallel_groups.items():
            if len(components) > 1:
                lines.extend(
                    [
                        f"**Level {level}**: {len(components)} parallel builds",
                        f"- Components: {', '.join(components)}",
                        "",
                    ]
                )

    # Build phases
    if build_opt and "build_phases" in build_opt:
        phases = build_opt["build_phases"]
        lines.extend(
            [
                "### Optimized Build Phases",
                "",
            ]
        )

        for phase, components in phases.items():
            lines.extend(
                [
                    f"#### {phase}",
                    f"Components ({len(components)}): {', '.join(components)}",
                    "",
                ]
            )

    # External dependencies analysis
    if build_opt and "external_dependencies" in build_opt:
        ext_deps = build_opt["external_dependencies"]
        lines.extend(
            [
                "### External Dependencies Summary",
                "",
            ]
        )

        # Count most common external dependencies
        dep_count = {}
        for comp, deps in ext_deps.items():
            for dep in deps:
                dep_count[dep] = dep_count.get(dep, 0) + 1

        most_common = sorted(dep_count.items(), key=lambda x: x[1], reverse=True)[:10]

        lines.extend(
            [
                "**Most Common External Dependencies**:",
                "",
            ]
        )

        for dep, count in most_common:
            lines.append(f"- **{dep}**: required by {count} components")

        lines.extend(
            [
                "",
                "**Per-Component External Dependencies**:",
                "",
            ]
        )

        for comp, deps in sorted(ext_deps.items()):
            lines.append(f"- **{comp}**: {', '.join(deps)}")

        lines.append("")

    # Recommendations
    if dep_analysis and "recommendations" in dep_analysis:
        recommendations = dep_analysis["recommendations"]
        lines.extend(
            [
                "### Build Optimization Recommendations",
                "",
            ]
        )

        for rec in recommendations:
            lines.append(f"- {rec}")

        lines.extend(
            [
                "",
                "### Additional Recommendations",
                "",
                "- **Containerization**: Use Docker for reproducible builds with all dependencies",
                "- **CI/CD Pipeline**: Implement parallel builds based on dependency levels",
                "- **Build Caching**: Cache builds at component level for faster iteration",
                "- **Resource Allocation**: Allocate more build resources to critical path components",
                "- **Dependency Management**: Monitor external dependencies for security updates",
                "",
            ]
        )

    # Implementation files
    lines.extend(
        [
            "### Generated Artifacts",
            "",
            "The analysis has generated the following optimization files:",
            "",
            "1. **dependency_analysis_report.json** - Complete dependency analysis",
            "2. **build_optimization_report.json** - Available components optimization",
            "3. **OPTIMAL_BUILD_SEQUENCE.md** - Step-by-step build instructions",
            "4. **CMakeLists_available.txt** - Optimized CMake configuration",
            "5. **CMakeLists_optimized.txt** - Complete optimized CMake configuration",
            "6. **dependency_graph.png** - Visual dependency graph",
            "",
            "### Integration with Existing Build System",
            "",
            "The optimization integrates with the existing OpenCog unified build system:",
            "",
            "- Uses existing `validate-integration.py` for validation",
            "- Extends `integrate-components.sh` functionality",
            "- Compatible with current CMakeLists.txt structure",
            "- Preserves existing dependency relationships",
            "",
        ]
    )

    return "\n".join(lines)


def validate_analysis() -> bool:
    """Validate that the analysis files were generated correctly"""
    required_files = [
        "dependency_analysis_report.json",
        "build_optimization_report.json",
        "OPTIMAL_BUILD_SEQUENCE.md",
        "CMakeLists_available.txt",
        "CMakeLists_optimized.txt",
    ]

    missing_files = []
    for filename in required_files:
        if not Path(filename).exists():
            missing_files.append(filename)

    if missing_files:
        print(f"Warning: Missing files: {', '.join(missing_files)}")
        return False

    print("✅ All analysis files generated successfully")
    return True


def main():
    """Generate and display summary report"""
    print("Generating OpenCog Complete Dependency Analysis Summary...")

    # Validate files exist
    if not validate_analysis():
        print("Some analysis files are missing. Run the analysis first.")
        return 1

    # Generate summary
    summary = generate_summary_report()

    # Save summary
    with open("DEPENDENCY_ANALYSIS_SUMMARY.md", "w") as f:
        f.write(summary)

    print("Summary saved to DEPENDENCY_ANALYSIS_SUMMARY.md")

    # Display key metrics
    reports = load_reports()
    if reports.get("build_optimization"):
        build_opt = reports["build_optimization"]
        print("\n🎯 Key Results:")
        print(f"   Available Components: {build_opt.get('total_available', 'N/A')}")
        print(f"   Critical Path: {' → '.join(build_opt.get('critical_path', []))}")

        if build_opt.get("parallel_groups"):
            max_parallel = max(len(comps) for comps in build_opt["parallel_groups"].values())
            print(f"   Max Parallel Jobs: {max_parallel}")

        phases = build_opt.get("build_phases", {})
        print(f"   Build Phases: {len(phases)}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
