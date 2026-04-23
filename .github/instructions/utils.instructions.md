---
applyTo: 'src/utils.js'
---

# Contexto permanente — utils.js

Este ficheiro contém funções puras extraídas de `comparador.html`.
Regras obrigatórias ao editar:

1. **Qualquer nova função adicionada aqui deve ser testada em `utils.test.js`**
   - Adiciona pelo menos um caso de sucesso, um caso limite, e um caso de erro
   - Casos limite documentados no AGENTS.md têm prioridade

2. **Funções puras apenas** — sem dependências de `S`, `CFG`, DOM, ou IndexedDB
   - Se a função precisar de `CFG`, recebe os valores como parâmetro explícito
   - Exemplo: `classify(pct, thresholds)` em vez de aceder `CFG.failThresholds` directamente

3. **Sem estado global** — não exportar variáveis mutáveis

4. **Compatibilidade com browser** — sem `import`/`export` (o HTML carrega o ficheiro via `<script src>`)
   - O Vitest usa `globals: true` no `vitest.config.js` para simular este ambiente

5. **Ao modificar uma função existente**, actualiza os testes correspondentes antes de fazer commit
