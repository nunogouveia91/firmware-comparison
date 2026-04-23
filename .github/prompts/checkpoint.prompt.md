---
mode: 'agent'
description: 'Commit checkpoint — actualiza docs e guarda progresso'
---

Faz um commit de checkpoint com os ficheiros actuais.

Passos:
0. **Verifica o `.gitignore`** — confirma que existe na raiz e que contém pelo menos:
    - `node_modules/`
    - `__pycache__/`
    - `*.pyc`
    - `uploads/`
Se não existir ou faltar entradas, cria/actualiza antes de continuar.
1. Actualiza `README.md` — reflecte as funcionalidades actuais da app
2. Actualiza `AGENTS.md` — reflecte mudanças de arquitectura, novo estado, novas funções
3. Actualiza `PRD.md` — reflecte novas features ou mudanças de comportamento
4. Corre `git add -A && git status` para ver o que vai no commit
5. Faz o commit: `git commit -m "checkpoint: <descrição breve do que mudou>"`
6. Faz push: `git push`