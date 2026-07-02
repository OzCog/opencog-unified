#!/usr/bin/env python3
"""
Create visualizations for the TODO analysis
"""
import json

import matplotlib
import matplotlib.pyplot as plt


matplotlib.use('Agg')
from collections import defaultdict


def create_visualizations():
    """Create charts for the analysis"""

    with open('actionable_todos_analysis.json') as f:
        analysis = json.load(f)

    stats = analysis['statistics']

    # Set up the figure with subplots
    plt.figure(figsize=(16, 12))

    # 1. Component Distribution
    ax1 = plt.subplot(2, 3, 1)
    components = sorted(stats['by_component'].items(), key=lambda x: x[1], reverse=True)
    comp_names = [c[0] for c in components]
    comp_counts = [c[1] for c in components]

    ax1.barh(comp_names, comp_counts, color='steelblue')
    ax1.set_xlabel('Number of Items')
    ax1.set_title('TODO Items by Component', fontweight='bold', fontsize=12)
    ax1.grid(axis='x', alpha=0.3)

    # 2. Complexity Distribution (Pie)
    ax2 = plt.subplot(2, 3, 2)
    complexity_data = stats['by_complexity']
    colors = {'simple': '#90EE90', 'medium': '#FFD700', 'complex': '#FF6B6B'}

    _wedges, _texts, _autotexts = ax2.pie(
        complexity_data.values(),
        labels=complexity_data.keys(),
        autopct='%1.1f%%',
        colors=[colors.get(k, 'gray') for k in complexity_data],
        startangle=90
    )
    ax2.set_title('Complexity Distribution', fontweight='bold', fontsize=12)

    # 3. Work Type Distribution
    ax3 = plt.subplot(2, 3, 3)
    work_types = sorted(stats['by_type'].items(), key=lambda x: x[1], reverse=True)
    wt_names = [w[0].replace('_', ' ').title() for w in work_types]
    wt_counts = [w[1] for w in work_types]

    ax3.barh(wt_names, wt_counts, color='coral')
    ax3.set_xlabel('Number of Items')
    ax3.set_title('TODO Items by Work Type', fontweight='bold', fontsize=12)
    ax3.grid(axis='x', alpha=0.3)

    # 4. Time Estimate Distribution
    ax4 = plt.subplot(2, 3, 4)
    time_order = ['30min-1hr', '1-2hrs', '2-4hrs', '4-8hrs', '8-16hrs', '1-3days', '2-5days', '3-7days']
    time_data = {k: stats['by_time'].get(k, 0) for k in time_order}

    ax4.bar(range(len(time_data)), time_data.values(), color='mediumpurple')
    ax4.set_xticks(range(len(time_data)))
    ax4.set_xticklabels(time_data.keys(), rotation=45, ha='right')
    ax4.set_ylabel('Number of Items')
    ax4.set_title('Time Estimate Distribution', fontweight='bold', fontsize=12)
    ax4.grid(axis='y', alpha=0.3)

    # 5. Component vs Complexity Heatmap
    ax5 = plt.subplot(2, 3, 5)

    # Build heatmap data
    components_list = sorted(stats['by_component'].keys(),
                            key=lambda x: stats['by_component'][x], reverse=True)
    complexity_list = ['simple', 'medium', 'complex']

    heatmap_data = []
    for component in components_list:
        row = []
        comp_items = analysis['by_component'][component]
        for complexity in complexity_list:
            count = sum(1 for item in comp_items if item['complexity'] == complexity)
            row.append(count)
        heatmap_data.append(row)

    im = ax5.imshow(heatmap_data, cmap='YlOrRd', aspect='auto')
    ax5.set_xticks(range(len(complexity_list)))
    ax5.set_xticklabels(complexity_list)
    ax5.set_yticks(range(len(components_list)))
    ax5.set_yticklabels(components_list)
    ax5.set_title('Component vs Complexity', fontweight='bold', fontsize=12)

    # Add text annotations
    for i in range(len(components_list)):
        for j in range(len(complexity_list)):
            ax5.text(j, i, heatmap_data[i][j],
                          ha="center", va="center", color="black", fontsize=9)

    plt.colorbar(im, ax=ax5)

    # 6. Summary Statistics
    ax6 = plt.subplot(2, 3, 6)
    ax6.axis('off')

    summary_text = f"""
SUMMARY STATISTICS

Total Actionable Items: {stats['total_items']}

Quick Wins (≤2hrs): {stats['by_time'].get('30min-1hr', 0) + stats['by_time'].get('1-2hrs', 0)}
Medium Effort (2-8hrs): {stats['by_time'].get('2-4hrs', 0) + stats['by_time'].get('4-8hrs', 0)}
High Effort (8hrs+): {stats['by_time'].get('8-16hrs', 0) + sum(v for k, v in stats['by_time'].items() if 'day' in k)}

Top Components:
  1. MOSES: {stats['by_component'].get('moses', 0)} items
  2. NLP: {stats['by_component'].get('nlp', 0)} items
  3. Chatbot: {stats['by_component'].get('chatbot', 0)} items

Work Type Breakdown:
  Bug Fixes: {stats['by_type'].get('bug_fix', 0)}
  Incomplete: {stats['by_type'].get('incomplete_implementation', 0)}
  Features: {stats['by_type'].get('feature_addition', 0)}
  Enhancements: {stats['by_type'].get('enhancement', 0)}
"""

    ax6.text(0.1, 0.9, summary_text, transform=ax6.transAxes,
            fontsize=11, verticalalignment='top', fontfamily='monospace',
            bbox={'boxstyle': 'round', 'facecolor': 'wheat', 'alpha': 0.3})

    plt.tight_layout()
    plt.savefig('actionable_todos_analysis.png', dpi=150, bbox_inches='tight')
    print("Visualization saved to actionable_todos_analysis.png")

    # Create a second figure for priority breakdown
    _fig2, axes = plt.subplots(2, 2, figsize=(14, 10))

    items = analysis['analyzed_items']

    # Quick wins by component
    ax = axes[0, 0]
    quick_wins = [item for item in items if item['time_estimate'] in ['30min-1hr', '1-2hrs']]
    qw_by_comp = defaultdict(int)
    for item in quick_wins:
        qw_by_comp[item['component']] += 1

    if qw_by_comp:
        ax.bar(qw_by_comp.keys(), qw_by_comp.values(), color='lightgreen')
        ax.set_ylabel('Number of Items')
        ax.set_title('Quick Wins by Component (≤2hrs)', fontweight='bold')
        ax.tick_params(axis='x', rotation=45)
        ax.grid(axis='y', alpha=0.3)

    # Bug fixes by component
    ax = axes[0, 1]
    bug_fixes = [item for item in items if item['work_type'] == 'bug_fix']
    bf_by_comp = defaultdict(int)
    for item in bug_fixes:
        bf_by_comp[item['component']] += 1

    ax.bar(bf_by_comp.keys(), bf_by_comp.values(), color='lightcoral')
    ax.set_ylabel('Number of Items')
    ax.set_title('Bug Fixes by Component', fontweight='bold')
    ax.tick_params(axis='x', rotation=45)
    ax.grid(axis='y', alpha=0.3)

    # Feature additions by component
    ax = axes[1, 0]
    features = [item for item in items if item['work_type'] == 'feature_addition']
    feat_by_comp = defaultdict(int)
    for item in features:
        feat_by_comp[item['component']] += 1

    if feat_by_comp:
        ax.bar(feat_by_comp.keys(), feat_by_comp.values(), color='skyblue')
        ax.set_ylabel('Number of Items')
        ax.set_title('Feature Additions by Component', fontweight='bold')
        ax.tick_params(axis='x', rotation=45)
        ax.grid(axis='y', alpha=0.3)

    # Effort distribution by component (stacked bar)
    ax = axes[1, 1]

    effort_categories = {
        'Quick (≤2hrs)': ['30min-1hr', '1-2hrs'],
        'Medium (2-8hrs)': ['2-4hrs', '4-8hrs'],
        'High (8hrs+)': ['8-16hrs', '1-3days', '2-5days', '3-7days']
    }

    comp_effort = defaultdict(lambda: defaultdict(int))
    for item in items:
        comp = item['component']
        for cat_name, time_vals in effort_categories.items():
            if item['time_estimate'] in time_vals:
                comp_effort[comp][cat_name] += 1

    components_sorted = sorted(comp_effort.keys(),
                               key=lambda x: sum(comp_effort[x].values()),
                               reverse=True)[:8]

    bottoms = [0] * len(components_sorted)
    colors_effort = ['#90EE90', '#FFD700', '#FF6B6B']

    for i, (cat_name, color) in enumerate(zip(effort_categories.keys(), colors_effort, strict=False)):
        values = [comp_effort[comp][cat_name] for comp in components_sorted]
        ax.bar(components_sorted, values, bottom=bottoms, label=cat_name, color=color)
        bottoms = [b + v for b, v in zip(bottoms, values, strict=False)]

    ax.set_ylabel('Number of Items')
    ax.set_title('Effort Distribution by Component', fontweight='bold')
    ax.tick_params(axis='x', rotation=45)
    ax.legend()
    ax.grid(axis='y', alpha=0.3)

    plt.tight_layout()
    plt.savefig('priority_breakdown.png', dpi=150, bbox_inches='tight')
    print("Priority breakdown saved to priority_breakdown.png")

if __name__ == '__main__':
    create_visualizations()
