import json,glob,os,collections
R='/root/uap-tracker/research/'
files=sorted(glob.glob(R+'*.json'))
nodes={}   # id -> list of (file, kind, label, cls)
edges=[]
dupes=collections.defaultdict(list)
for f in files:
    dom=os.path.basename(f)[:-5]
    d=json.load(open(f))
    for p in d.get('people',[]):
        nodes.setdefault(p['id'],[]).append((dom,'person',p.get('label'),p.get('cls','person')))
    for e in d.get('entities',[]):
        nodes.setdefault(e['id'],[]).append((dom,'entity',e.get('label'),e.get('cls')))
    for ed in d.get('edges',[]):
        edges.append((dom,ed.get('a'),ed.get('b'),ed.get('type'),ed.get('note','')))
print("FILES:",len(files))
print("UNIQUE NODE IDS:",len(nodes))
print("TOTAL NODE RECORDS:",sum(len(v) for v in nodes.values()))
print("TOTAL EDGES:",len(edges))
dup={k:v for k,v in nodes.items() if len(v)>1}
print("IDS DEFINED IN >1 FILE:",len(dup))
# dangling
defined=set(nodes)
dang=collections.Counter()
dangsrc=collections.defaultdict(set)
for dom,a,b,t,n in edges:
    for x in (a,b):
        if x not in defined:
            dang[x]+=1
            dangsrc[x].add(dom)
print("DANGLING UNIQUE IDS:",len(dang))
print("DANGLING EDGE-ENDPOINT REFS:",sum(dang.values()))
json.dump({k:{'count':v,'files':sorted(dangsrc[k])} for k,v in dang.most_common()},open('/tmp/w2/dangling.json','w'),indent=1)
# degree
deg=collections.Counter()
for dom,a,b,t,n in edges:
    deg[a]+=1; deg[b]+=1
json.dump({k:deg.get(k,0) for k in nodes},open('/tmp/w2/degree.json','w'),indent=1)
json.dump({k:[list(x) for x in v] for k,v in dup.items()},open('/tmp/w2/dupes.json','w'),indent=1)
print()
print("TOP 60 DANGLING:")
for k,v in dang.most_common(60): print(f"  {v:3d}  {k}   <- {','.join(sorted(dangsrc[k]))}")
