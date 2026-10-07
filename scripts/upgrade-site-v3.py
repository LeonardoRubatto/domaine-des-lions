"""Apply the requested gallery, open information and integrated-tour redesign."""
from pathlib import Path
import ast
import re
root=Path(__file__).resolve().parents[1]
builder=root/'scripts/build-site.py'
text=builder.read_text(encoding='utf-8')

def replace_function(name, replacement):
    global text
    node=next(n for n in ast.parse(text).body if isinstance(n,ast.FunctionDef) and n.name==name)
    lines=text.splitlines(keepends=True)
    text=''.join(lines[:node.lineno-1])+replacement.strip()+'\n'+''.join(lines[node.end_lineno:])

replace_function('button', '''
def button(label,href=None,attrs='',secondary=False):
    css='button button--hyperion' if CURRENT=='home' and 'Réserver' in label or 'Plan your stay'==label else 'button button--dione'
    inner=f'<span><span>{label}</span></span>' if 'hyperion' in css else f'<span>{label}</span>'
    if href: return f'<a class="{css}" href="{esc(href)}" {attrs}>{inner}</a>'
    return f'<button class="{css}" type="button" {attrs}>{inner}</button>'
''')
# The header keeps one familiar primary action in both languages, on every page.
text=text.replace("{button(tr('Réserver un séjour','Plan your stay'),path('stay'))}","<a class=\"button button--hyperion\" href=\"{path('stay')}\"><span><span>{tr('Réserver un séjour','Plan your stay')}</span></span></a>")
text=text.replace("{tr('Entrer dans le domaine en 3D','Step inside the estate in 3D')}","{tr('Découvrir la maison','Discover the house')}").replace('class="text-link" href="#visite"','class="text-link" href="#maison"')
replace_function('tour_section', '''
def tour_section():
    if CURRENT!='home':
        return f'<section class="tour-route wrap"><p>{tr("Prenez vos repères dans la maison et le jardin.","Get your bearings in the house and garden.")}</p>{button(tr("Explorer les espaces en 360°","Explore the spaces in 360°"),path("home")+"#visite")}</section>'
    scenes=[('pano6815',tr('Le salon','Living room'),'salons'),('pano6817',tr('La piscine','The pool'),'lion-piscine'),('pano6819',tr('Le jardin','The garden'),'Photo-2.7'),('pano6794',tr('La salle à manger','Dining room'),'salle-a-manger'),('pano6806',tr('Chambre Monet','Monet bedroom'),'chambre3')]
    choices=''.join(f'<button class="tour-scene" type="button" data-tour-scene="{scene}" aria-pressed="false">{picture(photo,sizes="160px")}<span>{label}</span></button>' for scene,label,photo in scenes)
    return f\'''<section class="tour-hub" id="visite"><div class="wrap"><div class="tour-hub-heading"><h2>{tr('Entrez dans le domaine.','Step inside the estate.')}</h2><p>{tr('Choisissez un espace, puis regardez autour de vous. La visite à 360° vous fait passer de la maison au jardin.','Choose a space, then look around. The 360° tour takes you from the house into the garden.')}</p></div><div class="tour-stage" data-tour-url="{TOUR}"><div class="tour-cover">{picture('Photo-2.2',sizes='(min-width: 1440px) 1280px, 100vw')}<button class="button button--fenrir" type="button" data-tour-start aria-label="{tr('Commencer la visite à 360°','Start the 360° tour')}"><svg class="progress" viewBox="0 0 100 100" aria-hidden="true"><circle class="progress__circle" cx="50" cy="50" r="49"/><circle class="progress__path" cx="50" cy="50" r="49" pathLength="1"/></svg><span>{tr('Entrer','Enter')}</span></button></div><div class="tour-inline-frame"></div></div><div class="tour-toolbar"><p class="tour-status" role="status">{tr('Maison & jardin · 360°','House & garden · 360°')}</p><div><button type="button" class="quiet-link" data-tour-expand hidden>{tr('Plein écran','Full screen')}</button><button type="button" class="quiet-link" data-tour-stop hidden>{tr('Fermer la visite','Close the tour')}</button><a class="quiet-link" href="{TOUR}" target="_blank" rel="noopener">{tr('Ouvrir à part','Open separately')}</a></div></div><div class="tour-scenes" aria-label="{tr('Choisir un espace à visiter','Choose a space to explore')}">{choices}</div></div></section>\'''
''')
# Turn source groups into visible illustrated chapters instead of disclosures.
text=text.replace("# These are the owner’s descriptions; disclosure changes hierarchy, not the information.","# Owner descriptions remain visible without any disclosure interaction.")
text=text.replace("expanded = ''.join(f'<details class=\"content-detail\"><summary>{esc(g[\"title\"])}</summary><div class=\"source-copy\">{render(g[\"blocks\"])}</div></details>' for g in groups if g['blocks'])", "expanded = ''.join(f'<section class=\"information-chapter\" id=\"chapter-{i}\"><h3>{esc(g[\"title\"])}</h3><div class=\"source-copy\">{render(g[\"blocks\"])}</div></section>' for i,g in enumerate(groups) if g['blocks'])")
# Keep all real testimonials and their translations; replace presentation only.
node=next(n for n in ast.parse(text).body if isinstance(n,ast.FunctionDef) and n.name=='reviews')
lines=text.splitlines(keepends=True)
function=''.join(lines[node.lineno-1:node.end_lineno])
return_pos=function.rfind('    return ')
review_return='''    return f\'''<section class="reviews-section"><div class="wrap"><div class="review-heading"><h2>{tr('Les mots de nos invités.','In our guests’ words.')}</h2><p class="review-note">{tr('Leurs témoignages sur le site du domaine.','Guest testimonials. French reviews translated into English.')}</p></div><div class="review-stage"><figure class="review-photo">{picture('maison',sizes='(min-width:900px) 38vw, 100vw')}</figure><div class="review-reading"><span class="quote-mark" aria-hidden="true">“</span><div class="review-track" tabindex="0" role="region" aria-roledescription="{tr('carrousel','carousel')}" aria-label="{tr('Témoignages des invités','Guest reviews')}">{''.join(markup for _,markup in cards)}</div><div class="review-bottom"><p class="review-position fineprint" aria-live="off"></p><div class="review-controls"><button class="button button--skoll" data-review-step="-1" aria-label="{tr('Avis précédent','Previous review')}"><span><span>‹</span></span></button><button class="rotation-control" data-review-rotation type="button">{tr('Mettre en pause','Pause slideshow')}</button><button class="button button--skoll" data-review-step="1" aria-label="{tr('Avis suivant','Next review')}"><span><span>›</span></span></button></div></div></div></div></div></section>\'''\n'''
replace_function('reviews',function[:return_pos]+review_return)
# Large composed gallery chapter, then all preserved photographs.
replace_function('gallery', '''
def gallery():
    keys=[k for k in PHOTOS if k not in ('1','2','3','4','5','home_title_1','footer-presentation') and not k.startswith('home_') and not k.startswith('homepage-')]
    lead=['maison3','salons','lion-piscine','chambre3','maison','tennis2','salle-a-manger','attraction2']
    keys=lead+[k for k in keys if k not in lead]
    gallery_items=[]
    for i,k in enumerate(keys):
        data=esc(json.dumps(image_data(k),ensure_ascii=False))
        gallery_items.append(f'<figure class="gallery-item" data-category="{category(k)}"><button type="button" data-photo="{data}" aria-haspopup="dialog" aria-label="{esc(tr("Agrandir : ","Enlarge: ")+caption(k))}">{picture(k,sizes="(min-width: 900px) 50vw, (min-width: 600px) 48vw, 100vw")}</button><figcaption>{caption(k)}</figcaption></figure>')
    filters=[('all',tr('Tout le domaine','The whole estate')),('house',tr('La maison','The house')),('bedrooms',tr('Les chambres','Bedrooms')),('relax',tr('La détente','Leisure')),('garden',tr('Le jardin','The garden'))]
    controls=''.join(f'<button type="button" data-filter="{key}" aria-pressed="{str(i==0).lower()}">{label}</button>' for i,(key,label) in enumerate(filters))
    featured=[('maison-3_4-',tr('La maison normande','The Normandy house')),('salons',tr('Sous les poutres','Under the timber beams')),('lion-piscine',tr('La piscine couverte','The covered pool')),('chambre3',tr('Les chambres','The bedrooms')),('Photo-2.7',tr('Le tennis et le jardin','Tennis and the garden'))]
    slides=''.join(f'<div class="album-slide {"is-current" if i==0 else ""}" data-album-slide aria-hidden="{str(i!=0).lower()}"><div class="album-image-wrap">{picture(k,eager=i==0,sizes="(min-width:1440px) 1280px, 100vw")}</div></div>' for i,(k,title) in enumerate(featured))
    thumbs=''.join(f'<button type="button" data-album-index="{i}" aria-pressed="{str(i==0).lower()}" aria-label="{esc(title)}">{picture(k,sizes="160px")}<span>{title}</span></button>' for i,(k,title) in enumerate(featured))
    titles=esc(json.dumps([title for k,title in featured],ensure_ascii=False))
    return f\'''<section class="gallery-intro wrap"><p class="breadcrumb"><a href="{path('home')}">{tr('Accueil','Home')}</a> / {label('gallery')}</p><div class="gallery-title"><h1>{tr('L’album du domaine.','The estate’s album.')}</h1><p>{tr('La lumière dans les salons, les chambres sous les combles, le jardin tout autour. Prenez le temps de regarder.','Light in the living rooms, bedrooms under the eaves, the garden all around. Take time to look.')}</p></div></section><section class="album wrap" aria-label="{tr('Photographies choisies du domaine','Selected estate photographs')}" aria-roledescription="{tr('diaporama','slideshow')}" data-album-titles="{titles}"><div class="album-stage" tabindex="0">{slides}</div><div class="album-caption"><h2 data-album-title>{featured[0][1]}</h2><div><span data-album-count aria-live="polite">1 / {len(featured)}</span><button class="button button--skoll" data-album-step="-1" aria-label="{tr('Photo précédente','Previous photograph')}"><span><span>‹</span></span></button><button class="button button--skoll" data-album-step="1" aria-label="{tr('Photo suivante','Next photograph')}"><span><span>›</span></span></button></div></div><div class="album-thumbs">{thumbs}</div></section><section class="gallery-index wrap"><div class="gallery-index-heading"><h2>{tr('Tous les espaces.','Every space.')}</h2><p id="gallery-count" class="fineprint" aria-live="polite">{len(keys)} {tr('photographies','photographs')}</p></div><div class="gallery-filters" aria-label="{tr('Filtrer les photographies','Filter photographs')}">{controls}</div><div class="gallery-grid" aria-label="{tr('Photographies du domaine','Estate photographs')}">{''.join(gallery_items)}</div></section>{final_cta()}\'''
''')
node=next(n for n in ast.parse(text).body if isinstance(n,ast.FunctionDef) and n.name=='faq')
lines=text.splitlines(keepends=True)
function=''.join(lines[node.lineno-1:node.end_lineno])
return_pos=function.rfind('    return ')
replace_function('faq',function[:return_pos]+'''    headings=[tr('Votre groupe','Your group'),tr('La durée du séjour','Length of stay'),tr('Votre arrivée','Your arrival'),tr('La piscine','The pool'),tr('La tranquillité du lieu','Peace and quiet'),tr('Les services sur demande','Services on request')]
    return f'<section class="stay-information wrap"><h2>{tr("Votre séjour, en pratique.","Your stay, in practice.")}</h2><div class="stay-information-grid">'+''.join(f'<section class="practical-info"><h3>{headings[i]}</h3><p>{answer}</p></section>' for i,(question,answer) in enumerate(q))+'</div></section>'
''')
# Mark the four editorial photographs for the restrained source tilt curve.
text=text.replace('<figure class="intro-salon">','<figure class="intro-salon" data-tilt-frame>')
text=text.replace('<figure class="intro-bedroom">','<figure class="intro-bedroom" data-tilt-frame>')
text=text.replace('<a class="stay-tile"','<a data-tilt-frame class="stay-tile"')
text=text.replace('class="button button--hyperion"><span><span>{tr(\'Préparer ma demande\',\'Prepare my enquiry\')}</span></span>', 'class="button button--dione"><span>{tr(\'Préparer ma demande\',\'Prepare my enquiry\')}</span>')
builder.write_text(text,encoding='utf-8')
plan=root/'design-plan-v3.md'
content=plan.read_text(encoding='utf-8')
sections={
 'Signature': "La maison reste l'ouverture. Les chapitres piscine/tennis se superposent; quatre photographies éditoriales se redressent doucement au défilement. La visite est un espace 3D unique intégré à l'accueil, avec accès aux scènes réelles du salon, de la piscine, du jardin, de la salle à manger et de la chambre Monet. La galerie possède une grande scène photographique à transition circulaire, suivie d'un album de formats variés.",
 'Layout': "Les huit pages FR/EN subsistent. Les descriptions sont toujours visibles dans des chapitres ouverts, les informations pratiques sont disposées en deux colonnes, les avis apparaissent dans une galerie automatique avec pause. L'espace 3D n'est plus répété sur les pages internes; elles pointent vers l'accueil. La galerie commence par cinq grandes photos choisies, puis montre toutes les images dans une composition décalée. Mobile : une colonne, commandes 44px minimum, taille adaptée de la visite intégrée.",
 'Motion': "Accueil : Stacked Sections withDramaEffect=false, stackOffset=48px. Support : boutons Hyperion (200/300ms), Dione (300ms cubic-bezier(0.2,1,0.7,1)), Skoll (300ms cubic-bezier(0.7,0,0.2,1)), Fenrir (400ms cubic-bezier(0.7,0,0.3,1)); Scroll Tilted Grid adapté sur quatre photos, maxTilt=16/maxBlur=0, sans Lenis ni boucle. Galerie : Shapes Slideshow, clip circulaire, translation du cadre et contre-translation de l'image; 800ms cubic-bezier(0.2,0,0,1). Avis : 400ms, autoplay entre 9 et 60 secondes selon la longueur du texte, arrêté au focus/survol/hors écran/onglet caché et bouton Pause. Reduced motion : aucun autoplay, aucune transition ni tilt. Aucun effet ne masque des informations. Les comportements supplémentaires répondent à la demande explicite de Leonardo.",
 'Items': "- primitives/button-hover-styles — Hyperion au header; Dione pour les actions; Skoll pour les commandes; Fenrir pour entrer dans la visite. Code, séquences et structures spécifiques conservés, valeurs adaptées à la typographie et au tactile.\n- scroll/stacked-sections — port natif sans drama effect; offset48, mobile/RM/focus en flux normal.\n- scroll/scroll-tilted-grid — courbes géométriques du code stocké, port natif; valeurs modérées, sans blur ni Lenis, reset mobile/focus/RM.\n- gallery-carousel/shapes-slideshow — architecture, masque circulaire, déplacement opposé image/cadre conservés; port WAAPI, délai compressé à800ms, images visibles en plein cadre au repos, clavier et RM ajoutés.\nDescriptions ouvertes; iframe 3D à la demande, scènes vérifiées dans les fichiers publics du prestataire, aucun panorama recopié. Galerie classique aussi accessible via lightbox."
}
for name,body in sections.items():
    content=re.sub(r'(?ms)^## '+name+r'\n.*?(?=^## |\Z)','## '+name+'\n'+body+'\n\n',content)
plan.write_text(content,encoding='utf-8')
print('V3 rendering functions and reviewed design intent updated.')
