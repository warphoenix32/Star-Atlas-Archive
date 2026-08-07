import { promises as fs } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const scriptDirectory = path.dirname(fileURLToPath(import.meta.url));
const siteDirectory = path.resolve(scriptDirectory, "..");
const repositoryRoot = path.resolve(siteDirectory, "..", "..");
const knowledgeRoot = path.join(repositoryRoot, "knowledge");
const manifestPath = path.join(repositoryRoot, "publication", "manifests", "publication-manifest.json");
const outputPath = path.join(siteDirectory, "assets", "library-index.json");
const checkOnly = process.argv.includes("--check");
const githubBase = "https://github.com/warphoenix32/Star-Atlas-Archive/blob/main/";

const categoryLabels = {
  orientation: "Start here",
  timeline: "Timeline",
  governance: "Governance",
  gameplay: "Products & gameplay",
  economy: "Economy",
  organizations: "Organizations",
  people: "People",
  community: "Community",
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

const topicCategories = {
  Orientation: "orientation",
  Gameplay: "gameplay",
  Lore: "lore",
  Community: "community",
  "Community Media": "media",
  Technology: "technology",
  Governance: "governance",
  Treasury: "economy",
  Economy: "economy",
  Organizations: "organizations",
  Communications: "media",
};

const featuredKnowledgeTitles = new Set([
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

function recordId(prefix, value) {
  return `${prefix}-${value}`.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
}

const manifest = JSON.parse(await fs.readFile(manifestPath, "utf8"));
const publishedEntries = manifest.entries
  .filter((entry) => manifest.build_policy.include_statuses.includes(entry.status))
  .sort((a, b) => a.publication_id.localeCompare(b.publication_id));

const records = publishedEntries.map((entry) => {
  const category = topicCategories[entry.presentation.primary_topic] || "root";
  const id = recordId("publication", entry.slug);
  return {
    id,
    publicationId: entry.publication_id,
    title: entry.title,
    summary: entry.presentation.description || entry.presentation.summary,
    category,
    categoryLabel: categoryLabels[category] || entry.presentation.primary_topic,
    keywords: [...new Set([
      entry.title,
      entry.presentation.primary_topic,
      ...entry.presentation.related_topics,
    ].join(" ").split(/[^A-Za-z0-9-]+/).filter((word) => word.length > 2))].slice(0, 40),
    path: entry.content_path,
    contentPath: entry.content_path,
    url: `article.html?id=${encodeURIComponent(id)}`,
    sourceUrl: `${githubBase}${entry.content_path.split("/").map(encodeURIComponent).join("/")}`,
    featured: true,
    layer: "library",
    recordType: "published-article",
  };
});

for (const file of await markdownFiles(knowledgeRoot)) {
  const text = await fs.readFile(file, "utf8");
  const relativePath = path.relative(repositoryRoot, file).split(path.sep).join("/");
  const relativeKnowledgePath = path.relative(knowledgeRoot, file).split(path.sep).join("/");
  const firstSegment = relativeKnowledgePath.split("/")[0];
  const category = firstSegment.endsWith(".md") ? "root" : firstSegment;
  const fallback = path.basename(file, ".md").replaceAll("-", " ");
  const title = extractTitle(text, fallback);
  const id = recordId("knowledge", relativePath);
  records.push({
    id,
    title,
    summary: extractSummary(text),
    category,
    categoryLabel: categoryLabels[category] || category.replaceAll("-", " "),
    keywords: extractKeywords(text, title),
    path: relativePath,
    contentPath: relativePath,
    url: `article.html?id=${encodeURIComponent(id)}`,
    sourceUrl: `${githubBase}${relativePath.split("/").map(encodeURIComponent).join("/")}`,
    featured: featuredKnowledgeTitles.has(title),
    layer: "archive",
    recordType: "knowledge-record",
  });
}

records.sort((a, b) =>
  a.layer.localeCompare(b.layer)
  || Number(b.featured) - Number(a.featured)
  || a.category.localeCompare(b.category)
  || a.title.localeCompare(b.title));
const rendered = `${JSON.stringify(records, null, 2)}\n`;

if (checkOnly) {
  const existing = await fs.readFile(outputPath, "utf8").catch(() => "");
  if (existing !== rendered) {
    console.error("library-index.json is stale; run npm run index");
    process.exit(1);
  }
  console.log(`PASS search index fixed point: ${publishedEntries.length} published articles; ${records.length - publishedEntries.length} archive records`);
} else {
  await fs.mkdir(path.dirname(outputPath), { recursive: true });
  await fs.writeFile(outputPath, rendered, "utf8");
  console.log(`Wrote ${publishedEntries.length} published articles and ${records.length - publishedEntries.length} archive records to ${path.relative(repositoryRoot, outputPath)}`);
}
