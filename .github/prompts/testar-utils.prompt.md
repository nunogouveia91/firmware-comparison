---
mode: 'agent'
description: 'Criar/adaptar testes para funções novas ou modificadas em utils.js'
---

Ao adicionar ou modificar uma função em `src/utils.js`, faz o seguinte:

1. **Identifica a função** que foi adicionada ou modificada
2. **Abre `src/utils.test.js`** e verifica os testes existentes para essa função
3. **Adiciona ou actualiza testes** cobrindo:
   - Caso de sucesso típico
   - Casos limite (baseline=0, array vazio, valor nulo/undefined, string inválida)
   - Casos de erro documentados no AGENTS.md
4. **Corre os testes**: `npm test`
5. Se algum teste falhar, corrige a função **ou** o teste (dependendo de qual está errado)
6. Confirma que todos os testes passam antes de fazer commit

Função(ões) a testar:
