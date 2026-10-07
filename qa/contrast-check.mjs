import fs from 'node:fs';
import { APCAcontrast, sRGBtoY } from './apca-w3.mjs';
const rgb = hex => hex.replace('#','').match(/../g).map(v=>parseInt(v,16));
const luminance = value => rgb(value).map(v=>v/255).map(v=>v<=.04045?v/12.92:((v+.055)/1.055)**2.4).reduce((s,v,i)=>s+v*[.2126,.7152,.0722][i],0);
const pairs = [
  ['Primary text','#172319','#ffffff',60],
  ['Secondary text and captions','#3d5441','#ffffff',75],
  ['Review note on green 2','#3d5441','#f6f9f7',75],
  ['Pool text on clay 3','#172319','#f7e8e1',60],
  ['Pool fine print on clay 3','#3d5441','#f7e8e1',75],
  ['Dark section body','#e6ede7','#172319',60],
  ['Dark section title and buttons','#ffffff','#172319',60],
  ['Hyperion rest','#ffffff','#000000',60],
  ['Hyperion hover difference','#000000','#ffffff',60],
  ['Location label and legal text','#6c412d','#ffffff',75],
];
const results = pairs.map(([name,fg,bg,minimum])=>{
  const values=[luminance(fg),luminance(bg)].sort((a,b)=>b-a);
  const wcag=(values[0]+.05)/(values[1]+.05);
  const apca=Math.abs(APCAcontrast(sRGBtoY(rgb(fg)),sRGBtoY(rgb(bg))));
  return {name,fg,bg,wcag:Number(wcag.toFixed(2)),apca:Number(apca.toFixed(1)),minimum,pass:wcag>=4.5&&apca>=minimum};
});
fs.writeFileSync(new URL('./contrast-results.json',import.meta.url),JSON.stringify({note:'sRGB rounded equivalents from the generated OKLCH scales; exact rendered color values also inspected in browser.',results},null,2));
console.table(results);
process.exitCode=results.some(r=>!r.pass)?1:0;
