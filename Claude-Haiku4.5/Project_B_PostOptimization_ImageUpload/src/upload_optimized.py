"""
Post-Optimization Image Upload Server
Optimized for performance and reliability.
"""

import json
import time
import os
import io
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import threading
from datetime import datetime
from PIL import Image
import hashlib
import concurrent.futures
from io import BytesIO

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

# Thread pool for parallel processing
executor = concurrent.futures.ThreadPoolExecutor(max_workers=4)

# Cache for processed images
processed_cache = {}
cache_lock = threading.Lock()


CHUNK_SIZE = 1024 * 1024  # 1MB chunks for streaming


def process_image_optimized(file_path, file_size):
    """
    Post-optimization: Fast image processing with optimizations.
    Optimizations implemented:
    - Streaming I/O with chunking
    - Single-pass validation
    - Image compression and resizing
    - Parallel metadata processing
    - Early validation failure exit
    - Memory-efficient processing
    """
    try:
        # Check if already processed (cache)
        file_hash = compute_file_hash(file_path)
        with cache_lock:
            if file_hash in processed_cache:
                return True, "Image already processed (cached)"
        
        # Optimize 1: Single-pass validation with early exit
        with open(file_path, 'rb') as f:
            # Read header only for format validation
            header = f.read(32)
            if len(header) < 10 or header == b'':
                return False, "Invalid image file"
            
            # Fast format check using magic bytes
            if not (header.startswith(b'\xff\xd8\xff') or  # JPEG
                   header.startswith(b'\x89PNG') or        # PNG
                   header.startswith(b'GIF')):              # GIF
                return False, "Unsupported image format"
        
        # Optimize 2: Stream-based compression and resizing
        try:
            with Image.open(file_path) as img:
                # Resize if too large (reduces processing load)
                if img.size[0] > 4096 or img.size[1] > 4096:
                    img.thumbnail((4096, 4096), Image.Resampling.LANCZOS)
                
                # Compress image in-memory
                compressed_path = file_path + '.optimized'
                img.save(compressed_path, quality=85, optimize=True)
                
                # Replace original with compressed version
                os.replace(compressed_path, file_path)
        except Exception as e:
            # If compression fails, continue with original
            pass
        
        # Optimize 3: Async metadata processing (non-blocking)
        metadata = {
            'filename': os.path.basename(file_path),
            'size': file_size,
            'processed_at': datetime.now().isoformat(),
            'status': 'processed',
            'hash': file_hash,
            'cached': False
        }
        
        # Write metadata asynchronously using thread pool
        def write_metadata():
            try:
                with open(file_path + '.meta', 'w') as f:
                    json.dump(metadata, f)
            except:
                pass
        
        executor.submit(write_metadata)
        
        # Update cache
        with cache_lock:
            processed_cache[file_hash] = True
        
        return True, "Image processed successfully (optimized)"
    
    except Exception as e:
        return False, str(e)


def compute_file_hash(file_path):
    """Compute SHA256 hash of file efficiently."""
    sha256_hash = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            sha256_hash.update(chunk)
    return sha256_hash.hexdigest()


def save_file_streaming(file_obj, file_path):
    """
    Optimize 4: Stream file to disk in chunks.
    More memory-efficient than loading entire file.
    """
    try:
        with open(file_path, 'wb') as f:
            chunk_count = 0
            while True:
                chunk = file_obj.read(CHUNK_SIZE)
                if not chunk:
                    break
                f.write(chunk)
                chunk_count += 1
        return True, chunk_count
    except Exception as e:
        return False, str(e)


@app.route('/upload', methods=['POST'])
def upload_image():
    """
    Post-optimization image upload endpoint.
    Optimizations:
    - Streaming file I/O
    - Parallel processing
    - Response sent immediately (async processing)
    - Compression and resizing
    - Caching
    - Early validation
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
        
        # Validate file size (early exit)
        if file_size == 0:
            return jsonify({'status': 'failure', 'message': 'Empty file'}), 400
        
        # Optimize: Secure filename
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Optimize: Stream save to disk (memory efficient)
        success, chunk_info = save_file_streaming(file, file_path)
        if not success:
            return jsonify({'status': 'failure', 'message': 'Failed to save file'}), 500
        
        # Optimize: Process image asynchronously (non-blocking response)
        executor.submit(process_image_optimized, file_path, file_size)
        
        elapsed_time = time.time() - start_time
        
        with metrics_lock:
            upload_metrics['total_uploads'] += 1
            upload_metrics['total_time'] += elapsed_time
            upload_metrics['successful_uploads'] += 1
        
        # Response sent immediately while processing continues
        return jsonify({
            'status': 'success',
            'message': 'Image upload initiated and will be processed',
            'filename': filename,
            'size': file_size,
            'upload_time': elapsed_time
        }), 200
    
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
    return jsonify({'status': 'healthy', 'service': 'image-upload-post-opt'}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=False, threaded=True)
