from flask import Flask, request, jsonify
from image_processor import process_image
import os

app = Flask(__name__)
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), '..', 'uploads')
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.route('/upload', methods=['POST'])
def upload():
    data = request.get_data()
    filename = request.args.get('name', 'upload.bin')
    path = os.path.join(UPLOAD_DIR, filename)
    with open(path, 'wb') as f:
        f.write(data)

    size_bytes = len(data)
    # Simulate slow, synchronous processing that blocks the worker
    processing_seconds = process_image(path)

    return jsonify({
        'status': 'ok',
        'size_bytes': size_bytes,
        'processing_seconds': processing_seconds,
    }), 200


if __name__ == '__main__':
    # Run the Flask dev server (single-threaded) to demonstrate bottleneck
    app.run(host='0.0.0.0', port=8000)
