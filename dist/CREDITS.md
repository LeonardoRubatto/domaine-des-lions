# Credits

Logo, photographs, estate descriptions and guest testimonials: Le Domaine aux Lions, preserved from https://ledomaineauxlions.fr/ for this client presentation. Ownership remains with the original rights holders. Publication and commercial rights must be confirmed with the estate owner.

"CSS Button Hover Styles" by Codrops (ButtonHoverStyles), MIT.
https://github.com/codrops/ButtonHoverStyles/blob/main/css/base.css

"Stacked Sections" by codse (animata), MIT.
https://github.com/codse/animata/blob/main/animata/scroll/stacked-sections.tsx

Adaptation: local palette and typography, CSS motion tokens, keyboard parity, reduced motion, local responsive images. Original MIT notices included in `licenses/`.

"Shapes Slideshow (circular clip-path)" by Codrops (ShapesSlideshow), MIT.
https://github.com/codrops/ShapesSlideshow/blob/main/src/js/demo1/index.js

"Scroll Tilted Grid" by Harsh Jadhav (Componentry), MIT.
https://componentry.dev/r/scroll-tilted-grid.json

Shapes Slideshow is adapted to native Web Animations: circular masks and opposing frame/image translations remain; the transition is shortened to 800ms and images occupy their full frame at rest. Scroll Tilted Grid retains the stored geometry calculations with moderate values, no blur, no colour shift, no Lenis and a static mobile/reduced-motion state.

Virtual tour: existing Panotour/krpano presentation supplied for Le Domaine aux Lions by Fabien Lestrade. It remains hosted by its existing provider; this mockup opens it on request and offers a direct link. No tour model or provider code is republished.

Gallery filters use native reflow. Native HTML dialogs follow the system's APG guidance. Reviews rotate with a reading-time interval, explicit pause and focus/visibility guards; reduced motion disables automatic rotation.

Source Serif 4, Adobe, and Public Sans, US Web Design System: self-hosted variable fonts, SIL Open Font License 1.1. Original notices are included in `licenses/source-serif-4-OFL.txt` and `licenses/public-sans-OFL.txt`.

Design and static implementation: Telaventis. Local prospect presentation, not a commissioned or published client site.

"Progressive Blur" by ibelick (motion-primitives), MIT.
https://github.com/ibelick/motion-primitives/blob/main/components/core/progressive-blur.tsx

"Text Effect" by ibelick (motion-primitives), MIT.
https://github.com/ibelick/motion-primitives/blob/main/components/core/text-effect.tsx

Both are adapted to native DOM/CSS/Web Animations. The progressive blur uses six masked layers on the lower edge of large images (16% band, 6px maximum). Three headings use the word-level slide preset; four house/pool/tennis/review chapter headings use fade-in-blur with4px blur and12px travel. The complete accessible text is retained. The image album automatically advances every eight seconds, with pause, focus, hover, viewport and reduced-motion guards. Section boundaries share a shallow16px slide and92%-to100% fade, once, only for sections initially outside the viewport; focus and reduced motion restore a stable state instantly.

"Morphing Dialog" by ibelick (motion-primitives), MIT.
https://github.com/ibelick/motion-primitives/blob/main/components/core/morphing-dialog.tsx

Native adaptation preserves the shared thumbnail/image geometry and trigger state, with an explicit keyboard focus cycle and return. Meaningful photo labels and instant reduced-motion states address the documented source gaps. Full-resolution images decode before the viewer opens or changes photo. The motion-primitives MIT notice already included covers this component.

Airbnb and Booking.com symbols: Simple Icons, https://github.com/simple-icons/simple-icons (CC0 SVG artwork). Original trademarks belong to their respective owners and identify links to the estate's existing listings. Locally stored SVG sources are listed in research/booking-marks.json; their shapes remain unchanged, using Airbnb pink #FF5A5F and Booking.com blue #003580.
