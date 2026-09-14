export interface Rgb { r: number; g: number; b: number; a: number }

/** Parses hex, rgb(), hsl(), oklch(), and the CSS named colors. */
export function parse(input: string): Rgb | null { return null }

/** Formats an Rgb back to the shortest CSS representation that round-trips. */
export function format(c: Rgb, space?: 'hex' | 'rgb' | 'oklch'): string { return '' }
