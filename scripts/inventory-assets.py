"""Consolidate observed public client assets and make internal review sheets."""
import json
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageOps

ROOT = Path(__file__).resolve().parents[1]
RESEARCH = ROOT / 'research'
DEST = RESEARCH / 'assets'
DEST.mkdir(exist_ok=True)
records = {}
for manifest in sorted((RESEARCH / 'source-assets').glob('*/manifest.json')):
    data = json.loads(manifest.read_text(encoding='utf-8-sig'))
    for asset in data['assets']:
        if asset['kind'] != 'image' or asset['url'].startswith('inline-svg:'):
            continue
        source = manifest.parent / Path(asset['path']).name
        if not source.exists():
            continue
        if asset['url'] in records:
            continue
        record = {k: asset[k] for k in ('id', 'name', 'url', 'contentType')}
        try:
            with Image.open(source) as image:
                record.update(width=image.width, height=image.height, format=image.format)
                extension = { 'JPEG': '.jpg', 'PNG': '.png', 'WEBP': '.webp', 'ICO': '.ico' }.get(image.format, source.suffix)
        except Exception:
            continue
        target = DEST / (Path(asset['name']).stem + '-' + asset['id'][:6] + extension)
        target.write_bytes(source.read_bytes())
        record['localPath'] = target.relative_to(ROOT).as_posix()
        records[asset['url']] = record
items = list(records.values())
(RESEARCH / 'asset-inventory.json').write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding='utf-8')
photos = [item for item in items if item['width'] > 300 and item['height'] > 250]
for offset in range(0, len(photos), 24):
    batch = photos[offset:offset + 24]
    sheet = Image.new('RGB', (1280, math.ceil(len(batch) / 4) * 225), 'white')
    draw = ImageDraw.Draw(sheet)
    for index, item in enumerate(batch):
        x, y = (index % 4) * 320, (index // 4) * 225
        with Image.open(ROOT / item['localPath']) as image:
            thumb = ImageOps.contain(image.convert('RGB'), (308, 188))
            sheet.paste(thumb, (x + 6, y + 6))
        draw.text((x + 6, y + 198), item['name'][:42], fill='black')
        draw.text((x + 6, y + 213), f"{item['width']} x {item['height']}", fill='black')
    sheet.save(RESEARCH / f'contact-sheet-{offset // 24 + 1}.jpg', quality=90)
print(json.dumps({'assets': len(items), 'photoFiles': len(photos), 'contactSheets': math.ceil(len(photos) / 24)}))
