import requests
import time
import json
import os
from math import ceil

ROOT = os.path.dirname(os.path.dirname(__file__))
DATA_FILE = os.path.join(ROOT, 'data', 'test_data.json')
RESULTS_FILE = os.path.join(ROOT, 'performance', 'results_post.json')
LOG_FILE = os.path.join(ROOT, 'logs', 'log_post.txt')

os.makedirs(os.path.join(ROOT, 'logs'), exist_ok=True)
os.makedirs(os.path.join(ROOT, 'performance'), exist_ok=True)

with open(DATA_FILE, 'r') as f:
    tests = json.load(f)['tests']

results = []
server_url = 'http://127.0.0.1:8001/upload'

def make_payload(size_mb, corrupt=False):
    size = int(size_mb * 1024 * 1024)
    data = bytearray([0xFF]) * size
    if corrupt:
        data = data[: max(1, len(data)//10)]
    return bytes(data)

def send_chunked(name, data, chunk_size=1024*1024*5):
    total = ceil(len(data)/chunk_size)
    for i in range(total):
        chunk = data[i*chunk_size:(i+1)*chunk_size]
        headers = {'X-Chunk-Index': str(i), 'X-Total-Chunks': str(total)}
        r = requests.post(server_url + f'?name={name}', data=chunk, headers=headers, timeout=300)
        if r.status_code not in (200,202):
            raise Exception('Chunk failed', r.status_code, r.text)
        if r.status_code == 200:
            return r
    return r

for t in tests:
    entry = {'id': t['id'], 'expected': t.get('expected')}
    payload = make_payload(t.get('file_size_mb', 1), t.get('corrupt', False))
    start = time.time()
    try:
        r = send_chunked(t['id'], payload)
        elapsed = time.time() - start
        entry.update({'status_code': r.status_code, 'time': elapsed})
        entry['success'] = (r.status_code == 200)
        try:
            entry['response'] = r.json()
        except:
            entry['response'] = r.text
    except Exception as e:
        elapsed = time.time() - start
        entry.update({'status_code': None, 'time': elapsed, 'success': False, 'error': str(e)})

    results.append(entry)

with open(RESULTS_FILE, 'w') as f:
    json.dump(results, f, indent=2)

with open(LOG_FILE, 'w') as f:
    for r in results:
        f.write(json.dumps(r) + '\n')

print('Post-optimization tests complete. Results saved to', RESULTS_FILE)
