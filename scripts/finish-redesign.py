"""One-time source cleanup for the new templates; build-site.py remains the generator."""
import ast
from pathlib import Path

root = Path(__file__).resolve().parents[1]
file = root / 'scripts/build-site.py'
source = file.read_text(encoding='utf-8')
lines = source.splitlines(keepends=True)
nodes = [n for n in ast.parse(source).body if isinstance(n, ast.FunctionDef) and n.name.startswith('previous_')]
for node in reversed(nodes):
    del lines[node.lineno-1:node.end_lineno]
source = ''.join(lines)
replacements = {
    'Une maison<br>à partager.': 'Une maison pour 15 invités.',
    'A house<br>to share.': 'A house for 15 guests.',
    'La piscine.<br>À chaque saison.': 'La piscine couverte.',
    'The pool.<br>Every season.': 'The covered pool.',
    'Un match.<br>Puis le jardin.': 'Le tennis et le jardin.',
    'A match.<br>Then the garden.': 'Tennis and the garden.',
    'Explorez<br>le domaine<br>en 3D.': 'Explorez le domaine en 3D.',
    'Explore<br>the estate<br>in 3D.': 'Explore the estate in 3D.',
    'En famille<br>ou en équipe.': 'En famille ou en équipe.',
    'With family<br>or your team.': 'With family or your team.',
    'En famille.<br>Entre amis.': 'En famille et entre amis.',
    'With family.<br>With friends.': 'With family and friends.',
    'Séminaires<br>au domaine.': 'Séminaires au domaine.',
    'Team retreats<br>at the estate.': 'Team retreats at the estate.',
    'Votre séjour<br>en Normandie.': 'Fauguernon, dans le Pays d’Auge.',
    'Your stay<br>in Normandy.': 'Fauguernon, in the Pays d’Auge.',
    'Pour les petits, les grands, et les moments ensemble.': 'Toboggan géant, trampoline et tourniquet dans le jardin.',
    'For little ones, grown-ups and time together.': 'A giant slide, trampoline and roundabout in the garden.',
    'Un autre cadre pour travailler et échanger.': 'Fibre, projecteur et espaces modulables pour votre équipe.',
    'A different setting to work and share ideas.': 'Fibre internet, a projector and flexible spaces for your team.',
    '''{picture('piscine',sizes='(min-width: 900px) 58vw, 100vw')}''': '''{picture('lion-piscine',sizes='(min-width: 900px) 58vw, 100vw')}''',
    '''{picture('tennis2',sizes='(min-width: 900px) 58vw, 100vw')}''': '''{picture('Photo-2.7',sizes='(min-width: 900px) 58vw, 100vw')}''',
    'aria-labelledby="lightbox-caption" aria-labelledby="lightbox-caption"': 'aria-labelledby="lightbox-caption"',
    '''aria-label="{tr('Visite 3D du domaine','Estate 3D tour')}" aria-label="{tr('Visite 3D du domaine','Estate 3D tour')}"''': '''aria-label="{tr('Visite 3D du domaine','Estate 3D tour')}"''',
    '''<link rel="stylesheet" href="{PREFIX}tokens/ui.css">''': '''<link rel="stylesheet" href="{PREFIX}tokens/clay.css"><link rel="stylesheet" href="{PREFIX}tokens/ui.css">''',
    '''<button type="submit" class="button button--pan"><span>{tr('Préparer ma demande','Prepare my enquiry')}</span></button>''': '''<button type="submit" class="button button--hyperion"><span><span>{tr('Préparer ma demande','Prepare my enquiry')}</span></span></button>''',
    'Toute la place<br>de se retrouver.': 'Une maison<br>à partager.',
    'Room to<br>come together.': 'A house<br>to share.',
    'Arrivez. Installez-vous.': 'Un accueil en personne.',
    'Arrive. Settle in.': 'A personal welcome.',
    'À qui ferez-vous<br>une place ?': 'En famille<br>ou en équipe.',
    'Who will you<br>bring along?': 'With family<br>or your team.',
    'Le Pays d’Auge,<br>tout autour.': 'Votre séjour<br>en Normandie.',
    'The Pays d’Auge,<br>all around.': 'Your stay<br>in Normandy.',
    'Du temps ensemble.<br>De la place pour chacun.': 'Le domaine<br>en famille.',
    'Time together.<br>Room for everyone.': 'Family stays<br>at the estate.',
    'Votre équipe,<br>au vert.': 'Séminaires<br>au domaine.',
    'Your team,<br>in the countryside.': 'Team retreats<br>at the estate.',
    'Your team,<br>in the country.': 'Team retreats<br>at the estate.',
    'Les mots de nos invités.': 'Témoignages repris du site du domaine.',
    'Our guests’ own words.': 'Reviews published on the estate’s website, in their original French.',
    'Typographie système : Georgia et Segoe UI.': 'Typographies locales : Source Serif 4 et Public Sans, SIL Open Font License. Stacked Sections par codse (Animata), MIT.',
    'System typography: Georgia and Segoe UI.': 'Self-hosted fonts: Source Serif 4 and Public Sans, SIL Open Font License. Stacked Sections by codse (Animata), MIT.',
}
for before, after in replacements.items():
    source = source.replace(before, after)
file.write_text(source, encoding='utf-8')
print('Generator cleaned and ready.')
