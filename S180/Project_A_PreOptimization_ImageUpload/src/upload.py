from flask import Flask, request, jsonify
import time
import os

app = Flask(__name__)
UPLOAD_DIR = 'uploads'
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Config: small concurrency allowed
MAX_CONCURRENT = 2
current_concurrent = 0

@app.route('/upload', methods=['POST'])
def upload():
    global current_concurrent
    file = request.files.get('file')
    if not file:
        return jsonify({'status':'failure','reason':'no_file'}), 400

    # Simulate slow backend processing: sleep proportional to file size
    content = file.read()
    size_mb = len(content) / (1024*1024)

    # Simulate concurrency limit failure
    if current_concurrent >= MAX_CONCURRENT:
        return jsonify({'status':'failure','reason':'server_overloaded'}), 503

    current_concurrent += 1
    try:
        # slow processing (e.g., unoptimized image resize, heavy CPU)
        processing_time = 0.5 * size_mb  # 0.5s per MB
        time.sleep(processing_time)
        filename = os.path.join(UPLOAD_DIR, file.filename)
        with open(filename, 'wb') as f:
            f.write(content)
    finally:
        current_concurrent -= 1

    return jsonify({'status':'success','size_mb':size_mb,'processing_time':processing_time}), 200

if __name__ == '__main__':
    app.run(port=5001)
