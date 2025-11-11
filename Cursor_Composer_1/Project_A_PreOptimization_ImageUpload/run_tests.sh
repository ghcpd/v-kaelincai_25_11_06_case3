#!/bin/bash
# Run tests for Project A - Pre-Optimization Image Upload

echo "=========================================="
echo "Project A - Pre-Optimization Tests"
echo "=========================================="

# Change to project directory
cd "$(dirname "$0")"

# Setup environment
echo "Setting up environment..."
bash setup.sh

# Start server in background
echo "Starting pre-optimization server..."
python src/upload.py > logs/server_pre.log 2>&1 &
SERVER_PID=$!

# Wait for server to start
echo "Waiting for server to start..."
sleep 3

# Check if server is running
if ! ps -p $SERVER_PID > /dev/null; then
    echo "Error: Server failed to start"
    exit 1
fi

echo "Server started with PID: $SERVER_PID"

# Run tests
echo "Running tests..."
python tests/test_pre_optimization.py

# Stop server
echo "Stopping server..."
kill $SERVER_PID 2>/dev/null
wait $SERVER_PID 2>/dev/null

echo "=========================================="
echo "Project A tests completed"
echo "=========================================="

