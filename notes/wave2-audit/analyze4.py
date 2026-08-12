import json,glob,os,collections,re
from urllib.parse import urlparse
R='/root/uap-tracker/research/'
urls=collections.defaultdict(set)  # url -> files
allclaims=[]
for f in sorted(glob.glob(R+'*.json')):
    dom=os.path.basename(f)[:-5]
    d=json.load(open(f))
    def walk(o,path=''):
        if isinstance(o,dict):
            if 'url' in o and isinstance(o['url'],str): urls[o['url']].add(dom)
            for k,v in o.items(): walk(v,path+'/'+str(k))
        elif isinstance(o,list):
            for v in o: walk(v,path)
    walk(d)
    for coll,kind in ((d.get('people',[]),'person'),(d.get('entities',[]),'entity')):
        for r in coll:
            for c in (r.get('claims') or []):
                allclaims.append((dom,r['id'],c.get('tier'),c.get('source',''),c.get('text','')[:120]))
    for k,v in (d.get('entityInfo') or {}).items():
        if isinstance(v,dict):
            for c in (v.get('claims') or []):
                allclaims.append((dom,k,c.get('tier'),c.get('source',''),c.get('text','')[:120]))
print("UNIQUE URLS:",len(urls))
hosts=collections.Counter(urlparse(u).netloc for u in urls)
print("\nHOSTS:")
for h,c in hosts.most_common(60): print(f"  {c:4d} {h}")
print("\nTOTAL CLAIMS:",len(allclaims))
tc=collections.Counter(c[2] for c in allclaims); print("BY TIER:",dict(tc))
# tier1 with weak source
weak=[c for c in allclaims if c[2]==1 and (not c[3] or len(c[3])<12 or re.search(r'no attributed|unknown|n/a|see above',c[3],re.I))]
print("\nTIER-1 CLAIMS WITH WEAK/EMPTY SOURCE:",len(weak))
for c in weak[:40]: print("  ",c[0],c[1],'|',c[3],'|',c[4])
# tier1 sourced to secondary media
sec=[c for c in allclaims if c[2]==1 and re.search(r'youtube|podcast|substack|reddit|wikipedia|twitter|x\.com|medium\.com|joe rogan|newsnation|interview',c[3],re.I)]
print("\nTIER-1 SOURCED TO MEDIA/SECONDARY:",len(sec))
for c in sec[:50]: print("  ",c[0],'|',c[1],'|',c[3][:110])
json.dump(sorted([(u,sorted(v)) for u,v in urls.items()]),open('/tmp/w2/urls.json','w'),indent=0)
