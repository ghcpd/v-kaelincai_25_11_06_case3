import os
import time
import json
import threading
import requests
import tempfile
from subprocess import Popen

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
TEST_DATA = os.path.join(ROOT, 'test_data.json')
RESULT_FILE = os.path.join(ROOT, 'Project_B_PostOptimization_ImageUpload', 'performance', 'results_post.json')
LOG_FILE = os.path.join(ROOT, 'Project_B_PostOptimization_ImageUpload', 'logs', 'log_post.txt')

SERVER = 'http://127.0.0.1:5020'
proc = None

from tests.concurrent_helper import UploadThread


def start_server():
    global proc
    proc = Popen(['python', 'src/server_post.py'], cwd=os.path.join(ROOT, 'Project_B_PostOptimization_ImageUpload'))
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
    size_bytes = int(size_mb * 1024 * 1024)
    if corrupt:
        with open(path, 'wb') as f:
            f.write(os.urandom(min(size_bytes, 1024)))
        return
    from PIL import Image
    img = Image.new('RGB', (1200, 800), color=(255,255,255))
    img.save(path, 'JPEG')
    with open(path, 'ab') as f:
        remain = size_bytes - os.path.getsize(path)
        if remain > 0:
            f.write(b'\0' * remain)


def poll_status(uid, timeout=60):
    start_poll = time.time()
    while time.time() - start_poll < timeout:
        s = requests.get(SERVER + f'/status/{uid}', timeout=5)
        if s.json().get('status') == 'done':
            return True, s.json()
        if s.json().get('status') == 'failed':
            return False, s.json()
        time.sleep(0.5)
    return False, {'status': 'timeout'}


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

        if id == 't6':
            threads = []
            for i in range(5):
                t = UploadThread(SERVER, tmp, simulate_mbps)
                t.start()
                threads.append(t)
            for t in threads:
                t.join()
            subresults = []
            for t in threads:
                if t.result is None:
                    subresults.append({'success': False, 'error': 'no result'})
                elif 'error' in t.result:
                    subresults.append({'success': False, 'error': t.result['error']})
                else:
                    r = t.result['response']
                    elapsed = t.result['elapsed']
                    success = False
                    status_info = None
                    if r.status_code == 200 and r.json().get('status') == 'accepted':
                        uid = r.json().get('id')
                        s_ok, status_info = poll_status(uid, timeout=60)
                        success = s_ok
                    subresults.append({'success': success, 'time': elapsed, 'status': status_info})
            results.append({'id': id, 'expected': tc['expected_status'], 'subresults': subresults})
        else:
            start = time.time()
            try:
                r = UploadThread(SERVER, tmp, simulate_mbps)
                r.run()
                elapsed = r.result.get('elapsed') if r.result and 'elapsed' in r.result else None
                success = False
                status_info = None
                if r.result and 'response' in r.result:
                    resp = r.result['response']
                    if resp.status_code == 200 and resp.json().get('status') == 'accepted':
                        uid = resp.json().get('id')
                        s_ok, status_info = poll_status(uid, timeout=60)
                        success = s_ok
                results.append({'id': id, 'expected': tc['expected_status'], 'success': success, 'status': status_info, 'time': elapsed})
            except Exception as e:
                elapsed = time.time() - start
                results.append({'id': id, 'expected': tc['expected_status'], 'status': str(e), 'success': False, 'time': elapsed})
        # cleanup
        os.remove(tmp)

    stop_server()

    with open(RESULT_FILE, 'w') as f:
        json.dump(results, f, indent=2)
    with open(LOG_FILE, 'w') as f:
        f.write(json.dumps(results, indent=2))

    # compute time summary and write
    times = []
    successes = 0
    for r in results:
        if r['id'] == 't6':
            for s in r['subresults']:
                if s.get('time'):
                    times.append(s['time'])
                if s.get('success'):
                    successes += 1
        else:
            if r.get('time'):
                times.append(r['time'])
            if r.get('success'):
                successes += 1
    avg_time = sum(times) / len(times) if times else 0
    with open(os.path.join(ROOT, 'Project_B_PostOptimization_ImageUpload', 'performance', 'time_post.txt'), 'w') as tf:
        tf.write(json.dumps({'average_time': avg_time, 'successes': successes, 'total_requests': len(times)}))

    passed = 0
    for r in results:
        if r['id'] == 't6':
            succ = sum(1 for s in r['subresults'] if s['success'])
            if succ >= 3:
                passed += 1
        else:
            if r['success']:
                passed += 1

    print(f'Project B Post-Optimization: {passed}/{len(results)} tests passed')

if __name__ == '__main__':
    test_uploads()
