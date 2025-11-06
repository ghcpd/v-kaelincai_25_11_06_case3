#!/usr/bin/env bash
set -e
echo "Starting post-optimization server..."
python -u src/upload_optimized.py &
SERVER_PID=$!
sleep 1
echo "Running tests..."
python tests/test_post_optimization.py
echo "Stopping server..."
kill %SERVER_PID || true
