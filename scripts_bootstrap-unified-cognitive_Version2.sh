#!/bin/bash
# Cognitive Bootstrap Automation for OpenCog Unified

echo "✨ Bootstrapping Unified Cognitive Environment ✨"

# Install necessary packages
sudo apt update
sudo apt install -y build-essential cmake git docker docker-compose

# Prepare build directory
mkdir -p build && cd build

# Run unified CMake build
cmake ..
make -j$(nproc)

echo "✅ Cognitive build complete!"

# Docker Compose deployment
cd ..
docker-compose build
docker-compose up -d

echo "🚀 Cognitive containers are up and running!"