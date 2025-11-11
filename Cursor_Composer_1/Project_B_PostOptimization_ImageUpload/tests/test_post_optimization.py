"""
Test harness for post-optimization image upload
Tests the optimized upload functionality
"""
import os
import sys
import json
import time
import requests
import subprocess
import signal
from PIL import Image
from io import BytesIO

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

class ImageUploadTester:
    """Test harness for optimized image upload functionality"""
    
    def __init__(self, base_url='http://localhost:8001', server_process=None):
        self.base_url = base_url
        self.server_process = server_process
        self.results = []
        self.logs = []
    
    def log(self, message):
        """Log a message"""
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        print(log_entry)
        self.logs.append(log_entry)
    
    def create_test_image(self, width, height, format='JPEG', quality=95):
        """Create a test image with specified dimensions"""
        image = Image.new('RGB', (width, height), color='red')
        buffer = BytesIO()
        image.save(buffer, format=format, quality=quality)
        return buffer.getvalue()
    
    def create_large_image(self, size_mb):
        """Create a large test image approximately of specified size in MB"""
        # Approximate: 1MB ≈ 1000x1000 RGB image
        pixels_per_mb = 1000 * 1000
        total_pixels = int(size_mb * pixels_per_mb)
        # Calculate dimensions for square image
        side = int(total_pixels ** 0.5)
        return self.create_test_image(side, side)
    
    def upload_image(self, image_data, test_id, description):
        """Upload an image and measure performance"""
        self.log(f"Test {test_id}: {description}")
        self.log(f"  Image size: {len(image_data) / (1024*1024):.2f} MB")
        
        start_time = time.time()
        success = False
        error_message = None
        upload_time = None
        
        try:
            response = requests.post(
                f"{self.base_url}/upload",
                data=image_data,
                headers={'Content-Type': 'image/jpeg'},
                timeout=30  # 30 second timeout
            )
            
            upload_time = time.time() - start_time
            
            if response.status_code == 200:
                result_data = response.json()
                success = True
                self.log(f"  ✓ Success - Upload time: {upload_time:.3f}s")
                if 'compression_ratio' in result_data:
                    self.log(f"  Compression: {result_data['compression_ratio']:.2f}%")
                self.log(f"  Response: {json.dumps(result_data, indent=2)}")
            else:
                success = False
                error_message = f"HTTP {response.status_code}: {response.text}"
                self.log(f"  ✗ Failed - {error_message}")
                
        except requests.exceptions.Timeout:
            upload_time = time.time() - start_time
            success = False
            error_message = "Request timeout"
            self.log(f"  ✗ Timeout after {upload_time:.3f}s")
        except requests.exceptions.ConnectionError:
            upload_time = time.time() - start_time
            success = False
            error_message = "Connection error - server may not be running"
            self.log(f"  ✗ Connection error")
        except Exception as e:
            upload_time = time.time() - start_time
            success = False
            error_message = str(e)
            self.log(f"  ✗ Error: {error_message}")
        
        result = {
            'test_id': test_id,
            'description': description,
            'image_size_mb': round(len(image_data) / (1024*1024), 2),
            'success': success,
            'upload_time': round(upload_time, 3) if upload_time else None,
            'error_message': error_message
        }
        
        self.results.append(result)
        return result
    
    def run_tests(self, test_cases):
        """Run all test cases"""
        self.log("=" * 60)
        self.log("Starting Post-Optimization Image Upload Tests")
        self.log("=" * 60)
        
        for test_case in test_cases:
            test_id = test_case['test_id']
            description = test_case['description']
            image_size_mb = test_case.get('image_size_mb', 1)
            image_type = test_case.get('image_type', 'normal')
            
            if image_type == 'large':
                image_data = self.create_large_image(image_size_mb)
            elif image_type == 'corrupted':
                # Create corrupted image data
                image_data = b'INVALID_IMAGE_DATA' * 1000
            else:
                # Normal image
                width = int((image_size_mb * 1000 * 1000 / 3) ** 0.5)  # Approximate
                image_data = self.create_test_image(width, width)
            
            self.upload_image(image_data, test_id, description)
            time.sleep(0.5)  # Small delay between tests
        
        self.log("=" * 60)
        self.log("Tests completed")
        self.log("=" * 60)
        
        return self.results
    
    def save_results(self, output_file='results_post.json'):
        """Save test results to JSON file"""
        output_path = os.path.join('performance', output_file)
        os.makedirs('performance', exist_ok=True)
        
        with open(output_path, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        self.log(f"Results saved to {output_path}")
    
    def save_logs(self, output_file='log_post.txt'):
        """Save logs to text file"""
        log_path = os.path.join('logs', output_file)
        os.makedirs('logs', exist_ok=True)
        
        with open(log_path, 'w') as f:
            f.write('\n'.join(self.logs))
        
        self.log(f"Logs saved to {log_path}")

def load_test_cases():
    """Load test cases from JSON file"""
    test_data_path = os.path.join('data', 'test_data.json')
    if os.path.exists(test_data_path):
        with open(test_data_path, 'r') as f:
            return json.load(f)['test_cases']
    else:
        # Default test cases if file doesn't exist
        return [
            {
                'test_id': 'TC001',
                'description': 'Small image upload (1MB)',
                'image_size_mb': 1,
                'image_type': 'normal',
                'expected_status': 'success'
            },
            {
                'test_id': 'TC002',
                'description': 'Medium image upload (5MB)',
                'image_size_mb': 5,
                'image_type': 'normal',
                'expected_status': 'success'
            },
            {
                'test_id': 'TC003',
                'description': 'Large image upload (50MB)',
                'image_size_mb': 50,
                'image_type': 'large',
                'expected_status': 'success'
            },
            {
                'test_id': 'TC004',
                'description': 'Corrupted image upload',
                'image_size_mb': 0.1,
                'image_type': 'corrupted',
                'expected_status': 'failure'
            },
            {
                'test_id': 'TC005',
                'description': 'Very large image upload (100MB)',
                'image_size_mb': 100,
                'image_type': 'large',
                'expected_status': 'success'
            }
        ]

def main():
    """Main test execution"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Test post-optimization image upload')
    parser.add_argument('--url', default='http://localhost:8001', help='Server URL')
    parser.add_argument('--test-data', default='data/test_data.json', help='Test data file')
    args = parser.parse_args()
    
    # Load test cases
    test_cases = load_test_cases()
    
    # Create tester
    tester = ImageUploadTester(base_url=args.url)
    
    # Run tests
    results = tester.run_tests(test_cases)
    
    # Save results
    tester.save_results()
    tester.save_logs()
    
    # Print summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    successful = sum(1 for r in results if r['success'])
    total = len(results)
    avg_time = sum(r['upload_time'] for r in results if r['upload_time']) / total if total > 0 else 0
    
    print(f"Total tests: {total}")
    print(f"Successful: {successful}")
    print(f"Failed: {total - successful}")
    print(f"Average upload time: {avg_time:.3f}s")
    print("=" * 60)

if __name__ == '__main__':
    main()

