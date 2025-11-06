# Run tests script for Project A - Pre-Optimization Image Upload
# This script starts the server and runs the test suite

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Project A - Pre-Optimization Tests" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"

# Start the server in background
Write-Host "Starting Flask server..." -ForegroundColor Yellow
$serverProcess = Start-Process python -ArgumentList "src/upload.py" -PassThru -NoNewWindow
Write-Host "✓ Server started with PID: $($serverProcess.Id)" -ForegroundColor Green

# Wait for server to be ready
Write-Host "Waiting for server to be ready..." -ForegroundColor Yellow
Start-Sleep -Seconds 3

# Run tests
Write-Host "Running test suite..." -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan

cd tests
python test_pre_optimization.py

$testExitCode = $LASTEXITCODE

cd ..

# Stop server
Write-Host "Stopping server..." -ForegroundColor Yellow
Stop-Process -Id $serverProcess.Id -Force -ErrorAction SilentlyContinue
Write-Host "✓ Server stopped" -ForegroundColor Green

# Display results summary
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Test Execution Completed" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Results files:" -ForegroundColor Yellow
Write-Host "- tests/results_pre.json" -ForegroundColor Gray
Write-Host "- tests/logs/log_pre.txt" -ForegroundColor Gray
Write-Host "- tests/performance/time_pre.txt" -ForegroundColor Gray

if (Test-Path "tests/results_pre.json") {
    $results = Get-Content "tests/results_pre.json" | ConvertFrom-Json
    Write-Host "`nTest Summary:" -ForegroundColor Yellow
    Write-Host "Total Tests: $($results.total_tests)" -ForegroundColor Gray
    Write-Host "Passed: $($results.passed)" -ForegroundColor Green
    Write-Host "Failed: $($results.failed)" -ForegroundColor Red
    Write-Host "Total Time: $($results.total_time) seconds" -ForegroundColor Gray
}

exit $testExitCode
