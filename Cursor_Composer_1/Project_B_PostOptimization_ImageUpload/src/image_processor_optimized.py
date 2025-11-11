"""
Post-Optimization Image Processor
Optimized with compression, resizing, and parallel processing
"""
import time
from PIL import Image
from io import BytesIO
from concurrent.futures import ThreadPoolExecutor
import threading

class OptimizedImageProcessor:
    """Optimized image processor with compression and parallel processing"""
    
    def __init__(self, max_workers=4):
        self.processed_count = 0
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.lock = threading.Lock()
    
    def process_image(self, image_data, max_dimension=2048, quality=85):
        """
        Process image with optimizations:
        - Automatic resizing for large images
        - Compression to reduce file size
        - Optimized format conversion
        """
        start_time = time.time()
        
        # Open image
        image = Image.open(BytesIO(image_data))
        original_size = len(image_data)
        original_width, original_height = image.size
        
        # OPTIMIZATION 1: Resize if too large
        if original_width > max_dimension or original_height > max_dimension:
            ratio = min(max_dimension / original_width, max_dimension / original_height)
            new_width = int(original_width * ratio)
            new_height = int(original_height * ratio)
            image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # OPTIMIZATION 2: Compress image
        output = BytesIO()
        # Use optimized JPEG with quality setting
        image.save(output, format='JPEG', quality=quality, optimize=True)
        processed_data = output.getvalue()
        
        processing_time = time.time() - start_time
        
        with self.lock:
            self.processed_count += 1
        
        compression_ratio = (1 - len(processed_data) / original_size) * 100 if original_size > 0 else 0
        
        return {
            'processed_data': processed_data,
            'original_width': original_width,
            'original_height': original_height,
            'final_width': image.width,
            'final_height': image.height,
            'original_size': original_size,
            'compressed_size': len(processed_data),
            'compression_ratio': compression_ratio,
            'processing_time': processing_time
        }
    
    def process_batch(self, image_data_list, max_dimension=2048, quality=85):
        """Process multiple images in parallel"""
        futures = []
        for image_data in image_data_list:
            future = self.executor.submit(self.process_image, image_data, max_dimension, quality)
            futures.append(future)
        
        results = []
        for future in futures:
            results.append(future.result())
        
        return results
    
    def get_stats(self):
        """Get processing statistics"""
        return {
            'processed_count': self.processed_count
        }
    
    def shutdown(self):
        """Shutdown the executor"""
        self.executor.shutdown(wait=True)

