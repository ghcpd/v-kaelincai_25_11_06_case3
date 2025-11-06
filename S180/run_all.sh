#!/bin/bash
set -e

# Generate test fixtures
python shared_data/generate_test_files.py

# Start pre-optimization server
pushd Project_A_PreOptimization_ImageUpload/src
python upload.py &
PRE_PID=$!
popd
sleep 1

# Run pre-optimization tests
pushd Project_A_PreOptimization_ImageUpload/tests
python test_pre_optimization.py
popd
sleep 1

# Start post-optimization server
pushd Project_B_PostOptimization_ImageUpload/src
python upload_optimized.py &
POST_PID=$!
popd
sleep 1

pushd Project_B_PostOptimization_ImageUpload/tests
python test_post_optimization.py
popd

# Collect and compare
python tools/compare_results.py

# Kill servers
kill $PRE_PID || true
kill $POST_PID || true

echo "Done"
