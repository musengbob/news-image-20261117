// news-image-20261117 round 2 — "THE WORLD TODAY", Tuesday 17 November 2026.
// Node 22, standard library only. The entry image is the entry.png beside
// this file (built by compose.py); this program copies it to the output
// directory the grader reads. It runs with no network and writes the same
// bytes on every run.
//
// Local check:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, statSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const source = join(here, 'entry.png');

// The gate refuses anything over 1 MiB: fail loudly here instead of
// submitting an entry the scorer would reject.
const MAX_BYTES = 1048576;
const size = statSync(source).size;
if (size > MAX_BYTES) {
  throw new Error(`entry.png is ${size} bytes, over the ${MAX_BYTES} limit`);
}

mkdirSync(outDir, { recursive: true });
const dest = join(outDir, 'entry.png');
copyFileSync(source, dest);

// Verify the copy landed whole: a short write must never pass silently.
if (statSync(dest).size !== size) {
  throw new Error(`short copy: wrote ${statSync(dest).size} of ${size} bytes`);
}
