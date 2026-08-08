# Format notes

The HAR capture must include the bootstrap response (`/api/v3/session`). It carries
the per-title nonce used to order pages. Captures started mid-session are unusable.

Known failures seen in the wild:

- Pages returned as WebP instead of JPEG on newer reader builds. Pillow handles it,
  but the page-size heuristic mis-detects spreads.
- Titles with embedded video have interleaved MP4 entries that are skipped.
- The nonce rotates roughly every 24 hours, so an old HAR cannot be re-processed.
- No public documentation exists for the endpoint. Everything here was derived by
  observation and may break without warning.
