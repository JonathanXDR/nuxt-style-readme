import type { Directive } from 'vue'

export interface GlowlineOptions {
  colors?: [string, string]
  thickness?: number
  duration?: number
}

const defaults: Required<GlowlineOptions> = {
  colors: ['#00dc82', '#36e4da'],
  thickness: 2,
  duration: 1200,
}

export const vGlowline: Directive<HTMLElement, GlowlineOptions | undefined> = {
  mounted(el, binding) {
    const opts = { ...defaults, ...binding.value }
    el.style.backgroundImage = `linear-gradient(90deg, ${opts.colors[0]}, ${opts.colors[1]})`
    el.style.backgroundSize = `100% ${opts.thickness}px`
    el.style.backgroundPosition = '0 100%'
    el.style.backgroundRepeat = 'no-repeat'
    el.style.transition = `background-size ${opts.duration}ms`
  },
}

export function glowline(options?: GlowlineOptions): Directive<HTMLElement, GlowlineOptions | undefined> {
  return {
    mounted(el) {
      vGlowline.mounted?.(el, { value: options } as never, null as never, null as never)
    },
  }
}
