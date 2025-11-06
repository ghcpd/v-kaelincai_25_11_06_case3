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

# Aggregate
python - <<'PY'
import json
from pathlib import Path
pa = Path('Project_A_PreOptimization_ImageUpload/performance/results_pre.json')
pb = Path('Project_B_PostOptimization_ImageUpload/performance/results_post.json')
pta = Path('Project_A_PreOptimization_ImageUpload/performance/time_pre.txt')
ptb = Path('Project_B_PostOptimization_ImageUpload/performance/time_post.txt')
if not pa.exists() or not pb.exists():
    print('Missing results files')
    exit(1)
ra = json.loads(pa.read_text())
rb = json.loads(pb.read_text())
pta_json = json.loads(pta.read_text()) if pta.exists() else {}
ptb_json = json.loads(ptb.read_text()) if ptb.exists() else {}

summary = {}
for a in ra:
    tid = a['id']
    b = next((x for x in rb if x['id']==tid), None)
    summary[tid] = {'pre_time': a.get('time'), 'pre_success': a.get('success'), 'post_time': b.get('time') if b else None, 'post_success': b.get('success') if b else None}

with open('compare_report.md', 'w') as f:
    f.write('# Upload Performance Comparison\n\n')

# Also write a machine-readable summary
with open('s_shared_artifacts/results/compare_summary.json', 'w') as cs:
    json.dump({'summary': summary, 'pre_avg_time': pre_avg, 'post_avg_time': post_avg, 'improvement_pct': improvement}, cs, indent=2)

    f.write('Summary metrics (averages):\n')
    f.write(f'- Pre average time: {pta_json.get("average_time")}\n')
    f.write(f'- Post average time: {ptb_json.get("average_time")}\n')
    pre_avg = pta_json.get("average_time") or 0
    post_avg = ptb_json.get("average_time") or 0
    if pre_avg and post_avg:
        improvement = ((pre_avg - post_avg) / pre_avg) * 100
    else:
        improvement = None
    f.write(f'- Time improvement: {improvement}%\n')
    f.write(f'- Pre total successes: {pta_json.get("successes")}\n')
    f.write(f'- Post total successes: {ptb_json.get("successes")}\n\n')
    f.write('Per-test comparison:\n\n')
    for tid, val in summary.items():
        f.write(f'## {tid}\n')
        f.write(f'- pre_time: {val["pre_time"]}\n')
        f.write(f'- post_time: {val["post_time"]}\n')
        f.write(f'- pre_success: {val["pre_success"]}\n')
        f.write(f'- post_success: {val["post_success"]}\n\n')
print('Comparison saved to compare_report.md')
PY

cat compare_report.md
