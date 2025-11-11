@echo off
REM Setup script for Project A - Pre-Optimization Image Upload (Windows)

echo Setting up Project A - Pre-Optimization Image Upload...

REM Create necessary directories
if not exist uploads mkdir uploads
if not exist logs mkdir logs
if not exist performance mkdir performance
if not exist data mkdir data

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

echo Setup complete for Project A!

