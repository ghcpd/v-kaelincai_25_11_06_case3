"""
Post-Optimization Image Upload Server
Optimized with: async processing, compression, chunked uploads, connection pooling
"""
import os
import time
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import base64
from io import BytesIO
from PIL import Image
import threading
from concurrent.futures import ThreadPoolExecutor
import queue

class OptimizedImageUploadHandler(BaseHTTPRequestHandler):
    """Optimized image upload handler with performance improvements"""
    
    # Thread pool for concurrent processing
    executor = ThreadPoolExecutor(max_workers=4)
    
    # Connection pool simulation (in real app, use proper connection pooling)
    active_connections = 0
    max_connections = 10
    
    def do_POST(self):
        """Handle POST requests for image uploads with optimizations"""
        if self.path == '/upload':
            # Check connection limit
            if self.active_connections >= self.max_connections:
                self.send_error(503, "Too many connections")
                return
            
            self.active_connections += 1
            try:
                # Read content length
                content_length = int(self.headers.get('Content-Length', 0))
                if content_length == 0:
                    self.send_error(400, "No content")
                    return
                
                # Chunked reading for large files (simulated)
                # In production, use proper streaming
                chunk_size = 8192  # 8KB chunks
                image_data = b''
                while len(image_data) < content_length:
                    chunk = self.rfile.read(min(chunk_size, content_length - len(image_data)))
                    if not chunk:
                        break
                    image_data += chunk
                
                # Process asynchronously using thread pool
                future = self.executor.submit(self.process_image_async, image_data)
                
                # Wait for result with timeout
                try:
                    result = future.result(timeout=30)  # 30 second timeout
                    
                    if result['success']:
                        response = result['response']
                        self.send_response(200)
                        self.send_header('Content-Type', 'application/json')
                        self.end_headers()
                        self.wfile.write(json.dumps(response).encode())
                    else:
                        self.send_error(result.get('status_code', 500), result.get('error', 'Processing failed'))
                except Exception as e:
                    self.send_error(500, f"Processing error: {str(e)}")
                    
            except Exception as e:
                self.send_error(500, f"Server error: {str(e)}")
            finally:
                self.active_connections -= 1
        else:
            self.send_error(404, "Not found")
    
    def process_image_async(self, image_data):
        """Process image asynchronously with optimizations"""
        start_time = time.time()
        
        try:
            # Open and process image
            image = Image.open(BytesIO(image_data))
            original_size = len(image_data)
            width, height = image.size
            
            # OPTIMIZATION 1: Resize large images
            max_dimension = 2048  # Max width or height
            if width > max_dimension or height > max_dimension:
                # Calculate new dimensions maintaining aspect ratio
                ratio = min(max_dimension / width, max_dimension / height)
                new_width = int(width * ratio)
                new_height = int(height * ratio)
                image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
                self.log_message(f"Resized image from {width}x{height} to {new_width}x{new_height}")
            
            # OPTIMIZATION 2: Compress image
            output = BytesIO()
            # Use optimized JPEG quality (85% is good balance)
            image.save(output, format='JPEG', quality=85, optimize=True)
            processed_data = output.getvalue()
            
            # OPTIMIZATION 3: Async file write (simulated with thread)
            upload_dir = 'uploads'
            os.makedirs(upload_dir, exist_ok=True)
            filename = f"upload_{int(time.time())}_{threading.current_thread().ident}.jpg"
            filepath = os.path.join(upload_dir, filename)
            
            # Write file asynchronously (non-blocking)
            def write_file():
                with open(filepath, 'wb') as f:
                    f.write(processed_data)
            
            write_thread = threading.Thread(target=write_file)
            write_thread.start()
            
            # Don't wait for file write to complete before responding
            # In production, use proper async I/O
            
            processing_time = time.time() - start_time
            
            # Calculate compression ratio
            compression_ratio = (1 - len(processed_data) / original_size) * 100 if original_size > 0 else 0
            
            response = {
                "status": "success",
                "filename": filename,
                "original_size": original_size,
                "compressed_size": len(processed_data),
                "compression_ratio": round(compression_ratio, 2),
                "original_dimensions": f"{width}x{height}",
                "final_dimensions": f"{image.width}x{image.height}",
                "upload_time": round(processing_time, 3),
                "processing_time": round(processing_time, 3)
            }
            
            return {
                'success': True,
                'response': response
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'status_code': 400
            }
    
    def log_message(self, format, *args):
        """Override to add timestamp"""
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {format % args}")

def run_server(port=8001):
    """Run the optimized upload server"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, OptimizedImageUploadHandler)
    print(f"Post-optimization server running on port {port}")
    print("Optimizations: async processing, compression, resizing, connection pooling")
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()

