// news-image-20261117: writes one image summing up 17 November 2026 to /output/entry.png
// The image beside this file is a dense front page of that day: masthead
// THE WORLD TODAY, dated Tuesday, November 17, 2026, "29 stories, 6 continents",
// a lead photograph of the Kerch Bridge with a collapsed span under the
// headline "UKRAINE BRINGS DOWN KERCH BRIDGE SPAN", then three columns of short
// real stories grouped by continent — North America, Europe, Asia, Middle
// East, Africa, South America, Oceania — every headline a real, verified
// story of 17 November 2026 (Algenom, Just Security, NPR, Candid Dragon,
// OneTurn, The Profiler briefings of the day). compose.py in this directory
// rebuilds entry.png from photo.jpg; the program copies it byte for byte,
// so every run is identical.
import { copyFileSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';

const OUTPUT_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

mkdirSync(OUTPUT_DIR, { recursive: true });
copyFileSync(
  new URL('./entry.png', import.meta.url),
  join(OUTPUT_DIR, 'entry.png'),
);
