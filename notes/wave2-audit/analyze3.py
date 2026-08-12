import json,glob,os,collections,re
R='/root/uap-tracker/research/'
files=sorted(glob.glob(R+'*.json'))
nodes={}; recs=collections.defaultdict(list); edges=[]
einfo={}
for f in files:
    dom=os.path.basename(f)[:-5]
    d=json.load(open(f))
    for p in d.get('people',[]): p['_f']=dom;p['_k']='person';recs[p['id']].append(p);nodes[p['id']]=('person',p.get('label'))
    for e in d.get('entities',[]): e['_f']=dom;e['_k']=e.get('cls');recs[e['id']].append(e);nodes[e['id']]=(e.get('cls'),e.get('label'))
    for ed in d.get('edges',[]): ed['_f']=dom; edges.append(ed)
    for k,v in (d.get('entityInfo') or {}).items(): einfo.setdefault(k,[]).append((dom,v))
deg=collections.Counter()
for ed in edges: deg[ed['a']]+=1; deg[ed['b']]+=1
print("=== TOP 45 BY DEGREE ===")
for nid,c in deg.most_common(45):
    k=nodes.get(nid,('DANGLING',''))
    print(f"  {c:4d}  {nid} [{k[0]}]")
print()
print("=== MAJOR NODES WITH LOW DEGREE (deg<=4) but appearing in >=2 files or with big dossiers ===")
for nid,rs in recs.items():
    if deg.get(nid,0)<=4 and (len({r['_f'] for r in rs})>=2):
        print(f"  deg={deg.get(nid,0):2d} files={len({r['_f'] for r in rs})} {nid} [{nodes[nid][0]}]")
