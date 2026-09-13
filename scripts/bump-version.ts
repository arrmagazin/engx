// Bumps the integer cache-busting version in a `version` file.
// The service worker reads `/version` to derive its cache name, so bumping
// this on deploy invalidates stale client caches.
//
// Usage: bun scripts/bump-version.ts [path-to-version-file]
//   defaults to ./www/version (relative to cwd, i.e. the app dir)

import { readFileSync, writeFileSync } from "node:fs";
import { resolve } from "node:path";

const file = resolve(process.argv[2] ?? "./www/version");

let current = 0;
try {
  current = Number.parseInt(readFileSync(file, "utf8").trim(), 10) || 0;
} catch {
  // No version file yet — start from 0.
}

const next = current + 1;
writeFileSync(file, String(next));
console.log(`Bumped version: ${current} → ${next} (${file})`);
