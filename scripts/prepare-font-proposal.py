"""Self-host the local typography proposal from official Google Fonts sources."""
from pathlib import Path
from urllib.request import urlopen
from base64 import b64encode

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://raw.githubusercontent.com/google/fonts/main/ofl/'
FONTS = (
    ('alegreya/Alegreya%5Bwght%5D.ttf', 'alegreya.ttf', 'Alegreya', '400 440'),
    ('alegreyasans/AlegreyaSans-Regular.ttf', 'alegreya-sans-regular.ttf', 'Alegreya Sans', '400'),
    ('alegreyasans/AlegreyaSans-Medium.ttf', 'alegreya-sans-medium.ttf', 'Alegreya Sans', '500'),
)

if __name__ == '__main__':
    css = ['/* Local typography proposal. Original SIL OFL notices in licenses/. */']
    for source, name, family, weight in FONTS:
        path = ROOT / 'assets/fonts' / name
        if not path.exists():
            path.write_bytes(urlopen(BASE + source).read())
        # Inline font data preserves the existing standalone file:// delivery contract.
        data = b64encode(path.read_bytes()).decode('ascii')
        css.append(f"@font-face {{ font-family: '{family}'; font-style: normal; font-weight: {weight}; font-display: swap; src: url(data:font/ttf;base64,{data}) format('truetype'); }}")
        print(f'{family} {weight}: {path.stat().st_size} bytes')
    for family in ('alegreya', 'alegreyasans'):
        path = ROOT / 'licenses' / f'{family}-OFL.txt'
        if not path.exists():
            path.write_bytes(urlopen(BASE + family + '/OFL.txt').read())
    (ROOT / 'tokens/fonts.css').write_text('\n'.join(css) + '\n', encoding='utf-8')
