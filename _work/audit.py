import os, numpy as np
from PIL import Image
import collections, json
res=[]
for f in sorted(os.listdir('raw')):
    p='raw/'+f
    im=Image.open(p).convert('RGB'); w,h=im.size
    a=np.asarray(im).astype(np.int16)
    # border sample (8px frame)
    b=np.concatenate([a[:8].reshape(-1,3),a[-8:].reshape(-1,3),a[:,:8].reshape(-1,3),a[:,-8:].reshape(-1,3)])
    bm=b.mean(0); bstd=b.std(0).mean()
    # content mask = pixels far from white
    g=a.mean(2)
    mask=g<245
    ys,xs=np.where(mask)
    if len(ys)==0: bbox=(0,0,w,h)
    else: bbox=(int(xs.min()),int(ys.min()),int(xs.max()),int(ys.max()))
    x0,y0,x1,y1=bbox
    # margins as fraction
    marg=(x0/w, y0/h, (w-1-x1)/w, (h-1-y1)/h)
    touch=sum(1 for m in marg if m<0.005)
    fill=mask.sum()/(w*h)
    res.append(dict(f=f,w=w,h=h,ar=round(w/h,4),bg=[round(x,1) for x in bm.tolist()],
                    bgstd=round(float(bstd),2),marg=[round(m,4) for m in marg],touch=touch,fill=round(float(fill),4)))
json.dump(res,open('audit.json','w'),indent=0)
print('n=',len(res))
print('\n--- SIZES ---')
for k,v in collections.Counter((r['w'],r['h']) for r in res).most_common(15): print(f'{v:4}  {k}')
print('\n--- SQUARE? ---')
print(collections.Counter('square' if abs(r['ar']-1)<0.02 else ('portrait' if r['ar']<1 else 'landscape') for r in res))
print('\n--- BG WHITENESS (min channel of border mean) ---')
bs=[min(r['bg']) for r in res]
print('pure-ish white (>=250):', sum(1 for x in bs if x>=250))
print('off-white 240-250:', sum(1 for x in bs if 240<=x<250))
print('grey/other <240:', sum(1 for x in bs if x<240))
print('worst:', sorted([(round(min(r['bg']),1),r['f']) for r in res])[:12])
print('\n--- BORDER NOISE (std) ---')
print('noisy bg (std>6):', sum(1 for r in res if r['bgstd']>6))
print(sorted([(r['bgstd'],r['f']) for r in res],reverse=True)[:12])
print('\n--- CONTENT TOUCHING EDGE (cropped product) ---')
print(collections.Counter(r['touch'] for r in res))
print([r['f'] for r in res if r['touch']>=1][:30])
print('\n--- FILL RATIO ---')
print('tiny product (<10%):', sorted([(r['fill'],r['f']) for r in res])[:10])
print('huge (>70%):', sorted([(r['fill'],r['f']) for r in res],reverse=True)[:10])
