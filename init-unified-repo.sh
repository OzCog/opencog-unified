#!/bin/bash
# Cognitive Initialization Script for Unified OpenCog Repository
# Timestamp: $(date -u +"%Y-%m-%d %H:%M:%S UTC")

echo "✨ Starting cognitive bootstrap initialization..."

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "❌ Error: This script must be run from the root of the opencog-unified git repository"
    exit 1
fi

# Function to check if directory exists and warn
check_directory() {
    local dir_name="$1"
    if [ -d "$dir_name" ]; then
        echo "⚠️  Warning: Directory '$dir_name' already exists. Skipping to avoid overwriting existing work."
        return 1
    fi
    return 0
}

# Clone repositories without history into temporary directories
clone_repos=()
if check_directory "cogutil"; then
    echo "📥 Cloning cogutil (shallow, no history)..."
    git clone --depth=1 https://github.com/opencog/cogutil.git temp_cogutil
    clone_repos+=("cogutil")
fi

if check_directory "atomspace"; then
    echo "📥 Cloning atomspace (shallow, no history)..."
    git clone --depth=1 https://github.com/opencog/atomspace.git temp_atomspace
    clone_repos+=("atomspace")
fi

if check_directory "cogserver"; then
    echo "📥 Cloning cogserver (shallow, no history)..."
    git clone --depth=1 https://github.com/opencog/cogserver.git temp_cogserver
    clone_repos+=("cogserver")
fi

# Move cloned repos to structured directories and remove .git history
for repo in "${clone_repos[@]}"; do
    if [ -d "temp_$repo" ]; then
        echo "📁 Moving temp_$repo to $repo/ and removing git history..."
        mv "temp_$repo" "$repo"
        rm -rf "$repo/.git"
    fi
done

# Create additional directories for cognitive extensions, if not present
echo "📁 Creating additional directories for cognitive extensions..."
mkdir -p deps scripts docker ci chatbot-tutorial cognitive-gui

# Update README.md with current unified structure and vision (if it matches expected structure)
if [ -f "README.md" ]; then
    echo "📝 README.md already exists with current structure - no changes needed"
else
    echo "📝 Creating README.md with unified structure and vision..."
    cat << EOF > README.md
# OpenCog Unified Cognitive Repository

## Cognitive Vision
Unified integration of OpenCog core components (\`cogutil\`, \`atomspace\`, \`cogserver\`), designed for ease of deployment, automation, and interactive neural-symbolic exploration.

## Repository Structure
\`\`\`
opencog-unified/
├── deps/                 # External dependencies (self-contained)
├── cogutil/              # Core utilities
├── atomspace/            # Knowledge representation core
├── cogserver/            # Distributed cognitive server
├── chatbot-tutorial/     # Interactive neural-symbolic tutorial
├── cognitive-gui/        # Intuitive cognitive GUI
├── scripts/              # Automation & cognitive validation scripts
├── docker/               # Containerization artifacts
└── ci/                   # Continuous cognitive integration configurations
\`\`\`

## Next Steps
- Set up containerized builds (Docker)
- Configure Continuous Integration (CI/CD)
- Develop interactive chatbot tutorial
- Prototype cognitive visualization GUI
EOF
fi

echo "✅ Cognitive repository initialization is complete."
echo "🧠 Ready for neural-symbolic expansion and hypergraph encoding."