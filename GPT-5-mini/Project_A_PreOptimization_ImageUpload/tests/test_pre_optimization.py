import requests
import time
import json
import os

ROOT = os.path.dirname(os.path.dirname(__file__))
DATA_FILE = os.path.join(ROOT, 'data', 'test_data.json')
RESULTS_FILE = os.path.join(ROOT, 'performance', 'results_pre.json')
LOG_FILE = os.path.join(ROOT, 'logs', 'log_pre.txt')

os.makedirs(os.path.join(ROOT, 'logs'), exist_ok=True)
os.makedirs(os.path.join(ROOT, 'performance'), exist_ok=True)

with open(DATA_FILE, 'r') as f:
    tests = json.load(f)['tests']

results = []
server_url = 'http://127.0.0.1:8000/upload'

def make_payload(size_mb, corrupt=False):
    size = int(size_mb * 1024 * 1024)
    data = bytearray([0xFF]) * size
    if corrupt:
        # Truncate to simulate corruption
        data = data[: max(1, len(data)//10)]
    return bytes(data)

for t in tests:
    entry = {'id': t['id'], 'expected': t.get('expected')}
    payload = make_payload(t.get('file_size_mb', 1), t.get('corrupt', False))
    start = time.time()
    try:
        r = requests.post(server_url + '?name=%s.bin' % t['id'], data=payload, timeout=300)
        elapsed = time.time() - start
        entry.update({'status_code': r.status_code, 'time': elapsed})
        if r.status_code == 200:
            entry['success'] = True
        else:
            entry['success'] = False
        entry['response'] = r.json()
    except Exception as e:
        elapsed = time.time() - start
        entry.update({'status_code': None, 'time': elapsed, 'success': False, 'error': str(e)})

    results.append(entry)

with open(RESULTS_FILE, 'w') as f:
    json.dump(results, f, indent=2)

with open(LOG_FILE, 'w') as f:
    for r in results:
        f.write(json.dumps(r) + '\n')

print('Pre-optimization tests complete. Results saved to', RESULTS_FILE)
