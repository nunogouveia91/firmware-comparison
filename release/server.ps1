param([int]$Port = 8080)

$ErrorActionPreference = 'SilentlyContinue'
$srcDir = Join-Path $PSScriptRoot "src"

$listener = New-Object System.Net.HttpListener
$listener.Prefixes.Add("http://localhost:$Port/")

try {
    $listener.Start()
} catch {
    Write-Host "ERRO: Nao foi possivel iniciar na porta $Port." -ForegroundColor Red
    Write-Host "Tente fechar outras instancias da aplicacao." -ForegroundColor Yellow
    Read-Host "Prima Enter para sair"
    exit 1
}

Write-Host ""
Write-Host "  === Firmware Comparison ===" -ForegroundColor Cyan
Write-Host "  http://localhost:$Port/comparador.html" -ForegroundColor Green
Write-Host ""
Write-Host "  Feche esta janela para parar o servidor." -ForegroundColor Yellow
Write-Host ""

$mimeTypes = @{
    ".html" = "text/html; charset=utf-8"
    ".css"  = "text/css; charset=utf-8"
    ".js"   = "application/javascript; charset=utf-8"
    ".json" = "application/json"
    ".png"  = "image/png"
    ".jpg"  = "image/jpeg"
    ".ico"  = "image/x-icon"
    ".csv"  = "text/csv"
    ".zip"  = "application/zip"
}

while ($listener.IsListening) {
    try {
        $context  = $listener.GetContext()
        $req      = $context.Request
        $res      = $context.Response

        $path = $req.Url.LocalPath.TrimStart('/')
        if ([string]::IsNullOrEmpty($path)) {
            $path = "comparador.html"
        }

        $filePath = Join-Path $srcDir $path

        if (Test-Path $filePath -PathType Leaf) {
            $ext  = [System.IO.Path]::GetExtension($filePath).ToLower()
            $mime = if ($mimeTypes.ContainsKey($ext)) { $mimeTypes[$ext] } else { "application/octet-stream" }
            $bytes = [System.IO.File]::ReadAllBytes($filePath)
            $res.ContentType      = $mime
            $res.ContentLength64  = $bytes.Length
            $res.StatusCode       = 200
            $res.OutputStream.Write($bytes, 0, $bytes.Length)
            Write-Host "  200  /$path"
        } else {
            $res.StatusCode = 404
            $body = [System.Text.Encoding]::UTF8.GetBytes("404 Not Found: $path")
            $res.ContentLength64 = $body.Length
            $res.OutputStream.Write($body, 0, $body.Length)
            Write-Host "  404  /$path" -ForegroundColor Red
        }
    } catch {
        # ligacao fechada ou outro erro transitorio — ignorar
    } finally {
        try { $context.Response.OutputStream.Close() } catch {}
    }
}
