"""Acquire linked originals and emit responsive photos for the static mockup."""
import hashlib
import json
import re
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import urlopen, Request
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / 'assets' / 'photos'
DEST.mkdir(parents=True, exist_ok=True)
records = json.loads((ROOT / 'research/asset-inventory.json').read_text(encoding='utf-8'))
pages = json.loads((ROOT / 'research/content-inventory.json').read_text(encoding='utf-8'))
known = {r['url']: r for r in records}
urls = sorted({l['url'] for p in pages for l in p['links'] if urlparse(l['url']).hostname == 'ledomaineauxlions.fr' and re.search(r'\.(jpg|jpeg|png)$', l['url'], re.I)})
failures = []
def acquire(url):
    if url in known:
        return None
    name = Path(urlparse(url).path).name
    try:
        raw = urlopen(Request(url, headers={'User-Agent': 'Mozilla/5.0'}), timeout=30).read()
        target = ROOT / 'research/assets' / (Path(name).stem + '-original' + Path(name).suffix)
        target.write_bytes(raw)
        with Image.open(target) as im:
            return {'id': hashlib.sha256(url.encode()).hexdigest()[:16], 'name': name, 'url': url,
                    'localPath': target.relative_to(ROOT).as_posix(), 'width': im.width, 'height': im.height, 'format': im.format}
    except Exception as error:
        failures.append({'url': url, 'reason': str(error)})
with ThreadPoolExecutor(max_workers=4) as pool:
    records.extend(r for r in pool.map(acquire, urls) if r)
(ROOT / 'research/asset-inventory.json').write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding='utf-8')
best = {}
for r in records:
    if r['width'] <= 300 or r['height'] <= 250:
        continue
    key = re.sub(r'-(?:\d+x\d+|scaled)$', '', Path(r['name']).stem)
    if key not in best or r['width'] * r['height'] > best[key]['width'] * best[key]['height']:
        best[key] = r
def convert(entry):
    key, record = entry
    safe = re.sub(r'[^a-z0-9-]', '-', key.lower()).strip('-')
    widths = sorted({min(w, record['width']) for w in (640, 960, 1536)})
    with Image.open(ROOT / record['localPath']) as source:
        im = ImageOps.exif_transpose(source).convert('RGB')
        for width in widths:
            output = im.resize((width, round(im.height * width / im.width)), Image.Resampling.LANCZOS)
            output.save(DEST / f'{safe}-{width}.webp', quality=82, method=5)
            output.save(DEST / f'{safe}-{width}.avif', quality=64, speed=7)
    return key, {'key':safe, 'width':im.width, 'height':im.height, 'widths':widths, 'source':record['url']}
with ThreadPoolExecutor(max_workers=4) as pool:
    processed = dict(pool.map(convert, best.items()))
(ROOT / 'assets/photo-manifest.json').write_text(json.dumps(processed, ensure_ascii=False, indent=2), encoding='utf-8')
logo = next(r for r in records if r['name'] == 'Frame-36.png')
legacy = next(r for r in records if r['name'] == 'logo_header.png')
with Image.open(ROOT / logo['localPath']) as im:
    im.convert('RGBA').save(ROOT / 'assets/logo.png')
    # Derive the favicon from the original brand symbol, preserving its artwork.
    symbol = im.convert('RGBA').crop((0, 0, im.width, round(im.height * .68)))
    for size, name in ((16, 'favicon-16x16.png'),(32, 'favicon-32x32.png'),(180, 'apple-touch-icon.png')):
        icon = Image.new('RGBA', (size,size), 'white')
        thumb = ImageOps.contain(symbol, (round(size * .85),round(size * .85)))
        icon.alpha_composite(thumb, ((size-thumb.width)//2,(size-thumb.height)//2))
        icon.save(ROOT / 'assets' / name)
    icon.save(ROOT / 'favicon.ico', sizes=[(16,16),(32,32),(48,48)])
with Image.open(ROOT / legacy['localPath']) as im:
    im.convert('RGBA').save(ROOT / 'assets/logo-historical.png')
import base64
embedded = base64.b64encode((ROOT / 'assets/favicon-32x32.png').read_bytes()).decode()
(ROOT / 'assets/favicon.svg').write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32"><image width="32" height="32" href="data:image/png;base64,{embedded}"/></svg>',encoding='utf-8')
hero = best['maison3']
with Image.open(ROOT / hero['localPath']) as im:
    ImageOps.fit(im.convert('RGB'), (1200,630)).save(ROOT / 'assets/og.png')
(ROOT / 'research/asset-download-failures.json').write_text(json.dumps(failures, indent=2),encoding='utf-8')
print(json.dumps({'sourceFiles':len(records),'distinctPhotoSets':len(processed),'failures':failures}))
