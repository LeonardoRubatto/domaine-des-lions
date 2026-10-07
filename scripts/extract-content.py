"""Preserve public source content without a runtime dependency."""
import json
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin

ROOT = Path(__file__).resolve().parents[1]
VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'}

class Node:
    def __init__(self, tag='', attrs=None):
        self.tag, self.attrs, self.children = tag, dict(attrs or []), []
    def walk(self):
        yield self
        for child in self.children:
            if isinstance(child, Node):
                yield from child.walk()
    def text(self):
        if self.tag in ('script', 'style', 'noscript'):
            return ''
        return ''.join(child.text() if isinstance(child, Node) else child for child in self.children)

class Parser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node('document')
        self.stack = [self.root]
    def handle_starttag(self, tag, attrs):
        node = Node(tag, attrs)
        self.stack[-1].children.append(node)
        if tag not in VOID:
            self.stack.append(node)
    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.handle_endtag(tag)
    def handle_endtag(self, tag):
        for index in range(len(self.stack) - 1, 0, -1):
            if self.stack[index].tag == tag:
                del self.stack[index:]
                break
    def handle_data(self, data):
        self.stack[-1].children.append(data)

paths = {
    'fr-home': '/', 'fr-presentation': '/presentation/', 'fr-gallery': '/photo-gallery/',
    'fr-families': '/familles/', 'fr-business': '/entreprises/', 'fr-contact': '/calendar-and-contact/',
    'en-home': '/en/le-domaine-aux-lions/', 'en-presentation': '/en/presentation_/',
    'en-gallery': '/en/image-gallery/', 'en-families': '/en/families/',
    'en-business': '/en/professionals/', 'en-contact': '/en/contacts/',
}
pages = []
for slug, path in paths.items():
    source = ROOT / 'research' / 'source-pages' / f'{slug}.html'
    parser = Parser()
    parser.feed(source.read_text(encoding='utf-8-sig'))
    nodes = list(parser.root.walk())
    content = next((n for n in nodes if n.attrs.get('id') == 'content'), parser.root)
    url = 'https://ledomaineauxlions.fr' + path
    blocks = [{'tag': n.tag, 'text': ' '.join(n.text().split())} for n in content.walk() if n.tag in ('h1', 'h2', 'h3', 'h4', 'p', 'li') and n.text().strip()]
    links = [{'text': ' '.join(n.text().split()), 'url': urljoin(url, n.attrs.get('href', ''))} for n in nodes if n.tag == 'a' and n.attrs.get('href')]
    images = [{'url': urljoin(url, n.attrs.get('src', '')), 'alt': n.attrs.get('alt', ''), 'srcset': n.attrs.get('srcset', '')} for n in nodes if n.tag == 'img']
    reviews = next((n for n in nodes if n.attrs.get('id') == 'carouselFooterReviews'), None)
    pages.append({'id': slug, 'url': url, 'blocks': blocks, 'links': links, 'images': images,
                  'reviewsText': ' '.join(reviews.text().split()) if reviews else ''})
output = ROOT / 'research' / 'content-inventory.json'
output.write_text(json.dumps(pages, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps({'pages': len(pages), 'contentBlocks': sum(len(p['blocks']) for p in pages),
                  'bookingLinksOnSource': [l for p in pages for l in p['links'] if 'airbnb.' in l['url'] or 'booking.com' in l['url']]}))
