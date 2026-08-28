import csv, os, urllib.request, concurrent.futures as cf
CSV=r"C:\Users\Kojok\Downloads\products_export_1 (15).csv"
rows=list(csv.DictReader(open(CSV,encoding='utf-8')))
jobs=[]
for r in rows:
    u=r['Image Src']
    if not u: continue
    fn=os.path.join('raw', u.split('/')[-1].split('?')[0])
    if not os.path.exists(fn): jobs.append((u,fn))
def get(j):
    u,fn=j
    for a in range(3):
        try:
            req=urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'})
            d=urllib.request.urlopen(req,timeout=60).read()
            open(fn,'wb').write(d); return (fn,len(d),None)
        except Exception as e:
            if a==2: return (fn,0,str(e))
ok=bad=0
with cf.ThreadPoolExecutor(12) as ex:
    for fn,n,err in ex.map(get,jobs):
        if err: bad+=1; print('FAIL',fn,err)
        else: ok+=1
print(f'downloaded ok={ok} fail={bad} total={len(jobs)}')
