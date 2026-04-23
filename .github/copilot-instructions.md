# GitHub Copilot Instructions

## Workflow — IMPORTANT

**Do NOT create new branches.** Work directly in the current branch / main branch.  
**Do NOT suggest `git checkout -b` or branch creation commands** unless the user explicitly asks for a new branch.  
**Do NOT loop the user into repetitive checkout operations.**

All development is done in `src/comparador.html` — edit that file and commit directly.

---

## Project summary

Single-page web app for comparing firmware CSV exports.  
One file: `src/comparador.html` (HTML + CSS + JS, no build step).  
Flask (`app.py`) only serves it locally; no backend logic.

### Running locally

```bash
pip install -r requirements.txt
python app.py
# → http://localhost:5000
```

No build step, no npm, no compilation. Edit `src/comparador.html` and refresh the browser.

---

## Key rules when making changes

1. **Edit `src/comparador.html` directly** — that is the entire application.
2. **No build step** — plain ES2020+ JS inside `<script>` tags.
3. **Use `esc()` to escape user-provided strings** in template literals.
4. **Avoid duplicate `const` declarations** in the same scope.
5. **Check for unmatched backticks** — a stray backtick inside a template literal breaks the whole script.

### Checkpoints (last resort only)

Only use `git checkout` to **restore a single file** after a bad edit:

```bash
git checkout <hash> -- src/comparador.html
```

Do **not** create a new branch as a "checkpoint" — use `git commit` on the current branch instead:

```bash
git add src/comparador.html && git commit -m "checkpoint: before large change"
```

---

## Data model

| Variable | Meaning |
|---|---|
| `S.fw1[]` | FW-B files (Upgrade / Depois) |
| `S.fw2[]` | FW-A files (Control / Antes) |
| `CFG` | Global config (thresholds, clusters, weights) |

Full details in `AGENTS.md`.
