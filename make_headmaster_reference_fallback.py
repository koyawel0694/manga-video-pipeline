#!/usr/bin/env python3
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
base=Path('/home/john/manga-reviews/output/muhanui-mabeopsa/ch1')
out=base/'character_refs'/'headmaster_alpheus_ref.png'
refs=[base/'images'/f'page_{n:03d}.jpg' for n in (50,54,56,61)]
W,H=768,1376
sheet=Image.new('RGB',(W,H),'#F4F4F4'); draw=ImageDraw.Draw(sheet)
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',28)
small=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',16)
draw.text((W//2,30),'HEADMASTER ALPHEUS',fill='#111111',font=font,anchor='ma')
for i,p in enumerate(refs):
    im=Image.open(p).convert('RGB')
    cell_w,cell_h=360,560
    scale=min(cell_w/im.width,cell_h/im.height)
    im=im.resize((int(im.width*scale),int(im.height*scale)),Image.Resampling.LANCZOS)
    x=24+(i%2)*372; y=78+(i//2)*640
    draw.rectangle((x-6,y-6,x+cell_w+6,y+cell_h+6),fill='#FFFFFF',outline='#C8C8C8',width=2)
    sheet.paste(im,(x+(cell_w-im.width)//2,y+(cell_h-im.height)//2))
    draw.text((x+cell_w//2,y+cell_h+16),f'SOURCE PANEL {p.stem[-3:]}',fill='#444444',font=small,anchor='ma')
sheet.save(out,optimize=True)
manifest={'source_dir':str((base/'character_refs').resolve()),'files':[str(p) for p in sorted((base/'character_refs').glob('*.png'))], 'reused':False,'series':'The Infinite Mage','chapter':'1','notes':{'headmaster_alpheus_ref.png':'source-panel provenance fallback after image backend timeout; no invented artwork'}}
(base/'character_refs_source.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print('[OK] wrote provenance fallback',out)
