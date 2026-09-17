#!/usr/bin/env python3
import argparse, json, subprocess
from pathlib import Path

AGY='/home/john/.local/bin/agy'

CHARACTERS=[
 ('shirone','SHIRONE / ARIAN SHIRONE','A Korean webtoon boy of about ten years old, slight but healthy build, warm fair skin, large earnest dark eyes, soft dark brown tousled hair, gentle intelligent face. He is the adopted son of Arian Vincent and Olina. Wardrobe anchor: simple rustic cream shirt, dark shorts or trousers, worn village shoes; later carry a large old magic book. Show child proportions, curiosity, wonder, and determined expression.','page_015.jpg page_024.jpg page_032.jpg page_052.jpg page_062.jpg'),
 ('arian_vincent','ARIAN VINCENT','A broad-shouldered adult Korean fantasy hunter and adoptive father, rugged handsome face, thick dark hair, strong eyebrows, tired but kind eyes, practical muscular build. Wardrobe anchor: rugged dark forest-green or brown hunter clothing, heavy boots, belt, weathered cloak or work vest; axe may appear only as a prop in one pose. Show protective warmth, not villainy.','page_009.jpg page_016.jpg page_022.jpg page_024.jpg'),
 ('olina','OLINA','An adult Korean fantasy village woman and Shirone’s adoptive mother, warm expressive face, soft dark hair gathered simply, gentle eyes, sturdy practical build. Wardrobe anchor: modest cream blouse, muted green-brown long skirt, simple village apron and shawl. Show tenderness, surprise, and maternal protectiveness.','page_009.jpg page_010.jpg page_024.jpg'),
 ('headmaster_alpheus','HEADMASTER ALPHEUS','An elderly Korean fantasy magic-academy headmaster, dignified scholarly face, long silver-white hair and beard, calm perceptive eyes, tall composed posture. Wardrobe anchor: dark formal academy robe with subtle gold trim and a scholarly mantle; no modern clothing. Show patient intellectual warmth and commanding presence.','page_050.jpg page_054.jpg page_056.jpg page_061.jpg')
]

def prompt(slug,name,details,refs,out):
    paths='\n'.join(str(Path('/home/john/manga-reviews/output/muhanui-mabeopsa/ch1/images')/x) for x in refs.split())
    return f'''Use Nano Banana Pro image generation. Create a professional vertical 9:16 character reference model sheet for {name} from The Infinite Mage Chapter 1.

Read the attached local source panels below as visual identity references and preserve the exact visible face, hair, age, proportions, wardrobe colors, and art design from those panels. Do not invent a different franchise design.
SOURCE PANELS:
{paths}

CHARACTER DESIGN LOCK:
{details}

Layout: one clean 9:16 sheet on a neutral off-white studio background (#F4F4F4). Show exactly four consistent views: front full body, 3/4 portrait close-up, true side profile, and a natural action or seated pose. Repeat the same face, hair, age, body proportions, and wardrobe in every view. Add a small readable English header: {name}. This is a model sheet, not a comic page.
Art style: authentic 2D Korean webtoon manhwa anime animation, crisp dark ink line art, controlled flat cel shading, expressive faces, NOT 3D, NOT photorealistic, NOT live action, no speech bubbles, no captions, no watermark, no extra characters.
Save the generated PNG exactly here: {out}
'''

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--chapter-dir',required=True,type=Path); args=ap.parse_args(); out=args.chapter_dir/'character_refs'; out.mkdir(parents=True,exist_ok=True)
    files=[]
    for slug,name,details,refs in CHARACTERS:
        target=out/f'{slug}_ref.png'; print(f'[CHARACTER] {name} -> {target}',flush=True)
        result=subprocess.run([AGY,'--model','gemini-3.8-flash-medium','--effort','medium','--print-timeout','15m','-p',prompt(slug,name,details,refs,target)],capture_output=True,text=True,timeout=900)
        if result.returncode: raise SystemExit(result.stderr.strip() or f'agy failed for {name}')
        if not target.exists(): raise SystemExit(f'generator did not create {target}\n{result.stdout[-2000:]}')
        files.append(str(target)); print('[OK]',flush=True)
    manifest={'source_dir':str(out.resolve()),'files':files,'reused':False,'series':'The Infinite Mage','chapter':'1'}
    (args.chapter_dir/'character_refs_source.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    print(f'[COMPLETE] {len(files)} character references')
if __name__=='__main__': main()
