import { parse, format } from 'chroma-parse';

const ramp = ['#0a0a0a', '#1f1f1f', '#3d3d3d'].map((c) => format(parse(c)!, 'oklch'));
console.log(ramp);
