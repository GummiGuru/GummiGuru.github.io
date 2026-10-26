#!/usr/bin/env python3
"""Add images to the portfolio.
Usage: python3 add_images.py --title "Name" --category Characters img1.png [img2.jpg ...] [--no-push]
Multiple images get titles "Name 1", "Name 2"... Requires Pillow."""
import argparse, json, os, re, subprocess, sys
from PIL import Image
ROOT = os.path.dirname(os.path.abspath(__file__)); IMG = os.path.join(ROOT, "images"); MAN = os.path.join(ROOT, "gallery.json")
def slug(s): return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-") or "image"
def main():
    p = argparse.ArgumentParser(); p.add_argument("files", nargs="+"); p.add_argument("--title", required=True)
    p.add_argument("--category", required=True); p.add_argument("--quality", type=int, default=82); p.add_argument("--no-push", action="store_true")
    a = p.parse_args(); os.makedirs(IMG, exist_ok=True)
    data = json.load(open(MAN)) if os.path.exists(MAN) else []
    added = []
    for n, f in enumerate(a.files, 1):
        title = a.title if len(a.files) == 1 else f"{a.title} {n}"
        base = slug(title); name = base + ".webp"; k = 2
        while os.path.exists(os.path.join(IMG, name)): name = f"{base}-{k}.webp"; k += 1
        im = Image.open(f); im = im.convert("RGBA" if im.mode in ("RGBA", "LA", "P") else "RGB")
        im.thumbnail((1600, 1600), Image.LANCZOS); im.save(os.path.join(IMG, name), "WEBP", quality=a.quality, method=6)
        data.append({"file": name, "title": title, "category": a.category}); added.append(name); print("added", name)
    json.dump(data, open(MAN, "w"), indent=2, ensure_ascii=False)
    g = lambda *c: subprocess.run(["git", "-C", ROOT, *c], check=True)
    g("add", "gallery.json", *[os.path.join("images", x) for x in added]); g("commit", "-m", f"Add {len(added)} image(s): {a.title}")
    if not a.no_push: g("push", "origin", "HEAD:main")
if __name__ == "__main__": main()
