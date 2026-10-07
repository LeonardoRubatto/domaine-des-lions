## Intent
Faire découvrir et réserver une maison normande entière pour 15 invités. Maquette complète FR/EN, photos et logo du propriétaire, visite Panotour conservée.

## Directions
- A — La maison, pour vous · livre illustré des maisons à colombages du Pays d'Auge · ouverture asymétrique et grands chapitres du jardin qui se superposent.
- B — L'album normand · catalogue imprimé des peintres normands · miniatures encadrées, typographie compacte et navigation dans la marge.
- C — Le domaine à explorer · plan d'accueil physique d'une propriété · vue aérienne dominante et visite 3D au premier écran.
Obvious version: photo sombre sous un titre hôtelier, bouton capsule quelconque, chiffres géants et trois cartes d'équipements.
Chosen: A — choisi par Leonardo, avec une présence discrète de l'art. Il demande maintenant de construire; la lecture exhaustive restante est suspendue, sans prétendre qu'elle est terminée.

## Concept
Les colombages organisent la maison; le site organise les espaces que le groupe aura pour lui seul : salons, chambres, piscine, tennis et jardin.
Swap test: remplacer les photos par celles d'un hôtel casse les chapitres d'une maison privatisée, le lion sculpté près de la piscine couverte et la visite continue des pièces et du jardin. Les dimensions et équipements décrivent le domaine, sans prétention d'unicité.

## Signature
Après la façade et les pièces lumineuses, deux grands chapitres piscine/tennis se superposent comme les pages d'un livre de la propriété. Photos nettes, texte lisible, aucune information révélée uniquement par l'effet. La visite 3D suit avec une vue aérienne et un contrôle circulaire explicite.

## Not this
Pas de photo assombrie pour porter tout le texte, de paper-background, d'eyebrow répété, de pills, de numbered-index ou de reveal-every-heading. Une seule formule poétique au hero. Pas de tarifs, d'étoiles, d'avis ou de disponibilités inventés.

## Dials
- hero: asymmetric — grand titre et introduction décalée au-dessus de la façade
- grid: asymmetric — photographies de tailles différentes, chapitres 5/7, aucune série de trois cartes égales
- nav: top-bar — 80px desktop, 72px mobile, langue 44px et Hyperion rectangulaire
- type-voice: mixed — Source Serif 4 pour le livre de la maison, Public Sans pour l'information pratique
- type-scale: classic — 96px display / 17px body, fluide jusqu'à 52px mobile
- surface: white — blanc des fenêtres et vert seulement pour tennis et visite
- color: two-tone — jardin et terre cuite des sols, échelles OKLCH
- image: framed — photos rectangulaires nettes, sans coins arrondis ni filtres
- motion: mechanical — superposition de deux chapitres, comportements exacts des boutons, pas de scroll capturé
- voice: warm — invitation domestique, informations concrètes, mots du propriétaire
- override: navigation familière et photographies restent nécessaires pour ce lieu; les choix sont motivés par les contenus et l'accès à la réservation, pas par une rotation artificielle.

## Layout
Header → titre/façade → maison/salon/chambre → piscine/tennis → visite 3D → famille/équipe → avis hors footer → localisation → réservation directe ou Airbnb/Booking. Les 8 pages existent dans les deux langues; textes d'origine conservés dans les pages détaillées. Base 4px, contenu 1280px, paragraphes 640px, photos AVIF/WebP.

## Type
Source Serif 4 400/600, tradition du livre illustré qui relie colombages et tableaux; Public Sans 400/600 pour les légendes et la réservation internationale. Polices OFL locales, font-display swap. Échelle 14/17/24/32/48/96px, titres 1.1, boutons 1.2 sans exception. Aucun serif italique d'accent.

## Color
tokens/green.css généré par generate-color-scale.mjs --hue 150 --chroma 0.045; tokens/clay.css --hue 45 --chroma 0.075. tokens/ui.css applique blanc et vert-12 au texte, vert-11 aux liens. Hyperion conserve noir/blanc et mix-blend-mode difference du code exact. WCAG et APCA mesurés dans le rendu.

## Motion
Accueil: Stacked Sections withDramaEffect=false, deux panes, stackOffset=48px, sans runway. Désactivé sous 900px, sur écran peu haut et en reduced-motion; focus dans un chapitre désactive la superposition. Support éditorial: IntersectionObserver, entrée unique 600ms avec translation 20px, et profondeur photo au survol 600ms scale 1.03. Hyperion 200ms + 200ms label et remplissage 300ms cubic-bezier(0.7,0,0.2,1); Fenrir 400ms cubic-bezier(0.7,0,0.3,1). Galerie: FLIP 320ms cubic-bezier(0.2,0,0,1). Reduced motion instantané. Dialog: Tab contenu, Escape fermeture, retour explicite au déclencheur. Galerie: flèches gauche/droite; filtres aria-pressed; avis sans autoplay.

## Items
- primitives/button-hover-styles — Hyperion avec nested spans, animation verticale en deux phases et remplissage scaleX conservés. Fenrir garde cercle 120px, anneau 80px, expansion 1.2 et tracé SVG. Adaptations: type, anneau, focus-visible, reduced-motion, casse phrase.
- scroll/stacked-sections — conversion vanilla de withDramaEffect=false; sticky siblings et padding index*48 conservés. Adaptations: header, mobile/RM/focus, deux chapitres.
- transitions/flexbox-filter-flip — référence seulement; reflow natif sans copie du CodePen ni GSAP.
Details natifs pour les descriptions; dialog pour les photos et la vraie visite 3D; demande préparée localement; liens vers les annonces existantes.
