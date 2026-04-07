# Firmware Comparator

A single-page web application for comparing two sets of firmware CSV exports side by side. Built with Flask (Python) as a lightweight local server.

---

## Features

### 📂 Carregar Dados
- Upload multiple CSV files per firmware group (Upgrade vs Control)
- Drag-and-drop or file picker support
- Name each firmware group with a custom label
- Define number of units per group (used for the "desprezável" filter)
- Save and reload firmware datasets across sessions
- Save and load full analyses (data + config + clusters + thresholds)

### ⚖️ Comparação Direta
- Side-by-side comparison of all indicators between FW1 and FW2
- Automatic classification per indicator:
  - 🔴 **Blocker / Major** — degradation above configurable thresholds
  - 🟡 **Atenção** — small degradation
  - 🟢 **Good** — improvement beyond configurable threshold
  - ✅ **OK** — within acceptable range
  - **S/D** — no data in one or both groups
- Overall Score and Cluster Score (weighted)
- Filter by: Principais Diferenças, Falhas, Melhorias, Sem Dados, Todos
- Filter by cluster
- "Desprezável" auto-hide filter: hides indicators where both values are below a threshold (requires units to be set)
- Indicator type tags: **acum.** (no temporal reference), **méd. dia** (daily granularity), **méd. hora** (hourly granularity)
- Hide/show individual rows
- Click any indicator to inspect its raw data

### 📈 Comparação Temporal
- Time-series chart comparison between FW1 and FW2 per indicator
- Supports epoch ms timestamps and PT locale date strings (DD/MM/YYYY, HH:MM)

### 📊 Evolução
- Per-indicator evolution charts across the loaded files

### 📋 Dados
- Browse raw CSV data per file
- Average row shown for non-accumulative indicators
- Search indicators by name
- Toggle visibility of empty columns

### ⚙️ Definições
- **Limiares** — configure fail/warning/improvement percentage thresholds and labels; configure "desprezável" thresholds for accumulative and average indicators
- **Clusters** — group indicators into named clusters with icons and weights; export/import cluster config as JSON
- **Dados** — manage saved firmware datasets and analyses

### 📄 Relatório
- Generate a full printable HTML report with all indicators, cluster scores and summary statistics

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
└── src/
    └── comparador.html # Full application (single-page, no backend required)
```
