import { createReadStream, createWriteStream } from 'node:fs'
import { mkdtemp, rm, writeFile } from 'node:fs/promises'
import { tmpdir } from 'node:os'
import { join } from 'node:path'
import { createInterface } from 'node:readline'

export interface SortOptions {
  chunkBytes?: number
  tmpDir?: string
  comparator?: (a: string, b: string) => number
}

const lexicographic = (a: string, b: string): number => (a < b ? -1 : a > b ? 1 : 0)

export async function sortFile(input: string, output: string, opts: SortOptions = {}): Promise<void> {
  const chunkBytes = opts.chunkBytes ?? 64 * 1024 * 1024
  const comparator = opts.comparator ?? lexicographic
  const runDir = await mkdtemp(join(opts.tmpDir ?? tmpdir(), 'sortmerge-'))
  try {
    const runs = await writeSortedRuns(input, runDir, chunkBytes, comparator)
    await mergeRuns(runs, output, comparator)
  } finally {
    // Intermediate runs must not survive a crash, so cleanup happens even on throw.
    await rm(runDir, { recursive: true, force: true })
  }
}

async function writeSortedRuns(
  input: string,
  runDir: string,
  chunkBytes: number,
  comparator: (a: string, b: string) => number,
): Promise<string[]> {
  const runs: string[] = []
  let lines: string[] = []
  let bytes = 0
  const flush = async (): Promise<void> => {
    if (lines.length === 0) return
    const run = join(runDir, `run-${runs.length}.txt`)
    await writeFile(run, lines.sort(comparator).join('\n') + '\n')
    runs.push(run)
    lines = []
    bytes = 0
  }
  for await (const line of createInterface({ input: createReadStream(input) })) {
    lines.push(line)
    bytes += line.length + 1
    if (bytes >= chunkBytes) await flush()
  }
  await flush()
  return runs
}

async function mergeRuns(
  runs: string[],
  output: string,
  comparator: (a: string, b: string) => number,
): Promise<void> {
  const iterators = runs.map((run) =>
    createInterface({ input: createReadStream(run) })[Symbol.asyncIterator](),
  )
  const heads = await Promise.all(iterators.map((it) => it.next()))
  const out = createWriteStream(output)
  while (heads.some((head) => !head.done)) {
    let min = -1
    for (let i = 0; i < heads.length; i++) {
      if (heads[i].done) continue
      if (min === -1 || comparator(heads[i].value as string, heads[min].value as string) < 0) min = i
    }
    out.write((heads[min].value as string) + '\n')
    heads[min] = await iterators[min].next()
  }
  await new Promise<void>((resolve, reject) => {
    out.end((err?: Error | null) => (err ? reject(err) : resolve()))
  })
}
