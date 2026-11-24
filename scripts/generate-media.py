#!/usr/bin/env python3
"""Generate media.json for every product bundle from its LOCAL files.

Bundle layout (content/catalog/<category>/<slug>/):
    index.md
    <slug>.jpg        featured image (first image file in the bundle root)
    images/*.webp|jpg gallery images
    media.json        <- generated here (committed); images themselves are git-ignored

media.json stores only the remote base URL + filenames; templates build every product
image address from it. Usage:  python3 scripts/generate-media.py [--base URL]
"""
import argparse, json, pathlib

EXT = {".jpg", ".jpeg", ".png", ".webp", ".avif"}
ap = argparse.ArgumentParser()
ap.add_argument("--base", default="https://files.groznet.com/pitomnik95")
ap.add_argument("--content", default="content/catalog")
a = ap.parse_args()
root = pathlib.Path(a.content)
base = a.base.rstrip("/")
count = 0
for idx in sorted(root.glob("*/*/index.md")):
    b = idx.parent
    rel = b.relative_to(root.parent).as_posix()          # catalog/<category>/<slug>
    root_imgs = sorted(f.name for f in b.iterdir() if f.is_file() and f.suffix.lower() in EXT)
    gal_dir = b / "images"
    gallery = sorted(f.name for f in gal_dir.iterdir() if f.suffix.lower() in EXT) if gal_dir.is_dir() else []
    if not root_imgs and not gallery:
        print(f"skip (no local images): {rel}")
        continue
    media = {
        "remote_base_url": f"{base}/{rel}/images/",
        "featured_image": f"{base}/{rel}/{root_imgs[0]}" if root_imgs else f"{base}/{rel}/images/{gallery[0]}",
        "images": gallery,
    }
    (b / "media.json").write_text(json.dumps(media, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    count += 1
print(f"media.json written for {count} bundles (base: {base})")
