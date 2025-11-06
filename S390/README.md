# Upload Optimization Evaluation

This workspace contains two projects to evaluate image upload performance before and after optimizations.

Run instructions:
- For Linux/macOS/GitBash: `bash run_all.sh`
- For Windows: `run_all.bat` (calls bash script)

Note:
- Tests simulate network latency via header `X-Simulate-Mbps`.
- 200MB and 500MB tests are heavy and may use significant disk; ensure you have resources.
