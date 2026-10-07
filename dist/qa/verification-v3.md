# Vérification de la version 3 — 7 octobre 2026

16 pages statiques, huit FR et huit EN. Maquette locale, aucune publication.

## Constats navigateur

- Dimensions réelles contrôlées : 1440×900 et 390×844. Les 16 pages ont un scrollWidth de375px à390px de viewport (barre de défilement15px) : aucun débordement horizontal. Détail dans mobile-checks-v3.json.
- Galerie : passage automatique de1/5 à2/5 puis4/5 observé; pause affiche « Relancer le diaporama » et aria-live=polite. Suivant et flèche droite fonctionnent. Au repos, une seule diapositive active et clip-path circle(100%). Transition native800ms; deux diapositives pendant le mouvement.
- Filtre Les chambres :25 photographies; agrandissement1/25, Échap ferme et le focus revient au bouton Agrandir. Menu mobile : Échap revient au bouton Ouvrir le menu.
- Flou progressif : six couches par grand cadre, backdrop-filter final6px calculé dans le navigateur. Captures montrent la limite inférieure floutée et le reste net. Texte accessible complet conservé sur les trois titres découpés par mot.
- Avis : rotation observée deAvis1/8 àAvis2/8; un seul avis visible. Intervalles mesurés10300ms puis16600ms, selon la longueur. Survol et focus arrêtent la rotation; pause et reprise explicites.
- Visite 3D : un iframe à la demande; piscine=pano6817 et salle à manger=pano6794, panorama réel rendu. Plein écran vérifié; la commande « Réduire la visite » ramène au site. Fermer supprime l’iframe, restaure la couverture et le focus au bouton Commencer. Sur mobile, piscine chargée sans débordement, cadre360px.
- Descriptions :11 chapitres ouverts sur Le domaine, aucun details. Séjour : six informations pratiques directement visibles.
- Formulaire : départ égal à l’arrivée produit l’erreur explicite; dates valides génèrent une prévisualisation locale. Aucun e-mail envoyé. Liens Airbnb/Booking conservés.

## Vérification du code et limites

- JavaScript syntaxiquement valide. Motion Primitives Progressive Blur et Text Effect, Codrops Shapes Slideshow et boutons nommés, Componentry Scroll Tilted Grid, Animata Stacked Sections : code source lu, adaptations et licences dans CREDITS.md.
- Reduced motion : transitions CSS désactivées, WAAPI court-circuitée et animations en cours terminées, tilt statique, aucune rotation automatique. Vérifié par lecture du code; ce navigateur ne propose pas d’émulation de cette préférence via son API documentée.
- L’accès direct file:// a été refusé par la politique du navigateur. Le contrat de portabilité est contrôlé statiquement (ressources relatives, polices embarquées, scripts classiques) et le site est testé via HTTP local; aucune vérification visuelle file:// prétendue.
- Le contrôle audit produit des pistes par mots-clés (« possible-reinvention »), souvent sans relation avec l’implémentation. Les patterns réellement utilisés sont attribués. Les valeurs de motion et d’espacement sont contrôlées séparément.
- Les mentions de propriétaire/hébergeur et les droits de publication restent à finaliser pour une mise en ligne; maquette noindex. La visite utilise le prestataire existant et une connexion Internet.

## Revue

Captures dans screenshots-v3/. Revue indépendante et contrôles du dossier dist consignés dans les fichiers QA associés après exécution.

## Correction après retour utilisateur

Le flash venait de l’état visible peint avant le reset WAAPI. Les photos déjà dans le premier viewport restent stables. Les autres portent image-await avant leur entrée : opacity0 constatée hors écran, puis0.973 pendant le mouvement et1 après retrait de la classe. Le diaporama attend image.decode avant le changement, sans vider le cadre sortant. Flou réduit à16%/6px après revue.
