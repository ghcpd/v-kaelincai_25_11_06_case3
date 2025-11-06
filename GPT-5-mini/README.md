# Evaluation: Image Upload Performance Optimization

This repository contains two projects demonstrating a slow image upload (Project A) and an optimized implementation (Project B). Run `run_all.sh` to execute both tests and generate a comparison report.

Project folders:
- `Project_A_PreOptimization_ImageUpload` - slow, blocking uploads
- `Project_B_PostOptimization_ImageUpload` - optimized chunked uploads + background processing

See `compare_report.md` after running tests for a summary of improvements.

Notes:
- This is a self-contained reproducible experiment. For Windows PowerShell, use the included `run_all.sh` in Git Bash or execute the steps manually in PowerShell by running the servers and test scripts.
