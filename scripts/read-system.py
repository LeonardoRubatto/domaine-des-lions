"""Bounded, complete text reads of the supplied design library, with a progress log."""
from pathlib import Path
import argparse,json
root=Path(r'C:\.Leonardo\Project\design system (website elements template)')
folder=Path(__file__).resolve().parents[1]/'research/design-system-reading'
chunks=json.loads((folder/'chunks.json').read_text(encoding='utf-8'))
parser=argparse.ArgumentParser();parser.add_argument('start',type=int);parser.add_argument('--chars',type=int,default=35000)
args=parser.parse_args();total=0;end=args.start;parts=[]
for number in range(args.start,len(chunks)):
    c=chunks[number];text=(root/c['path']).read_text(encoding='utf-8-sig')[c['start']:c['end']]
    if parts and total+len(text)>args.chars:break
    parts.append(f"FILE {number}: {c['path']} [{c['start']}:{c['end']}]\n{text}");total+=len(text);end=number+1
print('\n'.join(parts));print(f'\nNEXT_CHUNK={end}; CHARS_EMITTED={total}')
