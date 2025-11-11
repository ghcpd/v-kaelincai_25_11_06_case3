#!/bin/bash
# Master script to run both Project A and Project B tests and generate comparison report

echo "=========================================="
echo "Image Upload Performance Evaluation"
echo "=========================================="
echo ""

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Step 1: Run Project A (Pre-Optimization) tests
echo "=========================================="
echo "Step 1: Running Project A (Pre-Optimization) Tests"
echo "=========================================="
cd Project_A_PreOptimization_ImageUpload
bash run_tests.sh
cd ..

# Step 2: Run Project B (Post-Optimization) tests
echo ""
echo "=========================================="
echo "Step 2: Running Project B (Post-Optimization) Tests"
echo "=========================================="
cd Project_B_PostOptimization_ImageUpload
bash run_tests.sh
cd ..

# Step 3: Generate comparison report
echo ""
echo "=========================================="
echo "Step 3: Generating Comparison Report"
echo "=========================================="

# Check if results files exist
PRE_RESULTS="Project_A_PreOptimization_ImageUpload/performance/results_pre.json"
POST_RESULTS="Project_B_PostOptimization_ImageUpload/performance/results_post.json"

if [ ! -f "$PRE_RESULTS" ]; then
    echo "Error: Pre-optimization results not found at $PRE_RESULTS"
    exit 1
fi

if [ ! -f "$POST_RESULTS" ]; then
    echo "Error: Post-optimization results not found at $POST_RESULTS"
    exit 1
fi

# Generate comparison report
python generate_comparison_report.py "$PRE_RESULTS" "$POST_RESULTS" "compare_report.md"

echo ""
echo "=========================================="
echo "Evaluation Complete!"
echo "=========================================="
echo ""
echo "Results:"
echo "  - Pre-optimization results: $PRE_RESULTS"
echo "  - Post-optimization results: $POST_RESULTS"
echo "  - Comparison report: compare_report.md"
echo ""
echo "View the comparison report:"
echo "  cat compare_report.md"
echo ""

