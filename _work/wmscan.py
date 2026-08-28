import os, numpy as np
from PIL import Image
hits=[]
for f in sorted(os.listdir('raw')):
    im=Image.open('raw/'+f).convert('RGB'); w,h=im.size
    a=np.asarray(im).astype(np.float32)
    # scan lower 25% and upper 12% strips for small bright/dark text on flat bg
    for name,(y0,y1) in [('bottom',(int(h*0.78),h)),('top',(0,int(h*0.13)))]:
        strip=a[y0:y1]
        g=strip.mean(2)
        # local contrast via gradient
        gx=np.abs(np.diff(g,axis=1)).mean()
        # count of pixels differing from strip median by 8..70 (text on flat bg)
        med=np.median(g)
        d=np.abs(g-med)
        textish=((d>10)&(d<90)).mean()
        if gx>1.2 and 0.004<textish<0.35:
            hits.append((round(float(gx),2),round(float(textish),4),name,f))
hits.sort(reverse=True)
for x in hits[:45]: print(x)
print('total candidates', len(hits))
