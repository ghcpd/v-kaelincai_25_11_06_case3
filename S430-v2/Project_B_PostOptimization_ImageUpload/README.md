# Project B — Post-Optimization (Fast Upload)

Features:
- Upload endpoint returns quickly and moves heavy processing to background thread pool
- Reduced processing time per MB (0.012 sec/MB), uses concurrency to improve throughput
- Provides a /status/<id> route to query processing state

How to run:
1. ./setup.sh
2. ./run_tests.sh to run the automated tests

Notes on network simulation: The tests set a custom header `X-Simulate-Mbps` to estimate simulated network transfer time. This server will sleep for an estimated time based on file size and the provided bandwidth in Mbps. This is a lightweight way to simulate network limitations for testing purposes.

Improvements:
- Lower average upload latency and better throughput under concurrency.
- Background processing reduces request blocking.

Limitations:
- Background tasks may be lost if process restarts (use a persistent queue for production)
