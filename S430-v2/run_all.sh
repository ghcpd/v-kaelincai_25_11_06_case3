#!/usr/bin/env bash
set -e

# Run Project A
pushd Project_A_PreOptimization_ImageUpload
python -m pip install -r requirements.txt
python tests/test_pre_optimization.py
popd

# Run Project B
pushd Project_B_PostOptimization_ImageUpload
python -m pip install -r requirements.txt
python tests/test_post_optimization.py
popd

# Compare results
python - <<'PY'
import json
from pathlib import Path
ra = Path('Project_A_PreOptimization_ImageUpload/performance/results_pre.json')
rb = Path('Project_B_PostOptimization_ImageUpload/performance/results_post.json')
if not ra.exists() or not rb.exists():
    print('Missing results files')
    exit(1)
ra = json.loads(ra.read_text())
rb = json.loads(rb.read_text())

summary = {}
for a in ra:
    tid = a['id']
    b = next((x for x in rb if x['id']==tid), None)
    summary[tid] = {'pre_time': a['time'], 'pre_success': a['success'], 'post_time': b['time'] if b else None, 'post_success': b['success'] if b else None}

with open('compare_report.md', 'w') as f:
    f.write('# Upload Performance Comparison\n\n')
    f.write('Comparing upload times and success rates between Pre and Post optimized services.\n\n')
    for tid, val in summary.items():
        f.write(f'## {tid}\n')
        f.write(f'- pre_time: {val["pre_time"]}\n')
        f.write(f'- post_time: {val["post_time"]}\n')
        f.write(f'- pre_success: {val["pre_success"]}\n')
        f.write(f'- post_success: {val["post_success"]}\n\n')
print('Comparison saved to compare_report.md')
PY

cat compare_report.md
