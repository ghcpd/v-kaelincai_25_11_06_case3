#!/bin/bash
python -m pip install -r requirements.txt
pushd src
python upload_optimized.py &
PID=$!
popd
sleep 1
pushd tests
python test_post_optimization.py
popd
mv results_post.json ../results_post.json || true
kill $PID || true
