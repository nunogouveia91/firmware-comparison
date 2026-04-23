---
mode: 'agent'
description: 'Trabalhar na tab Comparação → Variação (gráfico temporal)'
---

Vou trabalhar na **tab Comparação → Variação** do `src/comparador.html`.

Contexto desta tab:
- Função de render principal: `renderVarView()`
- Gráfico de série temporal via Chart.js 4.4.3
- `alignedPairs[]` — pares `{label, v1ts, v2ts}` alinhados por posição (não por timestamp real)
- `misaligned` — true quando <20% de buckets se sobrepõem entre os dois FWs
- Modo "Cruzados" (default): bucket 1 FW-B vs bucket 1 FW-A, labels offset (`+0h`, `+4h`…)
- Modo "Separados": cada FW no seu timestamp real, eixo X partilhado
- Δ% usa sempre `alignedPairs` independentemente do modo de visualização

O que quero fazer:
