# Master run script for all tests - runs both pre and post optimization projects
# This script orchestrates the entire test execution and generates the comparison report

Write-Host "=================================================================================" -ForegroundColor Cyan
Write-Host "Image Upload Performance Optimization - Master Test Suite" -ForegroundColor Cyan
Write-Host "=================================================================================" -ForegroundColor Cyan
Write-Host ""

# Get current directory
$scriptDir = Get-Location
$startTime = Get-Date

# Helper function to run a project
function Run-ProjectTests {
    param(
        [string]$projectName,
        [string]$projectPath,
        [string]$scriptName
    )
    
    Write-Host ""
    Write-Host "################################################################################" -ForegroundColor Cyan
    Write-Host "Running: $projectName" -ForegroundColor Cyan
    Write-Host "################################################################################" -ForegroundColor Cyan
    
    # Check if project exists
    if (-not (Test-Path $projectPath)) {
        Write-Host "✗ ERROR: Project directory not found: $projectPath" -ForegroundColor Red
        return $false
    }
    
    # Change to project directory
    Push-Location $projectPath
    
    # Setup if needed
    if (-not (Test-Path "venv")) {
        Write-Host "Running setup..." -ForegroundColor Yellow
        if (Test-Path "setup.ps1") {
            & ".\setup.ps1"
            if ($LASTEXITCODE -ne 0) {
                Write-Host "✗ Setup failed" -ForegroundColor Red
                Pop-Location
                return $false
            }
        }
    }
    
    # Run tests
    Write-Host "Running tests..." -ForegroundColor Yellow
    if (Test-Path $scriptName) {
        & ".\$scriptName"
        $testResult = $LASTEXITCODE
    } else {
        Write-Host "✗ ERROR: Test script not found: $scriptName" -ForegroundColor Red
        Pop-Location
        return $false
    }
    
    Pop-Location
    
    return ($testResult -eq 0)
}

# Run Project A (Pre-Optimization)
$projectAPath = "Project_A_PreOptimization_ImageUpload"
$projectASuccess = Run-ProjectTests `
    "Project A - Pre-Optimization Image Upload" `
    $projectAPath `
    "run_tests.ps1"

# Run Project B (Post-Optimization)
$projectBPath = "Project_B_PostOptimization_ImageUpload"
$projectBSuccess = Run-ProjectTests `
    "Project B - Post-Optimization Image Upload" `
    $projectBPath `
    "run_tests.ps1"

# Generate comparison report
Write-Host ""
Write-Host "################################################################################" -ForegroundColor Cyan
Write-Host "Generating Comparison Report" -ForegroundColor Cyan
Write-Host "################################################################################" -ForegroundColor Cyan

Write-Host "Generating comparison report..." -ForegroundColor Yellow

# Check if both test result files exist
if ((Test-Path "$projectAPath/tests/results_pre.json") -and (Test-Path "$projectBPath/tests/results_post.json")) {
    python generate_comparison.py
    $comparisonResult = $LASTEXITCODE
    
    if ($comparisonResult -eq 0) {
        Write-Host "✓ Comparison report generated successfully" -ForegroundColor Green
    } else {
        Write-Host "✗ Failed to generate comparison report" -ForegroundColor Red
    }
} else {
    Write-Host "✗ Cannot generate comparison: Missing result files" -ForegroundColor Red
    if (-not (Test-Path "$projectAPath/tests/results_pre.json")) {
        Write-Host "  - Missing: $projectAPath/tests/results_pre.json" -ForegroundColor Red
    }
    if (-not (Test-Path "$projectBPath/tests/results_post.json")) {
        Write-Host "  - Missing: $projectBPath/tests/results_post.json" -ForegroundColor Red
    }
}

# Final Summary
Write-Host ""
Write-Host "=================================================================================" -ForegroundColor Cyan
Write-Host "MASTER TEST SUITE COMPLETED" -ForegroundColor Cyan
Write-Host "=================================================================================" -ForegroundColor Cyan

$endTime = Get-Date
$totalTime = ($endTime - $startTime).TotalSeconds

Write-Host ""
Write-Host "Summary:" -ForegroundColor Yellow
Write-Host "--------" -ForegroundColor Yellow
Write-Host "Project A (Pre-Optimization):   $(if ($projectASuccess) { '✓ PASSED' } else { '✗ FAILED' })" -ForegroundColor $(if ($projectASuccess) { 'Green' } else { 'Red' })
Write-Host "Project B (Post-Optimization):  $(if ($projectBSuccess) { '✓ PASSED' } else { '✗ FAILED' })" -ForegroundColor $(if ($projectBSuccess) { 'Green' } else { 'Red' })
Write-Host ""
Write-Host "Output Files:" -ForegroundColor Yellow
Write-Host "-----------" -ForegroundColor Yellow
Write-Host "Pre-Optimization Results:      $projectAPath/tests/results_pre.json" -ForegroundColor Gray
Write-Host "Post-Optimization Results:     $projectBPath/tests/results_post.json" -ForegroundColor Gray
Write-Host "Pre-Optimization Log:          $projectAPath/tests/logs/log_pre.txt" -ForegroundColor Gray
Write-Host "Post-Optimization Log:         $projectBPath/tests/logs/log_post.txt" -ForegroundColor Gray
Write-Host "Comparison Report:             compare_report.md" -ForegroundColor Gray
Write-Host ""
Write-Host "Total Execution Time: $([math]::Round($totalTime, 2)) seconds" -ForegroundColor Yellow
Write-Host ""
Write-Host "=================================================================================" -ForegroundColor Cyan

# Open comparison report if it exists
if (Test-Path "compare_report.md") {
    Write-Host ""
    Write-Host "To view the comparison report, open: compare_report.md" -ForegroundColor Cyan
}

exit $(if ($projectASuccess -and $projectBSuccess) { 0 } else { 1 })
