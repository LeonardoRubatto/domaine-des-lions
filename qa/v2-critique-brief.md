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
Faire découvrir et réserver une maison normande entière pour 15 invités. Maquette complète FR/EN, photos et logo du propriétaire, visite Panotour conservée.

**Concept**
Les colombages organisent la maison; le site organise les espaces que le groupe aura pour lui seul : salons, chambres, piscine, tennis et jardin.
Swap test: remplacer les photos par celles d'un hôtel casse les chapitres d'une maison privatisée, le lion sculpté près de la piscine couverte et la visite continue des pièces et du jardin. Les dimensions et équipements décrivent le domaine, sans prétention d'unicité.

**Signature moment**
Après la façade et les pièces lumineuses, deux grands chapitres piscine/tennis se superposent comme les pages d'un livre de la propriété. Photos nettes, texte lisible, aucune information révélée uniquement par l'effet. La visite 3D suit avec une vue aérienne et un contrôle circulaire explicite.

**Not this (the default version the plan rejected)**
Pas de photo assombrie pour porter tout le texte, de paper-background, d'eyebrow répété, de pills, de numbered-index ou de reveal-every-heading. Une seule formule poétique au hero. Pas de tarifs, d'étoiles, d'avis ou de disponibilités inventés.

**Dials**
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

**Type (including reasons for repeated typefaces)**
Source Serif 4 400/600, tradition du livre illustré qui relie colombages et tableaux; Public Sans 400/600 pour les légendes et la réservation internationale. Polices OFL locales, font-display swap. Échelle 14/17/24/32/48/96px, titres 1.1, boutons 1.2 sans exception. Aucun serif italique d'accent.

**Color (including reasons for repeated surfaces)**
tokens/green.css généré par generate-color-scale.mjs --hue 150 --chroma 0.045; tokens/clay.css --hue 45 --chroma 0.075. tokens/ui.css applique blanc et vert-12 au texte, vert-11 aux liens. Hyperion conserve noir/blanc et mix-blend-mode difference du code exact. WCAG et APCA mesurés dans le rendu.

**Layout**
Header → titre/façade → maison/salon/chambre → piscine/tennis → visite 3D → famille/équipe → avis hors footer → localisation → réservation directe ou Airbnb/Booking. Les 8 pages existent dans les deux langues; textes d'origine conservés dans les pages détaillées. Base 4px, contenu 1280px, paragraphes 640px, photos AVIF/WebP.

**Motion (including an intentional absence of motion)**
Accueil: Stacked Sections withDramaEffect=false, deux panes, stackOffset=48px, sans runway. Désactivé sous 900px, sur écran peu haut et en reduced-motion; focus dans un chapitre désactive la superposition. Support éditorial: IntersectionObserver, entrée unique 600ms avec translation 20px, et profondeur photo au survol 600ms scale 1.03. Hyperion 200ms + 200ms label et remplissage 300ms cubic-bezier(0.7,0,0.2,1); Fenrir 400ms cubic-bezier(0.7,0,0.3,1). Galerie: FLIP 320ms cubic-bezier(0.2,0,0,1). Reduced motion instantané. Dialog: Tab contenu, Escape fermeture, retour explicite au déclencheur. Galerie: flèches gauche/droite; filtres aria-pressed; avis sans autoplay.

**Items actually intended for the build**
- primitives/button-hover-styles — Hyperion avec nested spans, animation verticale en deux phases et remplissage scaleX conservés. Fenrir garde cercle 120px, anneau 80px, expansion 1.2 et tracé SVG. Adaptations: type, anneau, focus-visible, reduced-motion, casse phrase.
- scroll/stacked-sections — conversion vanilla de withDramaEffect=false; sticky siblings et padding index*48 conservés. Adaptations: header, mobile/RM/focus, deux chapitres.
- transitions/flexbox-filter-flip — référence seulement; reflow natif sans copie du CodePen ni GSAP.
Details natifs pour les descriptions; dialog pour les photos et la vraie visite 3D; demande préparée localement; liens vers les annonces existantes.

## What it actually looks like

- C:\.Leonardo\TELAVENTIS BUISNESSES websites\domaine aux lions\qa\screenshots\hero-desktop.jpg
- C:\.Leonardo\TELAVENTIS BUISNESSES websites\domaine aux lions\qa\screenshots\home-desktop.jpg
- C:\.Leonardo\TELAVENTIS BUISNESSES websites\domaine aux lions\qa\screenshots\home-mobile.jpg
- C:\.Leonardo\TELAVENTIS BUISNESSES websites\domaine aux lions\qa\screenshots\house-desktop.jpg
- C:\.Leonardo\TELAVENTIS BUISNESSES websites\domaine aux lions\qa\screenshots\stay-mobile.jpg
- C:\.Leonardo\TELAVENTIS BUISNESSES websites\domaine aux lions\qa\screenshots\tour-desktop.jpg
- C:\.Leonardo\TELAVENTIS BUISNESSES websites\domaine aux lions\qa\screenshots\v2-hero-desktop.png
- C:\.Leonardo\TELAVENTIS BUISNESSES websites\domaine aux lions\qa\screenshots\v2-hero-mobile.png
- C:\.Leonardo\TELAVENTIS BUISNESSES websites\domaine aux lions\qa\screenshots\v2-home-desktop.png
- C:\.Leonardo\TELAVENTIS BUISNESSES websites\domaine aux lions\qa\screenshots\v2-home-mobile.png
- C:\.Leonardo\TELAVENTIS BUISNESSES websites\domaine aux lions\qa\screenshots\v2-tour-mobile.png

## Machine scan (scripts/tells.mjs — regex heuristics, not a verdict)

| Tell | Count | Limit |
|---|---|---|
| eyebrow | 2 | 1/page |
| accent-word | 0 | 1/page |
| numbered-index | 0 | 1/page |
| arrow-links | 0 | 2/page |
| stats-band | 0 | 1/page, 1/site |
| three-equal-columns | 0 | 1/page, 1/site |
| pill-shapes | 0 | 2/page |
| reveal-every-heading | 0 | 3/page |
| paper-background | 0 | needs a reason in the plan |
| overused-font | 0 | needs a reason in the plan |

Nothing over its limit — which does not mean nothing is generic. The scan cannot see layout, photography, or copy.

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
