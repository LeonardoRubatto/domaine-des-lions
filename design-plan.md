## Intent
Présenter une maison normande privatisée pour 15 personnes et mener familles, amis et équipes vers une demande ou une réservation externe. FR et EN complets, maquette locale.

## Directions
- A — La maison, pour vous · brochure d'une maison ouverte à ses invités · hero full-bleed, grille 12-col, top-bar, type mixed/classic, surface photo/white, one-accent, images full-bleed, motion none, voix warm.
- B — L'album normand · album d'exposition des peintres de la région · hero minimalist, grille single-column, nav in-content, serif/flat, surface white, two-tone, images framed, motion mechanical, voix formal.
- C — Le domaine à explorer · plan physique d'un domaine à l'entrée · hero product-forward, grille modular, nav side-rail, sans/flat, surface brand-color, full-palette, images illustration/aerial, motion playful, voix technical.
Obvious version (not a direction): hôtel générique avec serif italique, fond crème, étoiles inventées, trois cartes et vidéo de stock.
Chosen: A — choisi par Leonardo, avec un accent discret sur l'art et une sélection des vraies photos.

## Concept
La maison à colombages s'ouvre sur ses pièces et son jardin : le visiteur découvre ce qu'il aura à lui seul, puis prépare le séjour de son groupe.
Swap test: une chambre d'hôtel ou une location de ville ne pourrait pas conserver l'ouverture maison entière, la piscine couverte, les jardins de 6000 m², le tennis et les chambres de peintres qui structurent ce parcours. Cette structure décrit cette propriété précisément, sans prétendre que tous ses attributs sont uniques.

## Signature
Au premier écran desktop, la vraie façade vue à travers le jardin porte l'invitation « Bienvenue chez vous »; un accès maison / piscine / jardin donne trois vues de la même propriété. Le lion photographié accompagne la piscine et l'art intervient dans la visite de la maison.

## Not this
Pas d'eyebrows répétés, d'accent-word italique, d'arrow-links systématiques, de stats-band gigantesque, de trois cartes égales, de reveal-every-heading, de paper-background par défaut. Pas de prix, étoiles, disponibilité ou score d'avis inventés.

## Dials
- hero: full-bleed — vraie maison à colombages derrière un texte court
- grid: 12-col — photos dominantes et textes à largeur de lecture
- nav: top-bar — une seule ligne et un switch FR/EN de 44px
- type-voice: mixed — Georgia pour les titres, Segoe UI pour la lecture
- type-scale: classic — display 80px desktop / body 18px
- surface: white — photos et petites zones vert sombre, sans papier crème
- color: one-accent — vert issu du jardin, terre cuite réservée aux détails
- image: full-bleed — photographie réelle sans filtre esthétique trompeur
- motion: cinematic — approche douce de la façade au scroll; galerie fluide; aucune animation automatique ni scroll imposé
- voice: warm — reprendre « Bienvenue chez vous » et les descriptions du propriétaire
- override: top-bar et photo restent les formes les plus lisibles pour les deux langues et le séjour; les choix sont justifiés par la maison, pas par une rotation arbitraire.

## Layout
Header compact → façade → confort concret → piscine/jardin → séjour famille/équipe en deux panneaux → visite 3D → avis réels → accès → demande. Pages domaine, familles, séminaires, galerie, séjour, accès et mentions légales, chacune en FR/EN. Spacing base 4px suivant rules/spacing.md; lectures max 680px et contenu max 1280px. Les photos salon/piano/chambre utilisent la pile Images Reveal; les deux Pan de l'accueil sont réservés au header et au hero, les autres actions restent secondaires.

## Type
Georgia serif traduit le caractère domestique et les œuvres, sans imiter une identité de palace. Segoe UI pour les textes et la réservation. Échelle fluide 18/24/32/48/96px, aucun chargement de police tiers. Georgia 400 pour les titres; Segoe UI 400 pour les textes, 600 pour les labels, 700 pour Pan (poids tiers déclaré). Boutons sur une ligne à 1.2, tracking titres -.025em, label caps .08em. Pan conserve le rayon 3rem du composant; autres surfaces sans rayon, bouton lecture 3D circulaire.

## Color
Scale generated with generate-color-scale.mjs --hue 150 --chroma 0.045; tokens/green.css et tokens/ui.css. White conserve la clarté des fenêtres, vert sombre issu du jardin, terre cuite issue des sols. Contrastes des vrais couples vérifiés avant livraison.

## Motion
160ms cubic-bezier(0.2, 0, 0, 1) pour boutons; 320ms pour la grille; 640ms pour les photos. Mode expressif. Accueil: zoom façade au scroll (signature), Pan (support), trois photos qui se redressent et passent devant au hover/focus (support). Les panneaux famille/équipe et 3D restent immobiles. Galerie: reflow FLIP et zoom 1.035, Pan du header. Zoom façade de 1 à 1.08 au scroll desktop sans pin et fallback statique. Aucune boucle. Reduced motion: instant état final, transition none. Menu et lightbox: focus initial, Escape, retour au déclencheur.

## Items
- primitives/button-hover-styles — variante Pan: capsule 3rem, contour 2px, label difference et fond qui remonte conservés; seuls palette/police/timing locaux et corrections focus-visible/reduced-motion. Deux maximum par page.
- image-treatment/images-reveal — pile et redressement au survol conservés, trois photos client, liens et focus équivalent, moteur CSS au lieu de Motion, pas de mount animation.
- transitions/flexbox-filter-flip — référence de grille filtrable, réimplémentation sans copier le code à licence inconnue et sans moteur GSAP.
- scroll/scrolltrigger-image-zoom — référence pour approcher la façade, réimplémentation CSS native, sans pin, GSAP ou code du CodePen.
Les autres structures utilisent la plateforme native décrite dans le manuel : details, dialog, grid. La 3D réutilise le Panotour du client dans une fenêtre immersive ouverte volontairement, avec lien direct de secours, sans reconstruire le domaine.
