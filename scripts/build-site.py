"""Build a bilingual, portable static website from preserved client content."""
import html
import json
from pathlib import Path
import re
import runpy
Parser = runpy.run_path(str(Path(__file__).with_name('extract-content.py')))['Parser']
ROOT = Path(__file__).resolve().parents[1]
PHOTOS = json.loads((ROOT / 'assets/photo-manifest.json').read_text(encoding='utf-8'))
SOURCES = {p['id']:p for p in json.loads((ROOT / 'research/content-inventory.json').read_text(encoding='utf-8'))}
TOUR = 'https://fabienlestrade-support.com/visites-virtuelles/domaine-aux-lions/domaine-des-lions.html'
AIRBNB = 'https://www.airbnb.fr/rooms/47524920'
BOOKING = 'https://www.booking.com/hotel/fr/domaine-aux-lions-piscine-tennis-20-min-deauville.html'
BASE = 'https://example.com/'
PAGES = ['home','house','family','business','gallery','stay','access','legal']
PATHS = {'fr':['index.html','domaine.html','en-famille.html','seminaires.html','galerie.html','sejour.html','acces.html','mentions-legales.html'],
         'en':['en/index.html','en/the-house.html','en/family-stays.html','en/team-retreats.html','en/gallery.html','en/your-stay.html','en/getting-here.html','en/legal.html']}
LANG = 'fr'
PREFIX = ''

def tr(fr,en): return fr if LANG == 'fr' else en
def esc(value): return html.escape(str(value),quote=True)
def path(page,lang=None):
    target = PATHS[lang or LANG][PAGES.index(page)]
    return PREFIX + target
def asset(file): return PREFIX + 'assets/' + file
def button(label,href=None,attrs='',secondary=False):
    css='button button--hyperion' if CURRENT=='home' and 'Réserver' in label or 'Plan your stay'==label else 'button button--dione'
    inner=f'<span><span>{label}</span></span>' if 'hyperion' in css else f'<span>{label}</span>'
    if href: return f'<a class="{css}" href="{esc(href)}" {attrs}>{inner}</a>'
    return f'<button class="{css}" type="button" {attrs}>{inner}</button>'

CAPTIONS = {
 'home_slide_2':('Les salons ouverts sur la piscine','Living rooms opening onto the pool'),
 'home_slide_3':('Une chambre sous les combles','A bedroom under the eaves'),
 'homepage-slide5':('Le bassin et son abri','The pool and its enclosure'),
 'homepage-slide6':('Le court de tennis privé','The private tennis court'),
 'home_title_1':('La façade, côté jardin','The façade from the garden'),
 'footer-presentation':('Le domaine vu entre les graminées','The estate through the garden grasses'),
 'maison3':('La maison à colombages, au cœur du jardin','The timber-framed house in its garden'),
 'maison-3_4-':('La façade du Domaine aux Lions','The façade of Le Domaine aux Lions'),
 'maison':('Le jardin et la maison normande','The garden and the Normandy house'),
 'maison4NB':('La maison vue entre les branches','The house seen through the branches'),
 'maison5':('La maison et la piscine depuis le jardin','The house and pool from the garden'),
 'bocage':('La campagne du Pays d’Auge','The Pays d’Auge countryside'),
 'VA-maisonpiscine':('Vue aérienne de la maison et de la piscine','An aerial view of the house and pool'),
 'VAtennis':('Le court de tennis depuis le ciel','An aerial view of the tennis court'),
 'Photo-2.1':('Vue aérienne du domaine et du court de tennis','An aerial view of the estate and tennis court'),
 'Photo-2.2':('Le domaine entouré de verdure','The estate surrounded by greenery'),
 'salons':('Les salons sous les poutres de la maison','The living spaces beneath the timber beams'),
 'salon-piscine':('Le salon ouvert sur la terrasse et la piscine','The living room facing the terrace and pool'),
 'salons-billard':('Le billard au cœur du grand salon','The billiards table in the large living room'),
 'salle-a-manger':('La salle à manger autour de la cheminée','The dining room around the fireplace'),
 'salon-racine':('Les espaces de détente du rez-de-jardin','The garden-floor lounge areas'),
 'piano':('Le piano et le baby-foot','The piano and table football'),
 'lion-piscine':('Un lion du domaine devant la piscine couverte','An estate lion beside the covered pool'),
 'piscine':('La piscine couverte et sa terrasse','The covered pool and terrace'),
 'piscine2':('L’intérieur de la piscine couverte','Inside the covered pool'),
 'tennis2':('Le court de tennis, entre les arbres','The tennis court between the trees'),
 'Photo-2.7':('Le court de tennis et la campagne','The tennis court and countryside'),
 'Photo-2.6':('L’entrée du court de tennis','The entrance to the tennis court'),
 'Garden-1':('Les arbres du jardin','The garden trees'),
 'Garden-2':('Le trampoline et les jeux du jardin','The trampoline and garden games'),
 'Garden-3':('Un lion sculpté devant la maison','A sculpted lion in front of the house'),
 'attraction':('Les jeux dans le jardin du domaine','Games in the estate garden'),
 'attraction2':('Le toboggan géant et le jardin','The giant slide and the garden'),
 'attraction3':('Le trampoline et le tourniquet','The trampoline and roundabout'),
 'SDBjacuzzi':('Le jacuzzi intérieur','The indoor hot tub'),
 'SDB1':('Une salle d’eau du domaine','A shower room in the house'),
 'SDB2':('Une salle de bain sous les combles','A bathroom beneath the eaves'),
 'couloir-C':('Le couloir de l’étage','The upstairs hallway'),
 'bateau':('Un détail de décoration de la maison','A decorative detail in the house'),
 'Game-room':('Billard et baby-foot dans la maison','Billiards and table football in the house'),
 'Ninja':('Le parcours Ninja Warrior dans le jardin','The garden Ninja Warrior course'),
 'Slackline':('La slackline du jardin','The garden slackline'),
 'Ping-pong':('La table de ping-pong sur la terrasse','The terrace table tennis table'),
 'High-chairs':('Les deux chaises hautes à disposition','The two available high chairs'),
 'Transats':('Les transats pour les tout-petits','The baby bouncy chairs'),
 'Table-bebe':('La table à langer','The changing table'),
 '1':('Plan d’approche depuis Paris et Lisieux','Approach map from Paris and Lisieux'),
 '2':('La signalisation du chemin de la Boullaye','Signs for Chemin de la Boullaye'),
 '3':('Le parking et le chemin vers l’entrée piétonne','Parking and the path to the pedestrian entrance'),
 '4':('Le repère à l’entrée du parking','The landmark by the parking entrance'),
 '5':('Le panneau du parking privé','The private parking sign'),
}
def caption(key):
    if key.startswith('chambre') or key.startswith('IMG_'):
        return tr('Une chambre du Domaine aux Lions','A bedroom at Le Domaine aux Lions')
    return tr(*CAPTIONS.get(key,('Un espace du Domaine aux Lions','A space at Le Domaine aux Lions')))
def picture(key,alt=None,css='',eager=False,sizes='(min-width: 900px) 50vw, 100vw'):
    p = PHOTOS[key]
    sets = lambda fmt: ', '.join(f'{asset("photos/"+p["key"]+"-"+str(w)+"."+fmt)} {w}w' for w in p['widths'])
    src = asset(f'photos/{p["key"]}-{p["widths"][-1]}.webp')
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    return f'<picture class="{css}"><source type="image/avif" srcset="{sets("avif")}" sizes="{sizes}"><source type="image/webp" srcset="{sets("webp")}" sizes="{sizes}"><img src="{src}" width="{p["width"]}" height="{p["height"]}" alt="{esc(alt or caption(key))}" {load} decoding="async"></picture>'
def image_data(key):
    p = PHOTOS[key]
    return {'src':asset(f'photos/{p["key"]}-{p["widths"][-1]}.webp'),'alt':caption(key)}

LABELS = {
 'home':('Le Domaine aux Lions','Le Domaine aux Lions'), 'house':('Le domaine','The house'),
 'family':('En famille','Family stays'), 'business':('Séminaires','Team retreats'),
 'gallery':('En images','Gallery'), 'stay':('Préparer votre séjour','Plan your stay'),
 'access':('Nous trouver','Getting here'), 'legal':('Mentions légales','Legal & privacy'),
}
def label(page): return tr(*LABELS[page])
def nav_links():
    return ''.join(f'<a href="{path(p)}" {"aria-current=page" if p == CURRENT else ""}>{label(p)}</a>' for p in ('house','family','business','gallery','access'))
def header():
    other = 'en' if LANG == 'fr' else 'fr'
    return f'''<a class="skip" href="#main">{tr('Aller au contenu','Skip to content')}</a>
<header class="header"><a class="brand" href="{path('home')}" aria-label="{tr('Le Domaine aux Lions, accueil','Le Domaine aux Lions, home')}"><img src="{asset('logo.png')}" width="150" height="150" alt=""><span>Le Domaine<br>aux Lions</span></a>
<nav class="desktop-nav" aria-label="{tr('Navigation principale','Main navigation')}">{nav_links()}</nav>
<div class="header-actions"><a class="language" href="{path(CURRENT,other)}" lang="{other}" aria-label="{tr('Read this page in English','Lire cette page en français')}">{other.upper()}</a><a class="button button--hyperion" href="{path('stay')}"><span><span>{tr('Réserver un séjour','Plan your stay')}</span></span></a><button class="menu-toggle" type="button" data-open="menu" aria-label="{tr('Ouvrir le menu','Open menu')}" aria-haspopup="dialog" aria-controls="menu"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 7h18M3 17h18"/></svg></button></div></header>
<dialog id="menu" class="menu-dialog" aria-label="{tr('Navigation du site','Site navigation')}"><div class="dialog-heading"><span>Le Domaine aux Lions</span><button data-close class="icon-button" aria-label="{tr('Fermer le menu','Close menu')}">×</button></div><nav aria-label="{tr('Navigation mobile','Mobile navigation')}">{nav_links()}<a href="{path('stay')}">{label('stay')}</a><a href="{path(CURRENT,other)}" lang="{other}">{tr('English','Français')}</a></nav></dialog>'''
def footer():
    return f'''<footer class="footer"><div class="footer-main wrap"><a href="{path('home')}" class="footer-brand"><img src="{asset('logo-historical.png')}" width="160" height="160" alt="Le Domaine aux Lions, logo historique"></a><div><h2>{tr('Au plaisir de vous accueillir.','We look forward to welcoming you.')}</h2><p>700 chemin de la Boullaye<br>14100 Fauguernon · Normandie</p></div><div class="footer-links"><a href="mailto:ledomaineauxlions@gmail.com">ledomaineauxlions@gmail.com</a><a href="tel:+33630868569">+33 (0)6 30 86 85 69</a><div class="socials"><a href="https://instagram.com/le_domaine_aux_lions" target="_blank" rel="noopener">Instagram</a><a href="https://www.facebook.com/Le-Domaine-aux-Lions-108084324781768/" target="_blank" rel="noopener">Facebook</a></div></div></div>
<div class="footer-bottom wrap"><span>© 2026 Le Domaine aux Lions</span><a href="{path('legal')}">{label('legal')}</a><span>{tr('Maquette de présentation','Presentation mockup')}</span><a href="https://telaventis.fr" target="_blank" rel="noopener">{tr('Site par','Site by')} Telaventis</a></div></footer>
<dialog id="lightbox" class="lightbox" aria-labelledby="lightbox-caption" aria-describedby="lightbox-help"><div class="viewer-surface"></div><div class="viewer-heading viewer-chrome"><span>{tr('L’album du domaine','The estate’s album')}</span><button type="button" data-close class="viewer-close" aria-label="{tr('Fermer la photo','Close photo')}"><span>{tr('Fermer','Close')}</span><svg viewBox="0 0 24 24" aria-hidden="true"><path d="m5 5 14 14M19 5 5 19"/></svg></button></div><div class="viewer-stage"><div class="viewer-frame"><img id="lightbox-image" alt=""></div></div><div class="viewer-navigation viewer-chrome"><button class="viewer-arrow" type="button" data-photo-step="-1" aria-label="{tr('Photo précédente','Previous photograph')}"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="m14 5-7 7 7 7"/></svg></button><button class="viewer-arrow" type="button" data-photo-step="1" aria-label="{tr('Photo suivante','Next photograph')}"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="m10 5 7 7-7 7"/></svg></button></div><div class="viewer-caption viewer-chrome"><p id="lightbox-caption"></p><p id="lightbox-count" aria-live="polite"></p></div><p id="lightbox-help" class="sr-only">{tr('Flèches gauche et droite pour parcourir les photos. Échap pour revenir à la galerie.','Use left and right arrow keys to browse photographs. Escape returns to the gallery.')}</p></dialog>
<script src="{PREFIX}site.js" defer></script><script src="{PREFIX}v3.js" defer></script>'''

def tour_section():
    if CURRENT!='home':
        return f'<section class="tour-route wrap"><p>{tr("Prenez vos repères dans la maison et le jardin.","Get your bearings in the house and garden.")}</p>{button(tr("Explorer les espaces en 360°","Explore the spaces in 360°"),path("home")+"#visite")}</section>'
    scenes=[('pano6815',tr('Le salon','Living room'),'salons'),('pano6817',tr('La piscine','The pool'),'lion-piscine'),('pano6819',tr('Le jardin','The garden'),'Photo-2.7'),('pano6794',tr('La salle à manger','Dining room'),'salle-a-manger'),('pano6806',tr('Chambre Monet','Monet bedroom'),'chambre3')]
    choices=''.join(f'<button class="tour-scene" type="button" data-tour-scene="{scene}" aria-label="{esc(label)}" aria-pressed="false">{picture(photo,sizes="160px")}<span>{label}</span></button>' for scene,label,photo in scenes)
    return f'''<section class="tour-hub" id="visite"><div class="wrap"><div class="tour-hub-heading"><h2>{tr('Entrez dans le domaine.','Step inside the estate.')}</h2><p>{tr('Choisissez un espace, puis regardez autour de vous. La visite à 360° vous fait passer de la maison au jardin.','Choose a space, then look around. The 360° tour takes you from the house into the garden.')}</p></div><div class="tour-stage" data-tour-url="{TOUR}"><div class="tour-cover">{picture('Photo-2.2',sizes='(min-width: 1440px) 1280px, 100vw')}<button class="button button--fenrir" type="button" data-tour-start aria-label="{tr('Commencer la visite à 360°','Start the 360° tour')}"><svg class="progress" viewBox="0 0 100 100" aria-hidden="true"><circle class="progress__circle" cx="50" cy="50" r="49"/><circle class="progress__path" cx="50" cy="50" r="49" pathLength="1"/></svg><span>{tr('Entrer','Enter')}</span></button></div><div class="tour-inline-frame"></div></div><div class="tour-toolbar"><p class="tour-status" role="status">{tr('Maison & jardin · 360°','House & garden · 360°')}</p><div><button type="button" class="quiet-link" data-tour-expand hidden>{tr('Plein écran','Full screen')}</button><button type="button" class="quiet-link" data-tour-stop hidden>{tr('Fermer la visite','Close the tour')}</button><a class="quiet-link" href="{TOUR}" target="_blank" rel="noopener">{tr('Ouvrir à part','Open separately')}</a></div></div><div class="tour-scenes" aria-label="{tr('Choisir un espace à visiter','Choose a space to explore')}">{choices}</div></div></section>'''

def final_cta():
    return f'''<section class="final-cta wrap"><div><h2>{tr('Réserver le domaine.','Book the estate.')}</h2><p>{tr('Choisissez vos dates. Nous vous aidons à préparer la suite.','Choose your dates. We’ll help you plan the rest.')}</p></div><div class="final-actions">{button(tr('Préparer mon séjour','Plan my stay'),path('stay'))}{platform_links()}</div></section>'''

def platform_links():
    return f'<div class="platform-shortcuts">{platform_brand("airbnb", "Airbnb", AIRBNB)}{platform_brand("bookingdotcom", "Booking.com", BOOKING)}</div>'

def platform_brand(slug, name, url):
    return f'<a class="booking-brand" href="{url}" target="_blank" rel="noopener" aria-label="{esc(tr("Consulter l’annonce sur ","View the listing on ")+name)}"><img src="{asset("brands/"+slug+".svg")}" width="28" height="28" alt=""><span>{name}</span></a>'
def details_blocks(source_type):
    blocks = SOURCES[f'{LANG}-{source_type}']['blocks']
    intro,groups = [],[]
    current = None
    for b in blocks:
        if b['tag'] == 'h1': continue
        if b['tag'].startswith('h'):
            current = {'title':b['text'],'blocks':[]}
            groups.append(current)
        elif current is None:
            intro.append(b)
        else: current['blocks'].append(b)
    def render(blocks):
        result = ''; list_open = False
        for b in blocks:
            if b['tag'] == 'li':
                if not list_open: result += '<ul>'; list_open=True
                result += f'<li>{esc(b["text"])}</li>'
            else:
                if list_open: result += '</ul>'; list_open=False
                text = esc(b['text']).replace('https://www.authenticnormandy.fr/', '<a href="https://www.authenticnormandy.fr/" target="_blank" rel="noopener">authenticnormandy.fr</a>')
                result += f'<p>{text}</p>'
        if list_open: result += '</ul>'
        return result
    # Owner descriptions remain visible without any disclosure interaction.
    chapters=[]
    for i,g in enumerate(groups):
        if not g['blocks']: continue
        title=g['title'].lower()
        photo=None
        matches=[(['rez-de-jardin','garden floor'],'salons'),(['tennis'],'Photo-2.7'),(['jardin','garden','outside','grands','bigger'],'Garden-1'),(['chambre','bedroom','étage','floor'],'chambre3'),(['terrasse','terrace'],'Photo-2.1'),(['petits','little'],'High-chairs'),(['intérieur','inside'],'Game-room'),(['séminaire','seminar'],'salle-a-manger')]
        for words,key in matches:
            if any(w in title for w in words): photo=key; break
        image=picture(photo,sizes='(min-width:900px) 42vw, 100vw') if photo else ''
        chapters.append(f'<section class="information-chapter {"with-photo" if photo else ""}" id="chapter-{i}"><div><h3>{esc(g["title"])}</h3><div class="source-copy">{render(g["blocks"])}</div></div>{image}</section>')
    expanded=''.join(chapters)
    return render(intro), expanded

def reviews():
    parser = Parser(); parser.feed((ROOT/'research/source-pages/fr-home.html').read_text(encoding='utf-8-sig'))
    review_node = next(n for n in parser.root.walk() if n.attrs.get('id') == 'carouselFooterReviews')
    cards = []
    translations = {
      'Laure': 'I can only recommend David and Svitlana’s house; communication with them was very easy! The house is perfectly equipped for adults and children alike. The garden is a real paradise, and a weekend is too short to try every activity: pool, tennis, pétanque, zip line, trampoline, roundabout… The dining spaces are ideal for large groups, and there is plenty of crockery. We had a dream weekend!',
      'Sebastien': 'A very pleasant, spacious house with a magnificent garden. Our stay was perfect in every way!',
      'Faustine': 'A beautiful, comfortable house in a wonderful setting. Everything has been thought of to make your stay as enjoyable as possible!',
      'Manon': 'We had an excellent stay at this absolutely magnificent estate, both inside and outside — the pool is incredible. Communication was very easy and the welcome very warm!',
      'Sophie': 'A beautiful house with a wonderfully equipped garden, with plenty to delight adults and children. The house is lovely too; everyone can find a space and an atmosphere that suits them. Games are available for every age, with things to do whatever the weather…',
      'Quentin': 'A very restorative stay in a magnificent house, with everything to please adults and children: a pool, sports and children’s games! The house is clean and nothing is missing.',
      'Priscilla': 'An amazing stay in this magnificent house. Contact with the owners was very easy. There were 15 of us, and we made the most of everything available: billiards, tennis, the hot tub, table tennis and more… Wonderful! An incredible stay. I highly recommend it. We will definitely return!',
    }
    for n in review_node.walk():
        if 'carousel-item' not in n.attrs.get('class','').split(): continue
        heading = next((x for x in n.walk() if x.tag == 'h5'),None)
        paragraphs = [x.text().strip() for x in n.walk() if x.tag == 'p']
        if heading and paragraphs:
            name = heading.text().strip().rstrip(':').strip()
            quote = translations.get(name, ' '.join(paragraphs)) if LANG == 'en' else ' '.join(paragraphs)
            cards.append((name, f'<figure class="review"><blockquote>{esc(quote)}</blockquote><figcaption>{esc(name)}<span>{tr("Témoignage publié sur le site du domaine","Guest review published on the estate’s website")}</span></figcaption></figure>'))
    order = ['Faustine','Coen','Manon','Sebastien','Laure','Sophie','Quentin','Priscilla']
    cards.sort(key=lambda item: order.index(item[0]) if item[0] in order else len(order))
    return f'''<section class="reviews-section"><div class="wrap"><div class="review-heading"><h2>{tr('Les mots de nos invités.','In our guests’ words.')}</h2><p class="review-note">{tr('Leurs témoignages sur le site du domaine.','Guest testimonials. French reviews translated into English.')}</p></div><div class="review-stage"><figure class="review-photo">{picture('maison',sizes='(min-width:900px) 38vw, 100vw')}</figure><div class="review-reading"><div class="review-track" tabindex="0" role="region" aria-roledescription="{tr('carrousel','carousel')}" aria-label="{tr('Témoignages des invités','Guest reviews')}">{''.join(markup for _,markup in cards)}</div><div class="review-bottom"><p class="review-position fineprint" aria-live="off"></p><div class="review-controls"><button class="button button--skoll" data-review-step="-1" aria-label="{tr('Avis précédent','Previous review')}"><span><span>‹</span></span></button><button class="rotation-control" data-review-rotation type="button">{tr('Mettre en pause','Pause slideshow')}</button><button class="button button--skoll" data-review-step="1" aria-label="{tr('Avis suivant','Next review')}"><span><span>›</span></span></button></div></div></div></div></div></section>'''


def home():
    return f'''<section class="hero hero-estate wrap"><figure class="hero-image">{picture('maison-3_4-',css='hero-photo',eager=True,sizes='(min-width: 1440px) 1080px, (min-width: 769px) 85vw, 100vw')}</figure><figure class="hero-detail">{picture('piano',sizes='(min-width: 769px) 200px, 120px')}</figure><div class="hero-title"><h1>Le Domaine<br>aux Lions</h1></div><div class="hero-description"><p>{tr('Une maison à colombages, huit chambres et un grand jardin. Tout le domaine est à vous.','A timber-framed house, eight bedrooms and a large garden. The whole estate is yours.')}</p><div class="hero-booking"><span>{tr("Réserver sur","Book on")}</span>{platform_links()}</div></div><div class="hero-setting"><p>{tr('Maison entière · jusqu’à 15 invités','Whole house · up to 15 guests')}</p><p class="hero-location"><span class="hero-location-desktop">{tr('Fauguernon, Normandie<br>À environ 2 heures de Paris','Fauguernon, Normandy<br>Around 2 hours from Paris')}</span><span class="hero-location-mobile">{tr('Normandie · À environ 2 h de Paris','Normandy · Around 2 hours from Paris')}</span></p></div></section>
<section class="home-intro wrap" id="maison"><div class="intro-title"><h2>{tr('Une maison pour 15 invités.','A house for 15 guests.')}</h2><p>{tr('Nous avons pensé notre maison pour vous ! Confortable et luxueuse comme un hôtel, équipée comme un club de vacances. La tranquillité et l’exclusivité en prime.','We have designed our home with your comfort in mind: the comfort and luxury of a hotel, the facilities of a holiday resort, with added privacy and tranquillity.')}</p><a class="text-link" href="{path('house')}">{tr('Découvrir les espaces et équipements','Explore the spaces and facilities')}</a></div><figure class="intro-salon" data-tilt-frame>{picture('salons',sizes='(min-width: 900px) 58vw, 100vw')}<figcaption>{tr('150 m² de pièces à vivre, sous les poutres.','150 m² of living spaces beneath the timber beams.')}</figcaption></figure><figure class="intro-bedroom" data-tilt-frame>{picture('chambre3',sizes='(min-width: 900px) 32vw, 100vw')}<figcaption>{tr('Huit chambres et leurs annexes.','Eight bedrooms and their annexes.')}</figcaption></figure><div class="intro-comfort"><h3>{tr('Un accueil en personne.','A personal welcome.')}</h3><p>{tr('Les lits sont faits. Le linge est fourni. Nous vous accueillons en personne pour vous faire découvrir les lieux.','The beds are made. Linen is provided. We welcome you in person and show you around.')}</p><p class="art-note">{tr('Et au fil des pièces, des tableaux de peintres normands et des créations contemporaines.','And throughout the house, paintings by Normandy artists and contemporary works.')}</p><a class="text-link" href="{path('gallery')}?filter=bedrooms">{tr('Voir les chambres','See the bedrooms')}</a></div></section>
<section class="leisure-deck wrap" aria-label="{tr('La piscine et le jardin','The pool and garden')}" data-stacked-deck><div class="leisure-pane" data-stacked-card style="--index:1"><div class="leisure-chapter pool-chapter" data-stacked-content><div class="chapter-copy"><h2>{tr('La piscine couverte.','The covered pool.')}</h2><p>{tr('Couverte, sécurisée et chauffée à 28 °C toute l’année. Du premier bain du matin aux longueurs de l’après-midi.','Covered, secured and heated to 28°C all year. From a morning dip to an afternoon swim.')}</p><p class="fineprint">{tr('Accessible de 8 h à 20 h. La température peut varier en cas de grand froid.','Open from 8am to 8pm. Temperature may vary in exceptionally cold weather.')}</p><a class="text-link" href="{path('house')}#equipements">{tr('Les équipements du domaine','The estate’s facilities')}</a></div>{picture('lion-piscine',sizes='(min-width: 900px) 58vw, 100vw')}</div></div><div class="leisure-pane" data-stacked-card style="--index:2"><div class="leisure-chapter garden-chapter" data-stacked-content><div class="chapter-copy"><h2>{tr('Le tennis et le jardin.','Tennis and the garden.')}</h2><p>{tr('Un court de tennis privé et 6 000 m² de verdure. Pétanque, ping-pong, jeux et barbecue : chacun trouve sa façon de profiter du grand air.','A private tennis court and 6,000 m² of greenery. Pétanque, table tennis, games and a barbecue: everyone can enjoy the outdoors in their own way.')}</p><a class="text-link" href="{path('family')}">{tr('Profiter du domaine en famille','Enjoy the estate with family')}</a></div>{picture('Photo-2.7',sizes='(min-width: 900px) 58vw, 100vw')}</div></div></section>
{tour_section()}
<section class="stays wrap" id="sejours"><h2>{tr('En famille ou en équipe.','With family or your team.')}</h2><div class="stay-pair"><a data-tilt-frame class="stay-tile" href="{path('family')}">{picture('attraction2',sizes='(min-width: 900px) 60vw, 100vw')}<div><h3>{tr('En famille et entre amis.','With family and friends.')}</h3><p>{tr('Toboggan géant, trampoline et tourniquet dans le jardin.','A giant slide, trampoline and roundabout in the garden.')}</p><span>{tr('Découvrir les séjours en famille','Explore family stays')}</span></div></a><a data-tilt-frame class="stay-tile" href="{path('business')}">{picture('salle-a-manger',sizes='(min-width: 900px) 38vw, 100vw')}<div><h3>{tr('Séminaires au domaine.','Team retreats at the estate.')}</h3><p>{tr('Fibre, projecteur et espaces modulables pour votre équipe.','Fibre internet, a projector and flexible spaces for your team.')}</p><span>{tr('Organiser un séminaire','Plan a team retreat')}</span></div></a></div></section>
{reviews()}
<section class="location-section wrap">{picture('bocage',sizes='(min-width: 900px) 58vw, 100vw')}<div><h2>{tr('Fauguernon, dans le Pays d’Auge.','Fauguernon, in the Pays d’Auge.')}</h2><p>{tr('Fauguernon. Un hameau tranquille, bordé de champs. Deauville et Honfleur à moins de trente minutes, Paris à environ deux heures.','Fauguernon. A quiet hamlet surrounded by fields. Less than thirty minutes from Deauville and Honfleur, around two hours from Paris.')}</p><p class="location-address">700 chemin de la Boullaye<br>14100 Fauguernon, France</p><a class="text-link" href="{path('access')}">{tr('Préparer mon arrivée','Plan my arrival')}</a></div></section>{final_cta()}'''

def page_intro(title,description,photo):
    return f'<section class="page-intro wrap"><div><p class="breadcrumb"><a href="{path("home")}">{tr("Accueil","Home")}</a> / {label(CURRENT)}</p><h1>{title}</h1><p>{description}</p></div>{picture(photo,eager=True)}</section>'
def house():
    intro,details = details_blocks('presentation')
    return page_intro(tr('Une maison entière,<br>rien que pour vous.','A whole house,<br>all to yourselves.'),tr('Huit chambres, de grands espaces à partager et le calme du Pays d’Auge. Jusqu’à 15 invités.','Eight bedrooms, generous shared spaces and the peace of the Pays d’Auge. Up to 15 guests.'),'salons') + f'''<section class="house-story wrap"><div class="source-copy">{intro}</div><div class="house-facts"><p><strong>15</strong>{tr('invités maximum','guests maximum')}</p><p><strong>8</strong>{tr('chambres & annexes','bedrooms & annexes')}</p><p><strong>5</strong>{tr('salles de bains','bathrooms')}</p><p><strong>6 000 m²</strong>{tr('de jardin','of garden')}</p></div></section>
<section class="art-section wrap">{picture('piano')}<div><h2>{tr('Une maison où l’art<br>a sa place.','A house with<br>room for art.')}</h2><p>{tr('Les chambres portent les noms de peintres de la région. Reproductions des peintres normands et créations contemporaines accompagnent votre séjour, au fil des pièces.','The bedrooms bear the names of painters from the region. Reproductions of Normandy paintings and contemporary works accompany your stay throughout the house.')}</p><a class="text-link" href="{path('gallery')}?filter=bedrooms">{tr('Voir les chambres','See the bedrooms')}</a></div></section>
<section class="equipment-section wrap" id="equipements"><div class="section-heading"><h2>{tr('La maison, dans le détail.','The house, in detail.')}</h2><p>{tr('Tous les espaces, les équipements et les services du domaine.','All the spaces, facilities and services at the estate.')}</p></div><div class="equipment-layout"><div class="detail-list">{details}</div><div class="equipment-photos">{picture('SDBjacuzzi')}{picture('piscine')}{picture('Garden-1')}</div></div></section>{tour_section()}{final_cta()}'''
def stays(kind):
    source='families' if kind=='family' else 'business'
    intro,details=details_blocks(source)
    if kind=='family':
        title=tr('Le domaine<br>en famille.','Family stays<br>at the estate.')
        description=tr('Les jeunes Lions de tout âge sont bienvenus au domaine.','Children of all ages are welcome at the estate.')
        photo='attraction2'; side='Game-room'
    else:
        title=tr('Séminaires au domaine.','Team retreats at the estate.')
        description=tr('Séminaires, groupes de travail et retraites, jusqu’à 15 personnes.','Team retreats, workshops and work seminars for up to 15 people.')
        photo='salle-a-manger'; side='Photo-2.1'
    return page_intro(title,description,photo) + f'<section class="audience-detail wrap"><div class="source-copy">{intro}</div><div class="audience-layout"><div class="detail-list">{details}</div>{picture(side)}</div><div class="audience-action">{button(tr("Parlons de votre séjour","Tell us about your stay"),path("stay")+("?type=business" if kind=="business" else "?type=family"))}<a class="text-link" href="{path("house")}">{tr("Découvrir toute la maison","Explore the whole house")}</a></div></section>{tour_section()}'

def category(key):
    if key == 'home_slide_3': return 'bedrooms'
    if key in ('homepage-slide5','homepage-slide6'): return 'relax'
    if key == 'footer-presentation': return 'garden'
    if key.startswith('chambre') or key.startswith('IMG_') or key.startswith('SDB'): return 'bedrooms'
    if any(s in key.lower() for s in ['piscine','tennis','basket','ping-pong']): return 'relax'
    if key.startswith('Garden') or key.startswith('attraction') or key in ['Ninja','Slackline','Photo8_defile','bocage','Photo-2.1','Photo-2.2']: return 'garden'
    return 'house'
def gallery():
    keys=[k for k in PHOTOS if k not in ('1','2','3','4','5')]
    lead=['maison3','salons','lion-piscine','chambre3','maison','tennis2','salle-a-manger','attraction2']
    keys=lead+[k for k in keys if k not in lead]
    gallery_items=[]
    for i,k in enumerate(keys):
        data=esc(json.dumps(image_data(k),ensure_ascii=False))
        visible_caption = '' if caption(k) in ('Une chambre du Domaine aux Lions','Un espace du Domaine aux Lions','A bedroom at Le Domaine aux Lions','A space at Le Domaine aux Lions') else caption(k)
        gallery_items.append(f'<figure class="gallery-item {"gallery-panorama" if k=="home_title_1" else ""}" data-category="{category(k)}"><button type="button" data-photo="{data}" aria-haspopup="dialog" aria-label="{esc(tr("Agrandir : ","Enlarge: ")+caption(k))}">{picture(k,sizes="(min-width: 900px) 50vw, (min-width: 600px) 48vw, 100vw")}</button><figcaption>{visible_caption}</figcaption></figure>')
    filters=[('all',tr('Tout le domaine','The whole estate')),('house',tr('La maison','The house')),('bedrooms',tr('Les chambres','Bedrooms')),('relax',tr('La détente','Leisure')),('garden',tr('Le jardin','The garden'))]
    controls=''.join(f'<button type="button" data-filter="{key}" aria-pressed="{str(i==0).lower()}">{label}</button>' for i,(key,label) in enumerate(filters))
    featured=[('maison-3_4-',tr('La maison normande','The Normandy house')),('salons',tr('Sous les poutres','Under the timber beams')),('lion-piscine',tr('La piscine couverte','The covered pool')),('chambre3',tr('Les chambres','The bedrooms')),('Photo-2.7',tr('Le tennis et le jardin','Tennis and the garden'))]
    slides=''.join(f'<div class="album-slide {"is-current" if i==0 else ""}" data-album-slide aria-hidden="{str(i!=0).lower()}"><div class="album-image-wrap">{picture(k,eager=i==0,sizes="(min-width:1440px) 1280px, 100vw")}</div></div>' for i,(k,title) in enumerate(featured))
    thumbs=''.join(f'<button type="button" data-album-index="{i}" aria-pressed="{str(i==0).lower()}" aria-label="{esc(title)}">{picture(k,sizes="160px")}<span>{title}</span></button>' for i,(k,title) in enumerate(featured))
    titles=esc(json.dumps([title for k,title in featured],ensure_ascii=False))
    return f'''<section class="gallery-intro wrap"><p class="breadcrumb"><a href="{path('home')}">{tr('Accueil','Home')}</a> / {label('gallery')}</p><div class="gallery-title"><h1>{tr('L’album du domaine.','The estate’s album.')}</h1><p>{tr('La lumière dans les salons, les chambres sous les combles, le jardin tout autour. Prenez le temps de regarder.','Light in the living rooms, bedrooms under the eaves, the garden all around. Take time to look.')}</p></div></section><section class="album wrap" aria-label="{tr('Photographies choisies du domaine','Selected estate photographs')}" aria-roledescription="{tr('diaporama','slideshow')}" data-album-titles="{titles}"><div class="album-stage" tabindex="0">{slides}</div><div class="album-caption"><h2 data-album-title>{featured[0][1]}</h2><div><span data-album-count aria-live="polite">1 / {len(featured)}</span><button class="button button--skoll" data-album-step="-1" aria-label="{tr('Photo précédente','Previous photograph')}"><span><span>‹</span></span></button><button class="button button--skoll" data-album-step="1" aria-label="{tr('Photo suivante','Next photograph')}"><span><span>›</span></span></button></div></div><div class="album-rotation"><button type="button" class="rotation-control" data-album-rotation>{tr("Mettre en pause","Pause slideshow")}</button></div><div class="album-thumbs">{thumbs}</div></section><section class="gallery-index wrap"><div class="gallery-index-heading"><h2>{tr('Tous les espaces.','Every space.')}</h2><p id="gallery-count" class="fineprint" aria-live="polite">{len(keys)} {tr('photographies','photographs')}</p></div><div class="gallery-filters" aria-label="{tr('Filtrer les photographies','Filter photographs')}">{controls}</div><div class="gallery-grid" aria-label="{tr('Photographies du domaine','Estate photographs')}">{''.join(gallery_items)}</div></section>{final_cta()}'''

def faq():
    q=[(tr('Combien de personnes peut-on accueillir ?','How many guests can stay?'),tr('La maison accueille jusqu’à 15 invités, dans 8 chambres et leurs annexes. Contactez les propriétaires pour adapter les couchages à votre groupe.','The house welcomes up to 15 guests in 8 bedrooms and their annexes. Contact the owners to arrange sleeping configurations for your group.')),
       (tr('Quelle est la durée minimum du séjour ?','What is the minimum stay?'),tr('Le site du domaine indique 2 nuits minimum hors vacances scolaires et 5 nuits pendant les vacances scolaires. Les possibilités en semaine sont à voir avec les propriétaires.','The estate’s website states a minimum of 2 nights outside school holidays and 5 nights during school holidays. Ask the owners about weekday stays.')),
       (tr('Que faut-il prévoir à l’arrivée ?','What is provided on arrival?'),tr('Les lits sont faits et les serviettes de toilette et de piscine sont fournies. Le ménage est réalisé après votre départ; la cuisine et la vaisselle sont à nettoyer, et les poubelles à trier et déposer dans les bacs derrière la maison. Une caution de 1 500 € est demandée.','Beds are made, and bathroom and pool towels are provided. Cleaning takes place after departure; guests clean the kitchen and dishes, and sort and leave rubbish in the bins behind the house. A €1,500 security deposit is requested.')),
       (tr('La piscine est-elle ouverte toute l’année ?','Is the pool open all year?'),tr('La piscine couverte et sécurisée est chauffée à 28 °C toute l’année. Cette température peut varier en cas de grand froid. Les horaires indiqués sont de 8 h à 20 h.','The covered, secured pool is heated to 28°C all year. Water temperature can vary during exceptionally cold weather. The stated opening hours are 8am to 8pm.')),
       (tr('Peut-on organiser une fête ?','Can we hold a party?'),tr('Le domaine privilégie la tranquillité. Pas de fête ni de musique à l’extérieur, et pas de bruit après 23 h, conformément aux conditions du site d’origine.','The estate values peace and quiet. No parties or outdoor music, and no noise after 11pm, as stated in the original website’s conditions.')),
       (tr('Quels services peut-on demander ?','Which additional services are available?'),tr('Baby-sitting, activités pour petits et grands, traiteur, massages et mise en relation avec des prestataires peuvent être proposés sur demande. Les propriétaires préciseront les possibilités et les tarifs.','Babysitting, activities for children and adults, catering, massages and introductions to suppliers may be available on request. The owners will confirm options and prices.'))]
    headings=[tr('Votre groupe','Your group'),tr('La durée du séjour','Length of stay'),tr('Votre arrivée','Your arrival'),tr('La piscine','The pool'),tr('La tranquillité du lieu','Peace and quiet'),tr('Les services sur demande','Services on request')]
    return f'<section class="stay-information wrap"><h2>{tr("Votre séjour, en pratique.","Your stay, in practice.")}</h2><div class="stay-information-grid">'+''.join(f'<section class="practical-info"><h3>{headings[i]}</h3><p>{answer}</p></section>' for i,(question,answer) in enumerate(q))+'</div></section>'
def stay():
    return f'''<section class="booking-intro wrap"><p class="breadcrumb"><a href="{path('home')}">{tr('Accueil','Home')}</a> / {label('stay')}</p><h1>{tr('Préparons<br>votre séjour.','Let’s plan<br>your stay.')}</h1><p>{tr('Parlez-nous de vos dates et de votre groupe, ou consultez les annonces du domaine sur les plateformes de réservation.','Tell us your dates and about your group, or explore the estate’s listings on booking platforms.')}</p></section>
<section class="booking-layout wrap"><div class="booking-request"><h2>{tr('Contacter les propriétaires','Contact the owners')}</h2><p>{tr('Une question, des dates, un séminaire ? Préparez votre demande.','A question, dates in mind, a team retreat? Prepare your enquiry.')}</p><form id="stay-form"><div class="form-pair"><label>{tr('Arrivée souhaitée','Preferred arrival')}<input type="date" name="arrival" required></label><label>{tr('Départ souhaité','Preferred departure')}<input type="date" name="departure" required></label></div><div class="form-pair"><label>{tr('Nombre d’invités','Number of guests')}<input type="number" name="guests" min="1" max="15" value="8" required></label><label>{tr('Votre séjour','Your stay')}<select name="type"><option value="family">{tr('En famille','Family stay')}</option><option value="friends">{tr('Entre amis','With friends')}</option><option value="business">{tr('Séminaire / équipe','Team retreat')}</option></select></label></div><label>{tr('Votre message (facultatif)','Your message (optional)')}<textarea name="message" rows="4" placeholder="{tr('Parlez-nous de votre séjour…','Tell us about your stay…')}"></textarea></label><p class="form-error" id="form-error" role="alert"></p><button type="submit" class="button button--dione"><span>{tr('Préparer ma demande','Prepare my enquiry')}</span></button><p class="fineprint">{tr('Votre demande s’affichera avant l’ouverture de votre messagerie. Les propriétaires confirmeront les disponibilités et les conditions.','You can review your enquiry before opening your email app. The owners will confirm availability and conditions.')}</p><div id="email-preview" hidden><h3>{tr('Votre demande est prête','Your enquiry is ready')}</h3><p>{tr('Vérifiez le message dans votre messagerie avant de l’envoyer. Vous pouvez aussi copier le texte ci-dessous.','Check the message in your email app before sending it. You can also copy the text below.')}</p><pre></pre><a class="text-link" id="email-link" href="mailto:ledomaineauxlions@gmail.com">{tr('Ouvrir l’e-mail préparé','Open the prepared email')}</a></div></form><div class="direct-contact"><a href="mailto:ledomaineauxlions@gmail.com">ledomaineauxlions@gmail.com</a><a href="tel:+33630868569">+33 (0)6 30 86 85 69</a></div></div><aside class="booking-alternatives">{picture('chambre3')}<h2>{tr('Réserver sur une plateforme','Book through a platform')}</h2><p>{tr('Consultez les dates, les tarifs et les conditions directement sur l’annonce du domaine.','See dates, rates and conditions directly on the estate’s listing.')}</p><a class="platform-link" href="{AIRBNB}" target="_blank" rel="noopener"><span class="platform-identity"><img src="{asset("brands/airbnb.svg")}" width="32" height="32" alt="">Airbnb</span><span>{tr('Voir l’annonce','View the listing')}</span></a><a class="platform-link" href="{BOOKING}" target="_blank" rel="noopener"><span class="platform-identity"><img src="{asset("brands/bookingdotcom.svg")}" width="32" height="32" alt="">Booking.com</span><span>{tr('Voir l’annonce','View the listing')}</span></a><p class="fineprint">{tr('Vous continuerez sur le site de la plateforme. Les tarifs et conditions y sont précisés.','You will continue on the platform’s website, where rates and conditions are provided.')}</p><p>{tr('Maison entière · Jusqu’à 15 invités<br>Accueil en personne · Linge fourni','Entire house · Up to 15 guests<br>Personal welcome · Linen provided')}</p></aside></section>{faq()}'''
def access():
    cards=''.join(f'<figure class="arrival-photo"><button type="button" data-photo="{esc(json.dumps(image_data(k),ensure_ascii=False))}" aria-haspopup="dialog" aria-label="{esc(tr("Agrandir : ","Enlarge: ")+caption(k))}">{picture(k,sizes="(min-width:900px) 30vw, 100vw")}</button><figcaption>{caption(k)}</figcaption></figure>' for k in ('1','3','2','4','5'))
    maps='https://www.google.com/maps/search/?api=1&query=700+chemin+de+la+Boullaye+14100+Fauguernon'
    return page_intro(tr('Votre arrivée<br>au domaine.','Your arrival<br>at the estate.'),tr('700 chemin de la Boullaye, 14100 Fauguernon. Au cœur du Pays d’Auge.','700 chemin de la Boullaye, 14100 Fauguernon. In the heart of the Pays d’Auge.'),'bocage')+f'<section class="access-content wrap"><div><h2>{tr("Bienvenue en Normandie.","Welcome to Normandy.")}</h2><p>{tr("À environ 2 h de Paris et à moins de 30 min de Deauville et Honfleur. Le domaine se trouve au bout d’une impasse, dans un hameau bordé de champs.","Around 2 hours from Paris and less than 30 minutes from Deauville and Honfleur. The estate sits at the end of a lane in a hamlet bordered by fields.")}</p><p>{tr("Un parking privé pour huit voitures vous attend, à 50 mètres de l’entrée piétonne. Utilisez les repères ci-dessous pour votre arrivée.","Private parking for eight cars is available, 50 metres from the pedestrian entrance. Use the landmarks below for your arrival.")}</p>{button(tr("Ouvrir l’itinéraire","Get directions"),maps,attrs="target=\"_blank\" rel=\"noopener\"")}</div><div class="contact-panel"><h2>{tr("Restons en contact.","Get in touch.")}</h2><a href="mailto:ledomaineauxlions@gmail.com">ledomaineauxlions@gmail.com</a><a href="tel:+33630868569">+33 (0)6 30 86 85 69</a><p>700 chemin de la Boullaye<br>14100 Fauguernon, France</p></div></section><section class="arrival-section wrap"><h2>{tr("Les repères pour nous trouver.","Landmarks to find us.")}</h2><div class="arrival-grid">{cards}</div></section>{final_cta()}'
def legal():
    return f'''<section class="legal wrap"><h1>{label('legal')}</h1><div class="legal-notice"><strong>{tr('Maquette — informations à compléter avant publication.','Mockup — information required before publication.')}</strong><p>{tr('L’identité juridique complète de l’éditeur, son immatriculation, le directeur de publication et l’hébergeur final doivent être confirmés par le propriétaire.','The publisher’s full legal identity, registration details, publication director and final hosting provider must be confirmed by the owner.')}</p></div>
<h2>{tr('Éditeur du site','Site publisher')}</h2><p>Le Domaine aux Lions<br>700 chemin de la Boullaye, 14100 Fauguernon<br>ledomaineauxlions@gmail.com · +33 6 30 86 85 69</p><p>{tr('Raison sociale, forme juridique, SIRET, TVA et directeur de publication : [À CONFIRMER].','Legal name, legal form, registration number, VAT status and publication director: [TO BE CONFIRMED].')}</p>
<h2>{tr('Hébergement','Hosting')}</h2><p>{tr('Maquette locale. Hébergeur de production, adresse et site : [À CONFIRMER].','Local mockup. Production hosting provider, address and website: [TO BE CONFIRMED].')}</p>
<h2>{tr('Données personnelles','Personal data')}</h2><p>{tr('Cette maquette ne dispose pas de serveur de formulaire. La préparation d’une demande se déroule dans votre navigateur; l’e-mail est envoyé uniquement si vous le décidez dans votre messagerie. Le traitement des demandes reçues et leur durée de conservation doivent être précisés par le propriétaire avant publication.','This mockup has no form server. Enquiries are prepared in your browser; email is sent only if you choose to send it in your email app. The owner must specify how received enquiries are handled and retained before publication.')}</p><p>{tr('Pour les demandes relatives à vos données, contactez ledomaineauxlions@gmail.com. Informations sur vos droits :','For requests concerning your data, contact ledomaineauxlions@gmail.com. Information about your rights:')} <a href="https://www.cnil.fr/" target="_blank" rel="noopener">CNIL</a>.</p>
<h2>{tr('Cookies et services externes','Cookies and external services')}</h2><p>{tr('Cette maquette ne dépose pas de cookies et ne charge aucun outil d’analyse. Les photos et les polices sont locales. La visite 3D externe est chargée uniquement quand vous la lancez; son prestataire peut appliquer sa propre politique. Airbnb, Booking.com, les réseaux sociaux et Google Maps ouvrent leurs propres sites.','This mockup sets no cookies and loads no analytics. Photos and fonts are local. The external 3D tour loads only when you launch it; its supplier may apply its own policy. Airbnb, Booking.com, social networks and Google Maps open their own websites.')}</p>
<h2>{tr('Propriété intellectuelle et crédits','Intellectual property and credits')}</h2><p>{tr('Les photographies, logos et textes ont été repris du site du Domaine aux Lions pour cette proposition. Leur réutilisation et les conditions de livraison du domaine, de l’hébergement et du code seront à confirmer avec le propriétaire avant mise en ligne. Conception de la proposition : Telaventis.','Photos, logos and text are preserved from the Domaine aux Lions website for this proposal. Reuse and delivery terms for the domain, hosting and source code must be confirmed with the owner before publication. Proposal design: Telaventis.')}</p><p>“CSS Button Hover Styles” by Codrops (ButtonHoverStyles), MIT. <a href="https://github.com/codrops/ButtonHoverStyles/blob/main/css/base.css" target="_blank" rel="noopener">Source</a>.</p><p>{tr('Pattern de grille filtrable étudié dans la bibliothèque Design Memory; réimplémentation native, aucun code du CodePen copié. Visite 3D : Panotour, prestataire existant du domaine. Typographies locales : Alegreya et Alegreya Sans, SIL Open Font License. Stacked Sections par codse (Animata), MIT.','Filterable grid pattern studied in Design Memory; native implementation, no CodePen code copied. 3D tour: Panotour, the estate’s existing supplier. Self-hosted fonts: Alegreya and Alegreya Sans, SIL Open Font License. Stacked Sections by codse (Animata), MIT.')}</p><p>{tr('Dernière mise à jour : 7 octobre 2026.','Last updated: 7 October 2026.')}</p></section>'''

DESCRIPTIONS={
 'home':('Une maison normande privatisée pour 15 invités. Piscine couverte, tennis, jardin et confort, au cœur du Pays d’Auge.','A private Normandy house for up to 15 guests. Covered pool, tennis, garden and comfort in the Pays d’Auge.'),
 'house':('Découvrez la maison, ses huit chambres, sa piscine couverte, son jacuzzi, son jardin et tous les équipements du Domaine aux Lions.','Explore the house, eight bedrooms, covered pool, hot tub, garden and all the facilities at Le Domaine aux Lions.'),
 'family':('Un séjour en famille au Domaine aux Lions : jeux au jardin, piscine, équipements pour les bébés et activités pour tous les âges.','Family stays at Le Domaine aux Lions: garden games, a pool, baby equipment and activities for every age.'),
 'business':('Séminaires et retraites pour votre équipe, jusqu’à 15 personnes, avec fibre, projecteur et espaces modulables en Normandie.','Team retreats and seminars for up to 15 guests, with fibre internet, projector and flexible spaces in Normandy.'),
 'gallery':('Toutes les photographies du Domaine aux Lions : maison, chambres, jardin, piscine, tennis et espaces de détente.','Browse Le Domaine aux Lions photos: house, bedrooms, garden, pool, tennis and leisure spaces.'),
 'stay':('Préparez votre séjour au Domaine aux Lions : contacter les propriétaires, consulter les plateformes et connaître les conditions.','Plan your stay at Le Domaine aux Lions: contact the owners, explore booking platforms and read the conditions.'),
 'access':('Adresse, itinéraire, parking et repères d’arrivée au Domaine aux Lions à Fauguernon, dans le Pays d’Auge.','Address, directions, parking and arrival landmarks for Le Domaine aux Lions in Fauguernon, Pays d’Auge.'),
 'legal':('Mentions légales et informations sur les données personnelles de la proposition pour Le Domaine aux Lions.','Legal and privacy information for the Le Domaine aux Lions website proposal.'),
}
def head(page):
    title=label(page)+' — Le Domaine aux Lions' if page!='home' else tr('Le Domaine aux Lions — Votre maison en Normandie','Le Domaine aux Lions — Your house in Normandy')
    desc=tr(*DESCRIPTIONS[page]); url=BASE+PATHS[LANG][PAGES.index(page)]
    alternate=''.join(f'<link rel="alternate" hreflang="{l}" href="{BASE+PATHS[l][PAGES.index(page)]}">' for l in ('fr','en'))
    schema={'@context':'https://schema.org','@type':'LodgingBusiness','name':'Le Domaine aux Lions','description':desc,'email':'ledomaineauxlions@gmail.com','telephone':'+33630868569','address':{'@type':'PostalAddress','streetAddress':'700 chemin de la Boullaye','postalCode':'14100','addressLocality':'Fauguernon','addressCountry':'FR'},'sameAs':['https://instagram.com/le_domaine_aux_lions']}
    return f'''<!DOCTYPE html><html lang="{LANG}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{esc(title)}</title><meta name="description" content="{esc(desc)}"><meta name="robots" content="noindex, nofollow"><meta name="theme-color" content="#172319"><!-- Local mockup: replace example.com with the approved deployment domain before publication. --><link rel="canonical" href="{url}">{alternate}<link rel="alternate" hreflang="x-default" href="{BASE+PATHS['fr'][PAGES.index(page)]}"><meta property="og:type" content="website"><meta property="og:locale" content="{tr('fr_FR','en_GB')}"><meta property="og:site_name" content="Le Domaine aux Lions"><meta property="og:url" content="{url}"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:image" content="{BASE}assets/og.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="{caption('maison3')}"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{esc(title)}"><meta name="twitter:description" content="{esc(desc)}"><meta name="twitter:image" content="{BASE}assets/og.png"><link rel="icon" href="{asset('favicon.svg')}" type="image/svg+xml"><link rel="icon" href="{asset('favicon-32x32.png')}" sizes="32x32" type="image/png"><link rel="icon" href="{asset('favicon-16x16.png')}" sizes="16x16" type="image/png"><link rel="apple-touch-icon" href="{asset('apple-touch-icon.png')}"><link rel="stylesheet" href="{PREFIX}tokens/green.css"><link rel="stylesheet" href="{PREFIX}tokens/clay.css"><link rel="stylesheet" href="{PREFIX}tokens/fonts.css"><link rel="stylesheet" href="{PREFIX}tokens/ui.css"><link rel="stylesheet" href="{PREFIX}style.css"><link rel="stylesheet" href="{PREFIX}v3.css"><script type="application/ld+json">{json.dumps(schema,ensure_ascii=False)}</script></head><body data-language="{LANG}" data-page="{page}">'''

renderers={'home':home,'house':house,'family':lambda:stays('family'),'business':lambda:stays('business'),'gallery':gallery,'stay':stay,'access':access,'legal':legal}
urls=[]
for LANG in ('fr','en'):
    PREFIX='' if LANG=='fr' else '../'
    for CURRENT in PAGES:
        destination=ROOT / PATHS[LANG][PAGES.index(CURRENT)]
        destination.parent.mkdir(exist_ok=True)
        markup=head(CURRENT)+header()+'<main id="main">'+renderers[CURRENT]()+'</main>'+footer()+'</body></html>'
        destination.write_text(markup,encoding='utf-8')
        urls.append((LANG,CURRENT,BASE+PATHS[LANG][PAGES.index(CURRENT)]))
(ROOT/'robots.txt').write_text('User-agent: *\nDisallow: /\n',encoding='utf-8')
xml=['<?xml version="1.0" encoding="UTF-8"?>','<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
for lang,page,url in urls:
    xml.append('<url><loc>'+url+'</loc><lastmod>2026-10-07</lastmod><changefreq>monthly</changefreq><priority>'+('1.0' if page=='home' else '0.2' if page=='legal' else '0.8')+'</priority>'+''.join(f'<xhtml:link rel="alternate" hreflang="{l}" href="{BASE+PATHS[l][PAGES.index(page)]}"/>' for l in ('fr','en'))+'</url>')
xml.append('</urlset>')
(ROOT/'sitemap.xml').write_text('\n'.join(xml),encoding='utf-8')
print(json.dumps({'pagesBuilt':len(urls),'languages':['fr','en']}))
