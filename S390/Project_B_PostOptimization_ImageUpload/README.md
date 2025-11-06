# Project B - Post-Optimization Fast Upload

This project optimizes upload handling by returning quickly and processing images in background threads.

Run: 
- Setup: `./setup.sh`
- Tests: `./run_tests.sh` (starts the server and uploads test images; polls status endpoint)

Improvements:
- Reduced processing time: 0.012 sec/MB (simulated)
- Background thread pool processes uploads concurrently (ThreadPoolExecutor)

Limitations:
- Background in-memory queue not persistent; for production, use task queue like Celery + Redis.
