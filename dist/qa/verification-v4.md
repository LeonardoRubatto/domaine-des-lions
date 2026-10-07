# Vérification de la révision v4 — 8 octobre 2026

Maquette locale FR/EN; aucune publication. Les contrôles v3 des autres parcours sont conservés dans verification-v3.md. Cette révision concerne le hero, les six photos restaurées, les marques de réservation et la visionneuse.

| Promesse | Implémentation | Preuve et résultat |
|---|---|---|
| Hero sans surtitre ni bandeau sombre | build-site.py, v3.css `.hero-estate` | Captures réelles1440×900 et390×844. Nouvelle composition mobile avec nom dans le retrait blanc, informations compactes, liens visibles. Contrôle320px sans débordement. |
| Toutes les photos conservées | CAPTIONS, category, gallery, access | photo-coverage-v4.json :76 récupérées,71 en galerie,5 pour l’arrivée, aucune absente. Les six nouvelles ont une catégorie et une légende FR/EN. |
| Filtre et viewer cohérents | site.js photoButtons | Mobile : nouvelle chambre visible dans le filtre chambres (26 images), compteur13/26 dans le viewer; tout le domaine40/71. Navigation droite vers le bassin41/71. |
| Symboles de réservation | assets/brands; platform_links | Airbnb rose et Booking.com bleu dès le hero, dans les actions finales et sur la page séjour. Liens existants conservés. Marques stables, soulignement au survol/focus. |
| Ouverture continue, sans flash | preparePhoto, animateViewer | Image décodée avant ouverture/changement. Six observations dans viewer-opening-v4.json : opacité du fond0.52→0.82→0.92→0.98→0.999→1, aucune remise à zéro observée. Captures séquentielles viewer-opening0–5. |
| Commandes et clavier | closePhoto, keydown, native dialog | Desktop : Tab du dernier bouton revient à Fermer; Shift-Tab depuis Fermer va à Suivante. Échap ferme, aria-expanded repasse false, focus revient à la miniature et body déverrouillé. Flèches changent photo et compteur. |
| Fermeture douce et interruption | closePhoto | Clic sur la marge mobile ferme et retourne le focus. Échap pendant l’ouverture ferme proprement; ouverture suivante fonctionnelle. Console inspectée : aucune erreur. |
| Anglais et tactile | builder footer traduit | Viewer EN de la nouvelle chambre : caption correcte,40/71, Close/Previous/Next. Contrôles mesurés48px de haut, flèches48px de large. |
| Reduced motion | reduced media query et JS | Code inspecté : animations instantanées, finish des animations en cours si changement, aucun autoplay dans le viewer. Mode système réduit non émulé dans cette passe; aucune réussite navigateur prétendue. |

La revue indépendante a identifié un défaut réel : le fond terminait son animation à400ms et reprenait l’opacité0 de la classe d’ouverture jusqu’à800ms. Les deux animations d’ouverture durent maintenant800ms; les mesures successives ci-dessus vérifient la correction. La revue a validé les captures mobile révisées.

Dernière demande vérifiée : fondu commun92%→100% et déplacement16px aux sections,800ms, une seule fois, seulement pour les sections initialement hors écran. Six titres ciblés à l’accueil : nom, maison, piscine, tennis, visite et témoignages; les quatre titres ajoutés utilisent Text Effect fade-in-blur4px/12px. Observer navigateur à l’entrée de la piscine : opacité0.971→0.992 et translation5.7→1.58px, puis état stable; texte blur0.394→none. Captures complètes1440/390 actualisées.

Contrôle clavier supplémentaire :12 Tab natifs depuis le haut jusqu’au bouton de visite hors écran. La section est immédiatement opacity1/transformnone, tous les mots du titre opacity1/filternone/transformnone; seconde observation identique après le callback. La revue a fait compléter le garde-fou : les descendants sont désobservés et leurs animations terminées au focus, et les deux observers ignorent une section contenant le focus, même si une entrée était déjà en file d’attente. Reduced motion reste vérifié dans le code uniquement.

Contrôles de livraison :16 pages, références locales sans erreur dans check-site-v4.txt; tells sans limite dépassée. L’audit a signalé trois769px qui sont des seuils de breakpoint (bord768/769), et non des espacements; les autres messages sont des rapprochements heuristiques de noms de composants, examinés avec les sources choisies. Aucun changement aux tokens pour masquer ces faux positifs.

Limites conservées : contrôle réel HTTP localhost; le protocole file:// a été bloqué par la politique du navigateur lors de la passe précédente, sans contournement. L’accessibilité tactile/clavier n’équivaut pas à un test de lecteur d’écran. Les SVG identifient les plateformes; aucune réservation ni transaction effectuée.
