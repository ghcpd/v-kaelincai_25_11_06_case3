#!/usr/bin/env bash
set -e
ROOT=$(pwd)

echo "Running Project A (pre-optimization) tests"
pushd Project_A_PreOptimization_ImageUpload
python -u src/upload.py &
SERVER_PID=$!
sleep 1
python tests/test_pre_optimization.py
kill %SERVER_PID || true
popd

echo "Running Project B (post-optimization) tests"
pushd Project_B_PostOptimization_ImageUpload
python -u src/upload_optimized.py &
SERVER_PID=$!
sleep 1
python tests/test_post_optimization.py
kill %SERVER_PID || true
popd

echo "Generating comparison report"
python compare_results.py
