#!/usr/bin/env python3
"""
Generate a comprehensive sorted FIXME catalog by difficulty
"""

import json
from collections import defaultdict


def generate_fixme_catalog():
    """Generate the sorted FIXME catalog markdown document."""

    # Load the analysis report
    with open("fixme_analysis_report.json") as f:
        data = json.load(f)

    markdown_content = """# OpenCog Unified FIXME Implementation Catalog

## Executive Summary

This document provides a comprehensive categorization of all **{total_instances} FIXME instances** found in the OpenCog Unified repository, sorted by implementation difficulty to guide development priorities and resource allocation.

### Summary Statistics

| Difficulty Level | Count | Percentage | Estimated Total Effort |
|-----------------|-------|------------|------------------------|
| **VERY_HARD** | {very_hard_count} | {very_hard_pct:.1f}% | 6-18 months |
| **HARD** | {hard_count} | {hard_pct:.1f}% | 2-8 months |
| **MEDIUM** | {medium_count} | {medium_pct:.1f}% | 3-12 months |
| **EASY** | {easy_count} | {easy_pct:.1f}% | 1-4 weeks |

**Total files affected**: {files_affected}

---

## Implementation Priority Recommendations

### 🔥 Critical Priority (VERY_HARD)
These items require specialized expertise and significant architectural work. Consider outsourcing to domain experts or dedicating senior developers full-time.

### ⚡ High Priority (HARD)
These items impact core functionality, performance, and reliability. Should be addressed by experienced developers with relevant domain knowledge.

### 📋 Medium Priority (MEDIUM)
Standard implementation work that can be distributed among team members based on component expertise.

### ✅ Easy Wins (EASY)
Quick fixes suitable for new contributors or as warm-up tasks.

---

""".format(
        total_instances=data["summary"]["total_instances"],
        very_hard_count=data["summary"]["by_difficulty"].get("VERY_HARD", 0),
        hard_count=data["summary"]["by_difficulty"].get("HARD", 0),
        medium_count=data["summary"]["by_difficulty"].get("MEDIUM", 0),
        easy_count=data["summary"]["by_difficulty"].get("EASY", 0),
        very_hard_pct=(data["summary"]["by_difficulty"].get("VERY_HARD", 0) / data["summary"]["total_instances"] * 100),
        hard_pct=(data["summary"]["by_difficulty"].get("HARD", 0) / data["summary"]["total_instances"] * 100),
        medium_pct=(data["summary"]["by_difficulty"].get("MEDIUM", 0) / data["summary"]["total_instances"] * 100),
        easy_pct=(data["summary"]["by_difficulty"].get("EASY", 0) / data["summary"]["total_instances"] * 100),
        files_affected=data["summary"]["files_affected"],
    )

    # Process each difficulty level
    difficulty_order = ["VERY_HARD", "HARD", "MEDIUM", "EASY"]
    difficulty_icons = {"VERY_HARD": "🚨", "HARD": "⚡", "MEDIUM": "📋", "EASY": "✅"}

    for difficulty in difficulty_order:
        if difficulty not in data["by_difficulty"]:
            continue

        instances = data["by_difficulty"][difficulty]
        icon = difficulty_icons[difficulty]

        markdown_content += f"\n## {icon} {difficulty.replace('_', ' ').title()} Priority ({len(instances)} items)\n\n"

        # Group by component/category for better organization
        by_component = defaultdict(list)
        for instance in instances:
            component = instance["file_path"].split("/")[0]
            by_component[component].append(instance)

        for component, comp_instances in sorted(by_component.items()):
            markdown_content += f"### {component.title()} Component ({len(comp_instances)} items)\n\n"

            for i, instance in enumerate(comp_instances, 1):
                markdown_content += format_instance(instance, i)

            markdown_content += "\n"

    # Add implementation guidance
    markdown_content += """
---

## Implementation Guidance

### VERY_HARD Items - Specialized Expertise Required

**Characteristics:**
- Distributed systems algorithms
- Research-level computational problems
- Exponential complexity algorithms
- Byzantine fault tolerance
- Consensus mechanisms

**Recommended Approach:**
- Consult academic literature and research papers
- Consider collaboration with research institutions
- Prototype and test extensively before production
- May require months of dedicated research and development

### HARD Items - Senior Developer Focus

**Characteristics:**
- Thread safety and concurrency issues
- Performance-critical algorithms
- Complex recursive implementations
- Memory management optimizations

**Recommended Approach:**
- Assign to senior developers with domain expertise
- Implement comprehensive unit and integration tests
- Use static analysis tools (ThreadSanitizer, Valgrind)
- Code review by multiple senior developers

### MEDIUM Items - Standard Development Work

**Characteristics:**
- Feature implementations
- Algorithm completions
- Stub replacements
- API enhancements

**Recommended Approach:**
- Can be distributed among team members
- Follow standard development workflows
- Implement with appropriate test coverage
- Regular code review process

### EASY Items - Entry-level Tasks

**Characteristics:**
- Documentation updates
- Comment improvements
- Simple code cleanups
- Minor feature additions

**Recommended Approach:**
- Suitable for new contributors
- Good for onboarding and learning codebase
- Can be completed in parallel with other work

---

## Component Analysis

"""

    # Add component breakdown
    by_component_stats = defaultdict(lambda: defaultdict(int))
    for difficulty, instances in data["by_difficulty"].items():
        for instance in instances:
            component = instance["file_path"].split("/")[0]
            by_component_stats[component][difficulty] += 1

    markdown_content += "| Component | VERY_HARD | HARD | MEDIUM | EASY | Total |\n"
    markdown_content += "|-----------|-----------|------|--------|------|-------|\n"

    for component in sorted(by_component_stats.keys()):
        stats = by_component_stats[component]
        total = sum(stats.values())
        markdown_content += f"| {component} | {stats['VERY_HARD']} | {stats['HARD']} | {stats['MEDIUM']} | {stats['EASY']} | {total} |\n"

    markdown_content += """
---

## Next Steps

1. **Immediate Actions** (Next 2 weeks)
   - Begin with EASY items to build momentum
   - Identify domain experts for VERY_HARD items
   - Set up development environment and testing infrastructure

2. **Short Term** (1-3 months)
   - Complete all EASY items
   - Begin systematic work on MEDIUM items
   - Research and plan approach for HARD items

3. **Medium Term** (3-12 months)
   - Complete MEDIUM and HARD items
   - Begin prototyping solutions for VERY_HARD items
   - Establish partnerships for specialized expertise

4. **Long Term** (12+ months)
   - Complete all FIXME items
   - Establish maintenance practices to prevent accumulation
   - Create contributor guidelines for high-quality code

---

*This catalog was generated automatically by analyzing {total_instances} FIXME instances across {files_affected} files in the OpenCog Unified repository.*
""".format(total_instances=data["summary"]["total_instances"], files_affected=data["summary"]["files_affected"])

    return markdown_content


def format_instance(instance, index):
    """Format a single FIXME instance for the markdown document."""

    # Truncate long FIXME text
    fixme_text = instance["fixme_text"]
    if len(fixme_text) > 100:
        fixme_text = fixme_text[:97] + "..."

    # Clean up the FIXME text for display
    fixme_display = fixme_text.replace("// ", "").replace("/// ", "").replace("; ", "").replace("# ", "").strip()

    return f"""
**{index}.** `{instance["file_path"]}:{instance["line_number"]}`

**Issue:** {fixme_display}

**Category:** {instance["category"]}
**Effort:** {instance["estimated_effort"]}
**Reasoning:** {instance["reasoning"]}

<details>
<summary>View Code Context</summary>

```
{chr(10).join(instance["context_lines"])}
```
</details>

"""


def main():
    catalog_content = generate_fixme_catalog()

    with open("FIXME-SORTED-CATALOG.md", "w") as f:
        f.write(catalog_content)

    print("Generated FIXME-SORTED-CATALOG.md")
    print("Document contains comprehensive categorization of all FIXME instances")


if __name__ == "__main__":
    main()
