[![hoverkit banner](./.github/assets/banner.svg)](https://hoverkit.dev)

[![npm version][npm-version-src]][npm-href]
[![npm downloads][npm-downloads-src]][npm-href]
[![License][license-src]][license-href]

# hoverkit

Hover intent detection for plain DOM elements, without a framework.

- [📖 &nbsp;Documentation](https://hoverkit.dev)
- [👾 &nbsp;Playground](./playground)

## Features

- 🎯 **Intent detection:** Fires only after the pointer settles instead of on every pass-through.
- ⏱️ **Tunable delay:** Sets the settle time in milliseconds through the delay option.
- 📐 **Movement tolerance:** Ignores pointer jitter below the tolerance radius you set.
- 🪶 **Zero dependencies:** Ships as one small ES module with TypeScript declarations.

## 🚀 Quick Start

Install the package:

```bash
npm install hoverkit
```

## 💻 Usage

Attach a handler that fires once the pointer settles, and call the returned function to detach:

```ts
import { onHoverIntent } from 'hoverkit'

const stop = onHoverIntent(card, () => card.classList.add('active'), { delay: 120, tolerance: 6 })
```

## ⚙️ Configuration

| Option | Default | Effect |
| ------ | ------- | ------ |
| `delay` | `100` | Milliseconds the pointer must settle before the handler fires |
| `tolerance` | `4` | Pixel radius of movement ignored while settling |

## 🛠️ Development

All checks run through npm scripts:

```bash
npm run build   # bundle with unbuild
npm test        # run the test suite with Vitest
npm run lint    # ESLint
```

## ⚖️ License

Licensed under the [MIT license](./LICENSE) © Example Author.

<!-- Badges -->

[npm-version-src]: https://img.shields.io/npm/v/hoverkit/latest.svg?style=flat&colorA=18181B&colorB=28CF8D
[npm-downloads-src]: https://img.shields.io/npm/dm/hoverkit.svg?style=flat&colorA=18181B&colorB=28CF8D
[npm-href]: https://npmjs.com/package/hoverkit
[license-src]: https://img.shields.io/npm/l/hoverkit.svg?style=flat&colorA=18181B&colorB=28CF8D
[license-href]: ./LICENSE
