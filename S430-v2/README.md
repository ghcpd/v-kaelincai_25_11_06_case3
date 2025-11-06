# Upload Optimization Evaluation

This workspace contains two projects to evaluate performance before and after optimizations.

How to run tests:
1. Install Python and optionally create a venv
2. From the workspace root run: bash run_all.sh (Linux/macOS/GitBash) or run_all.bat (Windows)

Notes on network simulation: tests emulate limited bandwidth by using `X-Simulate-Mbps` HTTP header which both servers understand.
