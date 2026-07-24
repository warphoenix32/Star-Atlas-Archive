const recordElement = document.querySelector(".knowledge-record");
const titleElement = document.querySelector("#record-title");
const summaryElement = document.querySelector("#record-summary");
const categoryElement = document.querySelector("#record-category");
const pathElement = document.querySelector("#record-path");
const contentElement = document.querySelector("#record-content");
const sourceLink = document.querySelector("#source-link");

let records = [];
let currentRecord = null;

function escapeHtml(value = "") {
  return value.replace(/[&<>'"]/g, (character) => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    "'": "&#39;",
    '"': "&quot;",
  })[character]);
}

function stripFrontMatter(markdown) {
  if (!markdown.startsWith("---")) return markdown;
  const end = markdown.indexOf("\n---", 3);
  if (end < 0) return markdown;
  return markdown.slice(end + 4).trim();
}

function slug(value) {
  return value.toLowerCase().replace(/<[^>]+>/g, "").replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
}

function safeHref(rawHref) {
  const href = rawHref.trim().replace(/^<|>$/g, "");
  if (/^(https?:|mailto:)/i.test(href) || href.startsWith("#")) return href;

  const [pathPart, fragment = ""] = href.split("#", 2);
  if (!pathPart) return fragment ? `#${encodeURIComponent(fragment)}` : "#";

  const base = new URL(`https://library.invalid/${currentRecord.path}`);
  const resolved = new URL(pathPart, base).pathname.replace(/^\//, "");
  const linkedRecord = records.find((record) => record.path.toLowerCase() === decodeURIComponent(resolved).toLowerCase());
  if (linkedRecord) return `${linkedRecord.url}${fragment ? `#${slug(fragment)}` : ""}`;
  if (/^(archive|graph|knowledge|operations|publication)\//.test(resolved)) {
    return `https://github.com/warphoenix32/Star-Atlas-Archive/blob/main/${resolved.split("/").map(encodeURIComponent).join("/")}`;
  }
  return "#";
}

function renderInline(value) {
  const tokens = [];
  let prepared = value.replace(/`([^`]+)`/g, (_, code) => {
    const token = `@@TOKEN${tokens.length}@@`;
    tokens.push(`<code>${escapeHtml(code)}</code>`);
    return token;
  });
  prepared = prepared.replace(/\[([^\]]+)\]\(([^)]+)\)/g, (_, label, href) => {
    const token = `@@TOKEN${tokens.length}@@`;
    const destination = safeHref(href);
    const external = /^(https?:|mailto:)/i.test(destination);
    tokens.push(`<a href="${escapeHtml(destination)}"${external ? ' target="_blank" rel="noopener noreferrer"' : ""}>${escapeHtml(label)}</a>`);
    return token;
  });
  prepared = escapeHtml(prepared)
    .replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>")
    .replace(/__([^_]+)__/g, "<strong>$1</strong>")
    .replace(/(?<!\*)\*([^*]+)\*(?!\*)/g, "<em>$1</em>");
  tokens.forEach((token, index) => {
    prepared = prepared.replace(`@@TOKEN${index}@@`, token);
  });
  return prepared;
}

function tableCells(line) {
  return line.trim().replace(/^\||\|$/g, "").split("|").map((cell) => cell.trim());
}

function isBlockStart(lines, index) {
  const line = lines[index] || "";
  const next = lines[index + 1] || "";
  return !line.trim()
    || /^#{1,6}\s/.test(line)
    || /^```/.test(line)
    || /^>\s?/.test(line)
    || /^\s*[-*+]\s+/.test(line)
    || /^\s*\d+[.)]\s+/.test(line)
    || /^\s*(---+|___+|\*\*\*+)\s*$/.test(line)
    || (line.includes("|") && /^\s*\|?\s*:?-{3,}/.test(next));
}

function renderMarkdown(markdown) {
  const lines = markdown.replace(/\r\n/g, "\n").split("\n");
  const output = [];
  let index = 0;

  while (index < lines.length) {
    const line = lines[index];
    if (!line.trim()) { index += 1; continue; }

    const fence = line.match(/^```\s*([\w-]*)/);
    if (fence) {
      const code = [];
      index += 1;
      while (index < lines.length && !/^```/.test(lines[index])) code.push(lines[index++]);
      index += 1;
      output.push(`<pre><code${fence[1] ? ` class="language-${escapeHtml(fence[1])}"` : ""}>${escapeHtml(code.join("\n"))}</code></pre>`);
      continue;
    }

    const heading = line.match(/^(#{1,6})\s+(.+)$/);
    if (heading) {
      const level = heading[1].length;
      const text = renderInline(heading[2].replace(/\s+#+\s*$/, ""));
      output.push(`<h${level} id="${slug(heading[2])}">${text}</h${level}>`);
      index += 1;
      continue;
    }

    if (line.includes("|") && /^\s*\|?\s*:?-{3,}/.test(lines[index + 1] || "")) {
      const headers = tableCells(line);
      index += 2;
      const rows = [];
      while (index < lines.length && lines[index].includes("|") && lines[index].trim()) rows.push(tableCells(lines[index++]));
      output.push(`<div class="table-wrap"><table><thead><tr>${headers.map((cell) => `<th>${renderInline(cell)}</th>`).join("")}</tr></thead><tbody>${rows.map((row) => `<tr>${row.map((cell) => `<td>${renderInline(cell)}</td>`).join("")}</tr>`).join("")}</tbody></table></div>`);
      continue;
    }

    const listMatch = line.match(/^\s*([-*+]|\d+[.)])\s+(.+)$/);
    if (listMatch) {
      const ordered = /^\d/.test(listMatch[1]);
      const items = [];
      while (index < lines.length) {
        const item = lines[index].match(/^\s*([-*+]|\d+[.)])\s+(.+)$/);
        if (!item || /^\d/.test(item[1]) !== ordered) break;
        items.push(`<li>${renderInline(item[2])}</li>`);
        index += 1;
      }
      output.push(`<${ordered ? "ol" : "ul"}>${items.join("")}</${ordered ? "ol" : "ul"}>`);
      continue;
    }

    if (/^>\s?/.test(line)) {
      const quoted = [];
      while (index < lines.length && /^>\s?/.test(lines[index])) quoted.push(lines[index++].replace(/^>\s?/, ""));
      output.push(`<blockquote>${quoted.map(renderInline).join("<br>")}</blockquote>`);
      continue;
    }

    if (/^\s*(---+|___+|\*\*\*+)\s*$/.test(line)) {
      output.push("<hr>");
      index += 1;
      continue;
    }

    const paragraph = [line.trim()];
    index += 1;
    while (index < lines.length && !isBlockStart(lines, index)) paragraph.push(lines[index++].trim());
    output.push(`<p>${renderInline(paragraph.join(" "))}</p>`);
  }
  return output.join("\n");
}

function showError(message) {
  titleElement.textContent = "Record unavailable";
  summaryElement.textContent = "The requested knowledge record could not be opened.";
  contentElement.innerHTML = `<p class="record-error">${escapeHtml(message)} Return to the Library and choose another record.</p>`;
  recordElement.setAttribute("aria-busy", "false");
}

async function openRecord() {
  const requestedId = new URLSearchParams(window.location.search).get("id");
  const response = await fetch("assets/library-index.json");
  if (!response.ok) throw new Error("The Library index is unavailable.");
  records = await response.json();
  currentRecord = records.find((record) => record.id === requestedId);
  if (!currentRecord) throw new Error("This record is not present in the current Library index.");

  const knowledgePath = currentRecord.path.replace(/^knowledge\//, "");
  const contentResponse = await fetch(`content/${knowledgePath.split("/").map(encodeURIComponent).join("/")}`);
  if (!contentResponse.ok) throw new Error("The repository knowledge file could not be retrieved.");
  const markdown = stripFrontMatter(await contentResponse.text());

  document.title = `${currentRecord.title} · Star Atlas Library`;
  titleElement.textContent = currentRecord.title;
  summaryElement.textContent = currentRecord.summary;
  categoryElement.textContent = currentRecord.categoryLabel;
  pathElement.textContent = currentRecord.path.replace(/^knowledge\//, "").replace(/\.md$/, "").replaceAll("/", " · ").replaceAll("-", " ");
  sourceLink.href = currentRecord.sourceUrl;
  contentElement.innerHTML = renderMarkdown(markdown);
  recordElement.setAttribute("aria-busy", "false");
}

openRecord().catch((error) => {
  console.error(error);
  showError(error.message);
});
