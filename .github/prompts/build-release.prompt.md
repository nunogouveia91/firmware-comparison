---
mode: 'agent'
description: 'Build release ZIP — empacota a app para distribuição (2 cliques, sem Python)'
---

Cria o ficheiro ZIP de distribuição da app.

## Regras

- O ZIP final chama-se `firmware-comparison.zip` e fica na raiz do repositório.
- Dentro do ZIP a estrutura deve ser:
  ```
  firmware-comparison/
    abrir.bat
    server.ps1
    src/
      comparador.html
      utils.js
      index.html
  ```
- Após criar o ZIP, remove qualquer pasta temporária criada durante o processo.
- Se já existir um `firmware-comparison.zip` anterior, substitui-o.
- Não inclui no ZIP: `node_modules/`, `__pycache__/`, `*.pyc`, `.git/`, `uploads/`, ficheiros de teste, ficheiros de configuração de desenvolvimento.

## Passos

1. **Verifica pré-condições** — confirma que existem: `release/server.ps1`, `release/abrir.bat`, `src/comparador.html`, `src/utils.js`, `src/index.html`. Se algum faltar, para e reporta o erro.

2. **Remove artefactos anteriores** — apaga `firmware-comparison.zip` e `dist/` se existirem.

3. **Cria estrutura temporária** — cria a pasta `dist/firmware-comparison/` com os ficheiros:
   - `dist/firmware-comparison/abrir.bat` ← copia de `release/abrir.bat`
   - `dist/firmware-comparison/server.ps1` ← copia de `release/server.ps1`
   - `dist/firmware-comparison/src/comparador.html` ← copia de `src/comparador.html`
   - `dist/firmware-comparison/src/utils.js` ← copia de `src/utils.js`
   - `dist/firmware-comparison/src/index.html` ← copia de `src/index.html`

4. **Cria o ZIP** — compacta `dist/firmware-comparison/` para `firmware-comparison.zip` na raiz.

5. **Limpa** — remove a pasta `dist/` inteira.

6. **Valida** — confirma que `firmware-comparison.zip` existe e lista o seu conteúdo.

7. **Reporta** — mostra tamanho do ZIP e caminho absoluto. Exemplo de output esperado:
   ```
   Release criado: firmware-comparison.zip (2.1 MB)
   Caminho: C:\...\firmware-comparison.zip
   Conteúdo: 5 ficheiros
   ```

## Comandos PowerShell de referência

```powershell
# Passo 2 — limpar
Remove-Item -Force firmware-comparison.zip -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force dist -ErrorAction SilentlyContinue

# Passo 3 — copiar
$null = New-Item -ItemType Directory -Force dist/firmware-comparison/src
Copy-Item release/abrir.bat    dist/firmware-comparison/
Copy-Item release/server.ps1   dist/firmware-comparison/
Copy-Item src/comparador.html dist/firmware-comparison/src/
Copy-Item src/utils.js        dist/firmware-comparison/src/
Copy-Item src/index.html      dist/firmware-comparison/src/

# Passo 4 — zip
Compress-Archive -Path dist/firmware-comparison -DestinationPath firmware-comparison.zip -Force

# Passo 5 — limpar
Remove-Item -Recurse -Force dist

# Passo 6 — validar
Get-ChildItem firmware-comparison.zip | Select-Object Name, @{N='MB';E={[math]::Round($_.Length/1MB,2)}}
```
