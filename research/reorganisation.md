# Le Domaine aux Lions — étude et architecture

Étude du 7 octobre 2026. Source : https://ledomaineauxlions.fr/. Direction retenue par Leonardo : « La maison, pour vous », avec présence discrète de l'art. Langues : français et anglais. Destination : maquette locale de prospection.

## Ce qui est conservé

Les logos actuels et historiques, les photographies, la visite virtuelle existante, les descriptions de la maison et des équipements, les contenus famille et entreprise, les témoignages et leurs noms, les informations d'arrivée, les liens sociaux, le contact et les conditions de séjour. Les textes bruts des 12 pages sont archivés dans `source-pages/`; leurs blocs, images et liens dans `content-inventory.json`. Les sources sont séparées de la nouvelle copie de navigation.

## Constats observés

| Élément | Observation vérifiable | Conséquence et décision |
|---|---|---|
| Navigation desktop | Environ 176px de haut à 1440×900; grand logo vertical, sept destinations dont la langue. | Réduire le logo avec toutes ses proportions conservées; une seule barre, langue courte, action de séjour visible. |
| Navigation FR | Le lien textuel « Le Domaine aux Lions » dirige vers `/en/le-domaine-aux-lions/`. | Des équivalents linguistiques corrects pour chaque page; le switch conserve la page consultée. |
| Accueil | « Plus de détails » est l'action principale; contact plus bas. | Faire de l'organisation du séjour le prochain pas explicite; conserver une visite secondaire. |
| Conversion | Aucun lien Airbnb ou Booking.com trouvé dans les 12 HTML sources; la page contact est principalement une page d'accès. | Page séjour propre, demande réelle par messagerie et plateformes clairement identifiées. |
| Présentation | Pièces, chambres, cuisine, jardin, familles et conditions sur une même page très longue. | Préserver tous les détails, répartir les intentions, introduire des groupes de contenu lisibles. |
| Galerie | 39 entrées, non organisées par espace et essentiellement sans texte alternatif. | Classement maison / chambres / détente / jardin; captions descriptives; lightbox avec clavier. |
| Avis | Huit témoignages répétés dans le pied de page. | Témoignages dans un vrai moment de réassurance avant la demande; footer concis. Aucun score ajouté. |
| 3D | Panotour / krpano externe, opérationnel dans le navigateur le jour de l'étude. | Visite mise en contexte sur l'accueil et le domaine; ouverture volontaire du vrai tour, sans charge initiale lourde. |
| Identité | Deux logos distincts, façade à colombages, tomettes, poutres, lions décoratifs, peintures normandes. | Design issu du lieu et des assets, sans remplacer le logo ni appliquer un univers hôtelier générique. |

Les hauteurs sont des mesures de la vue inspectée, pas une promesse pour tout écran. Les effets de conversion sont des hypothèses de conception; aucune donnée d'analytics du client n'a été consultée.

## Architecture et migration du contenu

| Ancien contenu | Nouvelle destination | Place sur l'accueil |
|---|---|---|
| Accueil / Home | Accueil | Maison privatisée, 15 invités, localisation et action principale |
| Présentation générale | Le domaine / The house | Invitation et quelques photos de séjour |
| Rez-de-jardin, étage, chambres, peintres | Le domaine, groupes détaillés | Salon principal et clin d'œil à l'art |
| Piscine, terrasse, tennis, buanderie, jardin | Le domaine, équipements détaillés | Piscine et jardin expliqués avec les vraies photos |
| Toutes les photographies publiques | Galerie / Gallery + photos contextuelles | Sélection réduite, accès à toute la galerie |
| Familles, activités, équipements bébé | En famille / Family stays | Un panneau à côté du séjour professionnel |
| Entreprises, fibre, projecteur, whiteboard, prestataires | Séminaires / Team retreats | Un panneau avec demande dédiée |
| Linge, lits, ménage, services complémentaires | Le domaine + Préparer votre séjour | Réassurance de confort et accueil personnel |
| Caution, minimum de nuits, tranquillité | Préparer votre séjour + FAQ | FAQ avant l'action finale |
| 3D TOUR | Lien du vrai tour sur accueil et domaine | Aperçu photographique et action explicite |
| Contact, adresse, cartes et cinq images d'arrivée | Accès / Getting here + séjour | Localisation courte; route vers l'accès complet |
| Huit avis clients | Section témoignages de l'accueil | Après découverte, avant préparation du séjour |
| Instagram, Facebook, logo historique | Footer | Pied de page sobre, contact et crédit Telaventis |

## Parcours de réservation

1. Le visiteur comprend qu'il réserve une maison entière pour son groupe, avec un maximum de 15 personnes.
2. Le bouton principal mène à « Préparer votre séjour ». Il peut préciser dates, nombre d'invités et motif du séjour.
3. Le formulaire prépare un e-mail; l'interface indique clairement qu'il ouvre la messagerie et que rien n'est envoyé par le site. Aucun backend fictif.
4. Airbnb et Booking.com sont des chemins alternatifs vers les annonces publiques identifiées, avec leurs conditions et tarifs. Aucun prix ni disponibilité importés.
5. Le visiteur professionnel est conduit au même contact, avec la demande séminaire explicitée.
6. Les conditions et l'accès sont accessibles avant de poursuivre. L'offre reste compatible avec la tranquillité exigée par le propriétaire : aucun positionnement fête ou événement bruyant.

Annonces identifiées lors de la recherche : https://www.airbnb.fr/rooms/47524920 et https://www.booking.com/hotel/fr/domaine-aux-lions-piscine-tennis-20-min-deauville.html. Les adresses identifient cette propriété; les canaux privilégiés et leurs conditions devront être confirmés avec le propriétaire avant publication.

## Direction visuelle et choix des photos

La façade vue depuis le jardin ouvre le site. Les vues du salon, du billard, du piano, de la piscine couverte et du court de tennis rendent l'offre précise. Les photos de chambres lumineuses de la galerie servent de présentation; les séries plus récentes restent disponibles et ne sont pas supprimées. Les dates des fichiers ne prouvent pas l'état actuel des chambres : cette correspondance est à valider avec le propriétaire. Les vues aériennes aident à comprendre la propriété, sans inventer les positions des installations.

L'art est un détail réel de la maison : chambres aux noms de peintres normands, reproductions et œuvres contemporaines. Aucune liste de noms de chambres n'est inventée. Les lions décoratifs restent présents dans les photographies et le logo historique. Les originaux ne sont pas retouchés pour simuler un équipement ou un standing supérieur.

## Design system : application concrète

Racine : `C:/\.Leonardo/Project/design system (website elements template)` (voir le chemin absolu résolu dans la session). Plan enregistré, tokens de projet, échelle de couleur OKLCH générée, primitives consultées avant écriture et variantes adaptées. Bouton Codrops `pan` avec focus clavier et préférence de mouvement; grille filtrable inspirée du pattern référencé, sans copier son code; dialogs et disclosures natifs selon le manuel.

Un seul effet de bouton discret, pas de scroll forcé, pas de WebGL décoratif. Les photographies livrées sont locales, responsive AVIF/WebP. Vérification : pages FR/EN, liens, formulaires, focus, mobile 390px, desktop 1440px, audit et critique indépendante.

## Points à confirmer avant mise en ligne

- Conditions et canaux de réservation privilégiés; coût, calendriers et annulation ne sont pas exposés par le site actuel.
- Le site indique 8 chambres, et l'annonce Airbnb mentionne 11 avec annexes; conserver la distinction et ne pas promettre une configuration nouvelle.
- L'accueil mentionne 2h / moins de 30min, la présentation 1h45 / 20min; utiliser la formulation prudente de l'accueil.
- Les textes actuels vus dans le navigateur disent piscine chauffée toute l'année à 28°C avec réserve de grand froid. Des anciens extraits de moteurs contiennent des saisons différentes; utiliser la version actuelle et faire confirmer avant publication.
- Les horaires piscine 8h–20h figurent en français mais pas partout en anglais; aligner les informations pratiques en traduction.
- Les mentions légales complètes, l'identité juridique de l'éditeur et l'hébergeur final restent inconnus. La maquette présente ce manque sur la page juridique et reste non indexable.

La maquette peut être montrée au prospect. Elle ne remplace pas les validations du propriétaire sur les informations commerciales et juridiques.
