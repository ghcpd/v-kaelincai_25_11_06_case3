@echo off
REM Run tests for Project B - Post-Optimization Image Upload (Windows)

echo ==========================================
echo Project B - Post-Optimization Tests
echo ==========================================

REM Change to project directory
cd /d "%~dp0"

REM Setup environment
echo Setting up environment...
call setup.bat

REM Start server in background
echo Starting post-optimization server...
start /B python src/upload_optimized.py > logs\server_post.log 2>&1

REM Wait for server to start
echo Waiting for server to start...
timeout /t 3 /nobreak >nul

REM Run tests
echo Running tests...
python tests/test_post_optimization.py

REM Stop server (find and kill Python process on port 8001)
echo Stopping server...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8001 ^| findstr LISTENING') do taskkill /F /PID %%a >nul 2>&1

echo ==========================================
echo Project B tests completed
echo ==========================================

