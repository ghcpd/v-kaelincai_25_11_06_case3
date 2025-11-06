# Project A - Pre-Optimization Slow Upload

This project simulates slow, blocking image uploads with synchronous processing.

Run: 

- Setup: `./setup.sh` (creates venv and installs dependencies)
- Tests: `./run_tests.sh` (runs tests which start the Flask server and execute uploads)

Notes:
- Test data includes large images (200MB and 500MB), corrupted input, and a concurrency test.
- Use caution: generating 500MB test image may consume significant disk space.
- Server simulates slow processing: 0.05 sec/MB.
