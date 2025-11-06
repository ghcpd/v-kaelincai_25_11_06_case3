"""
Pre-Optimization Image Upload Server
Demonstrates performance bottlenecks in image upload handling.
"""

import json
import time
import os
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import threading
from datetime import datetime

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB max file size
app.config['UPLOAD_FOLDER'] = './uploads'

# Create uploads directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Global metrics tracking
upload_metrics = {
    'total_uploads': 0,
    'successful_uploads': 0,
    'failed_uploads': 0,
    'total_time': 0
}

# Lock for thread-safe metrics updates
metrics_lock = threading.Lock()


def process_image_slow(file_path, file_size):
    """
    Pre-optimization: Slow image processing with blocking I/O.
    This demonstrates the performance bottleneck:
    - Uncompressed file reading
    - Sequential processing
    - Redundant validation passes
    - No streaming or chunking
    """
    try:
        # Inefficient: Read entire file into memory
        with open(file_path, 'rb') as f:
            image_data = f.read()
        
        # Simulate expensive validation (sequential, no optimization)
        time.sleep(0.5)  # Artificial processing delay
        
        # Redundant: Re-read file for each processing step
        with open(file_path, 'rb') as f:
            data = f.read()
            # Inefficient validation without early exit
            if len(data) < 10:
                return False, "Image too small"
            
            # Sequential format check
            time.sleep(0.3)  # Simulating format validation
            
            # Sequential corruption check
            time.sleep(0.3)  # Simulating integrity validation
        
        # Simulate storing metadata (blocking operation)
        metadata = {
            'filename': os.path.basename(file_path),
            'size': file_size,
            'processed_at': datetime.now().isoformat(),
            'status': 'processed'
        }
        
        # Write metadata synchronously (blocking)
        with open(file_path + '.meta', 'w') as f:
            json.dump(metadata, f)
        
        return True, "Image processed successfully"
    
    except Exception as e:
        return False, str(e)


@app.route('/upload', methods=['POST'])
def upload_image():
    """
    Pre-optimization image upload endpoint.
    Demonstrates bottlenecks:
    - No compression
    - No parallel processing
    - Full file processing before returning response
    - Synchronous I/O operations
    """
    start_time = time.time()
    
    try:
        # Check if file is in request
        if 'file' not in request.files:
            return jsonify({'status': 'failure', 'message': 'No file part'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'status': 'failure', 'message': 'No selected file'}), 400
        
        # Get file size
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)
        
        # Validate file size
        if file_size == 0:
            return jsonify({'status': 'failure', 'message': 'Empty file'}), 400
        
        # Inefficient: Sequential file operations
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Save file without streaming (blocking operation)
        file.save(file_path)
        
        # Process image (this blocks the response)
        success, message = process_image_slow(file_path, file_size)
        
        elapsed_time = time.time() - start_time
        
        with metrics_lock:
            upload_metrics['total_uploads'] += 1
            upload_metrics['total_time'] += elapsed_time
            if success:
                upload_metrics['successful_uploads'] += 1
            else:
                upload_metrics['failed_uploads'] += 1
        
        if success:
            return jsonify({
                'status': 'success',
                'message': message,
                'filename': filename,
                'size': file_size,
                'upload_time': elapsed_time
            }), 200
        else:
            return jsonify({
                'status': 'failure',
                'message': message,
                'upload_time': elapsed_time
            }), 400
    
    except Exception as e:
        elapsed_time = time.time() - start_time
        with metrics_lock:
            upload_metrics['total_uploads'] += 1
            upload_metrics['failed_uploads'] += 1
            upload_metrics['total_time'] += elapsed_time
        
        return jsonify({
            'status': 'failure',
            'message': f'Upload failed: {str(e)}',
            'upload_time': elapsed_time
        }), 500


@app.route('/metrics', methods=['GET'])
def get_metrics():
    """Get current upload metrics."""
    with metrics_lock:
        metrics = upload_metrics.copy()
    
    if metrics['total_uploads'] > 0:
        metrics['average_time'] = metrics['total_time'] / metrics['total_uploads']
        metrics['success_rate'] = (metrics['successful_uploads'] / metrics['total_uploads']) * 100
    
    return jsonify(metrics), 200


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({'status': 'healthy', 'service': 'image-upload-pre-opt'}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
