import { createServer } from "node:http";
import { promises as fs } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const knowledge = path.resolve(root, "..", "..", "knowledge");
const port = Number(process.env.PORT || 4173);
const types = { ".html": "text/html; charset=utf-8", ".css": "text/css; charset=utf-8", ".js": "text/javascript; charset=utf-8", ".json": "application/json; charset=utf-8", ".md": "text/markdown; charset=utf-8", ".webp": "image/webp" };

createServer(async (request, response) => {
  const requested = decodeURIComponent(new URL(request.url, `http://${request.headers.host}`).pathname);
  const relative = requested === "/" ? "index.html" : requested.replace(/^\/+/, "");
  const contentRequest = relative.startsWith("content/");
  const base = contentRequest ? knowledge : root;
  const localPath = contentRequest ? relative.slice("content/".length) : relative;
  const target = path.resolve(base, localPath);
  if (target !== base && !target.startsWith(`${base}${path.sep}`)) {
    response.writeHead(403).end("Forbidden");
    return;
  }
  try {
    const content = await fs.readFile(target);
    response.writeHead(200, { "Content-Type": types[path.extname(target)] || "application/octet-stream" });
    response.end(content);
  } catch {
    response.writeHead(404).end("Not found");
  }
}).listen(port, "127.0.0.1", () => {
  console.log(`Star Atlas Library: http://127.0.0.1:${port}`);
});
