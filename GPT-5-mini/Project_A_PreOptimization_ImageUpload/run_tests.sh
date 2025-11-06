#!/usr/bin/env bash
set -e
echo "Starting pre-optimization server..."
python -u src/upload.py &
SERVER_PID=$!
sleep 1
echo "Running tests..."
python tests/test_pre_optimization.py
echo "Stopping server..."
kill %SERVER_PID || true
