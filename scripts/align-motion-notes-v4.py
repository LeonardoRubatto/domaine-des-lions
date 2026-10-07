from pathlib import Path
root=Path(__file__).resolve().parents[1]
p=root/'design-plan-v3.md'
s=p.read_text(encoding='utf-8')
s=s.replace('léger décalage vertical24px pour quatre blocs éditoriaux, une fois à l’entrée','fondu de92% à100% et décalage vertical16px aux ruptures de section, une fois à l’entrée')
s=s.replace('Trois titres seulement : Text Effect, slide par mot, 400ms avec stagger50ms plafonné à300ms, texte accessible entier.','Six titres maximum à l’accueil : Text Effect, slide par mot pour le nom et la visite, fade-in-blur4px pour maison, piscine, tennis et témoignages;400ms avec stagger50ms plafonné à200 ou300ms, texte accessible entier. Le titre de galerie conserve son slide.')
s=s.replace('Text Effect ajouté aux trois titres éditoriaux maison, art et témoignages','Text Effect ajouté aux quatre titres éditoriaux maison, piscine, tennis et témoignages')
s=s.replace('Les trois titres déjà animés conservent leur slide','Le nom du domaine, le titre de la visite et le titre de galerie conservent leur slide')
s=s.replace('Budget maximal de six titres à l’accueil','Budget maximal de six titres à l’accueil')
p.write_text(s,encoding='utf-8')
p=root/'CREDITS.md'
s=p.read_text(encoding='utf-8').replace('three house/art/review chapter headings','four house/pool/tennis/review chapter headings')
p.write_text(s,encoding='utf-8')
