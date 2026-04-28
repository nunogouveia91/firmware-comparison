@echo off
chcp 65001 >nul
title Firmware Comparison

set PORT=8080
set SCRIPT=%~dp0server.ps1

:: Se a porta ja estiver ocupada, apenas abre o browser (instancia ja a correr)
powershell -NoProfile -Command ^
  "if (Get-NetTCPConnection -LocalPort %PORT% -State Listen -ErrorAction SilentlyContinue) { exit 1 } else { exit 0 }"

if %errorlevel%==1 (
    echo Servidor ja a correr. A abrir browser...
    start http://localhost:%PORT%/comparador.html
    exit /b 0
)

:: Iniciar servidor numa janela PowerShell separada
start "Firmware Comparison" powershell -NoProfile -ExecutionPolicy Bypass -File "%SCRIPT%" -Port %PORT%

:: Aguardar o servidor arrancar
timeout /t 2 /nobreak >nul

:: Abrir no browser padrao
start http://localhost:%PORT%/comparador.html
