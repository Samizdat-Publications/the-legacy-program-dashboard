import json,glob,os,collections
R='/root/uap-tracker/research/'
files=sorted(glob.glob(R+'*.json'))
nodes={}; people={}; ents={}
edges=[]; tl=[]
einfo={}
for f in files:
    dom=os.path.basename(f)[:-5]
    d=json.load(open(f))
    for p in d.get('people',[]):
        p['_f']=dom; people.setdefault(p['id'],[]).append(p); nodes.setdefault(p['id'],[]).append((dom,'person',p.get('label')))
    for e in d.get('entities',[]):
        e['_f']=dom; ents.setdefault(e['id'],[]).append(e); nodes.setdefault(e['id'],[]).append((dom,e.get('cls'),e.get('label')))
    for ed in d.get('edges',[]): ed['_f']=dom; edges.append(ed)
    for t in d.get('timeline',[]): t['_f']=dom; tl.append(t)
    for k,v in (d.get('entityInfo') or {}).items(): einfo.setdefault(k,[]).append(dom)
defined=set(nodes)
# instId/locId refs
ref=collections.Counter(); refsrc=collections.defaultdict(set)
for pid,ps in people.items():
    for p in ps:
        for k in ('instId','locId'):
            v=p.get(k)
            if v and v not in defined:
                ref[v]+=1; refsrc[v].add(p['_f']+':'+k)
print("DANGLING instId/locId:",len(ref))
for k,v in ref.most_common(): print(f"  {v:3d} {k}  <- {','.join(sorted(refsrc[k]))}")
# timeline node refs
tref=collections.Counter()
for t in tl:
    for n in (t.get('nodes') or []):
        if n not in defined: tref[n]+=1
print("\nDANGLING timeline node refs:",len(tref), tref.most_common(20))
# entityInfo keys not defined
print("\nentityInfo keys with no node:",[k for k in einfo if k not in defined])
print("TIMELINE ENTRIES:",len(tl))
# degree
deg=collections.Counter()
for ed in edges: deg[ed['a']]+=1; deg[ed['b']]+=1
# source counts
def srccount(rec): return len(rec.get('sources') or [])
def claimcount(rec): return len(rec.get('claims') or [])
rows=[]
for nid,recs in nodes.items():
    allrecs = people.get(nid,[])+ents.get(nid,[])
    s=sum(srccount(r) for r in allrecs)
    uniqurl=set()
    for r in allrecs:
        for sr in (r.get('sources') or []):
            if isinstance(sr,dict) and sr.get('url'): uniqurl.add(sr['url'])
    # entityInfo sources
    rows.append((nid,recs[0][1],recs[0][2],deg.get(nid,0),len(uniqurl),sum(claimcount(r) for r in allrecs),','.join(sorted({r['_f'] for r in allrecs}))))
json.dump(rows,open('/tmp/w2/rows.json','w'),indent=0)
thin=[r for r in rows if r[4]<2]
print("\nNODES WITH <2 UNIQUE SOURCE URLS:",len(thin))
for r in sorted(thin,key=lambda x:-x[3])[:70]: print(f"  deg={r[3]:3d} src={r[4]} claims={r[5]} {r[0]} [{r[1]}] ({r[6]})")
