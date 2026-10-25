// Shared helpers for the roadmap pages (index.html = highway map, tasks.html = task board).
// Reads window.ROADMAP_DATA (or fallback) from roadmap.js and exposes window.RM.
(() => {
  const data = window.ROADMAP_DATA || window.PROJECT_ROADMAP || window.COMPLETIONIST_ROADMAP;

  // Day/night and Palette themes
  const THEME_KEY = "roadmap:theme";
  const PALETTE_KEY = "roadmap:palette";

  try {
    const t = localStorage.getItem(THEME_KEY);
    if (t === "light" || t === "dark") document.documentElement.dataset.theme = t;
    const p = localStorage.getItem(PALETTE_KEY);
    if (p) document.documentElement.dataset.palette = p;
  } catch {}

  function isDark() {
    const t = document.documentElement.dataset.theme;
    return t ? t === "dark" : matchMedia("(prefers-color-scheme: dark)").matches;
  }

  function bindThemeButton(btn) {
    if (!btn) return;
    const paint = () => {
      const dark = isDark();
      btn.setAttribute("aria-pressed", String(dark));
      btn.innerHTML = dark
        ? `<svg viewBox="0 0 16 16" width="14" height="14" aria-hidden="true"><path d="M13.5 10.2A6 6 0 0 1 5.8 2.5a6 6 0 1 0 7.7 7.7Z" fill="currentColor"/></svg><span>Night</span>`
        : `<svg viewBox="0 0 16 16" width="14" height="14" aria-hidden="true"><circle cx="8" cy="8" r="3.2" fill="currentColor"/><path d="M8 1v2M8 13v2M1 8h2M13 8h2M3 3l1.4 1.4M11.6 11.6 13 13M3 13l1.4-1.4M11.6 4.4 13 3" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg><span>Day</span>`;
    };
    btn.addEventListener("click", () => {
      const next = isDark() ? "light" : "dark";
      document.documentElement.dataset.theme = next;
      try { localStorage.setItem(THEME_KEY, next); } catch {}
      paint();
      document.dispatchEvent(new CustomEvent("rm:theme"));
    });
    matchMedia("(prefers-color-scheme: dark)").addEventListener("change", () => {
      paint();
      document.dispatchEvent(new CustomEvent("rm:theme"));
    });
    paint();
  }

  function bindPaletteSelector(sel) {
    if (!sel) return;
    const cur = document.documentElement.dataset.palette || "evergreen";
    sel.value = cur;
    sel.addEventListener("change", () => {
      const val = sel.value;
      document.documentElement.dataset.palette = val;
      try { localStorage.setItem(PALETTE_KEY, val); } catch {}
      document.dispatchEvent(new CustomEvent("rm:theme"));
    });
  }

  const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c]);
  const rich = (s) => esc(s).replace(/`([^`]+)`/g, "<code>$1</code>");
  const words = (s) => String(s || "").split(/\s+/).filter(Boolean).length;
  const parseVer = (v) => String(v).split(".").map(Number);
  const cmpVer = (a, b) => { const x = parseVer(a), y = parseVer(b); return x[0] - y[0] || x[1] - y[1] || x[2] - y[2]; };
  const tierOf = (v) => { const [, minor, patch] = parseVer(v); return patch ? "patch" : minor ? "minor" : "major"; };
  const fmtDate = (iso) => { if (!iso) return ""; const [y, m, d] = iso.split("-").map(Number); return new Date(y, m - 1, d).toLocaleDateString("en-US", { year: "numeric", month: "short", day: "numeric" }); };

  const STATUS = {
    doing: { label: "Doing", rank: 0 },
    unverified: { label: "Unverified", rank: 1 },
    next: { label: "Next", rank: 2 },
    blocked: { label: "Blocked", rank: 3 },
    todo: { label: "To do", rank: 4 },
    done: { label: "Done", rank: 5 },
    dropped: { label: "Dropped", rank: 6 },
  };
  const RELEASE_STATUS = { released: "Released", next: "Up next", planned: "Planned" };
  const MS_STATUS = { active: "Active", done: "Done", planned: "Planned" };

  if (!data) {
    window.RM = { data: null, bindThemeButton, bindPaletteSelector, esc, rich };
    return;
  }

  const highways = data.highways || [];
  const hwById = Object.fromEntries(highways.map((h) => [h.id, h]));
  const hwOfArea = {};
  for (const h of highways) for (const a of h.areas || []) hwOfArea[a] = h;

  const DEFAULT_PALETTE_COLORS = [
    "#0B6E4B", "#5E3BA3", "#0CA1A7", "#D97706", "#2563EB", "#DC2626", "#7C3AED", "#059669"
  ];

  // Dynamically register --hw-<id> CSS variables for any user-defined highways
  try {
    const styleEl = document.createElement("style");
    let cssVars = ":root {\n";
    highways.forEach((h, idx) => {
      const c = h.color || DEFAULT_PALETTE_COLORS[idx % DEFAULT_PALETTE_COLORS.length];
      cssVars += `  --hw-${h.id}: ${c};\n`;
    });
    cssVars += "}\n";
    styleEl.textContent = cssVars;
    document.head.appendChild(styleEl);
  } catch {}

  const hwColor = (id) => {
    const h = hwById[id];
    if (h && h.color) return h.color;
    const idx = highways.findIndex((item) => item.id === id);
    const fallback = idx >= 0 ? DEFAULT_PALETTE_COLORS[idx % DEFAULT_PALETTE_COLORS.length] : "#0B6E4B";
    return `var(--hw-${id}, ${fallback})`;
  };

  const hwOpenAt = (h, version) => !h.opens || cmpVer(version, h.opens) >= 0;

  const tasks = (data.tasks || []).map((t) => ({ ...t, stories: t.stories || [], hw: hwOfArea[t.area] || null }));
  const releaseByVersion = Object.fromEntries((data.releases || []).map((r) => [r.version, r]));
  const releasePlans = data.releasePlans || {};

  const groups = (data.releases || []).filter((r) => releasePlans[r.version]).map((r) => {
    const plan = releasePlans[r.version] || {};
    return {
      ...plan,
      id: r.version,
      version: r.version,
      release: r,
      status: r.status === "released" ? "done" : r.version === data.activeRelease ? "active" : "planned",
      tasks: tasks.filter((t) => t.targetRelease === r.version),
    };
  });
  const groupByVersion = Object.fromEntries(groups.map((g) => [g.version, g]));
  for (const t of tasks) {
    t.ms = groupByVersion[t.targetRelease] || { id: t.targetRelease, title: releaseByVersion[t.targetRelease]?.title || t.targetRelease };
  }

  const live = (list) => list.filter((t) => t.status !== "dropped");
  const progress = (list) => {
    const l = live(list);
    return {
      done: l.filter((t) => t.status === "done").length,
      active: l.filter((t) => t.status === "doing" || t.status === "unverified" || t.status === "next" || t.status === "blocked").length,
      total: l.length,
    };
  };

  const highwaysOf = (r) => {
    if (Array.isArray(r.highways) && r.highways.length) return r.highways;
    const own = tasks.filter((t) => (r.status === "released" ? t.shippedIn === r.version : t.targetRelease === r.version) && t.status !== "dropped");
    const used = new Set(own.map((t) => t.hw?.id).filter(Boolean));
    if (!used.size && r.status === "released" && tierOf(r.version) === "major") {
      return highways.filter((h) => hwOpenAt(h, r.version)).map((h) => h.id);
    }
    return highways.filter((h) => used.has(h.id)).map((h) => h.id);
  };

  window.RM = {
    data,
    highways,
    hwById,
    hwOfArea,
    hwColor,
    hwOpenAt,
    highwaysOf,
    tasks,
    releases: data.releases || [],
    releaseByVersion,
    releasePlans,
    groups,
    groupByVersion,
    live,
    progress,
    parseVer,
    cmpVer,
    tierOf,
    fmtDate,
    esc,
    rich,
    words,
    STATUS,
    RELEASE_STATUS,
    MS_STATUS,
    bindThemeButton,
    bindPaletteSelector,
  };
})();
