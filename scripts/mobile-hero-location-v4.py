from pathlib import Path
p=Path(__file__).resolve().parent/'build-site.py'
s=p.read_text(encoding='utf-8')
old='<p>{tr(\'Fauguernon, Normandie<br>À environ 2 heures de Paris\',\'Fauguernon, Normandy<br>Around 2 hours from Paris\')}</p>'
new='<p class="hero-location"><span class="hero-location-desktop">{tr(\'Fauguernon, Normandie<br>À environ 2 heures de Paris\',\'Fauguernon, Normandy<br>Around 2 hours from Paris\')}</span><span class="hero-location-mobile">{tr(\'Normandie · À environ 2 h de Paris\',\'Normandy · Around 2 hours from Paris\')}</span></p>'
assert old in s
p.write_text(s.replace(old,new),encoding='utf-8')
