from flask import Flask, request, jsonify
import os
import time
from PIL import Image
import io

app = Flask(__name__)
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), '..', 'uploads')
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.route('/health')
def health():
    return 'ok'

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

    # Processing time: 0.05 sec/MB (slow)
    processing_time = (size / (1024.0*1024.0)) * 0.05
    time.sleep(processing_time)

    try:
        Image.open(io.BytesIO(content)).verify()
    except Exception:
        return jsonify({'status': 'error', 'reason': 'corrupt image'}), 400

    file_path = os.path.join(UPLOAD_DIR, f'{int(time.time()*1000)}_{file.filename}')
    with open(file_path, 'wb') as f:
        f.write(content)

    return jsonify({'status': 'success', 'size_bytes': size})

if __name__ == '__main__':
    app.run(port=5010)
