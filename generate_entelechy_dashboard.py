#!/usr/bin/env python3
"""
Generate visual summary charts for entelechy introspection
"""

import json

import matplotlib.pyplot as plt


def create_entelechy_dashboard():
    """Create comprehensive dashboard of introspection results"""

    # Load data
    with open("entelechy_introspection.json") as f:
        entelechy_data = json.load(f)

    with open("fragmentations.json") as f:
        frag_data = json.load(f)

    # Create figure with subplots
    fig = plt.figure(figsize=(16, 12))
    fig.suptitle("OpenCog Unified Entelechy Introspection Dashboard", fontsize=16, fontweight="bold")

    # 1. Entelechy Assessment Radar Chart
    ax1 = plt.subplot(2, 3, 1, projection="polar")
    create_entelechy_radar(ax1, entelechy_data)

    # 2. Component Completeness
    ax2 = plt.subplot(2, 3, 2)
    create_component_health(ax2, entelechy_data)

    # 3. Fragmentation by Severity
    ax3 = plt.subplot(2, 3, 3)
    create_severity_distribution(ax3, frag_data)

    # 4. Top Fragmented Components
    ax4 = plt.subplot(2, 3, 4)
    create_top_fragmented(ax4, frag_data)

    # 5. Dimensional Analysis
    ax5 = plt.subplot(2, 3, 5)
    create_dimensional_scores(ax5, entelechy_data)

    # 6. Code Health Metrics
    ax6 = plt.subplot(2, 3, 6)
    create_code_health(ax6, entelechy_data)

    plt.tight_layout(rect=[0, 0.03, 1, 0.97])
    plt.savefig("entelechy_dashboard.png", dpi=300, bbox_inches="tight")
    print("✅ Generated: entelechy_dashboard.png")

    plt.close()


def create_entelechy_radar(ax, data):
    """Create radar chart for entelechy metrics"""
    categories = ["Actualization", "Completeness", "Coherence", "Vitality", "Alignment"]
    values = [
        data["entelechy_assessment"]["actualization_score"],
        data["entelechy_assessment"]["completeness_score"],
        data["entelechy_assessment"]["coherence_score"],
        data["entelechy_assessment"]["vitality_score"],
        data["entelechy_assessment"]["alignment_score"],
    ]

    # Number of variables
    N = len(categories)
    angles = [n / float(N) * 2 * 3.14159 for n in range(N)]
    values += values[:1]  # Complete the circle
    angles += angles[:1]

    ax.plot(angles, values, "o-", linewidth=2, color="#2E86AB")
    ax.fill(angles, values, alpha=0.25, color="#2E86AB")
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, size=9)
    ax.set_ylim(0, 1)
    ax.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])
    ax.set_yticklabels(["20%", "40%", "60%", "80%", "100%"], size=7)
    ax.set_title("Entelechy Assessment", fontweight="bold", pad=20)
    ax.grid(True)


def create_component_health(ax, data):
    """Create bar chart of component layer health"""
    layers = ["Foundation", "Core", "Logic", "Cognitive", "Advanced", "Learning", "Language", "Integration"]
    health = [
        data["dimensional_insights"]["ontological"]["foundation_layer"]["health"],
        data["dimensional_insights"]["ontological"]["core_layer"]["health"],
        data["dimensional_insights"]["ontological"]["specialized_layers"]["logic"]["health"],
        data["dimensional_insights"]["ontological"]["specialized_layers"]["cognitive"]["health"],
        data["dimensional_insights"]["ontological"]["specialized_layers"]["advanced"]["health"],
        data["dimensional_insights"]["ontological"]["specialized_layers"]["learning"]["health"],
        data["dimensional_insights"]["ontological"]["specialized_layers"]["language"]["health"],
        data["dimensional_insights"]["ontological"]["specialized_layers"]["integration"]["health"],
    ]

    colors = ["#06A77D" if h >= 0.8 else "#F77F00" if h >= 0.6 else "#D62828" for h in health]

    ax.barh(layers, health, color=colors)
    ax.set_xlim(0, 1.1)
    ax.set_xlabel("Health Score")
    ax.set_title("Component Layer Health", fontweight="bold")
    ax.axvline(x=0.8, color="green", linestyle="--", alpha=0.3, linewidth=1)
    ax.axvline(x=0.6, color="orange", linestyle="--", alpha=0.3, linewidth=1)

    for i, (_layer, h) in enumerate(zip(layers, health, strict=False)):
        ax.text(h + 0.02, i, f"{h:.0%}", va="center", fontsize=9)


def create_severity_distribution(ax, data):
    """Create pie chart of fragmentation severity"""
    levels = data["by_severity"]
    sizes = [len(levels["critical"]), len(levels["high"]), len(levels["medium"]), len(levels["low"])]
    labels = [f"Critical\n({sizes[0]})", f"High\n({sizes[1]})", f"Medium\n({sizes[2]})", f"Low\n({sizes[3]})"]
    colors = ["#D62828", "#F77F00", "#FCBF49", "#06A77D"]

    _wedges, texts, autotexts = ax.pie(sizes, labels=labels, colors=colors, autopct="%1.1f%%", startangle=90)

    for text in texts:
        text.set_fontsize(9)
    for autotext in autotexts:
        autotext.set_color("white")
        autotext.set_fontweight("bold")
        autotext.set_fontsize(9)

    ax.set_title("Fragmentation by Severity", fontweight="bold")


def create_top_fragmented(ax, data):
    """Create horizontal bar chart of top fragmented components"""
    top_comps = data["top_fragmented_components"][:8]
    components = [c["component"][:20] for c in top_comps]  # Truncate long names
    counts = [c["fragment_count"] for c in top_comps]

    colors = ["#2E86AB"] * len(components)

    ax.barh(components, counts, color=colors)
    ax.set_xlabel("Fragment Count")
    ax.set_title("Most Fragmented Components", fontweight="bold")
    ax.invert_yaxis()

    for i, count in enumerate(counts):
        ax.text(count + 5, i, str(count), va="center", fontsize=9)


def create_dimensional_scores(ax, data):
    """Create bar chart of dimensional analysis scores"""
    dimensions = [
        "Ontological\n(Being)",
        "Teleological\n(Purpose)",
        "Cognitive\n(Cognition)",
        "Integrative\n(Integration)",
        "Evolutionary\n(Growth)",
    ]

    scores = [
        data["dimensional_insights"]["ontological"]["architectural_completeness"],
        data["dimensional_insights"]["teleological"]["actualization_trajectory"],
        data["dimensional_insights"]["cognitive"]["cognitive_completeness"],
        data["dimensional_insights"]["integrative"]["integration_health"],
        data["dimensional_insights"]["evolutionary"]["evolutionary_potential"],
    ]

    # Normalize to 0-1 scale
    scores = [min(s, 1.0) for s in scores]

    colors = ["#06A77D" if s >= 0.8 else "#F77F00" if s >= 0.6 else "#D62828" for s in scores]

    ax.bar(range(len(dimensions)), scores, color=colors)
    ax.set_xticks(range(len(dimensions)))
    ax.set_xticklabels(dimensions, fontsize=8)
    ax.set_ylim(0, 1.1)
    ax.set_ylabel("Score")
    ax.set_title("Multi-Dimensional Analysis", fontweight="bold")
    ax.axhline(y=0.8, color="green", linestyle="--", alpha=0.3, linewidth=1)
    ax.axhline(y=0.6, color="orange", linestyle="--", alpha=0.3, linewidth=1)

    for i, score in enumerate(scores):
        ax.text(i, score + 0.03, f"{score:.0%}", ha="center", fontsize=9)


def create_code_health(ax, data):
    """Create stacked bar chart of code markers"""
    categories = ["TODO", "FIXME", "STUB"]
    counts = [
        data["metrics"]["todo_count"],
        data["metrics"]["fixme_count"],
        data["metrics"]["stub_count"],
    ]

    colors = ["#F77F00", "#D62828", "#9B2226"]

    ax.bar(categories, counts, color=colors)
    ax.set_ylabel("Marker Count")
    ax.set_title("Code Health Markers", fontweight="bold")

    for i, count in enumerate(counts):
        ax.text(i, count + 30, str(count), ha="center", fontsize=10, fontweight="bold")

    total = sum(counts)
    ax.text(
        0.5,
        max(counts) * 0.8,
        f"Total: {total}",
        transform=ax.transAxes,
        ha="center",
        fontsize=12,
        bbox={"boxstyle": "round", "facecolor": "wheat", "alpha": 0.5},
    )


if __name__ == "__main__":
    print("📊 Generating Entelechy Dashboard...")
    create_entelechy_dashboard()
    print("✅ Dashboard generation complete!")
