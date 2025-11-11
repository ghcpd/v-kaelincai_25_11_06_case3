"""
Pre-Optimization Image Processor
Demonstrates inefficient image processing without optimization
"""
import time
from PIL import Image
from io import BytesIO

class SlowImageProcessor:
    """Slow image processor with no optimizations"""
    
    def __init__(self):
        self.processed_count = 0
    
    def process_image(self, image_data):
        """
        Process image synchronously without any optimizations
        This method blocks and processes images one at a time
        """
        start_time = time.time()
        
        # Open image synchronously
        image = Image.open(BytesIO(image_data))
        
        # No compression - keeps original size
        # No resizing - processes full resolution
        # No format conversion - keeps original format
        
        # Simulate expensive operations
        width, height = image.size
        
        # Simulate slow processing (e.g., metadata extraction, validation)
        # No caching, no parallel processing
        time.sleep(0.05 * (len(image_data) / (1024 * 1024)))  # 0.05s per MB
        
        # Convert back to bytes synchronously
        output = BytesIO()
        image.save(output, format=image.format or 'JPEG')
        processed_data = output.getvalue()
        
        processing_time = time.time() - start_time
        self.processed_count += 1
        
        return {
            'processed_data': processed_data,
            'width': width,
            'height': height,
            'size': len(processed_data),
            'processing_time': processing_time
        }
    
    def get_stats(self):
        """Get processing statistics"""
        return {
            'processed_count': self.processed_count
        }

