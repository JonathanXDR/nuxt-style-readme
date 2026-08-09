export interface HoverIntentOptions {
  delay?: number
  tolerance?: number
}

export function onHoverIntent(
  el: HTMLElement,
  handler: (event: PointerEvent) => void,
  opts: HoverIntentOptions = {},
): () => void {
  const delay = opts.delay ?? 100
  const tolerance = opts.tolerance ?? 4
  let timer: ReturnType<typeof setTimeout> | undefined
  let last: PointerEvent | undefined

  const onMove = (event: PointerEvent) => {
    if (last && Math.hypot(event.clientX - last.clientX, event.clientY - last.clientY) < tolerance) return
    last = event
    clearTimeout(timer)
    timer = setTimeout(() => handler(event), delay)
  }
  const onLeave = () => {
    clearTimeout(timer)
    last = undefined
  }

  el.addEventListener('pointermove', onMove)
  el.addEventListener('pointerleave', onLeave)
  return () => {
    clearTimeout(timer)
    el.removeEventListener('pointermove', onMove)
    el.removeEventListener('pointerleave', onLeave)
  }
}
