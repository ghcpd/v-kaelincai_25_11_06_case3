import time
import os

def process_image(path: str) -> float:
    """
    Simulate a slow, CPU-bound image processing task by reading the file
    and performing blocking work proportional to size.
    Returns the simulated processing time in seconds.
    """
    size = os.path.getsize(path)
    size_mb = max(1, size / (1024 * 1024))

    # Slow processing: 0.15s per MB to simulate heavy resizing/filters
    processing_seconds = size_mb * 0.15

    # Do blocking sleep in small chunks to allow interruptibility in tests
    start = time.time()
    remaining = processing_seconds
    while remaining > 0:
        step = min(0.5, remaining)
        time.sleep(step)
        remaining -= step

    return time.time() - start
