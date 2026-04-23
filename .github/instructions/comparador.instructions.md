---
applyTo: 'src/comparador.html'
---

# Contexto permanente — comparador.html

## Arquitectura
Ficheiro único `src/comparador.html` (HTML + CSS + JS inline). Sem build step, sem npm, sem módulos. Funções puras de utilidade estão também em `src/utils.js` (carregado via `<script src="utils.js">`).

## Estado global
- `S.fw1[]` / `S.fw2[]` — arrays de ficheiros carregados `{ name, headers[], rows[], averages, included }`
- `fw1Label` / `fw2Label` — nomes dos grupos (FW-B = Upgrade/Depois, FW-A = Control/Antes)
- `CFG` — configuração global (thresholds, clusters, weights), persistida via IndexedDB

## Terminologia
- `fw1` = FW-B = Upgrade / Depois (o firmware novo a avaliar)
- `fw2` = FW-A = Control / Antes (referência)

## Tabs — identificadas pelo propósito funcional
| Tab | Propósito | Função de render principal |
|---|---|---|
| Carregar Dados | Upload de CSVs ou ZIP; gestão de ficheiros | `renderLists()` |
| Comparação → Diferenças | Comparação lado-a-lado de médias com classificação | `renderCmpView()` |
| Comparação → Variação | Gráfico de série temporal com alinhamento por posição | `renderVarView()` |
| Evolução | Métricas estatísticas por indicador com paginação | `renderEvolView()` |
| Dados | Browser de CSVs raw | `renderDadosView()` |
| Definições | Thresholds, clusters, gestão de dados guardados | `renderDefsView()` |

## Funções puras (também em utils.js)
- `isTs(h)` — detecta coluna de timestamp pelo nome
- `isEpochMs(v)` — detecta epoch ms (9e11 < v < 5e12)
- `parseTs(v)` — converte epoch ms, ISO, e formato PT `DD/MM/YYYY, HH:MM`
- `getTsCol(f)` — encontra coluna de timestamp (por nome ou conteúdo ≥70%); resultado cacheado em `f._tsColCache`
- `esc(s)` — escapa HTML (usar sempre para strings de utilizador)
- `computeDelta(a1, a2)` — delta percentual; retorna `999999` quando baseline=0

## Padrões de código
- Re-render pattern: `root.innerHTML = ...` (sem DOM incremental)
- Template literals para todo o HTML gerado
- `esc()` obrigatório para qualquer string que venha do utilizador ou de ficheiros CSV
- Sem `const`/`let` antes da primeira utilização (sem hoisting)
- Sem `const` duplicados no mesmo scope

## Pitfalls frequentes
1. Backtick solto dentro de template literal quebra o `<script>` inteiro
2. `const` antes da declaração → `ReferenceError`
3. `const` duplicado no mesmo scope (copia-cola)
4. `computeDelta` com baseline=0 → usar o helper, nunca dividir directamente
5. `availInds` deve manter indicadores com dados em pelo menos um FW (não exigir ambos)
