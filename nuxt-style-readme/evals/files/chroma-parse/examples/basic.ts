import { parse, format } from 'chroma-parse';

console.log(format(parse('oklch(70% 0.1 200)')!, 'hex'));
