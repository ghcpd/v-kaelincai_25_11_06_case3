import threading
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
            try:
                r = requests.post(self.server + '/upload', files={'file': f}, headers=headers)
                self.result = r
            except Exception as e:
                self.result = e
