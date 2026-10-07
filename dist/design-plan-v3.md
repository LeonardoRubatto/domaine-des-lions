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
La maison reste l'ouverture. Les chapitres piscine/tennis se superposent; quatre photographies éditoriales se redressent doucement au défilement. La visite est un espace 3D unique intégré à l'accueil, avec accès aux scènes réelles du salon, de la piscine, du jardin, de la salle à manger et de la chambre Monet. La galerie possède une grande scène photographique à transition circulaire, suivie d'un album de formats variés.

## Not this
Pas de photo assombrie pour porter tout le texte, de paper-background, d'eyebrow répété, de pills, de numbered-index ou de reveal-every-heading. Aucun surtitre et aucune formule poétique au hero; le nom réel du domaine ouvre la présentation. Pas de tarifs, d'étoiles, d'avis ou de disponibilités inventés.

## Dials
- hero: asymmetric — photo dominante décalée à droite, nom du domaine dans un retrait blanc au bas du cadre, piano à gauche, informations après le titre
- grid: asymmetric — photographies de tailles différentes, chapitres 5/7, aucune série de trois cartes égales
- nav: top-bar — 80px desktop, 72px mobile, langue 44px et Hyperion rectangulaire
- type-voice: mixed — Alegreya pour le livre de la maison, Alegreya Sans pour l'information pratique
- type-scale: classic — 112px au hero / 96px display interne / 18px body, fluide jusqu'à44px sur320px
- surface: white — blanc des fenêtres et vert seulement pour tennis et visite
- color: two-tone — jardin et terre cuite des sols, échelles OKLCH
- image: framed — photos rectangulaires nettes, sans coins arrondis; flou progressif discret au bas des grandes images uniquement
- motion: mechanical — superposition de deux chapitres, comportements exacts des boutons, pas de scroll capturé
- voice: warm — invitation domestique, informations concrètes, mots du propriétaire
- override: navigation familière et photographies restent nécessaires pour ce lieu; les choix sont motivés par les contenus et l'accès à la réservation, pas par une rotation artificielle.

## Layout
Les huit pages FR/EN subsistent. Les descriptions sont toujours visibles dans des chapitres ouverts, les informations pratiques sont disposées en deux colonnes, les avis apparaissent dans une galerie automatique avec pause. L'espace 3D n'est plus répété sur les pages internes; elles pointent vers l'accueil. La galerie commence par cinq grandes photos choisies, puis montre toutes les images dans une composition décalée. Mobile : une colonne, commandes 44px minimum, taille adaptée de la visite intégrée.

## Type
Typographie validée le 8 octobre, autorisée pour push : Alegreya 400/440 pour les titres et les témoignages, Alegreya Sans 400/500 pour le texte et les commandes. Le dessin humaniste aux inflexions calligraphiques rappelle le livre illustré et les tableaux de la maison, avec un rythme moins neutre que l'ancienne paire Source Serif 4/Public Sans. Aucune revendication d'origine normande de la police. Texte courant à18px pour la petite hauteur d'œil de la sans; descriptions compactes à16/17px, légendes à14px. Navigation et actions à16px desktop, action du header à14px mobile; capacité et localisation à14px mobile. Deux graisses par famille, grands titres h1/h2 à440 à la demande de Leonardo, soit un léger renfort depuis400; h3 et témoignages à400 pour garder une présence domestique plutôt qu'institutionnelle. La valeur de graisse440 n'est pas une mesure de10% d'épaisseur optique. Polices OFL locales, font-display swap. Tailles des grands titres conservées, titres1.1 et boutons1.2; aucune italique d'accent.

## Color
tokens/green.css généré par generate-color-scale.mjs --hue 150 --chroma 0.045; tokens/clay.css --hue 45 --chroma 0.075. tokens/ui.css applique blanc et vert-12 au texte, vert-11 aux liens. Hyperion conserve noir/blanc et mix-blend-mode difference du code exact. WCAG et APCA mesurés dans le rendu.

## Motion
Accueil : Stacked Sections withDramaEffect=false, stackOffset=48px. Support : boutons Hyperion (200/300ms), Dione (300ms cubic-bezier(0.2,1,0.7,1)), Skoll (300ms cubic-bezier(0.7,0,0.2,1)), Fenrir (400ms cubic-bezier(0.7,0,0.3,1)); Scroll Tilted Grid adapté sur quatre photos, maxTilt=16/maxBlur=0, sans Lenis ni boucle. Passages entre sections : ouvertures de cadres de 800ms (inset8% vers0), fondu de92% à100% et décalage vertical16px aux ruptures de section, une fois à l’entrée. Six titres maximum à l’accueil : Text Effect, slide par mot pour le nom et la visite, fade-in-blur4px pour maison, piscine, tennis et témoignages;400ms avec stagger50ms plafonné à200 ou300ms, texte accessible entier. Le titre de galerie conserve son slide. Progressive Blur : six couches masquées, intensité1.2px, sur les16% inférieurs du hero et des grandes diapositives. Galerie : autoplay8000ms avec pause explicite, arrêt au focus/survol/hors écran/onglet caché; Shapes Slideshow, clip circulaire, translation du cadre et contre-translation de l'image; 800ms cubic-bezier(0.2,0,0,1). Avis : 400ms, autoplay entre 9 et 60 secondes selon la longueur du texte, arrêté au focus/survol/hors écran/onglet caché et bouton Pause. Reduced motion : aucun autoplay, aucune transition ni tilt. Les contenus restent visibles sans JS et après les entrées; les informations pratiques ne sont pas animées. 4px grid, exceptions0/1/2 pour traits et détails optiques. Les comportements supplémentaires répondent à la demande explicite de Leonardo.

## Items
- primitives/button-hover-styles — Hyperion au header; Dione pour les actions; Skoll pour les commandes; Fenrir pour entrer dans la visite. Code, séquences et structures spécifiques conservés, valeurs adaptées à la typographie et au tactile.
- scroll/stacked-sections — port natif sans drama effect; offset48, mobile/RM/focus en flux normal.
- scroll/scroll-tilted-grid — courbes géométriques du code stocké, port natif; valeurs modérées, sans blur ni Lenis, reset sur mobile, au focus et en reduced motion.
- gallery-carousel/shapes-slideshow — architecture, masque circulaire, déplacement opposé de l'image et du cadre conservés; port WAAPI, délai compressé à800ms, images visibles en plein cadre au repos, clavier et reduced motion ajoutés.
Descriptions ouvertes; iframe 3D à la demande, scènes vérifiées dans les fichiers publics du prestataire, aucun panorama recopié. Galerie classique aussi accessible via lightbox.


- backgrounds/progressive-blur — six couches et gradients du code source, intensité limitée au bas des grands cadres, overlay non interactif.
- text-effects/text-effect — preset slide, découpage par mot et texte sr-only intact, adaptation WAAPI avec IntersectionObserver et reduced motion.

Revue finale : le hero de la page En images défile automatiquement, conformément à la demande. La façade de l’accueil reste stable. Les images hors écran sont préparées avant observation; aucune remise à zéro de l’opacité pour les photos déjà affichées. Une diapositive attend le décodage de la suivante avant de la remplacer. Les captions génériques répétées sont retirées de la grille visible; les descriptions accessibles restent. Aucun nom de chambre attribué sans correspondance vérifiée. Le grand guillemet décoratif des avis est retiré. Les titres partagés en colonnes servent l’introduction de la photographie et des explications très courtes, pas une série de sections identiques.

Révision hero : retrait du surtitre, du bandeau sombre et des liens de découverte répétés. Composition depuis les primitives et layout.md : les heroes shaders inspectés sont inadaptés aux photos du lieu, donc aucun shader ajouté. Le blanc sous le nom forme un retrait dans la photographie, sans bordure ni ombre; une petite vue du piano relie intérieur et façade. Mobile : photo en tête, nom dessous, détail du piano associé à l’introduction. Les animations existantes restent, avec aucun reset des photos déjà affichées.

Révision v4 : sur mobile le piano est retiré du hero pour laisser la place à la réservation et aux informations. Symboles Airbnb et Booking.com locaux, couleurs de marque conservées, dès le hero et aux liens de réservation; seul le soulignement des liens s’anime (300ms), les marques restent stables. Les six photos anciennement exclues à cause de leur nom de fichier sont intégrées et légendées en FR/EN : salons dans la maison, chambre dans les chambres, bassin et tennis dans la détente, façade panoramique dans la maison et graminées dans le jardin. 71 photos dans la galerie; les cinq repères d’arrivée restent sur la page d’accès.

Hero mobile final : le retrait blanc du nom rejoint le bas de la façade; il dépasse de48px et les informations commencent72px après la photo. Capacité et localisation sont deux lignes compactes, suivies de la description et des marques. Photo de280 à360px, titre44 à64px; sur390px l’ensemble laisse apparaître le début du contenu suivant à844px. Le village reste dans l’adresse, la version desktop et la page d’accès; le repère mobile retient Normandie et2h de Paris pour éviter quatre lignes.

Dernière demande, transitions communes : aux vraies ruptures de section, fondu léger de92% à100% et déplacement vertical16px,800ms, une seule fois; préparation uniquement hors écran, aucun reset d’un élément déjà peint. Les longs chapitres de la maison passent séparément; les photos de grille, champs du formulaire et petits blocs pratiques ne multiplient pas cette transition. Anciennes entrées isolées des quatre blocs retirées pour éviter le cumul. Le scroll reste natif. Focus clavier et reduced motion donnent immédiatement le contenu stable.

Text Effect ajouté aux quatre titres éditoriaux maison, piscine, tennis et témoignages : preset fade-in-blur étudié dans le code source, intensité réduite de12 à4px, déplacement12px,400ms, stagger50ms plafonné200ms. Le nom du domaine, le titre de la visite et le titre de galerie conservent leur slide; textes pratiques, légendes, commandes et footer restent entiers. Budget maximal de six titres à l’accueil, pas un reveal de tous les titres. Aucun nouveau composant inventé dans le manifeste : les transitions de section sont un support natif de mise en page, les sources scroll étudiées imposant quatre images ou un scroll capturé étant inadaptées.

- transitions/morphing-dialog — source complète étudiée, port natif de la géométrie partagée miniature et photo. Ouverture 800ms et retour 400ms, cubic-bezier(0.2,0,0,1); toile blanche avec arrière-plan légèrement translucide, image sans bordure, croix de fermeture et flèches filaires de 48px. Décodage préalable, navigation croisée 400ms, légende et compteur discrets. Échap, clic sur la marge, cycle Tab/Shift-Tab explicite, retour du focus et aria-expanded synchronisé. Reduced motion instantané; aucune navigation automatique dans cette visionneuse. Les primitives filaires utilisent les slots du composant, sans reprendre les boutons rectangulaires de l’ancienne fenêtre.
