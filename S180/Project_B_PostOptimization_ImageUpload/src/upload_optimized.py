from flask import Flask, request, jsonify
import os, time
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)
UPLOAD_DIR = 'uploads'
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Use thread pool and async writes to improve concurrency
executor = ThreadPoolExecutor(max_workers=8)

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files.get('file')
    if not file:
        return jsonify({'status':'failure','reason':'no_file'}), 400

    content = file.read()
    size_mb = len(content)/(1024*1024)

    # optimized processing: non-blocking background task
    def process_and_store(filename, content):
        # simulate optimized processing: only 0.05s per MB + minimal IO latency
        processing_time = 0.05 * size_mb
        time.sleep(processing_time)
        with open(filename,'wb') as f:
            f.write(content)
        return processing_time

    filename = os.path.join(UPLOAD_DIR, file.filename)
    future = executor.submit(process_and_store, filename, content)

    # return early with accepted status
    return jsonify({'status':'accepted','size_mb':size_mb}), 202

if __name__ == '__main__':
    app.run(port=5002)
