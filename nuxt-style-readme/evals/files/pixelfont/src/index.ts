export interface Glyph {
  width: number
  rows: number[]
}

export const fonts: Record<string, Record<string, Glyph>> = {
  mono5: { A: { width: 5, rows: [0b01110, 0b10001, 0b11111, 0b10001, 0b10001] } },
  serif7: { A: { width: 7, rows: [0b0011100, 0b0100010, 0b1000001, 0b1111111, 0b1000001, 0b1000001, 0b1000001] } },
  pico8: { A: { width: 4, rows: [0b0110, 0b1001, 0b1111, 0b1001] } },
}

export function renderGlyph(ctx: CanvasRenderingContext2D, glyph: Glyph, x: number, y: number, scale = 1): void {
  glyph.rows.forEach((row, dy) => {
    for (let dx = 0; dx < glyph.width; dx++) {
      if (row & (1 << (glyph.width - 1 - dx))) ctx.fillRect(x + dx * scale, y + dy * scale, scale, scale)
    }
  })
}
