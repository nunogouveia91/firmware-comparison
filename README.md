# Firmware Comparison & Toolbox

A Flask web application that bundles three internal tools into a single lightweight server:

1. **Budget Tracker** – personal expense tracking with multi-wallet and category support  
2. **Firmware Comparator** – side-by-side comparison of two firmware CSV exports  
3. **Elasticsearch Export** – query an Elasticsearch / Kibana cluster and download results as CSV, JSON or NDJSON  

---

## Features

### 💰 Budget Tracker (`/budget`)
- Device-based user identity (no login required)
- Multiple named wallets with custom colours
- Expense categories with emoji icons, grouped as *basic*, *free* or *saving*
- Month-by-month filtering and per-wallet filtering
- Running totals and spending breakdown charts
- Full CRUD for expenses, wallets and categories
- Data stored locally in a SQLite database (`budget.db`)

### 📊 Firmware Comparator (`/comparador`)
- Upload two sets of CSV files (Firmware A vs Firmware B)
- Automatic detection of regressions (🔴), improvements (🟢) and warnings (🟡)
- Summary statistics and per-indicator averages
- Interactive Chart.js visualisations
- Configurable thresholds and sorting

### 🔍 Elasticsearch Export (`/elastic`)
- Connect to any Elasticsearch / OpenSearch cluster (HTTP or HTTPS)
- Basic authentication or API-key authentication
- Optional SSL certificate verification bypass
- Date-range and query-string filtering
- Preview results before downloading
- Scroll-API-based full export (up to 500 000 documents)
- Download as **CSV** (Excel-compatible UTF-8 BOM), **JSON**, or **NDJSON**
- Nested fields are automatically flattened with dot-notation keys

---

## Requirements

- Python 3.9+
- pip packages listed in `requirements.txt`:

```
flask>=2.3
requests>=2.31
urllib3>=2.0
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Running the application

```bash
python app.py
```

The server starts on **http://localhost:5000** and redirects `/` to `/budget`.

| Path | Description |
|------|-------------|
| `/budget` | Budget Tracker |
| `/comparador` | Firmware Comparator |
| `/elastic` | Elasticsearch Export |

---

## Project structure

```
.
├── app.py              # Flask application (routes + SQLite helpers)
├── requirements.txt    # Python dependencies
├── budget.db           # SQLite database (auto-created on first run)
└── src/
    ├── budget.html     # Budget Tracker UI (single-page)
    ├── comparador.html # Firmware Comparator UI (single-page)
    └── elastic.html    # Elasticsearch Export UI (single-page)
```

---

## REST API reference

### Users

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/users/<device_id>` | Get user by device ID |
| `POST` | `/api/users` | Create user (idempotent) |
| `PUT` | `/api/users/<id>` | Update user name |

### Wallets

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/wallets?user_id=` | List wallets for a user |
| `POST` | `/api/wallets` | Create wallet |
| `DELETE` | `/api/wallets/<id>` | Delete wallet |

### Categories

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/categories?user_id=` | List categories for a user |
| `POST` | `/api/categories` | Create category |
| `DELETE` | `/api/categories/<id>` | Delete category |

### Expenses

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/expenses?user_id=&wallet_id=&month=` | List expenses (filterable) |
| `POST` | `/api/expenses` | Create expense |
| `DELETE` | `/api/expenses/<id>` | Delete expense |

### Elasticsearch

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/elastic/test` | Test cluster connectivity |
| `POST` | `/api/elastic/indices` | List available indices |
| `POST` | `/api/elastic/query` | Preview up to 5 hits |
| `POST` | `/api/elastic/download` | Full export (scroll API) |

---

## Notes

- The SQLite database file `budget.db` is created automatically in the same directory as `app.py` on first run.
- The Elasticsearch export uses the [Scroll API](https://www.elastic.co/guide/en/elasticsearch/reference/current/scroll-api.html) and cleans up the scroll context after each export.
- All UI pages are self-contained single-page HTML files served from the `src/` folder.