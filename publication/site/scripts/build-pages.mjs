import { promises as fs } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const scriptDirectory = path.dirname(fileURLToPath(import.meta.url));
const site = path.resolve(scriptDirectory, "..");
const repository = path.resolve(site, "..", "..");
const output = path.join(site, "dist");
const manifestPath = path.join(repository, "publication", "manifests", "publication-manifest.json");
const publicFiles = ["index.html", "article.html", "styles.css", "article.css", "app.js", "article.js"];

await fs.rm(output, { recursive: true, force: true });
await fs.mkdir(output, { recursive: true });

for (const file of publicFiles) {
  await fs.copyFile(path.join(site, file), path.join(output, file));
}
await fs.cp(path.join(site, "assets"), path.join(output, "assets"), { recursive: true });
await fs.cp(path.join(repository, "knowledge"), path.join(output, "content", "knowledge"), { recursive: true });

const manifest = JSON.parse(await fs.readFile(manifestPath, "utf8"));
const publishedEntries = manifest.entries.filter((entry) =>
  manifest.build_policy.include_statuses.includes(entry.status));

for (const entry of publishedEntries) {
  const source = path.join(repository, ...entry.content_path.split("/"));
  const destination = path.join(output, "content", ...entry.content_path.split("/"));
  await fs.mkdir(path.dirname(destination), { recursive: true });
  await fs.copyFile(source, destination);
}

await fs.writeFile(path.join(output, ".nojekyll"), "", "utf8");

const records = JSON.parse(await fs.readFile(path.join(output, "assets", "library-index.json"), "utf8"));
const publicRecords = records.filter((record) => record.layer === "library");
if (publicRecords.length !== publishedEntries.length) {
  throw new Error(`Public index/build mismatch: ${publicRecords.length} index records for ${publishedEntries.length} published entries.`);
}
console.log(`Built GitHub Pages Library with ${publishedEntries.length} published articles and ${records.length - publishedEntries.length} archive records.`);
