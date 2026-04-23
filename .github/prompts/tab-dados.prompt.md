---
mode: 'agent'
description: 'Trabalhar na tab Dados (browser de CSVs raw)'
---

Vou trabalhar na **tab Dados** do `src/comparador.html`.

Contexto desta tab:
- Função de render principal: `renderDadosView()`
- Browser de CSVs raw — mostra os dados carregados em `S.fw1[]` e `S.fw2[]`
- `fmtCell(v, h)` — formata células (timestamps via `fmtTs()`, números com locale PT)
- `fmtTs(v)` — formata timestamp (epoch ms → `pt-PT` locale)

O que quero fazer:
