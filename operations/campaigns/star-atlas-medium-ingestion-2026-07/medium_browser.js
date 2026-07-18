#!/usr/bin/env node
"use strict";

const crypto = require("crypto");
const fs = require("fs");
const path = require("path");
const { chromium } = require("playwright");

function usage() {
  process.stderr.write(
    "Usage: node medium_browser.js <url> <metadata.json> <rendered.html> [scroll|single]\n",
  );
  process.exit(2);
}

function chromeExecutable() {
  const candidates = [
    process.env.MEDIUM_CHROME,
    process.env.CHROME_PATH,
    "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
    "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe",
  ].filter(Boolean);
  return candidates.find((candidate) => fs.existsSync(candidate));
}

async function main() {
  const [, , url, metadataPath, htmlPath, mode = "single"] = process.argv;
  if (!url || !metadataPath || !htmlPath) usage();

  const executablePath = chromeExecutable();
  const launch = {
    headless: true,
    args: ["--no-sandbox", "--disable-dev-shm-usage"],
  };
  if (executablePath) launch.executablePath = executablePath;

  const browser = await chromium.launch(launch);
  try {
    const page = await browser.newPage({
      userAgent: "Mozilla/5.0 (compatible; StarAtlasArchive/1.0; +https://github.com/warphoenix32/Star-Atlas-Archive)",
      viewport: { width: 1440, height: 1200 },
    });
    const response = await page.goto(url, {
      waitUntil: "domcontentloaded",
      timeout: 90000,
    });
    await page.waitForTimeout(1500);

    let stablePasses = 0;
    let previousPostCount = -1;
    let scrollPasses = 0;
    if (mode === "scroll") {
      while (stablePasses < 2 && scrollPasses < 80) {
        const postCount = await page.evaluate(() => {
          const ids = new Set();
          for (const anchor of document.querySelectorAll("a[href]")) {
            const href = anchor.href || "";
            const match = href.match(/(?:\/p\/|[-/])([0-9a-f]{12})(?:[?#/]|$)/i);
            if (match) ids.add(match[1].toLowerCase());
          }
          return ids.size;
        });
        stablePasses = postCount === previousPostCount ? stablePasses + 1 : 0;
        previousPostCount = postCount;
        scrollPasses += 1;
        await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
        await page.waitForTimeout(1200);
      }
    }

    const pageData = await page.evaluate(() => {
      const anchors = Array.from(document.querySelectorAll("a[href]")).map((anchor) => ({
        href: anchor.href,
        text: (anchor.textContent || "").replace(/\s+/g, " ").trim(),
      }));
      const metadata = {};
      for (const node of document.querySelectorAll("meta[name], meta[property]")) {
        const key = node.getAttribute("property") || node.getAttribute("name");
        if (key && node.content && !metadata[key]) metadata[key] = node.content;
      }
      const canonical = document.querySelector('link[rel="canonical"]')?.href || null;
      const jsonLd = Array.from(document.querySelectorAll('script[type="application/ld+json"]'))
        .map((node) => node.textContent || "")
        .filter(Boolean);
      return {
        anchors,
        canonical,
        json_ld: jsonLd,
        metadata,
        title: document.title,
        body_text_length: document.body?.innerText?.length || 0,
      };
    });
    const html = await page.content();
    const postIds = Array.from(
      new Set(
        pageData.anchors
          .map(({ href }) => href.match(/(?:\/p\/|[-/])([0-9a-f]{12})(?:[?#/]|$)/i)?.[1]?.toLowerCase())
          .filter(Boolean),
      ),
    ).sort();

    const output = {
      requested_url: url,
      final_url: page.url(),
      http_status: response ? response.status() : null,
      title: pageData.title,
      canonical_url: pageData.canonical,
      metadata: pageData.metadata,
      json_ld: pageData.json_ld,
      anchors: pageData.anchors,
      post_ids: postIds,
      final_item_count: postIds.length,
      scroll_passes: scrollPasses,
      stable_passes: stablePasses,
      body_text_length: pageData.body_text_length,
      rendered_html_sha256: crypto.createHash("sha256").update(html, "utf8").digest("hex"),
    };

    fs.mkdirSync(path.dirname(metadataPath), { recursive: true });
    fs.mkdirSync(path.dirname(htmlPath), { recursive: true });
    fs.writeFileSync(htmlPath, html, "utf8");
    fs.writeFileSync(metadataPath, JSON.stringify(output, null, 2) + "\n", "utf8");
  } finally {
    await browser.close();
  }
}

main().catch((error) => {
  process.stderr.write(`${error.stack || error}\n`);
  process.exit(1);
});
