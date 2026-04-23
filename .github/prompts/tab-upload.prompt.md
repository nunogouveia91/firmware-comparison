---
mode: 'agent'
description: 'Trabalhar na tab Carregar Dados (upload de ficheiros)'
---

Vou trabalhar na **tab Carregar Dados** do `src/comparador.html`.

Contexto desta tab:
- Função de render principal: `renderLists()`
- Modo "Dois Grupos": FW-A (esquerda, `fw2`) + FW-B (direita, `fw1`)
- Modo "ZIP": pasta `Firmware_A_Control/` + `Firmware_B_Upgrade/`
- Botão "Dados Guardados": painel com toggle interno Análises / Firmwares (default: Análises)
- Estado: `S.fw1[]`, `S.fw2[]`, `fw1Label`, `fw2Label`

O que quero fazer:
