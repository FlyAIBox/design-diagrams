#!/usr/bin/env node

import { existsSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { basename, dirname, extname, join, resolve } from "node:path";
import { pathToFileURL } from "node:url";
import { spawnSync } from "node:child_process";

function usage(message) {
  if (message) console.error(`ERROR: ${message}`);
  console.error("Usage: render_svg.mjs <diagram.svg> [--scale 2] [--output file.png] [--browser path]");
  process.exit(2);
}

const argv = process.argv.slice(2);
if (!argv.length) usage();

let input;
let output;
let scale = 2;
let browserOverride;

for (let index = 0; index < argv.length; index += 1) {
  const arg = argv[index];
  if (!arg.startsWith("--") && !input) {
    input = resolve(arg);
  } else if (arg === "--scale") {
    scale = Number(argv[++index]);
  } else if (arg === "--output") {
    output = resolve(argv[++index]);
  } else if (arg === "--browser") {
    browserOverride = resolve(argv[++index]);
  } else {
    usage(`unknown argument: ${arg}`);
  }
}

if (!input || !existsSync(input)) usage("input SVG does not exist");
if (!Number.isFinite(scale) || scale <= 0) usage("--scale must be a positive number");
if (extname(input).toLowerCase() !== ".svg") usage("input must be an .svg file");

const source = readFileSync(input, "utf8");
const viewBoxMatch = source.match(/\bviewBox\s*=\s*["']\s*(-?[\d.]+)[\s,]+(-?[\d.]+)[\s,]+([\d.]+)[\s,]+([\d.]+)\s*["']/i);
if (!viewBoxMatch) usage("SVG needs a numeric viewBox");

const viewWidth = Number(viewBoxMatch[3]);
const viewHeight = Number(viewBoxMatch[4]);
if (!(viewWidth > 0 && viewHeight > 0)) usage("viewBox width and height must be positive");

const pixelWidth = Math.round(viewWidth * scale);
const pixelHeight = Math.round(viewHeight * scale);
if (pixelWidth > 10000 || pixelHeight > 10000) usage("requested output exceeds 10000 pixels on one axis");

if (!output) {
  const stem = basename(input, extname(input));
  output = join(dirname(input), `${stem}.preview.png`);
}

function findOnPath(name) {
  const result = spawnSync("which", [name], { encoding: "utf8" });
  return result.status === 0 ? result.stdout.trim() : undefined;
}

const candidates = [
  browserOverride,
  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
  "/Applications/Chromium.app/Contents/MacOS/Chromium",
  "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
  "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
  findOnPath("google-chrome"),
  findOnPath("chromium"),
  findOnPath("chromium-browser"),
  findOnPath("microsoft-edge"),
].filter(Boolean);

const browser = candidates.find((candidate) => existsSync(candidate));
if (!browser) usage("no Chrome/Chromium browser found; pass --browser /path/to/browser");

const tempDir = mkdtempSync(join(tmpdir(), "design-diagrams-"));
const htmlPath = join(tempDir, "render.html");
const svgUrl = pathToFileURL(input).href.replaceAll("&", "&amp;").replaceAll('"', "&quot;");
const html = `<!doctype html>
<html>
<head>
<meta charset="utf-8">
<style>
  html, body { margin: 0; width: ${pixelWidth}px; height: ${pixelHeight}px; overflow: hidden; background: #fff; }
  img { display: block; width: ${pixelWidth}px; height: ${pixelHeight}px; object-fit: contain; }
</style>
</head>
<body><img src="${svgUrl}" alt=""></body>
</html>`;
writeFileSync(htmlPath, html, "utf8");

const result = spawnSync(
  browser,
  [
    "--headless=new",
    "--disable-gpu",
    "--hide-scrollbars",
    "--force-device-scale-factor=1",
    "--run-all-compositor-stages-before-draw",
    "--virtual-time-budget=1500",
    `--window-size=${pixelWidth},${pixelHeight}`,
    `--screenshot=${output}`,
    pathToFileURL(htmlPath).href,
  ],
  { encoding: "utf8" },
);

rmSync(tempDir, { recursive: true, force: true });

if (result.status !== 0 || !existsSync(output)) {
  console.error(result.stderr || result.stdout || "browser rendering failed");
  process.exit(1);
}

const png = readFileSync(output);
const isPng = png.length >= 24 && png.subarray(1, 4).toString("ascii") === "PNG";
if (!isPng) {
  console.error("ERROR: browser output is not a PNG");
  process.exit(1);
}
const actualWidth = png.readUInt32BE(16);
const actualHeight = png.readUInt32BE(20);
if (actualWidth !== pixelWidth || actualHeight !== pixelHeight) {
  console.error(`ERROR: expected ${pixelWidth}×${pixelHeight}, got ${actualWidth}×${actualHeight}`);
  process.exit(1);
}

console.log(`Rendered ${output}`);
console.log(`Dimensions: ${actualWidth}×${actualHeight} (${scale}× viewBox)`);

