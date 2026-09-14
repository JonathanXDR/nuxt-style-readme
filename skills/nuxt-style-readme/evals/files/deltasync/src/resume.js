// rsync restarts a file from zero when the connection drops mid-transfer.
// deltasync writes a chunk manifest first, so a resumed run only re-sends the
// chunks whose hashes are still missing on the far side.
export function planResume(localChunks, remoteHashes) {
  return localChunks.filter((c) => !remoteHashes.has(c.hash));
}
