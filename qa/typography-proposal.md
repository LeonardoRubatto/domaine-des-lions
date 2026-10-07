# Local typography proposal — 8 October 2026

Alegreya replaces Source Serif 4. Alegreya Sans replaces Public Sans. Fonts are hosted locally from the official Google Fonts repository with original SIL OFL notices. The existing standalone inline-font delivery contract remains.

Actual weights: Alegreya 400 for h3, quotes and the header name; 440 for h1/h2. The user requested a roughly10% stronger impression on selected headings. A 400→440 axis adjustment is a restrained visual proposal, not a measurement of10% physical stroke thickness. Alegreya Sans uses400 for copy and500 for labels/actions. Main body18px, navigation/actions16px desktop, header action14px mobile.

Real browser checks: all16 French/English pages at390px show the new computed families and heading weight440, with no horizontal overflow. Home also checked at320,1024 and1440px without overflow. Desktop and mobile full-page screenshots were captured after scrolling through the page to expose lazy images and existing entrances. No interaction logic changed.

Fresh-context review of all four final screenshots: ready, no visible clipping, awkward wrapping, crowded buttons or typography readability regression. Secondary14px captions remain delicate, while body and booking actions remain readable. Static screenshots do not establish animation/font-loading timing. Existing motion behavior was not changed.

Evidence: screenshots-type/, typography-mobile-checks.json and critique-brief-type.md. The user validated this typography and authorized the GitHub push on8 October2026.
