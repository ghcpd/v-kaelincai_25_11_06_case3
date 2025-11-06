import requests
import time
import json
import os

API='http://127.0.0.1:5001/upload'

with open('..\\data\\test_data.json') as f:
    TESTS=json.load(f)

results=[]
for t in TESTS:
    tid=t['id']
    path=t['input_payload'].get('file_path')
    expected=t['expected_status']

    def send_once():
        start=time.time()
        if path and os.path.exists(path):
            files={'file': open(path,'rb')}
        else:
            files={'file': ('bad.jpg', b'not an image')}
        resp=requests.post(API, files=files)
        elapsed=time.time()-start
        try:
            data=resp.json()
            status='success' if resp.status_code==200 else 'failure'
        except Exception as e:
            data={'error':str(e)}
            status='failure'
        return {'id':tid,'status':status,'elapsed':elapsed,'response':data}

    if tid=='t5':
        # concurrency test: run 4 parallel uploads
        import threading
        threads=[]
        out=[]
        def runner():
            out.append(send_once())
        for i in range(4):
            th=threading.Thread(target=runner)
            th.start()
            threads.append(th)
        for th in threads: th.join()
        results.extend(out)
        for r in out: print(r)
    else:
        r=send_once()
        results.append(r)
        print(r)

with open('../results_pre.json','w') as f:
    json.dump(results,f,indent=2)
