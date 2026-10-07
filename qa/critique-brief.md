# Critique brief — dist

You are reviewing a website you did not build. You are not here to be kind
or to admire it. Your job is to find every part of it that is generic — that
would look the same on another client's site — and to say, for each one,
what this client's own material could replace it with.

Do not suggest effects you have seen on other sites. Every fix you propose
must come from the concept below or from the client's own material (their
place, objects, documents, words, photographs). If a fix needs material the
site does not have, say what material to ask for.

## What the site is supposed to be (from the design plan)

**Intent and audience**
Présenter une maison normande privatisée pour 15 personnes et mener familles, amis et équipes vers une demande ou une réservation externe. FR et EN complets, maquette locale.

**Concept**
La maison à colombages s'ouvre sur ses pièces et son jardin : le visiteur découvre ce qu'il aura à lui seul, puis prépare le séjour de son groupe.
Swap test: une chambre d'hôtel ou une location de ville ne pourrait pas conserver l'ouverture maison entière, la piscine couverte, les jardins de 6000 m², le tennis et les chambres de peintres qui structurent ce parcours. Cette structure décrit cette propriété précisément, sans prétendre que tous ses attributs sont uniques.

**Signature moment**
Au premier écran desktop, la vraie façade vue à travers le jardin porte l'invitation « Bienvenue chez vous »; un accès maison / piscine / jardin donne trois vues de la même propriété. Le lion photographié accompagne la piscine et l'art intervient dans la visite de la maison.

**Not this (the default version the plan rejected)**
Pas d'eyebrows répétés, d'accent-word italique, d'arrow-links systématiques, de stats-band gigantesque, de trois cartes égales, de reveal-every-heading, de paper-background par défaut. Pas de prix, étoiles, disponibilité ou score d'avis inventés.

**Dials**
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

**Type (including reasons for repeated typefaces)**
Georgia serif traduit le caractère domestique et les œuvres, sans imiter une identité de palace. Segoe UI pour les textes et la réservation. Échelle fluide 18/24/32/48/96px, aucun chargement de police tiers. Georgia 400 pour les titres; Segoe UI 400 pour les textes, 600 pour les labels, 700 pour Pan (poids tiers déclaré). Boutons sur une ligne à 1.2, tracking titres -.025em, label caps .08em. Pan conserve le rayon 3rem du composant; autres surfaces sans rayon, bouton lecture 3D circulaire.

**Color (including reasons for repeated surfaces)**
Scale generated with generate-color-scale.mjs --hue 150 --chroma 0.045; tokens/green.css et tokens/ui.css. White conserve la clarté des fenêtres, vert sombre issu du jardin, terre cuite issue des sols. Contrastes des vrais couples vérifiés avant livraison.

**Layout**
Header compact → façade → confort concret → piscine/jardin → séjour famille/équipe en deux panneaux → visite 3D → avis réels → accès → demande. Pages domaine, familles, séminaires, galerie, séjour, accès et mentions légales, chacune en FR/EN. Spacing base 4px suivant rules/spacing.md; lectures max 680px et contenu max 1280px. Les photos salon/piano/chambre utilisent la pile Images Reveal; les deux Pan de l'accueil sont réservés au header et au hero, les autres actions restent secondaires.

**Motion (including an intentional absence of motion)**
160ms cubic-bezier(0.2, 0, 0, 1) pour boutons; 320ms pour la grille; 640ms pour les photos. Mode expressif. Accueil: zoom façade au scroll (signature), Pan (support), trois photos qui se redressent et passent devant au hover/focus (support). Les panneaux famille/équipe et 3D restent immobiles. Galerie: reflow FLIP et zoom 1.035, Pan du header. Zoom façade de 1 à 1.08 au scroll desktop sans pin et fallback statique. Aucune boucle. Reduced motion: instant état final, transition none. Menu et lightbox: focus initial, Escape, retour au déclencheur.

**Items actually intended for the build**
- primitives/button-hover-styles — variante Pan: capsule 3rem, contour 2px, label difference et fond qui remonte conservés; seuls palette/police/timing locaux et corrections focus-visible/reduced-motion. Deux maximum par page.
- image-treatment/images-reveal — pile et redressement au survol conservés, trois photos client, liens et focus équivalent, moteur CSS au lieu de Motion, pas de mount animation.
- transitions/flexbox-filter-flip — référence de grille filtrable, réimplémentation sans copier le code à licence inconnue et sans moteur GSAP.
- scroll/scrolltrigger-image-zoom — référence pour approcher la façade, réimplémentation CSS native, sans pin, GSAP ou code du CodePen.
Les autres structures utilisent la plateforme native décrite dans le manuel : details, dialog, grid. La 3D réutilise le Panotour du client dans une fenêtre immersive ouverte volontairement, avec lien direct de secours, sans reconstruire le domaine.

## What it actually looks like

- C:\.Leonardo\TELAVENTIS BUISNESSES websites\domaine aux lions\qa\screenshots\hero-desktop.jpg
- C:\.Leonardo\TELAVENTIS BUISNESSES websites\domaine aux lions\qa\screenshots\home-desktop.jpg
- C:\.Leonardo\TELAVENTIS BUISNESSES websites\domaine aux lions\qa\screenshots\home-mobile.jpg
- C:\.Leonardo\TELAVENTIS BUISNESSES websites\domaine aux lions\qa\screenshots\house-desktop.jpg
- C:\.Leonardo\TELAVENTIS BUISNESSES websites\domaine aux lions\qa\screenshots\stay-mobile.jpg
- C:\.Leonardo\TELAVENTIS BUISNESSES websites\domaine aux lions\qa\screenshots\tour-desktop.jpg

## Machine scan (scripts/tells.mjs — regex heuristics, not a verdict)

| Tell | Count | Limit |
|---|---|---|
| eyebrow | 12 | 1/page |
| accent-word | 0 | 1/page |
| numbered-index | 0 | 1/page |
| arrow-links | 0 | 2/page |
| stats-band | 0 | 1/page, 1/site |
| three-equal-columns | 1 | 1/page, 1/site |
| pill-shapes | 0 | 2/page |
| reveal-every-heading | 0 | 3/page |
| paper-background | 0 | needs a reason in the plan |
| overused-font | 0 | needs a reason in the plan |

Over the limit:
- en\index.html: small label directly above a heading (eyebrow/kicker): 3× here, limit 1 ("LE DOMAINE AUX LIONS · NORMANDIE"; "360°"; "Fauguernon, Pays d’Auge"). See rules/forbidden.md → House-style tells.
- index.html: small label directly above a heading (eyebrow/kicker): 3× here, limit 1 ("LE DOMAINE AUX LIONS · NORMANDIE"; "360°"; "Fauguernon, Pays d’Auge"). See rules/forbidden.md → House-style tells.

## House-style tells to look for (rules/forbidden.md)

Everything above is the 2023 "AI website." Ban it and a model moves to the
next most likely look — and this library's own output did exactly that. On
2026-09-22 four delivered sites (Bénard, La Cave d'Antoine, the Cave's wine
list, Jeanne Randu) were free of every tell above and shared the list below
instead; the Cave's revision-2 plan had already named several of them by
hand. See [`distinctiveness.md`](distinctiveness.md) for the evidence and
the method that replaces them.

**The rule: each tell is allowed within its limit, and beyond that only
with a reason written in the plan** (`## Not this`, `## Type`, or
`## Color`) — a reason that comes from the concept, not "it looks nice."
Limits are counted by `scripts/tells.mjs` (and reported live by
`audit.mjs`) where the tell is regex-detectable; the rest are for the
critique pass (`scripts/critique.mjs`).

| Tell | What it looks like | Limit | Checked by |
|---|---|---|---|
| `eyebrow` | A small uppercase tracked label directly above a heading ("DEPUIS 1982 — ENTREPRISE FAMILIALE"). | 1 per page | tells.mjs |
| `accent-word` | One word inside the headline set apart — italic serif, a highlighter marker, or the accent color ("un *calice*?"). | 1 per page | tells.mjs |
| `numbered-index` | `01 / 02 / 03` zero-padded numbering, usually mono, with hairline rules, as the default way to list anything. | 1 per page | tells.mjs |
| `arrow-links` | → or ↗ on every link and button. | 2 per page | tells.mjs |
| `stats-band` | A row of big numbers with small labels under them ("1982 · 12 · 100+"). | 1 per site | tells.mjs |
| `three-equal-columns` | Any trio of equal cards — features, testimonials, services. The triptych is the three-rounded-cards tell with better typography. | 1 per site | tells.mjs |
| `pill-shapes` | Pill-shaped buttons, tags and badges everywhere. | 2 per page | tells.mjs |
| `reveal-every-heading` | A mask/fade/split reveal on every heading as it enters. | 3 per page | tells.mjs |
| `paper-background` | A warm off-white "paper" page surface (cream, ivory, ecru) as the default instead of white. | needs a reason | tells.mjs |
| `overused-font` | Instrument Serif/Sans, Cormorant, Playfair Display, Fraunces, DM Sans/Serif, Manrope, Space Grotesk/Mono, Plus Jakarta Sans, Outfit, Syne, Satoshi, Poppins, Montserrat, Geist, JetBrains Mono as label decoration — and Inter. | needs a reason | tells.mjs |
| `split-section-header` | Every section opens the same way: label + title on the left, a short paragraph on the right. | 1–2 per page | critique |
| `floating-cards` | Cards "floating" over a photo or a colored band, soft shadow, as the default container ("card sospese"). | needs a reason | critique |
| `callouts-everywhere` | Asides, notes and bordered callouts sprinkled through every section. | needs a reason | critique |
| `split-hero-rounded-photo` | Headline left, one rounded-corner photo right — the split archetype with nothing of the client in the layout itself. | needs a reason | critique |
| `poetic-two-liner` | Headline as a short poetic couplet, subhead as two soft sentences ("Vino, taglieri e due chiacchiere. Da Antoine, senza tante cerimonie."). | 1 per site | critique — see [`content.md`](content.md) |

These are not bad in themselves — every one of them appears in good work.
They are banned as *defaults*: reached for because they make an empty
section look designed, the same way Inter and three rounded cards once did.
**This list is meant to grow**: when a critique finds a generic pattern not
listed here, add a row with the project as evidence, and add it to
`scripts/tells.mjs` if a regex can see it.

## Evidence boundaries

Review the consequential promises in this plan, not an external effect quota.
An intentional motion-free design needs no stagger, reveal or ambient animation.
For behavioral claims, request the relevant code and browser verification notes
or exercise the behavior yourself if browser access is available. Screenshot paths
listed here do not establish that you inspected them. A still image cannot prove
timing, interruption, keyboard/focus, preference changes or performance. The
machine scan is not browser evidence. Mark unavailable evidence as not checked;
do not invent a finding or a clean pass. Keep conclusions within the tested scope.

## Answer in exactly this shape

1. **Generic elements.** Every element that could appear unchanged on another
   client's site. For each: where it is (page, section, viewport), why it is
   generic, and the concrete replacement drawn from the concept or the
   client's material. Most important first. Aim for at least five; if you
   find fewer, say why the rest holds up.
2. **Swap test.** Put a competitor's name, logo and photographs into this
   site. What breaks? If nothing breaks, say so plainly — the concept is
   decoration, not structure.
3. **Signature.** Is the signature moment from the plan actually visible
   above the fold at 1440×900? At 390×844? Is it built from the concept, or
   is it a catalog effect with the client's photo in it?
4. **Tells.** Each house-style tell present, whether the plan gives a reason
   for it (## Not this / ## Type / ## Color), and whether that reason holds.
5. **Copy.** Headlines, labels and buttons that could be on any site in the
   same trade. Quote them and rewrite them from the client's own words.
6. **The three changes** that would make this site most specific to this
   client, ranked. Each one names what to remove, not only what to add.
7. **Plan evidence.** For up to three consequential promises (signature,
   layout or motion), give: promise | code location when available | visual
   or browser evidence | status. Use checked — finding, checked — clean,
   not checked (missing evidence), or not applicable (reason). A plan is
   intent, not proof; label visual observations separately from behavior.

Keep the whole answer under 600 words. No praise section.
