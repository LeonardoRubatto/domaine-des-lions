"""One-time explicit edits for the requested motion pass."""
from pathlib import Path
import shutil
root=Path(__file__).resolve().parents[1]
p=root/'scripts/build-site.py'
s=p.read_text(encoding='utf-8')
s=s.replace('data-tour-scene="{scene}" aria-pressed="false"','data-tour-scene="{scene}" aria-label="{esc(label)}" aria-pressed="false"')
s=s.replace('<div class="album-thumbs">{thumbs}</div>', '<div class="album-rotation"><button type="button" class="rotation-control" data-album-rotation>{tr("Mettre en pause","Pause slideshow")}</button></div><div class="album-thumbs">{thumbs}</div>')
p.write_text(s,encoding='utf-8')
p=root/'design-plan-v3.md';s=p.read_text(encoding='utf-8')
s=s.replace('sans coins arrondis ni filtres','sans coins arrondis; flou progressif discret au bas des grandes images uniquement')
s=s.replace('Galerie : Shapes Slideshow,', 'Passages entre sections : ouvertures de cadres de 800ms (inset8% vers0), léger décalage vertical24px pour quatre blocs éditoriaux, une fois à l’entrée. Trois titres seulement : Text Effect, slide par mot, 400ms avec stagger50ms plafonné à300ms, texte accessible entier. Progressive Blur : six couches masquées, intensité1.6px, sur les20% inférieurs du hero et des grandes diapositives. Galerie : autoplay8000ms avec pause explicite, arrêt au focus/survol/hors écran/onglet caché; Shapes Slideshow,')
s=s.replace('Aucun effet ne masque des informations.', 'Les contenus restent visibles sans JS et après les entrées; les informations pratiques ne sont pas animées. Espacement base4px, exceptions0/1/2 pour traits et détails optiques.')
s += '\n- backgrounds/progressive-blur — six couches et gradients du code source, intensité limitée au bas des grands cadres, overlay non interactif.\n- text-effects/text-effect — preset slide, découpage par mot et texte sr-only intact, adaptation WAAPI avec IntersectionObserver et reduced motion.\n'
p.write_text(s,encoding='utf-8')
p=root/'CREDITS.md';s=p.read_text(encoding='utf-8')
s += '\n"Progressive Blur" by ibelick (motion-primitives), MIT.\nhttps://github.com/ibelick/motion-primitives/blob/main/components/core/progressive-blur.tsx\n\n"Text Effect" by ibelick (motion-primitives), MIT.\nhttps://github.com/ibelick/motion-primitives/blob/main/components/core/text-effect.tsx\n\nBoth are adapted to native DOM/CSS/Web Animations. The progressive blur uses six masked layers on the lower edge of large images. Three headings use the word-level slide preset, with the complete accessible text retained. The image album automatically advances every eight seconds, with pause, focus, hover, viewport and reduced-motion guards.\n'
p.write_text(s,encoding='utf-8')
shutil.copy2(Path('C:/.Leonardo/Project/design system (website elements template)/items/text-effects/text-effect/LICENSE'),root/'licenses/motion-primitives.txt')
