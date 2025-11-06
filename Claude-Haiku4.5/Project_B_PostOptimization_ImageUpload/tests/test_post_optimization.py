"""
Test harness for Post-Optimization Image Upload (Project B)
Tests the optimized image upload implementation
"""

import requests
import json
import time
import os
import io
from datetime import datetime
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging
from PIL import Image
import hashlib

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/log_post.txt'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

SERVER_URL = 'http://localhost:5001'
TEST_DATA_PATH = '../test_data.json'
RESULTS_FILE = 'results_post.json'
PERFORMANCE_FILE = 'performance/time_post.txt'

# Create necessary directories
os.makedirs('logs', exist_ok=True)
os.makedirs('performance', exist_ok=True)
os.makedirs('test_images', exist_ok=True)


def generate_test_image(size_bytes, image_format='jpg', corrupted=False):
    """
    Generate a test image file of specified size.
    
    Args:
        size_bytes: Size of image in bytes
        image_format: Image format (jpg, png, gif, corrupted)
        corrupted: Whether to create a corrupted image
    
    Returns:
        BytesIO object containing image data
    """
    if corrupted or image_format == 'corrupted':
        # Generate corrupted/invalid image
        return io.BytesIO(b'INVALID_IMAGE_DATA_\x00\x01\x02')
    
    try:
        if image_format.lower() == 'jpg':
            # Create JPEG image
            width = max(1, int((size_bytes / 1000) ** 0.5))
            height = max(1, size_bytes // (width * 3))
            img = Image.new('RGB', (width, height), color=(73, 109, 137))
        
        elif image_format.lower() == 'png':
            # Create PNG image
            width = max(1, int((size_bytes / 1000) ** 0.5))
            height = max(1, size_bytes // (width * 4))
            img = Image.new('RGBA', (width, height), color=(73, 109, 137, 255))
        
        else:
            # Default to JPEG
            img = Image.new('RGB', (100, 100), color=(73, 109, 137))
        
        img_io = io.BytesIO()
        img.save(img_io, format='JPEG' if image_format.lower() in ['jpg', 'jpeg'] else 'PNG')
        img_io.seek(0)
        
        # Pad to desired size if necessary
        current_size = len(img_io.getvalue())
        if current_size < size_bytes:
            padding = size_bytes - current_size
            img_io.write(b'\x00' * padding)
        
        img_io.seek(0)
        return img_io
    
    except Exception as e:
        logger.error(f"Error generating test image: {e}")
        return io.BytesIO(b'\x00' * min(size_bytes, 1024))


def upload_image(test_case, test_id):
    """
    Upload an image to the post-optimization server.
    
    Args:
        test_case: Test case from test_data.json
        test_id: ID of the test case
    
    Returns:
        Dictionary with upload results
    """
    result = {
        'test_id': test_id,
        'test_name': test_case['name'],
        'timestamp': datetime.now().isoformat(),
        'status': 'unknown',
        'message': '',
        'upload_time': 0,
        'expected_status': test_case['expected_status'],
        'concurrent_uploads': test_case['concurrent_uploads']
    }
    
    try:
        # Generate test image
        logger.info(f"Generating test image for {test_id}: {test_case['name']}")
        image_data = generate_test_image(
            test_case['image_size_bytes'],
            test_case['image_format'],
            corrupted=(test_case['image_format'] == 'corrupted')
        )
        
        # Prepare file
        files = {
            'file': (f'test_image_{test_id}.jpg', image_data, 'image/jpeg')
        }
        
        # Upload with timing
        logger.info(f"Uploading {test_id}...")
        start_time = time.time()
        
        try:
            response = requests.post(
                f'{SERVER_URL}/upload',
                files=files,
                timeout=180  # 3 minutes timeout
            )
            
            upload_time = time.time() - start_time
            result['upload_time'] = upload_time
            
            logger.info(f"Response status: {response.status_code}")
            response_data = response.json()
            
            result['status'] = response_data.get('status', 'unknown')
            result['message'] = response_data.get('message', '')
            result['server_upload_time'] = response_data.get('upload_time', 0)
            
            # Verify expected status
            if result['status'] == result['expected_status']:
                result['test_result'] = 'PASS'
                logger.info(f"✓ {test_id} PASSED")
            else:
                result['test_result'] = 'FAIL'
                logger.warning(f"✗ {test_id} FAILED: Expected {result['expected_status']}, got {result['status']}")
        
        except requests.Timeout:
            upload_time = time.time() - start_time
            result['upload_time'] = upload_time
            result['status'] = 'timeout'
            result['message'] = 'Request timeout'
            result['test_result'] = 'FAIL' if result['expected_status'] == 'success' else 'PASS'
            logger.error(f"✗ {test_id} TIMEOUT after {upload_time:.2f}s")
        
        except Exception as e:
            upload_time = time.time() - start_time
            result['upload_time'] = upload_time
            result['status'] = 'error'
            result['message'] = str(e)
            result['test_result'] = 'FAIL' if result['expected_status'] == 'success' else 'PASS'
            logger.error(f"✗ {test_id} ERROR: {e}")
    
    except Exception as e:
        result['status'] = 'error'
        result['message'] = str(e)
        result['test_result'] = 'FAIL'
        logger.error(f"✗ {test_id} ERROR: {e}")
    
    return result


def run_single_test(test_case, test_id):
    """Run a single test case."""
    return upload_image(test_case, test_id)


def run_concurrent_test(test_case, test_id):
    """Run concurrent upload test."""
    num_concurrent = test_case['concurrent_uploads']
    
    logger.info(f"Starting concurrent upload test: {test_id} with {num_concurrent} concurrent uploads")
    
    results = []
    start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=num_concurrent) as executor:
        futures = []
        for i in range(num_concurrent):
            future = executor.submit(upload_image, test_case, f"{test_id}_concurrent_{i+1}")
            futures.append(future)
        
        for future in as_completed(futures):
            result = future.result()
            results.append(result)
    
    total_time = time.time() - start_time
    
    # Aggregate results
    success_count = sum(1 for r in results if r['status'] == 'success')
    
    aggregated = {
        'test_id': test_id,
        'test_name': test_case['name'],
        'timestamp': datetime.now().isoformat(),
        'total_concurrent': num_concurrent,
        'successful': success_count,
        'failed': num_concurrent - success_count,
        'total_time': total_time,
        'average_time': total_time / num_concurrent,
        'individual_results': results,
        'test_result': 'PASS' if success_count == num_concurrent else 'FAIL'
    }
    
    logger.info(f"Concurrent test {test_id} completed: {success_count}/{num_concurrent} successful in {total_time:.2f}s")
    
    return aggregated


def run_all_tests():
    """Run all test cases."""
    logger.info("=" * 80)
    logger.info("STARTING POST-OPTIMIZATION TEST SUITE")
    logger.info("=" * 80)
    
    # Load test data
    with open(TEST_DATA_PATH, 'r') as f:
        test_data = json.load(f)
    
    test_cases = test_data['test_cases']
    logger.info(f"Loaded {len(test_cases)} test cases")
    
    # Wait for server to be ready
    logger.info("Waiting for server to be ready...")
    for attempt in range(30):
        try:
            response = requests.get(f'{SERVER_URL}/health', timeout=5)
            if response.status_code == 200:
                logger.info("Server is ready!")
                break
        except:
            pass
        
        if attempt < 29:
            logger.info(f"Attempt {attempt + 1}/30: Server not ready, retrying...")
            time.sleep(1)
        else:
            logger.error("Server failed to start!")
            return []
    
    # Run tests
    all_results = []
    test_start = time.time()
    
    for i, test_case in enumerate(test_cases):
        test_id = test_case['test_id']
        logger.info(f"\nRunning test {i + 1}/{len(test_cases)}: {test_id}")
        
        if test_case['concurrent_uploads'] > 1:
            result = run_concurrent_test(test_case, test_id)
        else:
            result = run_single_test(test_case, test_id)
        
        all_results.append(result)
        
        # Add delay between tests
        time.sleep(2)
    
    total_test_time = time.time() - test_start
    
    # Save results
    results_summary = {
        'test_suite': 'Post-Optimization Image Upload',
        'total_tests': len(all_results),
        'passed': sum(1 for r in all_results if r.get('test_result') == 'PASS'),
        'failed': sum(1 for r in all_results if r.get('test_result') == 'FAIL'),
        'total_time': total_test_time,
        'start_time': datetime.now().isoformat(),
        'results': all_results
    }
    
    # Save to JSON
    with open(RESULTS_FILE, 'w') as f:
        json.dump(results_summary, f, indent=2)
    
    # Save timing data
    with open(PERFORMANCE_FILE, 'w') as f:
        f.write("Post-Optimization Performance Metrics\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"Total Test Time: {total_test_time:.2f} seconds\n")
        f.write(f"Total Tests: {len(all_results)}\n")
        f.write(f"Passed: {results_summary['passed']}\n")
        f.write(f"Failed: {results_summary['failed']}\n\n")
        f.write("Individual Test Timings:\n")
        f.write("-" * 80 + "\n")
        
        for result in all_results:
            test_name = result.get('test_name', result.get('test_id', 'Unknown'))
            if 'upload_time' in result:
                f.write(f"{result['test_id']}: {result['upload_time']:.2f}s - {test_name}\n")
            elif 'total_time' in result:
                f.write(f"{result['test_id']}: {result['total_time']:.2f}s (concurrent) - {test_name}\n")
    
    logger.info("\n" + "=" * 80)
    logger.info("TEST SUITE COMPLETED")
    logger.info("=" * 80)
    logger.info(f"Total Tests: {len(all_results)}")
    logger.info(f"Passed: {results_summary['passed']}")
    logger.info(f"Failed: {results_summary['failed']}")
    logger.info(f"Total Time: {total_test_time:.2f} seconds")
    logger.info(f"Results saved to: {RESULTS_FILE}")
    logger.info(f"Performance data saved to: {PERFORMANCE_FILE}")
    
    return all_results


if __name__ == '__main__':
    run_all_tests()
