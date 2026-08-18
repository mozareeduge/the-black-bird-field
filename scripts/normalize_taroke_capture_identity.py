#!/usr/bin/env python3
"""Normalize the inherited TAROKE desktop title to the owner-locked identity.

The desktop captures predate the final REMIXER identity correction. Rather than
redraw or regenerate their UI, this utility copies the already-rendered E glyph
from TAROKE into the title's second-character cell. It is idempotent: a capture
whose target glyph already matches the source glyph is left byte-untouched.
"""
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
DIR=ROOT/'public/assets/taroke-remixer'
FILES=['poster-desktop.webp','view-first_change-desktop.webp','view-midpoint-desktop.webp','view-last_change-desktop.webp']
SOURCE=(57,16,66,35)
TARGET_BOX=(82,16,91,35)
TARGET_XY=(82,16)

def mask(im, box):
    return [p > 30 for p in im.crop(box).convert('L').get_flattened_data()]

def iou(a,b):
    inter=sum(x and y for x,y in zip(a,b)); union=sum(x or y for x,y in zip(a,b))
    return inter/union if union else 1.0

for name in FILES:
    p=DIR/name; im=Image.open(p).convert('RGB')
    if im.width!=1400: raise SystemExit(f'unexpected capture width: {p} {im.size}')
    similarity=iou(mask(im,SOURCE),mask(im,TARGET_BOX))
    if similarity >= .93:
        print('already normalized',p,f'iou={similarity:.3f}')
        continue
    glyph=im.crop(SOURCE)
    im.paste(glyph,TARGET_XY)
    im.save(p,'WEBP',quality=96,method=6)
    print('normalized',p)
