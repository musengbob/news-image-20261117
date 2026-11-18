// Entry point for the news-image-20261117 entry.
//
// The front page is rendered by compose.py into entry.png (JPEG bytes
// under a .png name, as the competition allows). This program only copies
// that file into the output directory the grader provides, so both graded
// runs write exactly the same bytes.
//
//   MAKEFUN_OUTPUT_DIR=out node main.ts
import { copyFileSync, mkdirSync, readFileSync } from "node:fs";
import { createHash } from "node:crypto";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR;
if (!outDir) {
  throw new Error("MAKEFUN_OUTPUT_DIR is not set");
}

mkdirSync(outDir, { recursive: true });
const src = join(here, "entry.png");
const dst = join(outDir, "entry.png");
copyFileSync(src, dst);

// The two graded runs must write the same bytes, so confirm the copy
// landed intact before reporting success.
const digest = (path: string) =>
  createHash("sha256").update(readFileSync(path)).digest("hex");
if (digest(src) !== digest(dst)) {
  throw new Error(`copy mismatch: ${dst} differs from ${src}`);
}
console.log(`wrote ${dst}`);
