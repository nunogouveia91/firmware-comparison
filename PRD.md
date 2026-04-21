# PRD — Firmware Comparison Tool

**Versão:** 1.4  
**Data:** 2026-04-21  
**Branch:** dev  

---

## 1. Visão Geral

Aplicação web de página única (SPA) para comparação de exports CSV de firmware. Permite comparar dois grupos de ficheiros (FW-A vs FW-B, ou Antes vs Depois de uma actualização) com métricas estatísticas, classificação automática de indicadores e visualização temporal.

---

## 2. Objectivos

- Simplificar a análise de qualidade após actualizações de firmware
- Eliminar a necessidade de ferramentas externas (Excel, scripts ad-hoc)
- Permitir uso offline / sem infra-estrutura de servidor
- Manter toda a memória do utilizador local (privacidade, sem backend)

---

## 3. Utilizadores Alvo

- Engenheiros de qualidade de firmware
- Equipas de validação de releases
- Product managers que acompanham métricas de campo

---

## 4. Funcionalidades Principais

### 4.1 Carregar Dados
- Upload de múltiplos CSVs por grupo (FW-A e FW-B)
- Drag-and-drop e file picker
- **Toggle de modo de carregamento**: "Dois Grupos" (default) ou "ZIP"
  - Modo ZIP: carrega um único `.zip` com estrutura `Firmware_A_Control/` + `Firmware_B_Upgrade/`; distribui automaticamente os CSVs pelos grupos correctos
- Labels personalizados por grupo
- Definição de número de unidades por grupo
- Guardar/carregar datasets e análises completas (IndexedDB)
- Nome de análise gerado automaticamente com campos: **Modelo**, **Firmware Control/Antes**, **Firmware Upgrade/Depois**, **Tipo de Piloto** (alfas/betas); formato `YYYY-MM-DD_modelo_fw-control_fw-upgrade_piloto`; conflitos resolvidos com sufixo `_1`, `_2`, etc.
- Nome de dataset de firmware gerado com: **Modelo**, **Firmware**, **Tipo de Piloto**; mesmo formato e deduplication
- Export ZIP de análises

### 4.2 Comparação Directa
- Comparação lado a lado de todos os indicadores
- Classificação automática: Blocker, Major, Atenção, Good, OK, S/D
- Score global e Score por cluster (ponderado)
- Filtros: Principais Diferenças, Falhas, Melhorias, Sem Dados, Todos
- Filtro por cluster; filtro "Desprezável"
- Tags de tipo de indicador: acum., méd. dia, méd. hora

### 4.3 Comparação Temporal
- Gráfico de série temporal por indicador
- Modo "Períodos Cruzados" (alinhamento por posição, para cenários antes/depois)
- Modo "Períodos Separados" (timestamps reais em eixo X partilhado)
- Δ% sempre calculado por alinhamento posicional
- Suporte a epoch ms e strings PT locale (`DD/MM/YYYY, HH:MM`)

### 4.4 Evolução
- Métricas estatísticas por indicador: Score, Crescimento, Taxa/u.t., Var.Abs., Desvio Padrão, Sinal
- Tabela paginada (20 indicadores/página), colunas ordenáveis
- Selector FW-A / FW-B / Ambos

### 4.5 Dados
- Browser de CSV em bruto por ficheiro
- Linha de médias para indicadores não-acumulativos
- Pesquisa por nome de indicador; toggle de colunas vazias

### 4.6 Definições
- Limiares configuráveis (fail/warning/improvement)
- Clusters com ícones, pesos e export/import JSON
- Gestão de datasets e análises guardadas

### 4.7 Relatório
- Relatório HTML imprimível com todos os indicadores, scores por cluster e estatísticas

---

## 5. Requisitos Não-Funcionais

| Requisito | Detalhe |
|---|---|
| Sem backend em produção | Ficheiro HTML estático puro |
| Sem build step | Plain ES2020+, sem bundler |
| Persistência local | IndexedDB + localStorage (migração automática) |
| Compatibilidade | Browsers modernos (Chrome, Firefox, Edge, Safari) |
| Hosting | GitHub Pages, Netlify, Cloudflare Pages |

---

## 6. Arquitectura

```
app.py              → Flask (desenvolvimento local apenas)
requirements.txt    → flask>=2.3
.github/
  copilot-instructions.md  → Instruções para o AI agent (actualizar README, AGENTS.md e PRD em cada commit)
src/
  comparador.html   → Aplicação completa (HTML + CSS + JS)
AGENTS.md           → Instruções de arquitectura para agentes AI
PRD.md              → Este documento
README.md           → Documentação pública
```

---

## 7. Dependências Externas (CDN)

| Lib | Versão | Uso |
|---|---|---|
| chart.js | 4.4.3 | Gráficos |
| jszip | 3.10.1 | Export ZIP |

---

## 8. Fora de Âmbito

- Autenticação / autorização
- Sincronização de dados entre utilizadores
- Backend de persistência
- Pipeline CI/CD para testes automatizados

---

## 9. Histórico de Alterações

| Data | Versão | Descrição |
|---|---|---|
| 2026-04-21 | 1.0 | Criação inicial do PRD |
| 2026-04-21 | 1.1 | Toggle ZIP upload na tab Carregar Dados |
| 2026-04-21 | 1.2 | Nome estruturado ao guardar análise (modelo + firmware + piloto) |
| 2026-04-21 | 1.3 | Análise com fw_control + fw_upgrade separados; dialog de nome para datasets |
| 2026-04-21 | 1.4 | Botão “Dados Guardados” unifica Análises e Firmwares num único painel com toggle interno |
