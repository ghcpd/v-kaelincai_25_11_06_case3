#!/bin/bash
# Setup script for Project B - Post-Optimization Image Upload

echo "Setting up Project B - Post-Optimization Image Upload..."

# Create necessary directories
mkdir -p uploads
mkdir -p logs
mkdir -p performance
mkdir -p data

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

echo "Setup complete for Project B!"

