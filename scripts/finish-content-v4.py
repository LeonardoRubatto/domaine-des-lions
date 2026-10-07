from pathlib import Path
root=Path(__file__).resolve().parents[1]
p=root/'scripts/build-site.py'
s=p.read_text(encoding='utf-8')
s=s.replace('Une maison à colombages pour se retrouver. Les salons sous les poutres, les chambres, le jardin : tout le domaine est à vous.','Une maison à colombages, huit chambres et un grand jardin. Tout le domaine est à vous.')
s=s.replace('A timber-framed house for time together. Living rooms beneath the beams, bedrooms and the garden: the whole estate is yours.','A timber-framed house, eight bedrooms and a large garden. The whole estate is yours.')
s=s.replace('<a class="text-link" href="#maison">{tr(\'Découvrir les espaces\',\'Discover the spaces\')}</a></div><div class="hero-setting">','<div class="hero-booking"><span>{tr("Réserver sur","Book on")}</span>{platform_links()}</div></div><div class="hero-setting">')
for slug,name in [('airbnb','Airbnb'),('bookingdotcom','Booking.com')]:
    s=s.replace(f'<span>{name}</span><span>{{tr(\'Voir l’annonce\',\'View the listing\')}}</span>',f'<span class="platform-identity"><img src="{{asset("brands/{slug}.svg")}}" width="32" height="32" alt="">{name}</span><span>{{tr(\'Voir l’annonce\',\'View the listing\')}}</span>')
p.write_text(s,encoding='utf-8')
print('Hero booking routes and platform marks wired.')
