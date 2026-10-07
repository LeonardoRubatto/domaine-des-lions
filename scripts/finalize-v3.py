"""Finalize reviewed presentation details and record the flash correction."""
from pathlib import Path
root=Path(__file__).resolve().parents[1]
p=root/'design-plan-v3.md';s=p.read_text(encoding='utf-8')
s=s.replace('intensité1.6px, sur les20%', 'intensité1.2px, sur les16%')
s=s.replace('Espacement base4px, exceptions0/1/2', '4px grid, exceptions0/1/2')
s += '\nRevue finale : le hero de la page En images défile automatiquement, conformément à la demande. La façade de l’accueil reste stable. Les images hors écran sont préparées avant observation; aucune remise à zéro de l’opacité pour les photos déjà affichées. Une diapositive attend le décodage de la suivante avant de la remplacer. Les captions génériques répétées sont retirées de la grille visible; les descriptions accessibles restent. Aucun nom de chambre attribué sans correspondance vérifiée. Le grand guillemet décoratif des avis est retiré. Les titres partagés en colonnes servent l’introduction/photo et des explications très courtes, pas une série de sections identiques.\n'
p.write_text(s,encoding='utf-8')
p=root/'CREDITS.md';s=p.read_text(encoding='utf-8').replace('lower edge of large images.', 'lower edge of large images (16% band, 6px maximum).')
p.write_text(s,encoding='utf-8')
p=root/'qa/verification-v3.md';s=p.read_text(encoding='utf-8').replace('final8px','final6px')
s += '\n## Correction après retour utilisateur\n\nLe flash venait de l’état visible peint avant le reset WAAPI. Les photos déjà dans le premier viewport restent stables. Les autres portent image-await avant leur entrée : opacity0 constatée hors écran, puis0.973 pendant le mouvement et1 après retrait de la classe. Le diaporama attend image.decode avant le changement, sans vider le cadre sortant. Flou réduit à16%/6px après revue.\n'
p.write_text(s,encoding='utf-8')
p=root/'scripts/build-site.py';s=p.read_text(encoding='utf-8')
s=s.replace('<span class="quote-mark" aria-hidden="true">“</span>', '')
# Gallery captions are editorial additions; omit anonymous repeated inventory
# labels, while retaining truthful alt text and accessible enlarge controls.
s=s.replace("<figcaption>{esc(alt)}</figcaption>", "<figcaption>{esc(alt) if alt not in ('Une chambre du Domaine aux Lions','Un espace du Domaine aux Lions','A bedroom at Le Domaine aux Lions','A space at Le Domaine aux Lions') else ''}</figcaption>")
p.write_text(s,encoding='utf-8')
