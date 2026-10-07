"""Self-host the two licensed typefaces; no browser requests to a font CDN."""
from pathlib import Path
from urllib.request import urlopen

root = Path(__file__).resolve().parents[1]
(root / 'assets/fonts').mkdir(exist_ok=True)
families = {
    'source-serif-4': ('sourceserif4', 'SourceSerif4[opsz,wght].ttf'),
    'public-sans': ('publicsans', 'PublicSans[wght].ttf'),
}
for name, (folder, filename) in families.items():
    base = 'https://raw.githubusercontent.com/google/fonts/main/ofl/' + folder + '/'
    license_text = urlopen(base + 'OFL.txt').read()
    (root / 'licenses' / (name + '-OFL.txt')).write_bytes(license_text)
    ttf = root / 'assets/fonts' / (name + '.ttf')
    ttf.write_bytes(urlopen(base + filename.replace('[', '%5B').replace(']', '%5D')).read())
    print(name, ttf.stat().st_size)
