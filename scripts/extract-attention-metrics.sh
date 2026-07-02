#!/bin/bash
# ECAN-style Attention Metrics Extraction Script
# Extracts and logs attention allocation metrics for cognitive resource mapping

set -e

echo "🧠 ECAN-Style Attention Metrics Extraction"
echo "=========================================="

# Initialize metrics collection
METRICS_FILE="attention-metrics.json"
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# Function to calculate attention values based on code complexity and activity
calculate_attention_value() {
    local file_path="$1"
    local file_size

    file_size=$(stat -c%s "$file_path" 2>/dev/null || echo "0")
    local lines

    lines=$(wc -l < "$file_path" 2>/dev/null || echo "0")

    # Basic attention calculation: normalized by size and complexity indicators
    local complexity_score=0

    # Increase attention for files with cognitive keywords
    if grep -q -i -E "(cognitive|attention|ecan|atomspace|hypergraph)" "$file_path" 2>/dev/null; then
        complexity_score=$((complexity_score + 50))
    fi

    # Increase attention for neural-symbolic integration points
    if grep -q -i -E "(neural|symbolic|tensor|ggml)" "$file_path" 2>/dev/null; then
        complexity_score=$((complexity_score + 30))
    fi

    # Increase attention for scheme-c++ bridge points
    if grep -q -i -E "(scheme|scm|guile)" "$file_path" 2>/dev/null; then
        complexity_score=$((complexity_score + 20))
    fi

    # Base attention from file activity (size + lines)
    local base_attention

    base_attention=$((file_size / 100 + lines))
    local total_attention

    total_attention=$((base_attention + complexity_score))

    # Normalize to 0-100 scale
    local normalized_attention

    normalized_attention=$((total_attention > 100 ? 100 : total_attention))

    echo "$normalized_attention"
}

# Function to extract cognitive workload distribution
extract_cognitive_workload() {
    echo "📊 Analyzing cognitive workload distribution..."

    local cpp_attention=0
    local scheme_attention=0
    local ggml_attention=0
    local total_files=0

    # Process C++ files
    while IFS= read -r -d '' file; do
        local attention

        attention=$(calculate_attention_value "$file")
        cpp_attention=$((cpp_attention + attention))
        total_files=$((total_files + 1))
        echo "  C++ File: $(basename "$file") -> Attention: $attention"
    done < <(find . \( -name "*.cc" -o -name "*.cpp" -o -name "*.h" -o -name "*.hpp" \) -print0 2>/dev/null)

    # Process Scheme files
    while IFS= read -r -d '' file; do
        local attention

        attention=$(calculate_attention_value "$file")
        scheme_attention=$((scheme_attention + attention))
        total_files=$((total_files + 1))
        echo "  Scheme File: $(basename "$file") -> Attention: $attention"
    done < <(find . -name "*.scm" -print0 2>/dev/null)

    # Process GGML/tensor files
    while IFS= read -r -d '' file; do
        local attention

        attention=$(calculate_attention_value "$file")
        ggml_attention=$((ggml_attention + attention))
        total_files=$((total_files + 1))
        echo "  GGML/Tensor File: $(basename "$file") -> Attention: $attention"
    done < <(find . -path "*/ggml-tensor-kernel/*" \( -name "*.cc" -o -name "*.h" \) -print0 2>/dev/null)

    # Calculate distribution percentages
    local total_attention

    total_attention=$((cpp_attention + scheme_attention + ggml_attention))

    if [[ $total_attention -gt 0 ]]; then
        local cpp_percent

        cpp_percent=$((cpp_attention * 100 / total_attention))
        local scheme_percent

        scheme_percent=$((scheme_attention * 100 / total_attention))
        local ggml_percent

        ggml_percent=$((ggml_attention * 100 / total_attention))

        echo "📈 Cognitive Workload Distribution:"
        echo "  - C++/Native Processing: ${cpp_percent}% (${cpp_attention} units)"
        echo "  - Scheme/Symbolic Logic: ${scheme_percent}% (${scheme_attention} units)"
        echo "  - GGML/Tensor Operations: ${ggml_percent}% (${ggml_attention} units)"
        echo "  - Total Files Analyzed: $total_files"
        echo "  - Total Attention Units: $total_attention"
    else
        echo "⚠️  No cognitive workload detected"
    fi

    # Export metrics for JSON output
    export CPP_ATTENTION="$cpp_attention"
    export SCHEME_ATTENTION="$scheme_attention"
    export GGML_ATTENTION="$ggml_attention"
    export TOTAL_ATTENTION="$total_attention"
    export TOTAL_FILES="$total_files"
}

# Function to detect attention hotspots
detect_attention_hotspots() {
    echo ""
    echo "🔥 Detecting Attention Hotspots..."

    local hotspots=()

    # Find files with high attention values
    while IFS= read -r -d '' file; do
        local attention

        attention=$(calculate_attention_value "$file")
        if [[ $attention -gt 70 ]]; then
            hotspots+=("$(basename "$file"):$attention")
            echo "  🌟 High-attention file: $(basename "$file") (attention: $attention)"
        fi
    done < <(find . \( -name "*.cc" -o -name "*.cpp" -o -name "*.h" -o -name "*.scm" \) -print0 2>/dev/null)

    if [[ ${#hotspots[@]} -eq 0 ]]; then
        echo "  📊 No attention hotspots detected (all files < 70 attention units)"
    fi

    # Export hotspots for JSON
    export ATTENTION_HOTSPOTS="${hotspots[*]}"
}

# Function to calculate ECAN-style urgency and importance
calculate_ecan_urgency() {
    echo ""
    echo "⚡ Calculating ECAN-style Urgency Metrics..."

    local high_urgency=0
    local medium_urgency=0
    local low_urgency=0

    # Check recent modifications (simulate urgency from activity)
    if command -v git >/dev/null 2>&1; then
        # Files modified in last day (high urgency)
        local recent_files

        recent_files=$(git diff --name-only HEAD~1 2>/dev/null | wc -l || echo "0")
        high_urgency=$((recent_files * 10))

        # Files in staging (medium urgency)
        local staged_files

        staged_files=$(git diff --cached --name-only 2>/dev/null | wc -l || echo "0")
        medium_urgency=$((staged_files * 5))

        echo "  ⚡ High Urgency (recent changes): $high_urgency units"
        echo "  ⚠️  Medium Urgency (staged changes): $medium_urgency units"
    fi

    # Base urgency from system complexity
    local complexity_files

    complexity_files=$(find . \( -name "*.cc" -o -name "*.scm" \) | wc -l)
    low_urgency=$((complexity_files * 2))
    echo "  📊 Low Urgency (base complexity): $low_urgency units"

    local total_urgency


    total_urgency=$((high_urgency + medium_urgency + low_urgency))
    echo "  🎯 Total System Urgency: $total_urgency units"

    # Export urgency metrics
    export HIGH_URGENCY="$high_urgency"
    export MEDIUM_URGENCY="$medium_urgency"
    export LOW_URGENCY="$low_urgency"
    export TOTAL_URGENCY="$total_urgency"
}

# Function to generate JSON metrics report
generate_metrics_json() {
    echo ""
    echo "📋 Generating ECAN Metrics JSON Report..."

    cat > "$METRICS_FILE" << EOF
{
  "timestamp": "$TIMESTAMP",
  "ecan_attention_metrics": {
    "cognitive_workload_distribution": {
      "cpp_attention": $CPP_ATTENTION,
      "scheme_attention": $SCHEME_ATTENTION,
      "ggml_attention": $GGML_ATTENTION,
      "total_attention": $TOTAL_ATTENTION,
      "total_files_analyzed": $TOTAL_FILES
    },
    "attention_hotspots": [
$(IFS=$'\n'; for hotspot in $ATTENTION_HOTSPOTS; do
    filename=${hotspot%%:*}
    attention=${hotspot##*:}
    echo "      {\"filename\": \"$filename\", \"attention_level\": $attention},"
done | sed '$ s/,$//')
    ],
    "urgency_metrics": {
      "high_urgency": $HIGH_URGENCY,
      "medium_urgency": $MEDIUM_URGENCY,
      "low_urgency": $LOW_URGENCY,
      "total_urgency": $TOTAL_URGENCY
    },
    "cognitive_resource_allocation": {
      "neural_symbolic_integration_score": $((SCHEME_ATTENTION + CPP_ATTENTION)),
      "tensor_processing_capability": $GGML_ATTENTION,
      "overall_cognitive_complexity": $TOTAL_ATTENTION
    }
  },
  "meta_analysis": {
    "attention_balance": "$(if [[ $CPP_ATTENTION -gt $SCHEME_ATTENTION ]]; then echo "cpp_dominant"; elif [[ $SCHEME_ATTENTION -gt $CPP_ATTENTION ]]; then echo "scheme_dominant"; else echo "balanced"; fi)",
    "system_readiness": "$(if [[ $TOTAL_ATTENTION -gt 500 ]]; then echo "high"; elif [[ $TOTAL_ATTENTION -gt 200 ]]; then echo "medium"; else echo "low"; fi)",
    "cognitive_coherence": $((TOTAL_ATTENTION / (TOTAL_FILES + 1)))
  }
}
EOF

    echo "✅ ECAN metrics saved to: $METRICS_FILE"
}

# Main execution
main() {
    echo "Starting ECAN-style attention metrics extraction at $TIMESTAMP"
    echo ""

    # Run all analysis functions
    extract_cognitive_workload
    detect_attention_hotspots
    calculate_ecan_urgency
    generate_metrics_json

    echo ""
    echo "🎉 ECAN Attention Metrics Extraction Complete!"
    echo "📊 Results summary:"
    echo "   - Total Attention Units: $TOTAL_ATTENTION"
    echo "   - Files Analyzed: $TOTAL_FILES"
    echo "   - Attention Hotspots: $(echo "$ATTENTION_HOTSPOTS" | wc -w)"
    echo "   - System Urgency: $TOTAL_URGENCY units"
    echo "   - Metrics File: $METRICS_FILE"
    echo ""
    echo "🧠 Ready for cognitive resource optimization and recursive enhancement!"
}

# Run main function
main "$@"
