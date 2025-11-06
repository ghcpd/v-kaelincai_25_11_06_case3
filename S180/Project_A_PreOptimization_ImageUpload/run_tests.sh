#!/bin/bash
python -m pip install -r requirements.txt
# start server
pushd src
python upload.py &
PID=$!
popd
sleep 1
# run tests
pushd tests
python test_pre_optimization.py
popd
# collect logs
mv results_pre.json ../results_pre.json || true
kill $PID || true
