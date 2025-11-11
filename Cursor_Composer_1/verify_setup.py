"""
Verification script to check if all required files and directories are present
"""
import os
import sys

def check_file_exists(filepath, description):
    """Check if a file exists"""
    if os.path.exists(filepath):
        print(f"[OK] {description}: {filepath}")
        return True
    else:
        print(f"[MISSING] {description}: {filepath} - MISSING")
        return False

def check_directory_exists(dirpath, description):
    """Check if a directory exists"""
    if os.path.isdir(dirpath):
        print(f"[OK] {description}: {dirpath}")
        return True
    else:
        print(f"[MISSING] {description}: {dirpath} - MISSING")
        return False

def main():
    """Verify project setup"""
    print("=" * 60)
    print("Project Setup Verification")
    print("=" * 60)
    print()
    
    all_ok = True
    
    # Check Project A files
    print("Project A - Pre-Optimization:")
    print("-" * 60)
    all_ok &= check_file_exists("Project_A_PreOptimization_ImageUpload/src/upload.py", "Upload server")
    all_ok &= check_file_exists("Project_A_PreOptimization_ImageUpload/src/image_processor.py", "Image processor")
    all_ok &= check_file_exists("Project_A_PreOptimization_ImageUpload/tests/test_pre_optimization.py", "Test harness")
    all_ok &= check_file_exists("Project_A_PreOptimization_ImageUpload/data/test_data.json", "Test data")
    all_ok &= check_file_exists("Project_A_PreOptimization_ImageUpload/requirements.txt", "Requirements")
    all_ok &= check_file_exists("Project_A_PreOptimization_ImageUpload/setup.sh", "Setup script (Linux/Mac)")
    all_ok &= check_file_exists("Project_A_PreOptimization_ImageUpload/setup.bat", "Setup script (Windows)")
    all_ok &= check_file_exists("Project_A_PreOptimization_ImageUpload/run_tests.sh", "Run tests script (Linux/Mac)")
    all_ok &= check_file_exists("Project_A_PreOptimization_ImageUpload/run_tests.bat", "Run tests script (Windows)")
    print()
    
    # Check Project B files
    print("Project B - Post-Optimization:")
    print("-" * 60)
    all_ok &= check_file_exists("Project_B_PostOptimization_ImageUpload/src/upload_optimized.py", "Optimized upload server")
    all_ok &= check_file_exists("Project_B_PostOptimization_ImageUpload/src/image_processor_optimized.py", "Optimized image processor")
    all_ok &= check_file_exists("Project_B_PostOptimization_ImageUpload/tests/test_post_optimization.py", "Test harness")
    all_ok &= check_file_exists("Project_B_PostOptimization_ImageUpload/data/test_data.json", "Test data")
    all_ok &= check_file_exists("Project_B_PostOptimization_ImageUpload/requirements.txt", "Requirements")
    all_ok &= check_file_exists("Project_B_PostOptimization_ImageUpload/setup.sh", "Setup script (Linux/Mac)")
    all_ok &= check_file_exists("Project_B_PostOptimization_ImageUpload/setup.bat", "Setup script (Windows)")
    all_ok &= check_file_exists("Project_B_PostOptimization_ImageUpload/run_tests.sh", "Run tests script (Linux/Mac)")
    all_ok &= check_file_exists("Project_B_PostOptimization_ImageUpload/run_tests.bat", "Run tests script (Windows)")
    print()
    
    # Check shared files
    print("Shared Artifacts:")
    print("-" * 60)
    all_ok &= check_file_exists("test_data.json", "Shared test data")
    all_ok &= check_file_exists("generate_comparison_report.py", "Comparison report generator")
    all_ok &= check_file_exists("run_all.sh", "Master script (Linux/Mac)")
    all_ok &= check_file_exists("run_all.bat", "Master script (Windows)")
    all_ok &= check_file_exists("README.md", "Documentation")
    print()
    
    # Check Python version
    print("Environment:")
    print("-" * 60)
    python_version = sys.version_info
    print(f"Python version: {python_version.major}.{python_version.minor}.{python_version.micro}")
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 7):
        print("[WARNING] Python 3.7+ recommended")
        all_ok = False
    else:
        print("[OK] Python version is compatible")
    print()
    
    # Final summary
    print("=" * 60)
    if all_ok:
        print("[SUCCESS] All files are present and setup appears correct!")
        print()
        print("Next steps:")
        print("  Linux/Mac: bash run_all.sh")
        print("  Windows:   run_all.bat")
    else:
        print("[ERROR] Some files are missing. Please check the errors above.")
        sys.exit(1)
    print("=" * 60)

if __name__ == '__main__':
    main()

