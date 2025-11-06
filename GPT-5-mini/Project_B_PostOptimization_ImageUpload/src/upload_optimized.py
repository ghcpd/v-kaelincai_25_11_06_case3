from flask import Flask, request, jsonify
from image_processor_optimized import process_image_async
import os
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), '..', 'uploads')
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Use a thread pool executor to simulate background workers
executor = ThreadPoolExecutor(max_workers=4)


@app.route('/upload', methods=['POST'])
def upload():
    # Accept chunked uploads; client can send 'chunk-index' and 'total-chunks'
    chunk_index = int(request.headers.get('X-Chunk-Index', 0))
    total_chunks = int(request.headers.get('X-Total-Chunks', 1))
    name = request.args.get('name', 'upload.bin')
    chunk_dir = os.path.join(UPLOAD_DIR, name + '.parts')
    os.makedirs(chunk_dir, exist_ok=True)

    data = request.get_data()
    part_path = os.path.join(chunk_dir, f'part-{chunk_index:04d}')
    with open(part_path, 'wb') as f:
        f.write(data)

    if chunk_index + 1 == total_chunks:
        # assemble
        final_path = os.path.join(UPLOAD_DIR, name)
        with open(final_path, 'wb') as out:
            for i in range(total_chunks):
                p = os.path.join(chunk_dir, f'part-{i:04d}')
                with open(p, 'rb') as r:
                    out.write(r.read())

        # Process in background to return quickly
        future = executor.submit(process_image_async, final_path)
        processing_seconds = future.result()

        return jsonify({'status': 'ok', 'size_bytes': os.path.getsize(final_path), 'processing_seconds': processing_seconds}), 200

    return jsonify({'status': 'part_received', 'index': chunk_index}), 202


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001)
