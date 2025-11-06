# Project A — Pre-Optimization (Slow Upload)

This project implements a naive image upload service with simulated network and processing delays.

How to run:
1. ./setup.sh
2. ./run_tests.sh to run the automated tests

Notes on network simulation: The tests use a custom header `X-Simulate-Mbps` to instruct the server to simulate network latency for uploads (server sleeps proportional to file size and bandwidth). This lets you test behavior under constrained bandwidth conditions.

Endpoints:
- POST /upload (multipart form with 'file')
- GET /health

Limitations:
- Processing is synchronous and blocking.
- Per-MB processing time simulated as 0.05 sec/MB
- For large files or high traffic, service becomes slow and may time out
