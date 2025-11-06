# Image Upload Performance Comparison

This report compares upload performance between Project A (pre-optimization) and Project B (post-optimization).

How tests are run:
- `run_all.sh` runs test suites for both projects and aggregates the results into `compare_report.md` and `s_shared_artifacts/results/compare_summary.json`.

Expected improvements in Project B:
- Lower average upload latency (measured in seconds per upload)
- Higher throughput during concurrent uploads
- Better resilience for large images due to background processing

Visual evidence:
- See `s_shared_artifacts/screenshots` for example UI and response time screenshots.

Important: For accurate metrics, run tests on a stable host. Large test files (200MB) may quickly consume disk space and CPU; ensure you have enough capacity.

Limitations & next steps:
- This test harness uses simulated network latency. For production-like conditions, use an external traffic shaping tool or cloud environments.
- For persistent and fault-tolerant background processing consider adding a queue (Redis, RabbitMQ) and worker processes.
