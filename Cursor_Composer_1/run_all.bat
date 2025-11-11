@echo off
REM Master script to run both Project A and Project B tests and generate comparison report (Windows)

echo ==========================================
echo Image Upload Performance Evaluation
echo ==========================================
echo.

REM Get the directory where this script is located
cd /d "%~dp0"

REM Step 1: Run Project A (Pre-Optimization) tests
echo ==========================================
echo Step 1: Running Project A (Pre-Optimization) Tests
echo ==========================================
cd Project_A_PreOptimization_ImageUpload
call run_tests.bat
cd ..

REM Step 2: Run Project B (Post-Optimization) tests
echo.
echo ==========================================
echo Step 2: Running Project B (Post-Optimization) Tests
echo ==========================================
cd Project_B_PostOptimization_ImageUpload
call run_tests.bat
cd ..

REM Step 3: Generate comparison report
echo.
echo ==========================================
echo Step 3: Generating Comparison Report
echo ==========================================

REM Check if results files exist
set PRE_RESULTS=Project_A_PreOptimization_ImageUpload\performance\results_pre.json
set POST_RESULTS=Project_B_PostOptimization_ImageUpload\performance\results_post.json

if not exist "%PRE_RESULTS%" (
    echo Error: Pre-optimization results not found at %PRE_RESULTS%
    exit /b 1
)

if not exist "%POST_RESULTS%" (
    echo Error: Post-optimization results not found at %POST_RESULTS%
    exit /b 1
)

REM Generate comparison report
python generate_comparison_report.py "%PRE_RESULTS%" "%POST_RESULTS%" "compare_report.md"

echo.
echo ==========================================
echo Evaluation Complete!
echo ==========================================
echo.
echo Results:
echo   - Pre-optimization results: %PRE_RESULTS%
echo   - Post-optimization results: %POST_RESULTS%
echo   - Comparison report: compare_report.md
echo.
echo View the comparison report:
echo   type compare_report.md
echo.

pause

