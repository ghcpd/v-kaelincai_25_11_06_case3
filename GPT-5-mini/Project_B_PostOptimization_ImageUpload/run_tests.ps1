Write-Host "Starting post-optimization server..."
$p = Start-Process -FilePath python -ArgumentList 'src/upload_optimized.py' -PassThru
Start-Sleep -Seconds 1
Write-Host "Running tests..."
python tests/test_post_optimization.py
Write-Host "Stopping server..."
Stop-Process -Id $p.Id -ErrorAction SilentlyContinue
