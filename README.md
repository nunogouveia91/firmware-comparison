# Firmware Comparator

A single-page web application for comparing two sets of firmware CSV exports side by side — supporting both **FW-A vs FW-B** (firmware comparison) and **Antes vs Depois** (before/after upgrade) scenarios. Built with Flask (Python) as a lightweight local server.

---

## Usar a aplicação (Windows, sem instalações)

1. Descarrega o ficheiro **[firmware-comparison.zip](firmware-comparison.zip)**
2. Extrai a pasta para qualquer local
3. Dá duplo-clique em **`abrir.bat`**
4. O browser abre automaticamente em `http://localhost:8080/comparador.html`

> Não é necessário instalar Python, Node.js ou qualquer outro software. Requer apenas Windows com PowerShell (incluído em todas as versões modernas do Windows).

---

## Quick start (local — desenvolvimento)

```bash
pip install -r requirements.txt
python app.py
# → http://localhost:5000
```

No build step. Edit `src/comparador.html` and refresh.

## Unit tests

```bash
npm install
npm test
```

Tests use [Vitest](https://vitest.dev/) and cover the pure utility functions in `src/utils.js`. CI runs on every push via `.github/workflows/test.yml`.

---

## Project structure

```
app.py                  → Flask dev server (serves src/ as static files; includes /api/es-proxy)
requirements.txt        → flask>=2.3
src/
  comparador.html       → Complete app (HTML + CSS + JS, no build step)
  utils.js              → Pure utility functions (loaded by comparador.html)
  utils.test.js         → Vitest unit tests for utils.js
  index.html            → Redirect to comparador.html
package.json            → Vitest dev dependency
vitest.config.js        → Vitest configuration
tools/                  → Dev/debug scripts (Kibana field inspection, ES query testing)
ROADMAP.md              → Planned features and future ideas
.github/
  instructions/         → Copilot context files (per-file instructions)
  prompts/              → Reusable agent prompt templates
  workflows/test.yml    → CI: run npm test on push/PR
```

---

## Deployment

Pure static HTML — no backend needed for production.

- **GitHub Pages**: Settings → Pages → branch `main`, folder `/src`
- **Netlify / Cloudflare Pages**: publish directory `src`

Each user's data is stored locally in their own browser (IndexedDB / localStorage).

---

## Features

### 📂 Carregar Dados
- Upload multiple CSV files per group: **FW-A (Control / Antes)** on the left, **FW-B (Upgrade / Depois)** on the right
- **Load mode toggle**: "Dois Grupos" (default, two separate drop zones), "ZIP" (single `.zip` with `Firmware_A_Control/` and `Firmware_B_Upgrade/` folders; auto-distributes CSVs to the correct group), or **"ES"** (query Elasticsearch directly — configure URL + API Key in *Definições → 🔌 ES*)
- Drag-and-drop or file picker support
- Name each group with a custom label
- Define number of units per group (used for the "desprezável" filter)
- Save and reload firmware datasets across sessions (IndexedDB)
- Save and load full analyses (data + config + clusters + thresholds)
- Download all files from a saved analysis as a ZIP (`Firmware_A_Control/` + `Firmware_B_Upgrade/`)

### ⚖️ Comparação Direta
- Side-by-side comparison of all indicators between FW-A and FW-B
- Automatic classification per indicator:
  - 🔴 **Blocker / Major** — degradation above configurable thresholds
  - 🟡 **Atenção** — small degradation
  - 🟢 **Good** — improvement beyond configurable threshold
  - ✅ **OK** — within acceptable range
  - **S/D** — no data in one or both groups
- Overall Score and Cluster Score (weighted)
- Filter by: Principais Diferenças, Falhas, Melhorias, Sem Dados, Todos
- Filter by cluster
- "Desprezável" auto-hide filter
- Indicator type tags: **acum.**, **méd. dia**, **méd. hora**
- Hide/show individual rows; click any indicator to inspect raw data

### 📈 Comparação Temporal
- Time-series chart comparison between FW-A and FW-B per indicator
- **Períodos cruzados** (default) — aligns both periods by relative position (`+0h`, `+4h`…); works for before/after scenarios where timestamps don't overlap
- **Períodos separados** — each group plotted on its own real timestamps on a shared X axis
- Δ% variação always uses position-based alignment
- Supports epoch ms timestamps and PT locale date strings (`DD/MM/YYYY, HH:MM`)
- Auto-selects the indicator with highest variation on first load

### 📊 Evolução
- Per-indicator statistical metrics: **Score**, **Crescimento**, **Taxa/u.t.**, **Var.Abs.**, **Desvio Padrão**, **Sinal**
- Paginated table (20 indicators per page)
- Sortable columns; FW selector (FW-A / FW-B / Ambos)
- Expandable glossary of metrics

### 📋 Dados
- Browse raw CSV data per file
- Average row for non-accumulative indicators
- Search by indicator name; toggle empty columns

### ⚙️ Definições
- **Limiares** — configure fail/warning/improvement thresholds and labels
- **Clusters** — group indicators with icons and weights; export/import JSON
- **Dados** — manage saved datasets and analyses

### 📄 Relatório
- Printable HTML report with all indicators, cluster scores and summary statistics

---

## Memory & persistence

All data (configurations, saved firmwares, saved analyses) is stored **locally in each user's browser** (IndexedDB / localStorage). There is no server-side storage — each person who opens the app has their own isolated memory. Clearing browser data will erase saved data.

---

## Running locally

### Requirements

- Python 3.9+
- Flask

```bash
pip install -r requirements.txt
python app.py
```

Opens on **http://localhost:5000** (or via the Codespace port forwarding URL).

### Running without Python (direct file)

Since the app is a self-contained HTML file, you can also open `src/comparador.html` directly in a browser — though some browsers restrict IndexedDB on `file://` URLs, so the local Flask server is recommended for development.

---

## Online deployment (static hosting)

The app is a single static HTML file — **no backend required** for online hosting. Flask is only needed for local development.

Supported static hosting options (all free):

| Platform | Setup |
|---|---|
| **GitHub Pages** | Enable in repo Settings → Pages → branch `main`, folder `/src` |
| **Netlify** | Connect GitHub repo, publish directory: `src` |
| **Cloudflare Pages** | Connect GitHub repo, build output: `src` |

After deploying, each user's memory stays local to their own browser.

---

## Project structure

```
.
├── app.py              # Flask server for local development (serves src/ as static files)
├── requirements.txt    # Python dependencies (flask only)
├── AGENTS.md           # AI agent instructions (architecture, conventions, pitfalls)
├── PRD.md              # Product Requirements Document
├── .github/
│   └── copilot-instructions.md  # Copilot instructions (followed on every commit)
└── src/
    └── comparador.html # Complete application (HTML + CSS + JS, no build step)
```
