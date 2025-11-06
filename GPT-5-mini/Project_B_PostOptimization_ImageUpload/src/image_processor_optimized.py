import time
import os
from concurrent.futures import ThreadPoolExecutor


def process_image_async(path: str) -> float:
    """
    Simulate faster processing using concurrent workers and chunked I/O.
    Returns simulated processing duration.
    """
    size = os.path.getsize(path)
    size_mb = max(1, size / (1024 * 1024))

    # Optimized processing: 0.04s per MB with parallel chunks
    processing_seconds = size_mb * 0.04

    # Simulate parallel chunk processing
    chunks = min(8, max(1, int(size_mb)))
    def work(chunk_id):
        time.sleep(processing_seconds / chunks)

    start = time.time()
    with ThreadPoolExecutor(max_workers=chunks) as ex:
        futures = [ex.submit(work, i) for i in range(chunks)]
        for f in futures:
            f.result()

    return time.time() - start
