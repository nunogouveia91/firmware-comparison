# GitHub Copilot Instructions — firmware-comparison

## Project overview

Single-page web application for comparing firmware CSV exports. The **entire application lives in `src/comparador.html`** — one large self-contained HTML/CSS/JS file. The Flask server (`app.py`) simply serves it as a static file for local development; there is no backend logic.

**All development happens in `src/comparador.html`.**

---

## Architecture

```
app.py              → Flask: serves src/ as static files (local development only)
requirements.txt    → flask>=2.3
src/
  comparador.html   → Complete app (HTML + CSS + JS, no build step)
```

The app is a self-contained static HTML file. No build step, no npm, no compilation. Edit and refresh.

---

## ⚠️ Critical pitfalls — READ BEFORE EDITING

These are the most common mistakes that break the entire `<script>` block and force a `git checkout` revert:

1. **Stray backtick inside a template literal** — a single unmatched backtick inside any JS template string breaks the entire `<script>` block silently. Always verify backticks are balanced after every edit.
2. **`const` used before declaration** — functions are long; placing a `const` inside an `else` branch that is referenced by an earlier `if` block causes `ReferenceError`. Move declarations to the top of their scope.
3. **Duplicate `const` in the same scope** — occurs when copy-pasting code blocks; rename or remove duplicates.
4. **Delta = null when baseline is 0** — `fw2avg = 0` makes `(a1 - a2) / |a2|` divide by zero → `null`. Always use the `computeDelta()` helper (returns sentinel `999999`, displayed as `+∞`).
5. **Indicators disappearing** — `availInds` filtering must keep indicators that have data in **at least one** FW, not require data in both AND a non-zero delta.

---

## Coding conventions

- **No build step** — plain ES2020+ JS inside `<script>` tags; no modules, no bundler
- **No external state management** — global variables (`S`, `CFG`, `fw1Label`, etc.)
- **Re-render pattern** — most UI functions fully replace a root container with `root.innerHTML = ...`
- **Template literals** — all HTML generation uses template literals; always use `esc()` to escape any user-controlled string
- **`const` scoping** — avoid declaring `const` before its first use (no hoisting with `const`/`let`)
- **Avoid duplicate `const`** in the same scope — a common error when editing large template literal blocks

---

## Data model

- `S.fw1[]` / `S.fw2[]` — arrays of loaded file objects `{ name, headers[], rows[], averages, included }`
- `fw1Label` / `fw2Label` — custom display names for each group
- `CFG` — global config object (thresholds, clusters, weights) persisted via IndexedDB
- `S.fw1` = **FW-B (Upgrade / Depois)** — the new firmware being evaluated
- `S.fw2` = **FW-A (Control / Antes)** — the reference / before period

### Terminology

| Internal | UI label  | Meaning                            |
| -------- | --------- | ---------------------------------- |
| `fw1`    | FW-B      | Upgrade / Depois (new firmware)    |
| `fw2`    | FW-A      | Control / Antes (reference)        |

---

## Key functions

- `classify(pct)` — maps a % delta to level/label/color via `CFG.failThresholds`; positive pct = FW-B **worse** than FW-A
- `computeDelta(a1, a2)` — safe delta calculation; returns `999999` when `a2 === 0`
- `isEpochMs(v)` — detects epoch milliseconds (`9e11 < v < 5e12`)
- `parseTs(v)` — parses epoch ms, ISO strings, and PT locale `DD/MM/YYYY, HH:MM`
- `getTsCol(f)` — finds the timestamp column; result cached on `f._tsColCache`
- `esc(str)` — HTML-escapes user strings for safe injection into template literals
- `renderLists()` — re-renders file lists in both the sidebar and upload tab
- `refreshAll()` — full UI refresh after state change
- `toggleInclude(fw, idx, val)` — sets `S[fw][idx].included` and calls `refreshAll()`

---

## Tabs

- **Carregar Dados** — file upload; FW-A (Control/Antes) on left, FW-B (Upgrade/Depois) on right
- **Comparação → Comparação Direta** — side-by-side average comparison with classification
- **Comparação → Comparação Temporal** — time-series chart with position-based alignment (`alignedPairs`)
- **Evolução** — per-indicator statistical metrics (score, growth, rate, var.abs, std dev, signal)
- **Dados** — raw CSV browser
- **Definições** — thresholds, clusters, saved data management

---

## Persistence (IndexedDB via `IDB` helper)

- `CFG_KEY` — app config (thresholds, clusters, weights) — also mirrored in `localStorage` for legacy
- `DS_KEY` — saved firmware datasets
- `AN_KEY` — saved full analyses
- All storage is **local to each user's browser** — no server-side persistence

---

## External dependencies (CDN, no local install)

- `chart.js@4.4.3` — charts
- `jszip@3.10.1` — ZIP export

---

## Checkpoint / versioning workflow

**Always commit before large structural changes:**

```bash
git add -A && git commit -m "checkpoint: description" && git push
```

To revert `src/comparador.html` to a specific commit:

```bash
git checkout <hash> -- src/comparador.html
```

> Tip: keep commits small and frequent so checkouts only lose a small amount of work.
