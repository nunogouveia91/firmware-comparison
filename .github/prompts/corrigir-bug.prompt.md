---
mode: 'agent'
description: 'Diagnóstico estruturado de bugs no comparador'
---

Diagnóstico de bug no `src/comparador.html`. Verifica os suspeitos por esta ordem:

1. **Backtick solto** — procura template literals não fechados no bloco editado recentemente
2. **`const` antes da declaração** — verifica se algum `const`/`let` é usado antes de ser declarado
3. **`const` duplicado** — verifica duplicados no mesmo scope (copia-cola comum)
4. **`computeDelta` com baseline=0** — verifica se há divisões directas por `a2` sem usar o helper
5. **`availInds` demasiado restritivo** — indicadores devem aparecer se têm dados em pelo menos um FW

Descrição do sintoma:
