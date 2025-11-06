import os
import time
import json
import threading
import requests
import tempfile
from subprocess import Popen

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
TEST_DATA = os.path.join(ROOT, 'test_data.json')
RESULT_FILE = os.path.join(ROOT, 'Project_A_PreOptimization_ImageUpload', 'performance', 'results_pre.json')
LOG_FILE = os.path.join(ROOT, 'Project_A_PreOptimization_ImageUpload', 'logs', 'log_pre.txt')

SERVER = 'http://127.0.0.1:5010'

# helper to start server
proc = None

def start_server():
    global proc
    proc = Popen(['python', 'src/server_pre.py'], cwd=os.path.join(ROOT, 'Project_A_PreOptimization_ImageUpload'))
    # wait for health
    for i in range(20):
        try:
            r = requests.get(SERVER + '/health', timeout=1)
            if r.status_code == 200:
                return True
        except Exception:
            time.sleep(0.5)
    return False


def stop_server():
    global proc
    if proc:
        proc.terminate()
        proc.wait()


def create_dummy_image(path, size_mb, corrupt=False):
    # Create a JPEG-like file for PIL to accept, or make it invalid for corrupt
    size_bytes = int(size_mb * 1024 * 1024)
    if corrupt:
        with open(path, 'wb') as f:
            f.write(os.urandom(min(size_bytes, 1024)))
        return
    # create a simple RGB image and then pad to target size
    from PIL import Image
    img = Image.new('RGB', (1000, 1000), color=(73,109,137))
    img.save(path, 'JPEG')
    # pad
    with open(path, 'ab') as f:
        remain = size_bytes - os.path.getsize(path)
        if remain > 0:
            f.write(b'\0' * remain)


def test_uploads():
    with open(TEST_DATA, 'r') as f:
        cases = json.load(f)

    start_ok = start_server()
    if not start_ok:
        print('Failed to start server')
        return

    results = []
    for tc in cases:
        id = tc['id']
        size_mb = tc['size_mb']
        corrupt = (tc['name'] == 'corrupt_image')
        simulate_mbps = tc.get('simulate_mbps', 10)

        fd, tmp = tempfile.mkstemp(suffix='.jpg')
        os.close(fd)
        create_dummy_image(tmp, size_mb, corrupt=corrupt)

        start = time.time()
        try:
            with open(tmp, 'rb') as f:
                headers = {'X-Simulate-Mbps': str(simulate_mbps)}
                r = requests.post(SERVER + '/upload', files={'file': f}, headers=headers, timeout=300)
            elapsed = time.time() - start
            success = r.status_code == 200 and r.json().get('status') == 'success'
            results.append({'id': id, 'expected': tc['expected_status'], 'status': r.json() if r is not None else None, 'success': success, 'time': elapsed})
        except Exception as e:
            elapsed = time.time() - start
            results.append({'id': id, 'expected': tc['expected_status'], 'status': str(e), 'success': False, 'time': elapsed})
        finally:
            os.remove(tmp)

    stop_server()

    # save results
    with open(RESULT_FILE, 'w') as f:
        json.dump(results, f, indent=2)
    with open(LOG_FILE, 'w') as f:
        f.write(json.dumps(results, indent=2))

    # print summary
    passed = sum(1 for r in results if r['success'])
    print(f'Project A Pre-Optimization: {passed}/{len(results)} tests passed')

if __name__ == '__main__':
    test_uploads()
