#!/bin/bash
# Cognitive Initialization Script for Unified OpenCog Repository
# Timestamp: $(date -u +"%Y-%m-%d %H:%M:%S UTC")

REPO_NAME="opencog-unified"
echo "✨ Starting cognitive merge initialization into '$REPO_NAME'..."

# Setup unified repository
mkdir -p "$REPO_NAME"
cd "$_"
git init
echo "✔️ Initialized unified cognitive repository."

# Clone repos without history into temporary directories
git clone --depth=1 https://github.com/opencog/cogutil.git temp_cogutil
git clone --depth=1 https://github.com/opencog/atomspace.git temp_atomspace
git clone --depth=1 https://github.com/opencog/cogserver.git temp_cogserver

# Move cloned repos to structured directories
mv temp_cogutil cogutil
mv temp_atomspace atomspace
mv temp_cogserver cogserver

# Cleanup temp folders if needed
rm -rf temp_cogutil/.git temp_atomspace/.git temp_cogserver/.git

# Create additional directories for cognitive extensions
mkdir -p deps scripts docker ci chatbot-tutorial cognitive-gui

# Craft initial README.md
cat << EOF > README.md
# OpenCog Unified Cognitive Repository

## Cognitive Vision
Unified integration of OpenCog core components (\`cogutil\`, \`atomspace\`, \`cogserver\`), designed for ease of deployment, automation, and interactive neural-symbolic exploration.

## Repository Structure
\`\`\`
opencog-unified/
├── deps/                  # External dependencies (self-contained)
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

# Move cloned repos into organized directories
mv temp_cogutil cogutil
mv temp_atomspace atomspace
mv temp_cogserver cogserver

# Initialize Git and commit
git init
git add .
git commit -m "🧠 Initialized unified cognitive repository with self-contained OpenCog modules."

echo "✨ Cognitive repository is initialized and ready for recursive expansion."