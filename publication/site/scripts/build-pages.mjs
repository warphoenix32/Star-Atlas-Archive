import { promises as fs } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const scriptDirectory = path.dirname(fileURLToPath(import.meta.url));
const site = path.resolve(scriptDirectory, "..");
const repository = path.resolve(site, "..", "..");
const output = path.join(site, "dist");
const publicFiles = ["index.html", "article.html", "styles.css", "article.css", "app.js", "article.js"];

await fs.rm(output, { recursive: true, force: true });
await fs.mkdir(output, { recursive: true });

for (const file of publicFiles) {
  await fs.copyFile(path.join(site, file), path.join(output, file));
}
await fs.cp(path.join(site, "assets"), path.join(output, "assets"), { recursive: true });
await fs.cp(path.join(repository, "knowledge"), path.join(output, "content"), { recursive: true });
await fs.writeFile(path.join(output, ".nojekyll"), "", "utf8");

const records = JSON.parse(await fs.readFile(path.join(output, "assets", "library-index.json"), "utf8"));
console.log(`Built GitHub Pages Library with ${records.length} indexed knowledge records.`);
