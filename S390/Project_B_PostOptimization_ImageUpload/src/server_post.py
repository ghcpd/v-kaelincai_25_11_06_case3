from flask import Flask, request, jsonify
import os
import time
from PIL import Image
import io
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), '..', 'uploads')
os.makedirs(UPLOAD_DIR, exist_ok=True)
executor = ThreadPoolExecutor(max_workers=10)

processing_status = {}

@app.route('/health')
def health():
    return 'ok'

def process_image_in_background(uid, content, filename):
    size = len(content)
    processing_time = (size / (1024.0*1024.0)) * 0.012
    time.sleep(processing_time)
    try:
        Image.open(io.BytesIO(content)).verify()
    except Exception:
        processing_status[uid] = {'status': 'failed', 'reason': 'corrupt image'}
        return
    file_path = os.path.join(UPLOAD_DIR, f'{int(time.time()*1000)}_{filename}')
    with open(file_path, 'wb') as f:
        f.write(content)
    processing_status[uid] = {'status': 'done', 'size_bytes': size}

@app.route('/upload', methods=['POST'])
def upload():
    speed = request.headers.get('X-Simulate-Mbps')
    file = request.files.get('file')
    if file is None:
        return jsonify({'status': 'error', 'reason': 'no file provided'}), 400

    content = file.read()
    size = len(content)

    if speed:
        try:
            mbps = float(speed)
            simulated_upload_time = (size * 8) / (mbps * 1_000_000)
            time.sleep(simulated_upload_time)
        except Exception:
            pass

    uid = str(time.time()).replace('.', '')
    processing_status[uid] = {'status': 'processing'}
    executor.submit(process_image_in_background, uid, content, file.filename)

    return jsonify({'status': 'accepted', 'id': uid})

@app.route('/status/<uid>')
def status(uid):
    return jsonify(processing_status.get(uid, {'status': 'not_found'}))

if __name__ == '__main__':
    app.run(port=5020)
