# sortmerge

External merge sort for files that do not fit in memory.

## Features

- 🧮 **Bounded memory:** Sorts a file of any size inside a chunk budget you set.
- 🧵 **Streaming API:** Reads and writes as streams, so nothing is buffered whole.
- 🔤 **Custom comparators:** Any comparator that works with `Array.sort` works here.
- 🧹 **Self-cleaning:** Temporary runs are removed even when the process throws.

## 🚀 Install

```bash
npm install sortmerge
```

## 💻 Usage

```ts
import { sortFile } from 'sortmerge';

await sortFile('big.csv', 'sorted.csv', { chunkBytes: 64 * 1024 * 1024 });
```

## ⚙️ Configuration

| Option | Default | Effect |
| ------ | ------- | ------ |
| `chunkBytes` | `67108864` | Memory budget for each in-memory run |
| `tmpDir` | `os.tmpdir()` | Where intermediate runs are written |
| `comparator` | lexicographic | Ordering function applied to each line |

## 🛠️ Development

```bash
npm test        # run the test suite
npm run build   # bundle src/ into dist/
npm run lint    # ESLint
```

## ⚖️ License

Licensed under the [MIT license](./LICENSE) © Example Author.
