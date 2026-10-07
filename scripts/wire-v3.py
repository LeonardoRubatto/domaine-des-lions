from pathlib import Path
import re
root=Path(__file__).resolve().parents[1]
js=root/'site.js'
s=js.read_text(encoding='utf-8')
start=s.index('  // Editorial enter:')
end=s.index('  let opener',start)
s=s[:start]+s[end:]
start=s.index('  const reviewTrack =')
end=s.index('  const form =',start)
s=s[:start]+s[end:]
start=s.index('    if (!reduced.matches) {',s.index('  const filterGallery'))
end=s.index('    const count =',start)
s=s[:start]+s[end:]
js.write_text(s,encoding='utf-8')
builder=root/'scripts/build-site.py'
s=builder.read_text(encoding='utf-8')
s=s.replace('<script src="{PREFIX}site.js" defer></script>','<script src="{PREFIX}site.js" defer></script><script src="{PREFIX}v3.js" defer></script>')
s=s.replace('<link rel="stylesheet" href="{PREFIX}style.css">','<link rel="stylesheet" href="{PREFIX}style.css"><link rel="stylesheet" href="{PREFIX}v3.css">')
s=re.sub(r'\n<dialog id="tour".*?</dialog>\n', '\n',s,flags=re.S)
old="expanded = ''.join(f'<section class=\"information-chapter\" id=\"chapter-{i}\"><h3>{esc(g[\"title\"])}</h3><div class=\"source-copy\">{render(g[\"blocks\"])}</div></section>' for i,g in enumerate(groups) if g['blocks'])"
new='''chapters=[]
    for i,g in enumerate(groups):
        if not g['blocks']: continue
        title=g['title'].lower()
        photo=None
        matches=[(['tennis'],'Photo-2.7'),(['jardin','garden','outside','grands','bigger'],'Garden-1'),(['chambre','bedroom','étage','floor'],'chambre3'),(['terrasse','terrace'],'Photo-2.1'),(['petits','little'],'High-chairs'),(['intérieur','inside'],'Game-room'),(['séminaire','seminar'],'salle-a-manger'),(['rez-de-jardin','garden floor'],'salons')]
        for words,key in matches:
            if any(w in title for w in words): photo=key; break
        image=picture(photo,sizes='(min-width:900px) 42vw, 100vw') if photo else ''
        chapters.append(f'<section class="information-chapter {"with-photo" if photo else ""}" id="chapter-{i}"><div><h3>{esc(g["title"])}</h3><div class="source-copy">{render(g["blocks"])}</div></div>{image}</section>')
    expanded=''.join(chapters)'''
assert old in s
s=s.replace(old,new)
builder.write_text(s,encoding='utf-8')
style=root/'style.css'
s=style.read_text(encoding='utf-8')
s='\n'.join(line for line in s.splitlines() if not any(x in line for x in ['motion-ready','.is-visible','transition: transform 600ms']))+'\n'
style.write_text(s,encoding='utf-8')
delivery=root/'scripts/prepare-delivery.py'
s=delivery.read_text(encoding='utf-8').replace("('style.css','site.js'","('style.css','site.js','v3.css','v3.js'")
delivery.write_text(s,encoding='utf-8')
print('V3 wired; legacy reveal and carousel handlers removed; descriptions illustrated.')
