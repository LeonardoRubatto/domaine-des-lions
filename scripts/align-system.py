"""Bring the existing mockup onto the Design Memory grid and declared tokens."""
import json
from pathlib import Path
import re
root = Path(__file__).resolve().parents[1]
css_path = root/'style.css'
css = css_path.read_text(encoding='utf-8')
css = css.replace('outline: 3px','outline: 2px').replace('bottom: 6px','bottom: 8px')
for old,new in [('44px','48px'),('610px','608px'),('660px','656px'),('340px','336px'),
                ('900px','1024px'),('760px','768px'),('1000px','1024px'),('1200px','1280px')]:
    css=css.replace(old,new)
css=css.replace('letter-spacing: -.035em','letter-spacing: -.025em')
css=css.replace('letter-spacing: .16em','letter-spacing: .08em').replace('letter-spacing: .12em','letter-spacing: .08em')
css=css.replace('animation: house-arrival 1s','animation: house-arrival 640ms')
css=css.replace('.arrival-grid { display: grid; grid-template-columns: repeat(3,1fr);','.arrival-grid { display: grid; grid-template-columns: 1fr 1fr;')
css_path.write_text(css,encoding='utf-8')
tokens_path=root/'design-tokens.json'
tokens=json.loads(tokens_path.read_text(encoding='utf-8'))
tokens['spacing']['base']=4
tokens_path.write_text(json.dumps(tokens,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
build_path=root/'scripts/build-site.py'
build=build_path.read_text(encoding='utf-8')
build=build.replace('id="menu" class="menu-dialog"','id="menu" class="menu-dialog" aria-label="{tr(\'Navigation du site\',\'Site navigation\')}"')
build=build.replace('id="lightbox" class="lightbox"','id="lightbox" class="lightbox" aria-labelledby="lightbox-caption"')
build=build.replace('id="tour" class="tour-dialog"','id="tour" class="tour-dialog" aria-label="{tr(\'Visite 3D du domaine\',\'Estate 3D tour\')}"')
build=build.replace('de 6 000 m²,<br','de 6\u00a0000\u00a0m²,<br')
build=build.replace('A house with<br+room for art.\').replace(\'<br+\',\'<br>\')','A house with<br>room for art.\')')
build=build.replace('La maison, les chambres, les moments au jardin. Retrouvez toutes les photographies du site d’origine, y compris les différentes séries de chambres.','Entrez dans les pièces, découvrez les chambres et promenez-vous au jardin. La maison se dévoile, à votre rythme.')
build=build.replace('The house, bedrooms and time in the garden. Browse all the original site’s photographs, including the different bedroom photo collections.','Step into the living spaces, discover the bedrooms and wander through the garden. Explore the house at your own pace.')
build=build.replace('Les mots de nos invités, repris du site du domaine.','Les mots de nos invités.').replace('Our guests’ own words, preserved from the estate’s website.','Our guests’ own words.')
build=build.replace('Ouvrir votre messagerie\',\'Open your email app','Préparer ma demande\',\'Prepare my enquiry')
build=build.replace('Ce bouton ouvre votre messagerie avec un e-mail préparé. Rien n’est envoyé ni enregistré par ce site. Les propriétaires confirmeront les disponibilités et les conditions.','Votre demande s’affichera avant l’ouverture de votre messagerie. Les propriétaires confirmeront les disponibilités et les conditions.')
build=build.replace('This opens your email app with a prepared message. Nothing is sent or stored by this website. The owners will confirm availability and conditions.','You can review your enquiry before opening your email app. The owners will confirm availability and conditions.')
# Two Pan capsules on the home page: header + hero. Other CTAs use the restrained secondary style.
build=build.replace('button(label("stay"),path("stay"))','button(label("stay"),path("stay"),secondary=True)')
build=build.replace("{picture('salons',css='intro-main')}{picture('chambre3',css='intro-small')}","<a class=\"photo-card photo-card-main\" href=\"{path('gallery')}?filter=house\">{picture('salons',css='intro-main')}</a><a class=\"photo-card photo-card-art\" href=\"{path('house')}\">{picture('piano',css='intro-art')}</a><a class=\"photo-card photo-card-small\" href=\"{path('gallery')}?filter=bedrooms\">{picture('chambre3',css='intro-small')}</a>")
build=build.replace('Le confort d’un hôtel.<br>Une maison pour vous.','Une maison pensée<br>pour votre confort.').replace('Hotel comfort.<br>A house of your own.','A house designed<br>for your comfort.')
build=build.replace('La campagne normande.<br>À portée de séjour.','Au cœur du<br>Pays d’Auge.').replace('The Normandy countryside.<br>Within easy reach.','In the heart of<br>the Pays d’Auge.')
build=build.replace('Et si votre prochain séjour<br>commençait ici ?','Préparons votre séjour.').replace('Could your next stay<br>begin here?','Plan your stay.')
build_path.write_text(build,encoding='utf-8')
