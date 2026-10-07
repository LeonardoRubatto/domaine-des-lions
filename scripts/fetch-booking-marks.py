from pathlib import Path
import urllib.request
import json

root = Path(__file__).resolve().parents[1]
dest = root / 'assets/brands'
dest.mkdir(exist_ok=True)
records = []
for slug, colour in [('airbnb', 'FF5A5F'), ('bookingdotcom', '003580')]:
    url = f'https://raw.githubusercontent.com/simple-icons/simple-icons/develop/icons/{slug}.svg'
    with urllib.request.urlopen(url, timeout=30) as response:
        svg = response.read().decode('utf-8')
    assert '<svg' in svg and '<path' in svg
    svg = svg.replace('<svg ', f'<svg fill="#{colour}" ', 1)
    (dest / f'{slug}.svg').write_text(svg, encoding='utf-8')
    records.append({'slug': slug, 'source': url, 'colour': colour})
(root / 'research/booking-marks.json').write_text(json.dumps(records, indent=2), encoding='utf-8')
print('Saved two original Simple Icons brand marks.')
