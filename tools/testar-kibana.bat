@echo off
chcp 65001 >nul
title Kibana Connection Test
echo.
echo  A iniciar teste de ligacao ao Kibana...
echo  O resultado sera guardado em kibana-test-result.log
echo.
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0kibana-test.ps1"
