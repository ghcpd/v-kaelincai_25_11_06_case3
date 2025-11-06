Write-Host "Running Project A tests"
& .\Project_A_PreOptimization_ImageUpload\run_tests.ps1
Write-Host "Running Project B tests"
& .\Project_B_PostOptimization_ImageUpload\run_tests.ps1
Write-Host "Generating comparison report"
python compare_results.py
