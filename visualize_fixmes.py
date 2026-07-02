#!/usr/bin/env python3
"""
Create visualizations for C++ FIXME analysis
"""

import json

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt


# Load the detailed analysis
with open('cpp_fixme_detailed_analysis.json') as f:
    data = json.load(f)

# Create a figure with multiple subplots
fig = plt.figure(figsize=(16, 10))
fig.suptitle('C++ FIXME Analysis Dashboard', fontsize=20, fontweight='bold')

# 1. Severity Distribution (Pie Chart)
ax1 = plt.subplot(2, 3, 1)
severities = ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']
counts = [data['summary'][s.lower()] for s in severities]
colors = ['#d32f2f', '#f57c00', '#fbc02d', '#388e3c']
explode = (0.1, 0.05, 0, 0)

ax1.pie(counts, labels=severities, autopct='%1.1f%%', startangle=90,
        colors=colors, explode=explode, shadow=True)
ax1.set_title('Severity Distribution', fontweight='bold', fontsize=12)

# 2. Module Distribution (Horizontal Bar Chart)
ax2 = plt.subplot(2, 3, 2)
modules = list(data['module_summary'].keys())
module_counts = [sum(data['module_summary'][m].values()) for m in modules]

# Sort by count
sorted_data = sorted(zip(modules, module_counts, strict=False), key=lambda x: x[1], reverse=True)
modules_sorted, counts_sorted = zip(*sorted_data, strict=False)

y_pos = range(len(modules_sorted))
ax2.barh(y_pos, counts_sorted, color='#1976d2')
ax2.set_yticks(y_pos)
ax2.set_yticklabels(modules_sorted)
ax2.invert_yaxis()
ax2.set_xlabel('Number of FIXMEs')
ax2.set_title('FIXMEs by Module', fontweight='bold', fontsize=12)
ax2.grid(axis='x', alpha=0.3)

# Add count labels
for i, v in enumerate(counts_sorted):
    ax2.text(v + 0.5, i, str(v), va='center')

# 3. Category Distribution (Bar Chart)
ax3 = plt.subplot(2, 3, 3)
categories = list(data['category_summary'].keys())
cat_counts = [data['category_summary'][c] for c in categories]

# Sort by count
sorted_cat = sorted(zip(categories, cat_counts, strict=False), key=lambda x: x[1], reverse=True)
categories_sorted, cat_counts_sorted = zip(*sorted_cat, strict=False)

ax3.bar(range(len(categories_sorted)), cat_counts_sorted, color='#7b1fa2')
ax3.set_xticks(range(len(categories_sorted)))
ax3.set_xticklabels(categories_sorted, rotation=45, ha='right')
ax3.set_ylabel('Count')
ax3.set_title('FIXMEs by Category', fontweight='bold', fontsize=12)
ax3.grid(axis='y', alpha=0.3)

# 4. Module Severity Breakdown (Stacked Bar Chart)
ax4 = plt.subplot(2, 3, 4)
modules_for_stack = [m for m in modules_sorted if sum(data['module_summary'][m].values()) > 0]
critical_counts = [data['module_summary'][m]['critical'] for m in modules_for_stack]
high_counts = [data['module_summary'][m]['high'] for m in modules_for_stack]
medium_counts = [data['module_summary'][m]['medium'] for m in modules_for_stack]
low_counts = [data['module_summary'][m]['low'] for m in modules_for_stack]

x_pos = range(len(modules_for_stack))
width = 0.6

p1 = ax4.bar(x_pos, critical_counts, width, label='Critical', color='#d32f2f')
p2 = ax4.bar(x_pos, high_counts, width, bottom=critical_counts, label='High', color='#f57c00')
p3 = ax4.bar(x_pos, medium_counts, width,
             bottom=[i+j for i,j in zip(critical_counts, high_counts, strict=False)],
             label='Medium', color='#fbc02d')
p4 = ax4.bar(x_pos, low_counts, width,
             bottom=[i+j+k for i,j,k in zip(critical_counts, high_counts, medium_counts, strict=False)],
             label='Low', color='#388e3c')

ax4.set_xticks(x_pos)
ax4.set_xticklabels(modules_for_stack, rotation=45, ha='right')
ax4.set_ylabel('Count')
ax4.set_title('Module Severity Breakdown', fontweight='bold', fontsize=12)
ax4.legend(loc='upper right')
ax4.grid(axis='y', alpha=0.3)

# 5. Priority Summary (Text Box)
ax5 = plt.subplot(2, 3, 5)
ax5.axis('off')

summary_text = f"""
PRIORITY SUMMARY

Total FIXMEs: {data['total']}

CRITICAL: {data['summary']['critical']}
  • Security vulnerabilities
  • Crash risks
  • Immediate action required

HIGH: {data['summary']['high']}
  • Thread safety issues
  • Exception handling
  • Performance bottlenecks

MEDIUM: {data['summary']['medium']}
  • Incomplete features
  • Code quality issues
  • API design improvements

LOW: {data['summary']['low']}
  • Documentation
  • General improvements
"""

ax5.text(0.1, 0.9, summary_text, transform=ax5.transAxes,
         fontsize=10, verticalalignment='top', fontfamily='monospace',
         bbox={'boxstyle': 'round', 'facecolor': 'wheat', 'alpha': 0.3})

# 6. Top Issues Table
ax6 = plt.subplot(2, 3, 6)
ax6.axis('off')

top_issues_text = """
TOP PRIORITY ITEMS

1. TypeChoice.cc (CRITICAL)
   Exception suppression → undefined behavior

2. ValueSexpr.cc (CRITICAL)
   Input parsing vulnerability

3. TypeUtils.cc (HIGH)
   Should throw exception

4. AtomSpace.cc (HIGH)
   Recursive depth() bottleneck

5. CogServer.cc (HIGH)
   Spinning loop → use semaphore
"""

ax6.text(0.1, 0.9, top_issues_text, transform=ax6.transAxes,
         fontsize=10, verticalalignment='top', fontfamily='monospace',
         bbox={'boxstyle': 'round', 'facecolor': 'lightblue', 'alpha': 0.3})

plt.tight_layout()
plt.savefig('cpp_fixme_analysis_dashboard.png', dpi=300, bbox_inches='tight')
print("Dashboard saved to: cpp_fixme_analysis_dashboard.png")

# Create a second figure for the roadmap timeline
fig2, ax = plt.subplots(figsize=(14, 8))

# Define phases
phases = [
    {'name': 'Phase 1: Critical Issues', 'start': 0, 'duration': 1, 'color': '#d32f2f', 'items': 2},
    {'name': 'Phase 2: High Priority\n(Exception Handling)', 'start': 1, 'duration': 1, 'color': '#f57c00', 'items': 5},
    {'name': 'Phase 2: High Priority\n(Thread Safety & Perf)', 'start': 2, 'duration': 1, 'color': '#f57c00', 'items': 5},
    {'name': 'Phase 3: Storage Operations', 'start': 3, 'duration': 1, 'color': '#fbc02d', 'items': 8},
    {'name': 'Phase 3: Type System', 'start': 4, 'duration': 1, 'color': '#fbc02d', 'items': 8},
    {'name': 'Phase 3: Language Learning', 'start': 5, 'duration': 1, 'color': '#fbc02d', 'items': 8},
    {'name': 'Phase 3: MOSES', 'start': 6, 'duration': 1, 'color': '#fbc02d', 'items': 8},
    {'name': 'Phase 3: Refactoring', 'start': 7, 'duration': 1, 'color': '#fbc02d', 'items': 7},
]

# Draw timeline
for i, phase in enumerate(phases):
    ax.barh(i, phase['duration'], left=phase['start'], height=0.6,
            color=phase['color'], alpha=0.7, edgecolor='black', linewidth=1.5)

    # Add phase name
    ax.text(phase['start'] + phase['duration']/2, i,
            f"{phase['name']}\n({phase['items']} items)",
            ha='center', va='center', fontsize=9, fontweight='bold', color='white')

# Formatting
ax.set_yticks(range(len(phases)))
ax.set_yticklabels([])
ax.set_xlabel('Weeks', fontsize=12, fontweight='bold')
ax.set_title('C++ FIXME Resolution Roadmap', fontsize=16, fontweight='bold', pad=20)
ax.set_xlim(-0.5, 8.5)
ax.grid(axis='x', alpha=0.3, linestyle='--')

# Add legend
critical_patch = mpatches.Patch(color='#d32f2f', label='Critical (Week 1)')
high_patch = mpatches.Patch(color='#f57c00', label='High Priority (Weeks 2-3)')
medium_patch = mpatches.Patch(color='#fbc02d', label='Medium Priority (Weeks 4-8)')
ax.legend(handles=[critical_patch, high_patch, medium_patch], loc='upper right', fontsize=10)

# Add week markers
for week in range(9):
    ax.axvline(x=week, color='gray', linestyle=':', alpha=0.5)
    ax.text(week, -0.8, f'Week {week}', ha='center', fontsize=9)

plt.tight_layout()
plt.savefig('cpp_fixme_roadmap.png', dpi=300, bbox_inches='tight')
print("Roadmap saved to: cpp_fixme_roadmap.png")

print("\nVisualization complete!")
