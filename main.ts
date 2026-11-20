// Entry program for the make.fun bounty "Post a GTA 6 meme on X".
//
// The post itself is the entry: the house reads the meme and its text
// straight from X and hands them to the judge. This program does the
// one small job the gate needs — it hands the post's address over.
// It copies POST.json, which names the X post, from this repository
// into the output directory where the gate looks for it.
//
// It uses only the Node standard library, touches no network, reads
// no clock, and reads nothing outside the repository, so two runs
// always write the same bytes.

import { copyFileSync, mkdirSync } from "node:fs";
import { join } from "node:path";

const repoDir = process.env.MAKEFUN_BOT_DIR ?? "/bot";
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

mkdirSync(outDir, { recursive: true });

try {
  copyFileSync(join(repoDir, "POST.json"), join(outDir, "POST.json"));
} catch (error) {
  console.error(`could not copy POST.json: ${(error as Error).message}`);
  process.exit(1);
}
