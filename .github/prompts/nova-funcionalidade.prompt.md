---
mode: 'agent'
description: 'Template para adicionar nova funcionalidade ao comparador'
---

Antes de implementar, responde a estas perguntas sobre a nova funcionalidade:

1. **Em que tab aparece?** (Carregar Dados / Diferenças / Variação / Evolução / Dados / Definições)
2. **Que estado usa ou modifica?** (`S.fw1`, `S.fw2`, `CFG`, outro?)
3. **Precisa de nova função pura?** → Se sim, adiciona a `utils.js` e cria testes em `utils.test.js`
4. **Usa strings de utilizador ou dados de CSV?** → Obrigatório passar por `esc()`
5. **Tem casos limite?** → baseline=0, arrays vazios, timestamps em falta, ficheiros sem overlap

Regras de implementação:
- Não duplicar `const` no mesmo scope
- Não usar `const`/`let` antes da primeira utilização no scope
- Verificar backticks não fechados após editar template literals
- Re-render via `root.innerHTML = ...` (padrão existente)

Descrição da funcionalidade a implementar:
