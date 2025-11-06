import json
import os
pre=open('../Project_A_PreOptimization_ImageUpload/results_pre.json').read() if os.path.exists('../Project_A_PreOptimization_ImageUpload/results_pre.json') else '[]'
post=open('../Project_B_PostOptimization_ImageUpload/results_post.json').read() if os.path.exists('../Project_B_PostOptimization_ImageUpload/results_post.json') else '[]'
pre=json.loads(pre)
post=json.loads(post)

summary={'pre':{'count':len(pre),'avg_time':None},'post':{'count':len(post),'avg_time':None}}
if pre:
    summary['pre']['avg_time']=sum([r['elapsed'] for r in pre])/len(pre)
if post:
    summary['post']['avg_time']=sum([r['elapsed'] for r in post])/len(post)

with open('../compare_report.md','w') as f:
    f.write('# Compare Report\n\n')
    f.write('Pre avg time: %s\n' % summary['pre']['avg_time'])
    f.write('Post avg time: %s\n' % summary['post']['avg_time'])
    f.write('\nDetailed results:\n')
    f.write('## Pre\n')
    f.write(json.dumps(pre,indent=2))
    f.write('\n\n## Post\n')
    f.write(json.dumps(post,indent=2))

print('Report generated: compare_report.md')
