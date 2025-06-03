#!/bin/bash
echo "🧠 Bootstrapping Unified Cognitive Infrastructure..."

# Install necessary build tools and dependencies
sudo apt update
sudo apt install -y build-essential cmake git curl docker docker-compose

# Initialize cognitive build environment
mkdir -p build && cd build
cmake ..
make -j$(nproc)

echo "✅ Cognitive infrastructure successfully bootstrapped!"