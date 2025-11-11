"""
Pre-Optimization Image Upload Server
Demonstrates performance bottlenecks: synchronous processing, no compression, blocking I/O
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

class SlowImageUploadHandler(BaseHTTPRequestHandler):
    """Slow image upload handler with performance bottlenecks"""
    
    def do_POST(self):
        """Handle POST requests for image uploads"""
        if self.path == '/upload':
            try:
                # Read entire request body synchronously (blocking)
                content_length = int(self.headers.get('Content-Length', 0))
                if content_length == 0:
                    self.send_error(400, "No content")
                    return
                
                # Read all data at once - blocks until complete
                image_data = self.rfile.read(content_length)
                
                # Simulate slow processing - no optimization
                start_time = time.time()
                
                # Decode image synchronously
                try:
                    image = Image.open(BytesIO(image_data))
                    # Process image synchronously - no compression or resizing
                    # This simulates expensive operations
                    width, height = image.size
                    
                    # Simulate slow backend processing
                    # In real scenario: database writes, file system I/O, etc.
                    time.sleep(0.1 * (len(image_data) / (1024 * 1024)))  # 0.1s per MB
                    
                    # Simulate server overload during peak traffic
                    # No connection pooling, no async processing
                    processing_time = time.time() - start_time
                    
                    # Save image synchronously (blocking I/O)
                    upload_dir = 'uploads'
                    os.makedirs(upload_dir, exist_ok=True)
                    filename = f"upload_{int(time.time())}.jpg"
                    filepath = os.path.join(upload_dir, filename)
                    
                    # Synchronous file write - blocks
                    with open(filepath, 'wb') as f:
                        f.write(image_data)
                    
                    total_time = time.time() - start_time
                    
                    # Simulate failures during peak traffic (high load)
                    if total_time > 5.0:  # If processing takes too long, simulate failure
                        self.send_error(503, "Server overloaded")
                        return
                    
                    response = {
                        "status": "success",
                        "filename": filename,
                        "size": len(image_data),
                        "dimensions": f"{width}x{height}",
                        "upload_time": round(total_time, 3),
                        "processing_time": round(processing_time, 3)
                    }
                    
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps(response).encode())
                    
                except Exception as e:
                    self.send_error(400, f"Invalid image: {str(e)}")
                    
            except Exception as e:
                self.send_error(500, f"Server error: {str(e)}")
        else:
            self.send_error(404, "Not found")
    
    def log_message(self, format, *args):
        """Override to add timestamp"""
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {format % args}")

def run_server(port=8000):
    """Run the slow upload server"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, SlowImageUploadHandler)
    print(f"Pre-optimization server running on port {port}")
    print("Performance bottlenecks: synchronous processing, no compression, blocking I/O")
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()

