# Le Domaine aux Lions — maquette FR / EN

Ouvrir `index.html` dans un navigateur, ou servir ce dossier avec un serveur statique. La version anglaise commence dans `en/index.html`. Le dossier `dist/` contient uniquement le site livrable, ses ressources et ses crédits.

Huit pages dans chaque langue : accueil, domaine, famille, séminaires, galerie, séjour, accès et mentions légales. Logo et photographies conservés ; typographies locales ; galerie composée avec diaporama à transition circulaire et index filtrable ; avis automatiques avec pause ; descriptions ouvertes et illustrées ; un seul espace Panotour intégré à l’accueil, chargé à la demande avec accès aux scènes réelles. Demande de séjour préparée localement et liens Airbnb et Booking existants.

Le formulaire prépare un e-mail à relire dans la messagerie du visiteur. Il ne confirme ni disponibilités, ni tarif, ni réservation. La visite 3D reste hébergée par son prestataire et nécessite une connexion Internet.

Design Memory : boutons Codrops Hyperion, Dione, Skoll et Fenrir ; Animata Stacked Sections ; Codrops Shapes Slideshow ; Componentry Scroll Tilted Grid ; Motion Primitives Progressive Blur, Text Effect et Morphing Dialog ; couleurs OKLCH et tokens locaux. Diaporama automatique toutes les huit secondes avec pause, flou progressif au bas des grands cadres, transitions communes entre sections et six titres ciblés à l’accueil. Reduced motion désactive les mouvements et les rotations automatiques. Décisions finales : `design-plan-v3.md`. Vérifications : `qa/verification-v4.md`.

Cette maquette reste en `noindex`. Avant une mise en ligne, renseigner le domaine dans `scripts/build-site.py` (BASE), les informations légales du propriétaire et de l’hébergeur, puis adapter l’indexation. Les mentions à compléter sont signalées dans la page légale.

Régénérer le site : `python scripts/build-site.py`. Préparer le dossier livrable : `python scripts/prepare-delivery.py`. Aucune installation npm nécessaire pour utiliser le site.

Attributions et licences : `CREDITS.md` et `licenses/`.


Révision v4 : hero photographique sans surtitre ni bandeau sombre; 71 photos dans la galerie, dont les six nouvelles avec catégorie et légende FR/EN; cinq repères d’arrivée sur la page d’accès. Symboles Airbnb et Booking.com dès l’accueil et aux réservations. Visionneuse Morphing Dialog adaptée en JavaScript natif : géométrie de la miniature vers l’image entière, navigation filaire, fermeture animée, focus clavier et décodage préalable. Voir qa/verification-v4.md.
