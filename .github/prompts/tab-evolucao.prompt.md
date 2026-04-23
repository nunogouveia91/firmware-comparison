---
mode: 'agent'
description: 'Trabalhar na tab Evolução (métricas estatísticas por indicador)'
---

Vou trabalhar na **tab Evolução** do `src/comparador.html`.

Contexto desta tab:
- Função de render principal: `renderEvolView()`
- Métricas estatísticas por indicador: score, growth, rate, var.abs, std dev, signal
- Paginação de indicadores
- Tipos de indicador: `acc` (acumulativo, sem timestamp), `avg`, `avg-day`, `avg-hour`
- FW-B = Upgrade/Depois (`S.fw1`), FW-A = Control/Antes (`S.fw2`)

O que quero fazer:
