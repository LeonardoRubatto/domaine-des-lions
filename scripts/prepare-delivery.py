"""Copy the standalone website and its credits into the delivery folder."""
from pathlib import Path
import shutil
ROOT=Path(__file__).resolve().parents[1]
DEST=ROOT/'dist'
DEST.mkdir(exist_ok=True)
for folder in ('assets','tokens','en','licenses'):
    if (ROOT/folder).exists(): shutil.copytree(ROOT/folder,DEST/folder,dirs_exist_ok=True)
for filename in ('style.css','site.js','v3.css','v3.js','robots.txt','sitemap.xml','favicon.ico','CREDITS.md','README.md','telaventis-manifest.json','design-plan-v3.md','design-tokens.json'):
    if (ROOT/filename).exists(): shutil.copy2(ROOT/filename,DEST/filename)
pages = ('index.html','domaine.html','en-famille.html','seminaires.html','galerie.html','sejour.html','acces.html','mentions-legales.html')
for filename in pages: shutil.copy2(ROOT/filename,DEST/filename)
qa_dest=DEST/'qa'
qa_dest.mkdir(exist_ok=True)
for filename in ('verification-v3.md','critique-result-v3.md','mobile-checks-v3.json','tells-dist-v3.txt','verification-v4.md','critique-result-v4.md','photo-coverage-v4.json','browser-checks-v4.json','viewer-opening-v4.json','section-motion-v4.json','keyboard-section-v4.json','tells-dist-v4.txt'):
    if (ROOT/'qa'/filename).exists(): shutil.copy2(ROOT/'qa'/filename,qa_dest/filename)
obsolete = DEST/'source-home.html'
if obsolete.exists(): obsolete.unlink()
print(f'Static delivery prepared: {DEST}')
