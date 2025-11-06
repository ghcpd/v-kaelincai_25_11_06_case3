# Setup script for Project A - Pre-Optimization Image Upload
# This script sets up the environment and installs dependencies

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Project A - Pre-Optimization Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# Check if Python is installed
Write-Host "Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Python not found. Please install Python 3.9 or higher." -ForegroundColor Red
    exit 1
}

# Create virtual environment
Write-Host "Creating virtual environment..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "Virtual environment already exists. Skipping creation." -ForegroundColor Yellow
} else {
    python -m venv venv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "✗ Failed to create virtual environment" -ForegroundColor Red
        exit 1
    }
    Write-Host "✓ Virtual environment created" -ForegroundColor Green
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"

# Install dependencies
Write-Host "Installing dependencies from requirements.txt..." -ForegroundColor Yellow
pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Host "✗ Failed to install dependencies" -ForegroundColor Red
    exit 1
}
Write-Host "✓ Dependencies installed successfully" -ForegroundColor Green

# Create necessary directories
Write-Host "Creating necessary directories..." -ForegroundColor Yellow
New-Item -ItemType Directory -Path "uploads" -Force | Out-Null
New-Item -ItemType Directory -Path "logs" -Force | Out-Null
New-Item -ItemType Directory -Path "performance" -Force | Out-Null
Write-Host "✓ Directories created" -ForegroundColor Green

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Setup completed successfully!" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Run 'run_tests.ps1' to start the server and run tests" -ForegroundColor Yellow
Write-Host "2. Check logs/log_pre.txt for detailed test results" -ForegroundColor Yellow
Write-Host "3. Check performance/time_pre.txt for performance metrics" -ForegroundColor Yellow
