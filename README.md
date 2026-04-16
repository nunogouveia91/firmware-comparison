# Firmware Comparator

A single-page web application for comparing two sets of firmware CSV exports side by side — supporting both **FW-A vs FW-B** (firmware comparison) and **Antes vs Depois** (before/after upgrade) scenarios. Built with Flask (Python) as a lightweight local server.

---

## Features

### 📂 Carregar Dados
- Upload multiple CSV files per group: **FW-A (Control / Antes)** on the left, **FW-B (Upgrade / Depois)** on the right
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

## Requirements

- Python 3.9+
- Flask

```bash
pip install -r requirements.txt
```

---

## Running

```bash
python app.py
```

Opens on **http://localhost:5000** (or via the Codespace port forwarding URL).

---

## Project structure

```
.
├── app.py              # Flask server (serves static files only)
├── requirements.txt    # Python dependencies (flask only)
├── AGENTS.md           # AI agent instructions (architecture, conventions, pitfalls)
└── src/
    └── comparador.html # Complete application (HTML + CSS + JS, no build step)
```
