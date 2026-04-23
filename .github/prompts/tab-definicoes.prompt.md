---
mode: 'agent'
description: 'Trabalhar na tab Definições (thresholds, clusters, dados guardados)'
---

Vou trabalhar na **tab Definições** do `src/comparador.html`.

Contexto desta tab:
- Função de render principal: `renderDefsView()`
- Configuração: `CFG` (thresholds, clusters, weights) — persistida via IndexedDB (`CFG_KEY`)
- Gestão de análises guardadas (`AN_KEY`) e datasets de firmware (`DS_KEY`)
- Toda a persistência é local ao browser do utilizador (IndexedDB/localStorage)
- Migração: na primeira carga, dados do `localStorage` são migrados para IndexedDB

O que quero fazer:
