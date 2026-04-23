# AGENTS.md — AI Instructions for firmware-comparison

## Project overview

Single-page web application for comparing firmware CSV exports. The entire application lives in **`src/comparador.html`** — one large self-contained HTML/CSS/JS file. The Flask server (`app.py`) simply serves it as a static file; there is no backend logic.

---

## Architecture

```
app.py              → Flask: serves src/ as static files (local development only)
requirements.txt    → flask>=2.3
src/
  comparador.html   → Complete app (HTML + CSS + JS, no build step)
uploads/            → Not used at runtime (legacy folder)
```

**All development happens in `src/comparador.html`.**

The app is a self-contained static HTML file. Flask is only needed for local development. For online deployment, any static hosting service (GitHub Pages, Netlify, Cloudflare Pages) works — no backend required.

---

## Running locally

```bash
pip install -r requirements.txt
python app.py
# → http://localhost:5000
```

No build step, no npm, no compilation. Edit and refresh.

---

## Key concepts

### Data model
- `S.fw1[]` / `S.fw2[]` — arrays of loaded file objects `{ name, headers[], rows[], averages, included }`
- `fw1Label` / `fw2Label` — custom names for each group (FW-B = Upgrade/Depois, FW-A = Control/Antes)
- `CFG` — global config object (thresholds, clusters, weights) persisted via IndexedDB
- `S.fw1` = **FW-B (Upgrade / Depois)**, `S.fw2` = **FW-A (Control / Antes)**

### Terminology
| Internal | UI label | Meaning |
|---|---|---|
| `fw1` | FW-B | Upgrade / Depois (the new firmware being evaluated) |
| `fw2` | FW-A | Control / Antes (the reference / before period) |
| `unitsUpgrade` | Upgrade / Depois units | Device count for FW-B |
| `unitsControl` | Control / Antes units | Device count for FW-A |

### Tabs
- **Carregar Dados** — file upload; FW-A (Control/Antes) on left, FW-B (Upgrade/Depois) on right
- **Comparação → Comparação Direta** — side-by-side average comparison with classification
- **Comparação → Comparação Temporal** — time-series chart; supports misaligned time periods via position-based alignment (`alignedPairs`)
- **Evolução** — per-indicator statistical metrics (score, growth, rate, var.abs, std dev, signal) with pagination
- **Dados** — raw CSV browser
- **Definições** — thresholds, clusters, saved data management

### Timestamp handling
- `isEpochMs(v)` — detects epoch milliseconds (`9e11 < v < 5e12`)
- `parseTs(v)` — parses epoch ms, ISO strings, and PT locale `DD/MM/YYYY, HH:MM`
- `getTsCol(f)` — finds the timestamp column by name (`timestamp`, `time`, `date`) or by content (≥70% epoch ms values); result cached on `f._tsColCache`

### Classification
- `classify(pct)` — maps a percentage delta to a level/label/color based on `CFG.failThresholds`
- Positive pct = FW-B **worse** than FW-A (bad for quality indicators)
- Indicator types: `acc` (accumulative, no timestamp), `avg` (average), `avg-day` (daily granularity), `avg-hour` (hourly granularity)

### Temporal comparison alignment
When FW-A and FW-B have non-overlapping time periods (before/after scenario):
- `alignedPairs[]` — array of `{label, v1ts, v2ts}` zipped by position index
- `misaligned` — true when <20% of buckets overlap between the two FWs
- Default mode: **"Cruzados"** (position-aligned) — bucket 1 of FW-B vs bucket 1 of FW-A, offset labels (`+0h`, `+4h`…)
- Toggle mode: **"Separados"** — each FW plotted on its own real timestamps on a shared X axis
- Δ% always uses `alignedPairs` regardless of toggle

### Persistence (IndexedDB via `IDB` helper)
- `CFG_KEY` — app config (thresholds, clusters, weights) — also mirrored in `localStorage` for legacy
- `DS_KEY` — saved firmware datasets
- `AN_KEY` — saved full analyses (includes all file data + config + state)
- All storage is **local to each user's browser** — no server-side persistence
- Migration: on first load, data in `localStorage` is moved to IndexedDB automatically

### Deployment (static hosting)
- The app is a pure static HTML file — no backend needed for production
- GitHub Pages: enable in repo Settings → Pages → branch `main`, folder `/src`
- Netlify / Cloudflare Pages: connect repo, publish directory `src`
- Each user's memory is isolated to their own browser (IndexedDB/localStorage)

### External dependencies (CDN, no local install)
- `chart.js@4.4.3` — charts
- `jszip@3.10.1` — ZIP export of analysis files

---

## Coding conventions

- **No build step** — plain ES2020+ JS inside `<script>` tags; no modules, no bundler
- **No external state management** — global variables (`S`, `CFG`, `fw1Label`, etc.)
- **Re-render pattern** — most UI functions are full re-renders of a root container (`root.innerHTML = ...`)
- **Template literals** — all HTML generation uses template literals; use `esc()` to escape user strings
- **`const` scoping** — avoid declaring `const` before its first use (no hoisting with `const`/`let`)
- **Avoid duplicate `const` declarations** in the same scope — a common error when editing large template literal blocks

---

## Common pitfalls

1. **Syntax errors inside template literals** — a stray backtick inside a JS template string breaks the entire `<script>`. Always check for unmatched backticks after edits.
2. **`const` used before declaration** — since functions are long, placing a `const` inside an `else` branch that is referenced by an earlier `if` block causes `ReferenceError`. Move declarations to the top of their scope.
3. **Duplicate `const` in same scope** — occurs when copy-pasting blocks; rename or remove duplicates.
4. **Delta = null when baseline is 0** — `fw2avg = 0` makes `(a1 - a2) / |a2|` divide by zero → `null`. Use the `computeDelta()` helper which returns a large sentinel (`999999`) in this case, displayed as `+∞`.
5. **Indicators disappearing** — `availInds` filtering must keep indicators that have data in at least one FW, not require both AND non-zero delta.

---

## Checkpoint / versioning

Use git commits on the **current branch** as checkpoints **before** large structural changes.  
**Do NOT create a new branch** just to save a checkpoint — commit directly:

```bash
git add -A && git commit -m "checkpoint: description"
```

To revert a single file to a previous commit (last resort):
```bash
git checkout <hash> -- src/comparador.html
```

> ⚠️ **Never** suggest `git checkout -b <new-branch>` as a checkpoint strategy — it only creates branch clutter.
