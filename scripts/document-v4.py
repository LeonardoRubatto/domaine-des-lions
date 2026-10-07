from pathlib import Path
import json
root=Path(__file__).resolve().parents[1]
plan=root/'design-plan-v3.md'
s=plan.read_text(encoding='utf-8')
for old,new in [('rules/layout.md','layout.md'),('salons/maison','salons dans la maison'),('chambre/chambres','chambre dans les chambres'),('bassin et tennis/détente','bassin et tennis dans la détente'),('façade panoramique/maison','façade panoramique dans la maison'),('graminées/jardin','graminées dans le jardin'),('miniature/photo','miniature et photo')]: s=s.replace(old,new)
plan.write_text(s,encoding='utf-8')
photos=json.loads((root/'assets/photo-manifest.json').read_text(encoding='utf-8'))
gallery=(root/'galerie.html').read_text(encoding='utf-8')
access=(root/'acces.html').read_text(encoding='utf-8')
rows=[{'key':k,'gallery':f'photos/{p["key"]}-' in gallery,'access':f'photos/{p["key"]}-' in access} for k,p in photos.items()]
coverage={'recovered':len(photos),'gallery':sum(r['gallery'] for r in rows),'allPhotosPresent':all(r['gallery'] or r['access'] for r in rows),'photos':rows}
(root/'qa/photo-coverage-v4.json').write_text(json.dumps(coverage,ensure_ascii=False,indent=2),encoding='utf-8')
assert coverage['allPhotosPresent']
credits=root/'CREDITS.md'
notice='''Simple Icons SVG artwork is provided under CC0 1.0 Universal.\nhttps://github.com/simple-icons/simple-icons/blob/develop/LICENSE.md\nhttps://creativecommons.org/publicdomain/zero/1.0/\nTrademark rights in brand names and symbols remain with their owners.\n'''
(root/'licenses/simple-icons.txt').write_text(notice,encoding='utf-8')
readme=root/'README.md'
s=readme.read_text(encoding='utf-8')
s+='''\n\nRévision v4 : hero photographique sans surtitre ni bandeau sombre; 71 photos dans la galerie, dont les six nouvelles avec catégorie et légende FR/EN; cinq repères d’arrivée sur la page d’accès. Symboles Airbnb et Booking.com dès l’accueil et aux réservations. Visionneuse Morphing Dialog adaptée en JavaScript natif : géométrie de la miniature vers l’image entière, navigation filaire, fermeture animée, focus clavier et décodage préalable. Voir qa/verification-v4.md.\n'''
readme.write_text(s,encoding='utf-8')
print(json.dumps({k:v for k,v in coverage.items() if k!='photos'}))
