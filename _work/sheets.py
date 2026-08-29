import os
from PIL import Image, ImageDraw
files=sorted(os.listdir('raw'))
PER=30; COLS=6; CELL=300; LBL=22
os.makedirs('sheets',exist_ok=True)
for s in range(0,len(files),PER):
    chunk=files[s:s+PER]
    rows=(len(chunk)+COLS-1)//COLS
    sh=Image.new('RGB',(COLS*CELL, rows*(CELL+LBL)),(235,235,235))
    d=ImageDraw.Draw(sh)
    for i,f in enumerate(chunk):
        im=Image.open('raw/'+f).convert('RGB')
        im.thumbnail((CELL-8,CELL-8))
        cx=(i%COLS)*CELL; cy=(i//COLS)*(CELL+LBL)
        sh.paste(Image.new('RGB',(CELL,CELL),'white'),(cx,cy))
        sh.paste(im,(cx+(CELL-im.width)//2, cy+(CELL-im.height)//2))
        d.rectangle([cx,cy,cx+CELL-1,cy+CELL-1],outline=(180,180,180))
        d.text((cx+6,cy+CELL+4), f.replace('.jpg',''), fill=(20,20,20))
    sh.save(f'sheets/sheet_{s//PER:02d}.jpg',quality=86)
    print('sheet',s//PER,len(chunk))
