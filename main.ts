// news-image-20261117 entry: one picture of the world's news on Tuesday 17 November 2026.
// The picture (entry.png, drawn by tools/render.py) ships with the repository; this program
// copies it to /output/entry.png. Node 22, standard library only, no network.
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { readFileSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const image = readFileSync(new URL('./entry.png', import.meta.url));
writeFileSync(join(outDir, 'entry.png'), image);
