Write-Host "Starting pre-optimization server..."
$p = Start-Process -FilePath python -ArgumentList 'src/upload.py' -PassThru
Start-Sleep -Seconds 1
Write-Host "Running tests..."
python tests/test_pre_optimization.py
Write-Host "Stopping server..."
Stop-Process -Id $p.Id -ErrorAction SilentlyContinue
