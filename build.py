#!/usr/bin/env python3
"""Bundle index.html + photos/ into a single self-contained file.

Usage:  python3 build.py

Writes dist/index.html — every candidate photo embedded as a data URI, so the
page works with no photos/ folder next to it (email it, drag it onto Netlify
Drop, publish it anywhere). Re-run after adding or replacing a photo.
"""

import base64
import io
import json
import mimetypes
import re
import unicodedata
from pathlib import Path

try:
    from PIL import Image, ImageOps
except ImportError:
    Image = None

ROOT = Path(__file__).parent
SRC = ROOT / "index.html"
PHOTOS = ROOT / "photos"
DIST = ROOT / "dist"
EXTS = ["jpg", "jpeg", "png", "webp"]
SIZE = 400          # photos are square-cropped to this before embedding
QUALITY = 82


def slug(name):
    stripped = unicodedata.normalize("NFD", name.strip().lower())
    stripped = "".join(c for c in stripped if not unicodedata.combining(c))
    stripped = re.sub(r"[^a-z0-9\s-]", "", stripped)
    return re.sub(r"\s+", "-", stripped)


def candidate_paths(name, explicit):
    if explicit:
        return [ROOT / explicit]
    full = slug(name)
    stems = dict.fromkeys([full, full.replace("-", "_"), full.split("-")[0]])
    return [PHOTOS / f"{stem}.{ext}" for stem in stems for ext in EXTS]


def data_uri(path):
    """Square-crop and shrink to SIZE px, then base64-encode.

    Falls back to embedding the file untouched when Pillow is unavailable.
    """
    if Image is None:
        mime = mimetypes.guess_type(path.name)[0] or "image/jpeg"
        return f"data:{mime};base64,{base64.b64encode(path.read_bytes()).decode()}", path.stat().st_size

    img = Image.open(path)
    img = ImageOps.exif_transpose(img)                 # honour phone rotation
    img = ImageOps.fit(img, (SIZE, SIZE), Image.LANCZOS, centering=(0.5, 0.4))
    if img.mode not in ("RGB", "L"):
        img = img.convert("RGB")
    buf = io.BytesIO()
    img.save(buf, "JPEG", quality=QUALITY, optimize=True, progressive=True)
    raw = buf.getvalue()
    return "data:image/jpeg;base64," + base64.b64encode(raw).decode(), len(raw)


def main():
    html = SRC.read_text()

    block = re.search(r"const CANDIDATES = \[(.*?)\n\];", html, re.S)
    if not block:
        raise SystemExit("could not find the CANDIDATES array in index.html")

    entries = re.findall(
        r'\{\s*name:\s*"([^"]+)",\s*seat:\s*"([^"]+)",\s*photo:\s*"([^"]*)"\s*\}',
        block.group(1),
    )
    if not entries:
        raise SystemExit("could not parse any candidates")

    rebuilt, found = [], 0
    for name, seat, explicit in entries:
        photo = ""
        for path in candidate_paths(name, explicit):
            if path.is_file():
                photo, nbytes = data_uri(path)
                found += 1
                was = path.stat().st_size / 1024
                print(f"  embedded  {name:<18} {str(path.relative_to(ROOT)):<26}"
                      f" {was:>6.0f} KB -> {nbytes / 1024:>5.0f} KB")
                break
        else:
            print(f"  no photo  {name:<18} (initials circle)")
        rebuilt.append(
            "  { name: %s, seat: %s, photo: %s }"
            % (json.dumps(name), json.dumps(seat), json.dumps(photo))
        )

    html = html.replace(
        block.group(0),
        "const CANDIDATES = [\n" + ",\n".join(rebuilt) + "\n];",
    )

    DIST.mkdir(exist_ok=True)
    out = DIST / "index.html"
    out.write_text(html)
    size = out.stat().st_size / 1024
    print(f"\n{found}/{len(entries)} photos embedded -> {out.relative_to(ROOT)} ({size:.0f} KB)")
    if Image is None:
        print("  (install Pillow to shrink photos before embedding: pip install Pillow)")


if __name__ == "__main__":
    main()
