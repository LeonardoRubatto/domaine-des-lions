"""Replace the home opening while preserving the other editorial sections."""
from pathlib import Path
root=Path(__file__).resolve().parents[1]
p=root/'scripts/build-site.py'
s=p.read_text(encoding='utf-8')
a=s.index('    return f\'\'\'<section class="hero wrap"',s.index('def home():'))
b=s.index('\n<section class="home-intro',a)
opening='''    return f\'\'\'<section class="hero hero-estate wrap"><figure class="hero-image">{picture('maison-3_4-',css='hero-photo',eager=True,sizes='(min-width: 1440px) 1080px, (min-width: 769px) 85vw, 100vw')}</figure><figure class="hero-detail">{picture('piano',sizes='(min-width: 769px) 200px, 120px')}</figure><div class="hero-title"><h1>Le Domaine<br>aux Lions</h1></div><div class="hero-description"><p>{tr('Une maison à colombages pour se retrouver. Les salons sous les poutres, les chambres, le jardin : tout le domaine est à vous.','A timber-framed house for time together. Living rooms beneath the beams, bedrooms and the garden: the whole estate is yours.')}</p><a class="text-link" href="#maison">{tr('Découvrir les espaces','Discover the spaces')}</a></div><div class="hero-setting"><p>{tr('Maison entière · jusqu’à 15 invités','Whole house · up to 15 guests')}</p><p>{tr('Fauguernon, Normandie<br>À environ 2 heures de Paris','Fauguernon, Normandy<br>Around 2 hours from Paris')}</p></div></section>'''
s=s[:a]+opening+s[b:]
p.write_text(s,encoding='utf-8')
p=root/'design-plan-v3.md';s=p.read_text(encoding='utf-8')
s=s.replace('grand titre et introduction décalée au-dessus de la façade','photo dominante décalée à droite, nom du domaine dans un retrait blanc au bas du cadre, piano à gauche, informations après le titre')
s=s.replace('96px display / 17px body, fluide jusqu’à 52px mobile','112px display du nom / 17px body, fluide jusqu’à 52px mobile')
s=s.replace('Une seule formule poétique au hero.', 'Aucun surtitre et aucune formule poétique au hero; le nom réel du domaine ouvre la présentation.')
s=s.replace('Échelle 14/17/24/32/48/96px','Échelle 14/17/24/32/48/96/112px')
s += '\nRévision hero : retrait du surtitre, du bandeau sombre et des liens de découverte répétés. Composition depuis les primitives et rules/layout.md : les heroes shaders inspectés sont inadaptés aux photos du lieu, donc aucun shader ajouté. Le blanc sous le nom forme un retrait dans la photographie, sans bordure ni ombre; une petite vue du piano relie intérieur et façade. Mobile : photo en tête, nom dessous, détail du piano associé à l’introduction. Les animations existantes restent, avec aucun reset des photos déjà affichées.\n'
p.write_text(s,encoding='utf-8')
