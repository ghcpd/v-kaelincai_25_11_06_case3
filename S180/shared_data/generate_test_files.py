import os
import random
os.makedirs('c:\\chatWorkspace\\shared_data',exist_ok=True)
# Generate small (50KB), medium (2MB), large 200MB (simulate by zeros), and 500MB
sizes = {'small.jpg':50*1024, 'medium.jpg':2*1024*1024, 'large_200mb.bin':200*1024*1024, 'large_concurrent_500mb.bin':500*1024*1024}
for name, sz in sizes.items():
    path=os.path.join('c:\\chatWorkspace\\shared_data',name)
    if not os.path.exists(path):
        with open(path,'wb') as f:
            f.write(b'\0'*(min(sz,1024*1024)))
# For huge files, just create sparse-ish placeholder (to avoid huge repo size) - write 1MB and label as large
# Create corrupt file
with open('c:\\chatWorkspace\\shared_data\\corrupt.jpg','wb') as f:
    f.write(b'NOTJPEG')
print('Test fixtures created (placeholders).')
