import json
from pathlib import Path

pre = Path('Project_A_PreOptimization_ImageUpload/performance/results_pre.json')
post = Path('Project_B_PostOptimization_ImageUpload/performance/results_post.json')
out = Path('compare_report.md')

def load(p):
    if not p.exists():
        return []
    return json.loads(p.read_text())

pre_r = load(pre)
post_r = load(post)

def summarize(rs):
    total = len(rs)
    success = sum(1 for r in rs if r.get('success'))
    avg_time = sum(r.get('time',0) for r in rs)/total if total else 0
    return total, success, avg_time

pt, ps, pat = summarize(pre_r)
ot, os_, oat = summarize(post_r)

with out.open('w') as f:
    f.write('# Comparison Report\n\n')
    f.write('## Summary Metrics\n')
    f.write(f'- Pre: {ps}/{pt} success, avg time {pat:.2f}s\n')
    f.write(f'- Post: {os_}/{ot} success, avg time {oat:.2f}s\n')
    if pat and oat:
        improvement = (pat - oat)/pat*100
        f.write(f'- Avg time improvement: {improvement:.2f}%\n')

    f.write('\n## Details\n')
    f.write('### Pre results\n')
    for r in pre_r:
        f.write(f'- {r.get("id")}: success={r.get("success")}, time={r.get("time")}s\n')

    f.write('\n### Post results\n')
    for r in post_r:
        f.write(f'- {r.get("id")}: success={r.get("success")}, time={r.get("time")}s\n')

print('compare_report.md written')
