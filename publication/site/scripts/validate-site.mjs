import { promises as fs } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const scriptDirectory = path.dirname(fileURLToPath(import.meta.url));
const site = path.resolve(scriptDirectory, "..");
const repo = path.resolve(site, "..", "..");

const requiredFiles = [
  "index.html",
  "styles.css",
  "app.js",
  "assets/library-portal.webp",
  "assets/library-index.json",
  "README.md",
];

const failures = [];
for (const relative of requiredFiles) {
  const stat = await fs.stat(path.join(site, relative)).catch(() => null);
  if (!stat?.isFile() || stat.size === 0) failures.push(`missing or empty: ${relative}`);
}

const html = await fs.readFile(path.join(site, "index.html"), "utf8");
const css = await fs.readFile(path.join(site, "styles.css"), "utf8");
const script = await fs.readFile(path.join(site, "app.js"), "utf8");
const index = JSON.parse(await fs.readFile(path.join(site, "assets", "library-index.json"), "utf8"));

const requiredCopy = [
  "The Living Record of Star Atlas",
  "Explore the people, worlds, decisions, and ideas that shaped a civilization.",
  "Where would you like to begin?",
  "Enter the Library",
  "Explore the Timeline",
  "Discover the Archive",
  "Follow the Evidence",
];
requiredCopy.forEach((copy) => {
  if (!html.includes(copy)) failures.push(`missing approved copy: ${copy}`);
});

if (!html.includes("<main") || !html.includes("<nav") || !html.includes("<dialog")) {
  failures.push("semantic landing structure is incomplete");
}
if (!html.includes("aria-live") || !html.includes("aria-label") || !html.includes("skip-link")) {
  failures.push("accessibility landmarks or announcements are missing");
}
if (!css.includes("prefers-reduced-motion") || !css.includes(":focus-visible")) {
  failures.push("motion or keyboard-focus accessibility rules are missing");
}
if (!script.includes("showModal()") || !script.includes("loadIndex()")) {
  failures.push("library entrance or search index behavior is missing");
}

const knowledgeFiles = [];
async function visit(directory) {
  for (const entry of await fs.readdir(directory, { withFileTypes: true })) {
    const target = path.join(directory, entry.name);
    if (entry.isDirectory()) await visit(target);
    else if (entry.isFile() && entry.name.endsWith(".md")) knowledgeFiles.push(target);
  }
}
await visit(path.join(repo, "knowledge"));

if (index.length !== knowledgeFiles.length) {
  failures.push(`search index count ${index.length} does not match knowledge Markdown count ${knowledgeFiles.length}`);
}
const ids = new Set();
for (const record of index) {
  if (ids.has(record.id)) failures.push(`duplicate search record id: ${record.id}`);
  ids.add(record.id);
  if (!record.title || !record.summary || !record.category || !record.path || !record.url) {
    failures.push(`incomplete search record: ${record.id || "UNKNOWN"}`);
  }
  const target = path.join(repo, ...record.path.split("/"));
  if (!(await fs.stat(target).catch(() => null))?.isFile()) failures.push(`orphan search record: ${record.path}`);
}

const localReferences = [...html.matchAll(/(?:href|src)="(?!https?:|#|mailto:)([^"?]+)"/g)].map((match) => match[1]);
for (const reference of localReferences) {
  const clean = reference === "./" ? "index.html" : reference;
  if (!(await fs.stat(path.join(site, clean)).catch(() => null))) failures.push(`broken local reference: ${reference}`);
}

for (const [name, content] of [["index.html", html], ["styles.css", css], ["app.js", script]]) {
  if (/C:\\Users\\|C:\/Users\//i.test(content)) failures.push(`personal path leaked into ${name}`);
}

if (failures.length) {
  console.error(`FAIL site validation (${failures.length})\n${failures.join("\n")}`);
  process.exit(1);
}

console.log(`PASS site validation: ${requiredFiles.length} required files; ${index.length} indexed knowledge records; ${localReferences.length} local references`);
