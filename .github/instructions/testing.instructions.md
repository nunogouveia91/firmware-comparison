---
applyTo: 'src/utils.js'
---

# Instrução de testes — utils.js / utils.test.js

Sempre que adicionares ou modificares código em `src/utils.js`, segue este processo antes de fazer commit:

## 1. Nova função adicionada

Verifica se existe um bloco `describe('<nomeDaFunção>', ...)` em `src/utils.test.js`.

- **Se não existir** → cria o bloco seguindo este padrão:

```js
// ─── nomeDaFunção ─────────────────────────────────────────────────────────────
describe('nomeDaFunção', () => {
  it('<caso de sucesso principal>', () => { ... });
  it('<caso limite 1>', () => { ... });
  it('<caso de erro / input inválido>', () => { ... });
});
```

Regras mínimas:
- Pelo menos **1 caso de sucesso** (input válido, output esperado)
- Pelo menos **1 caso limite** (zero, string vazia, valor fora do intervalo)
- Pelo menos **1 caso de erro** (null, undefined, tipo errado)
- Casos limite documentados em `AGENTS.md` (secção "Common pitfalls") têm prioridade

- **Se já existir** → vai para o passo 2.

## 2. Função existente modificada

Revê os testes existentes do `describe` correspondente:

- Se o novo comportamento não está coberto → **adiciona** os `it()` necessários
- Se um `it()` existente contradiz o novo comportamento → **adapta-o** e adiciona comentário `// updated: <motivo>`
- Nunca apagues testes sem justificação explícita

## 3. Correr os testes

Depois de criar ou adaptar os testes, corre:

```bash
npm test
```

- Todos os testes devem passar (exit code 0) antes de fazer commit
- Se algum falhar por causa de uma alteração intencional ao comportamento, corrige o teste **e** documenta no commit message

## 4. Padrões obrigatórios

- Usa `describe` / `it` / `expect` do Vitest (já importados no ficheiro)
- Não uses `beforeEach` / `afterEach` a não ser que o estado precise de reset entre testes
- Não uses mocks para funções puras — passa os inputs directamente
- Mantém os separadores de secção `// ─── nomeDaFunção ──...` para consistência visual
- O ficheiro `vitest.config.js` usa `globals: true`, portanto as funções de `utils.js` estão disponíveis sem import

## 5. Funções que NÃO precisam de testes aqui

- Funções que dependem de `S`, `CFG`, DOM ou IndexedDB → pertencem a `comparador.html`, não a `utils.js`
- Se precisares de `CFG`, recebe os valores como parâmetro explícito (ver `utils.instructions.md`)
