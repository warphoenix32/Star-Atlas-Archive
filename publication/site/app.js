const dialog = document.querySelector(".library-dialog");
const portalForm = document.querySelector(".portal-search");
const portalQuery = document.querySelector("#portal-query");
const libraryForm = document.querySelector(".library-search");
const libraryQuery = document.querySelector("#library-query");
const resultsList = document.querySelector("#results-list");
const resultsCount = document.querySelector("#results-count");
const emptyState = document.querySelector("#empty-state");
const filters = document.querySelector("#category-filters");
const closeButton = document.querySelector(".dialog-close");
const menuToggle = document.querySelector(".menu-toggle");
const primaryMenu = document.querySelector(".primary-menu");

const CATEGORY_LABELS = {
  all: "All collections",
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
};

let records = [];
let activeCategory = "all";
let activeQuery = "";
let previousFocus = null;

function normalize(value = "") {
  return value
    .toLowerCase()
    .normalize("NFKD")
    .replace(/[\u0300-\u036f]/g, "")
    .replace(/[^a-z0-9]+/g, " ")
    .trim();
}

function scoreRecord(record, query) {
  if (!query) return record.featured ? 8 : 1;
  const tokens = normalize(query).split(" ").filter(Boolean);
  const title = normalize(record.title);
  const summary = normalize(record.summary);
  const keywords = normalize(record.keywords.join(" "));
  const category = normalize(record.categoryLabel);

  return tokens.reduce((score, token) => {
    if (title === token) return score + 20;
    if (title.startsWith(token)) score += 12;
    else if (title.includes(token)) score += 8;
    if (keywords.includes(token)) score += 4;
    if (category.includes(token)) score += 3;
    if (summary.includes(token)) score += 2;
    return score;
  }, 0);
}

function matchingRecords() {
  return records
    .filter((record) => activeCategory === "all" || record.category === activeCategory)
    .map((record) => ({ record, score: scoreRecord(record, activeQuery) }))
    .filter(({ score }) => !activeQuery || score > 0)
    .sort((a, b) => b.score - a.score || a.record.title.localeCompare(b.record.title))
    .slice(0, activeQuery ? 30 : 18)
    .map(({ record }) => record);
}

function renderResults() {
  const matches = matchingRecords();
  const collection = CATEGORY_LABELS[activeCategory] || "Collection";
  resultsCount.textContent = `${matches.length} ${matches.length === 1 ? "record" : "records"} shown · ${collection}`;
  resultsList.replaceChildren();
  emptyState.hidden = matches.length !== 0;

  matches.forEach((record) => {
    const item = document.createElement("li");
    item.className = "result-card";
    item.innerHTML = `
      <a href="${record.url}" target="_blank" rel="noopener noreferrer">
        <div>
          <h4>${escapeHtml(record.title)}</h4>
          <p>${escapeHtml(record.summary)}</p>
        </div>
        <div class="result-card__meta">
          <span>${escapeHtml(record.categoryLabel)}</span>
          <span class="result-card__arrow" aria-hidden="true">↗</span>
        </div>
      </a>`;
    resultsList.append(item);
  });
}

function escapeHtml(value) {
  return value.replace(/[&<>'"]/g, (character) => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    "'": "&#39;",
    '"': "&quot;",
  })[character]);
}

function renderFilters() {
  const counts = records.reduce((values, record) => {
    values[record.category] = (values[record.category] || 0) + 1;
    return values;
  }, { all: records.length });

  filters.replaceChildren();
  Object.entries(CATEGORY_LABELS)
    .filter(([category]) => counts[category])
    .forEach(([category, label]) => {
      const button = document.createElement("button");
      button.type = "button";
      button.dataset.category = category;
      button.setAttribute("aria-pressed", String(category === activeCategory));
      button.innerHTML = `<span>${label}</span><small>${counts[category]}</small>`;
      button.addEventListener("click", () => {
        activeCategory = category;
        [...filters.querySelectorAll("button")].forEach((item) => {
          item.setAttribute("aria-pressed", String(item.dataset.category === category));
        });
        renderResults();
      });
      filters.append(button);
    });
}

function openLibrary({ query = "", category = "all" } = {}) {
  previousFocus = document.activeElement;
  activeQuery = query;
  activeCategory = CATEGORY_LABELS[category] ? category : "all";
  libraryQuery.value = query;
  renderFilters();
  renderResults();
  if (!dialog.open) dialog.showModal();
  document.body.style.overflow = "hidden";
  window.setTimeout(() => libraryQuery.focus(), 60);
  closeMenu();
}

function closeLibrary() {
  if (!dialog.open) return;
  dialog.close();
  document.body.style.overflow = "";
  if (previousFocus instanceof HTMLElement) previousFocus.focus();
}

function closeMenu() {
  primaryMenu.dataset.open = "false";
  menuToggle.setAttribute("aria-expanded", "false");
}

portalForm.addEventListener("submit", (event) => {
  event.preventDefault();
  openLibrary({ query: portalQuery.value.trim() });
});

libraryForm.addEventListener("submit", (event) => event.preventDefault());
libraryQuery.addEventListener("input", () => {
  activeQuery = libraryQuery.value.trim();
  renderResults();
});

document.querySelectorAll("[data-library-mode]").forEach((button) => {
  button.addEventListener("click", () => openLibrary({ category: button.dataset.libraryMode }));
});

document.querySelectorAll("[data-library-query]").forEach((button) => {
  button.addEventListener("click", () => openLibrary({ query: button.dataset.libraryQuery }));
});

closeButton.addEventListener("click", closeLibrary);
dialog.addEventListener("click", (event) => {
  if (event.target === dialog) closeLibrary();
});
dialog.addEventListener("close", () => {
  document.body.style.overflow = "";
});

menuToggle.addEventListener("click", () => {
  const open = primaryMenu.dataset.open !== "true";
  primaryMenu.dataset.open = String(open);
  menuToggle.setAttribute("aria-expanded", String(open));
});

document.addEventListener("keydown", (event) => {
  if (event.key === "Escape" && dialog.open) closeLibrary();
  if (event.key === "/" && !event.ctrlKey && !event.metaKey && document.activeElement?.tagName !== "INPUT") {
    event.preventDefault();
    if (dialog.open) libraryQuery.focus();
    else openLibrary();
  }
});

async function loadIndex() {
  try {
    const response = await fetch("assets/library-index.json");
    if (!response.ok) throw new Error(`Index request failed: ${response.status}`);
    records = await response.json();
    renderFilters();
    renderResults();
  } catch (error) {
    resultsCount.textContent = "The library index could not be loaded.";
    emptyState.hidden = false;
    emptyState.textContent = "The entrance remains available, but search requires the generated repository index.";
    console.error(error);
  }
}

loadIndex();
