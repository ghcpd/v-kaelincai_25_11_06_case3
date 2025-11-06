import threading
import time
import requests

class UploadThread(threading.Thread):
    def __init__(self, server, path, speed):
        super().__init__()
        self.server = server
        self.path = path
        self.speed = speed
        self.result = None

    def run(self):
        with open(self.path, 'rb') as f:
            headers = {'X-Simulate-Mbps': str(self.speed)}
            start = time.time()
            try:
                r = requests.post(self.server + '/upload', files={'file': f}, headers=headers, timeout=600)
                elapsed = time.time() - start
                self.result = {'response': r, 'elapsed': elapsed}
            except Exception as e:
                self.result = {'error': str(e)}
