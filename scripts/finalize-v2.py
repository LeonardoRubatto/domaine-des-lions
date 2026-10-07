"""Small delivery corrections, including portable fonts, without network access."""
from pathlib import Path
import base64
root = Path(__file__).resolve().parents[1]
builder = root / 'scripts/build-site.py'
text = builder.read_text(encoding='utf-8')
text = text.replace('Témoignages repris du site du domaine.', 'Les mots de nos invités.')
text = text.replace('Reviews published on the estate’s website, in their original French.', 'In our guests’ words.')
duplicate = '<link rel="stylesheet" href="{PREFIX}tokens/clay.css"><link rel="stylesheet" href="{PREFIX}tokens/clay.css">'
text = text.replace(duplicate, '<link rel="stylesheet" href="{PREFIX}tokens/clay.css">')
if 'tokens/fonts.css' not in text:
    text = text.replace('<link rel="stylesheet" href="{PREFIX}tokens/ui.css">', '<link rel="stylesheet" href="{PREFIX}tokens/fonts.css"><link rel="stylesheet" href="{PREFIX}tokens/ui.css">')
text = text.replace("'<url><loc>'+url+'</loc><lastmod>2026-10-07</lastmod>'", "'<url><loc>'+url+'</loc><lastmod>2026-10-07</lastmod><changefreq>monthly</changefreq><priority>'+('1.0' if page=='home' else '0.2' if page=='legal' else '0.8')+'</priority>'")
builder.write_text(text, encoding='utf-8')
style = root / 'style.css'
style.write_text('\n'.join(line for line in style.read_text(encoding='utf-8').splitlines() if not line.startswith('@font-face'))+'\n',encoding='utf-8')
rules=[]
for family, name in [('Source Serif 4','source-serif-4'),('Public Sans','public-sans')]:
    encoded=base64.b64encode((root/'assets/fonts'/f'{name}.ttf').read_bytes()).decode('ascii')
    rules.append(f"@font-face {{ font-family: '{family}'; src: url('data:font/ttf;base64,{encoded}') format('truetype'); font-weight: 400 600; font-style: normal; font-display: swap; }}")
(root/'tokens/fonts.css').write_text('\n'.join(rules)+'\n',encoding='utf-8')
print('Final editorial fixes and portable font stylesheet prepared.')
