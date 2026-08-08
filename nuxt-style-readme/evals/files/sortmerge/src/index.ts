export interface SortOptions { chunkBytes?: number; tmpDir?: string; comparator?: (a: string, b: string) => number }
export async function sortFile(input: string, output: string, opts?: SortOptions): Promise<void> {}
