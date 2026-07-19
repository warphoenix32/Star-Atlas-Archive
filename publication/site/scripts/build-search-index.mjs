import { promises as fs } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const scriptDirectory = path.dirname(fileURLToPath(import.meta.url));
const siteDirectory = path.resolve(scriptDirectory, "..");
const repositoryRoot = path.resolve(siteDirectory, "..", "..");
const knowledgeRoot = path.join(repositoryRoot, "knowledge");
const outputPath = path.join(siteDirectory, "assets", "library-index.json");
const checkOnly = process.argv.includes("--check");
const githubBase = "https://github.com/warphoenix32/Star-Atlas-Archive/blob/main/";

const categoryLabels = {
  timeline: "Timeline",
  governance: "Governance",
  gameplay: "Products & gameplay",
  economy: "Economy",
  organizations: "Organizations",
  people: "People",
  media: "Media & sources",
  technology: "Technology",
  events: "Events",
  lore: "Lore",
  guilds: "Guilds",
  controversies: "Controversies",
  research: "Research",
  index: "Indexes",
  root: "Library guide",
};

const featuredTitles = new Set([
  "Master Timeline",
  "Governance Constitutional History",
  "Product Registry",
  "Institutional Overview",
  "Official Communications Chronology",
  "Star Atlas Historical Periodization",
]);

async function markdownFiles(directory) {
  const entries = await fs.readdir(directory, { withFileTypes: true });
  const nested = await Promise.all(entries
    .sort((a, b) => a.name.localeCompare(b.name))
    .map(async (entry) => {
      const entryPath = path.join(directory, entry.name);
      if (entry.isDirectory()) return markdownFiles(entryPath);
      return entry.isFile() && entry.name.endsWith(".md") ? [entryPath] : [];
    }));
  return nested.flat();
}

function cleanMarkdown(value) {
  return value
    .replace(/<!--.*?-->/gs, " ")
    .replace(/\[([^\]]+)\]\([^)]+\)/g, "$1")
    .replace(/[`*_>#|]/g, " ")
    .replace(/\s+/g, " ")
    .trim();
}

function extractTitle(text, fallback) {
  return text.match(/^#\s+(.+)$/m)?.[1].trim() || fallback;
}

function extractSummary(text) {
  const withoutFrontMatter = text.replace(/^---\s*[\s\S]*?\s*---\s*/, "");
  const paragraphs = withoutFrontMatter.split(/\n\s*\n/)
    .map(cleanMarkdown)
    .filter((paragraph) => paragraph && !paragraph.startsWith("#") && paragraph.length > 45);
  const summary = paragraphs[0] || "A reviewed entry in the Star Atlas historical knowledge collection.";
  return summary.length > 220 ? `${summary.slice(0, 217).trimEnd()}…` : summary;
}

function extractKeywords(text, title) {
  const headings = [...text.matchAll(/^#{2,4}\s+(.+)$/gm)].map((match) => cleanMarkdown(match[1]));
  return [...new Set([title, ...headings].join(" ").split(/[^A-Za-z0-9-]+/).filter((word) => word.length > 2))].slice(0, 40);
}

const files = await markdownFiles(knowledgeRoot);
const records = [];

for (const file of files) {
  const text = await fs.readFile(file, "utf8");
  const relativePath = path.relative(repositoryRoot, file).split(path.sep).join("/");
  const relativeKnowledgePath = path.relative(knowledgeRoot, file).split(path.sep).join("/");
  const firstSegment = relativeKnowledgePath.split("/")[0];
  const category = firstSegment.endsWith(".md") ? "root" : firstSegment;
  const fallback = path.basename(file, ".md").replaceAll("-", " ");
  const title = extractTitle(text, fallback);
  records.push({
    id: relativePath.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, ""),
    title,
    summary: extractSummary(text),
    category,
    categoryLabel: categoryLabels[category] || category.replaceAll("-", " "),
    keywords: extractKeywords(text, title),
    path: relativePath,
    url: `${githubBase}${relativePath.split("/").map(encodeURIComponent).join("/")}`,
    featured: featuredTitles.has(title),
  });
}

records.sort((a, b) => a.category.localeCompare(b.category) || a.title.localeCompare(b.title));
const rendered = `${JSON.stringify(records, null, 2)}\n`;

if (checkOnly) {
  const existing = await fs.readFile(outputPath, "utf8").catch(() => "");
  if (existing !== rendered) {
    console.error("library-index.json is stale; run npm run index");
    process.exit(1);
  }
  console.log(`PASS search index fixed point: ${records.length} records`);
} else {
  await fs.mkdir(path.dirname(outputPath), { recursive: true });
  await fs.writeFile(outputPath, rendered, "utf8");
  console.log(`Wrote ${records.length} records to ${path.relative(repositoryRoot, outputPath)}`);
}
