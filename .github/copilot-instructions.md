# GitHub Copilot Instructions — firmware-comparison

## Project overview

Single-page web application for comparing firmware CSV exports.  
The entire app lives in **`src/comparador.html`** (HTML + CSS + JS, no build step).  
Flask (`app.py`) only serves the file locally; production runs on GitHub Pages.

---

## How to run locally

```bash
pip install -r requirements.txt
python app.py
# → http://localhost:5000
```

No npm, no compilation. Edit `src/comparador.html` and refresh the browser.

---

## Repository structure

```
app.py              → Flask dev server
requirements.txt    → flask>=2.3
src/
  comparador.html   → The complete application
.github/
  workflows/
    deploy.yml      → Auto-deploy to GitHub Pages on push to main
```

---

## Copilot coding-agent workflow — what is expected from you (the user)

When GitHub Copilot's **coding agent** (cloud agent) finishes working on a task it opens a
**Pull Request (PR)** on GitHub with all the proposed changes.  
At that point you will see a banner or dialog with two options:

| Option | What it means | When to use it |
|--------|---------------|----------------|
| **Checkout** | Download the agent's branch to your local machine so you can run and test the changes yourself before merging. | Use this when you want to open the app in your browser, verify behaviour, or look at the diff in your own editor. |
| **Apply** | Accept the suggestion directly in the Copilot Chat panel (inline edit mode). | Use this only for small, in-editor inline suggestions — not for full agent PR reviews. |

### Recommended steps for reviewing a Copilot agent PR

1. **Open the PR** on GitHub (`github.com/<owner>/<repo>/pulls`).
2. **Read the PR description** — the agent lists every change it made in a checklist.
3. **Review the diff** in the "Files changed" tab on GitHub.
4. If you want to test locally:
   ```bash
   git fetch origin
   git checkout <branch-name-from-pr>
   python app.py          # open http://localhost:5000 to verify
   ```
5. If everything looks good, click **Merge pull request** on GitHub.
6. The `deploy.yml` workflow will automatically re-deploy the app to GitHub Pages.

> **You are never required to run any build or test commands** — this project has no build step
> and no automated test suite. A visual check in the browser is sufficient.

---

## Coding conventions (for the agent)

- All changes go in `src/comparador.html`.
- Use `esc()` to escape every user-supplied string rendered as HTML.
- Avoid duplicate `const` declarations in the same scope.
- Check for unmatched backticks in template literals after every edit.
- Use `computeDelta()` to avoid division-by-zero when the baseline average is 0.

For full details see [`AGENTS.md`](../AGENTS.md).
