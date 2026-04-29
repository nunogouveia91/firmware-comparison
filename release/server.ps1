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

        # ── ES proxy ──────────────────────────────────────────────
        if ($path -eq 'api/es-proxy' -and $req.HttpMethod -eq 'POST') {
            $esUrl    = $req.Headers['X-ES-Url']
            $apiKey   = $req.Headers['X-ES-ApiKey']
            $esPath   = $req.Headers['X-ES-Path']
            if ($esUrl -and $apiKey -and $esPath) {
                $target = "$($esUrl.TrimEnd('/'))/$($esPath.TrimStart('/'))"
                $reader = New-Object System.IO.StreamReader($req.InputStream)
                $bodyJson = $reader.ReadToEnd()
                $reader.Close()
                try {
                    $webReq = [System.Net.HttpWebRequest]::Create($target)
                    $webReq.Method = 'POST'
                    $webReq.ContentType = 'application/json'
                    $webReq.Headers.Add('Authorization', "ApiKey $apiKey")
                    $bodyBytes = [System.Text.Encoding]::UTF8.GetBytes($bodyJson)
                    $webReq.ContentLength = $bodyBytes.Length
                    $webReq.Timeout = 30000
                    $stream = $webReq.GetRequestStream()
                    $stream.Write($bodyBytes, 0, $bodyBytes.Length)
                    $stream.Close()
                    $webResp = $webReq.GetResponse()
                    $respStream = $webResp.GetResponseStream()
                    $respBytes = New-Object System.IO.MemoryStream
                    $respStream.CopyTo($respBytes)
                    $respStream.Close()
                    $data = $respBytes.ToArray()
                    $res.ContentType = 'application/json'
                    $res.StatusCode = 200
                    $res.ContentLength64 = $data.Length
                    $res.OutputStream.Write($data, 0, $data.Length)
                    Write-Host "  200  /api/es-proxy → $target"
                } catch [System.Net.WebException] {
                    $errResp = $_.Exception.Response
                    if ($errResp) {
                        $errStream = $errResp.GetResponseStream()
                        $errBytes  = New-Object System.IO.MemoryStream
                        $errStream.CopyTo($errBytes)
                        $errData = $errBytes.ToArray()
                        $res.StatusCode = [int]$errResp.StatusCode
                        $res.ContentType = 'application/json'
                        $res.ContentLength64 = $errData.Length
                        $res.OutputStream.Write($errData, 0, $errData.Length)
                    } else {
                        $errBody = [System.Text.Encoding]::UTF8.GetBytes($_.Exception.Message)
                        $res.StatusCode = 502
                        $res.ContentLength64 = $errBody.Length
                        $res.OutputStream.Write($errBody, 0, $errBody.Length)
                    }
                    Write-Host "  ERR  /api/es-proxy $($_.Exception.Message)" -ForegroundColor Red
                }
            } else {
                $errBody = [System.Text.Encoding]::UTF8.GetBytes('Missing headers')
                $res.StatusCode = 400
                $res.ContentLength64 = $errBody.Length
                $res.OutputStream.Write($errBody, 0, $errBody.Length)
            }
        # ── Static files ──────────────────────────────────────────
        } elseif (Test-Path (Join-Path $srcDir $path) -PathType Leaf) {
            $filePath = Join-Path $srcDir $path
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
