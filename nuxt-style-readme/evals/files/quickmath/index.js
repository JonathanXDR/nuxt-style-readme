export const clamp = (v, lo, hi) => Math.min(Math.max(v, lo), hi);
export const lerp = (a, b, t) => a + (b - a) * t;
export const remap = (v, a1, b1, a2, b2) => lerp(a2, b2, (v - a1) / (b1 - a1));
