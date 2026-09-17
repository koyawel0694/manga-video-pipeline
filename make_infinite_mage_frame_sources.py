#!/usr/bin/env python3
import argparse
from pathlib import Path
from PIL import Image

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--chapter-dir',required=True,type=Path); args=ap.parse_args()
    src=args.chapter_dir/'images'; out=args.chapter_dir/'clean_frame_crops'; out.mkdir(parents=True,exist_ok=True)
    files=sorted(src.glob('page_*.jpg'))+sorted(src.glob('page_*.jpeg'))+sorted(src.glob('page_*.png'))+sorted(src.glob('page_*.webp'))
    for f in files:
        n=int(f.stem.split('_')[-1]); band=min(5,(n-1)*6//len(files))+2
        target=out/f'b{band:02d}_{f.stem}.png'
        if target.exists(): continue
        with Image.open(f) as im: im.convert('RGB').save(target,optimize=True)
    print(f'[OK] {len(list(out.glob("*.png")))} narrative frame sources in {out}')
if __name__=='__main__': main()
