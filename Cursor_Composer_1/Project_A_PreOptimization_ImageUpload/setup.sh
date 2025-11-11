#!/bin/bash
# Setup script for Project A - Pre-Optimization Image Upload

echo "Setting up Project A - Pre-Optimization Image Upload..."

# Create necessary directories
mkdir -p uploads
mkdir -p logs
mkdir -p performance
mkdir -p data

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

echo "Setup complete for Project A!"

