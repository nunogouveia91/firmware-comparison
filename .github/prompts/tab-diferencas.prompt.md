---
mode: 'agent'
description: 'Trabalhar na tab Comparação → Diferenças'
---

Vou trabalhar na **tab Comparação → Diferenças** do `src/comparador.html`.

Contexto desta tab:
- Função de render principal: `renderCmpView()`
- Mostra comparação lado-a-lado de médias (FW-A vs FW-B) com classificação
- Classificação via `classify(pct)`: positivo = FW-B pior = mau para indicadores de qualidade
- `computeDelta(a1, a2)` para calcular delta % — baseline=0 devolve sentinel 999999
- `availInds` filtra indicadores com dados em pelo menos um FW

O que quero fazer:
