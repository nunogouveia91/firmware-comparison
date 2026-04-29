param(
    [string]$KibanaUrl  = "https://kibana.i9.clg.nos.pt",
    [string]$ApiKey     = "VnRiRzA1MEJCaUZzOS1KcGE3QTc6a290Yldtc20zSTk5Y0JnQ3RIMXRBdw==",
    [string]$LogFile    = "$PSScriptRoot\kibana-test-result.log"
)

$ErrorActionPreference = 'SilentlyContinue'
$lines = [System.Collections.Generic.List[string]]::new()

function Log {
    param([string]$msg, [string]$color = "White")
    $lines.Add($msg)
    Write-Host $msg -ForegroundColor $color
}

function Section { param([string]$t) Log ""; Log ("=" * 60) Cyan; Log "  $t" Cyan; Log ("=" * 60) Cyan }

function Test-Step {
    param([string]$label, [scriptblock]$action)
    Log ""
    Log ">> $label" Yellow
    try {
        $result = & $action
        Log "   OK" Green
        return $result
    } catch {
        Log "   ERRO: $_" Red
        return $null
    }
}

$headers = @{
    "Authorization" = "ApiKey $ApiKey"
    "kbn-xsrf"      = "true"
    "Content-Type"  = "application/json"
}

Section "KIBANA CONNECTION TEST — $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
Log "Host      : $KibanaUrl"
Log "Log file  : $LogFile"
Log "Machine   : $env:COMPUTERNAME"
Log "User      : $env:USERNAME"
Log "OS        : $([System.Environment]::OSVersion.VersionString)"
Log "PS version: $($PSVersionTable.PSVersion)"

# 1 — DNS
Section "1. DNS Resolution"
Test-Step "Resolver DNS de $((New-Object Uri $KibanaUrl).Host)" {
    $host_ = (New-Object Uri $KibanaUrl).Host
    $ip = [System.Net.Dns]::GetHostAddresses($host_) | Select-Object -First 1
    Log "   IP: $ip" Green
}

# 2 — TCP connectivity
Section "2. TCP Connectivity (porta 443)"
Test-Step "Ligar TCP a $((New-Object Uri $KibanaUrl).Host):443" {
    $h = (New-Object Uri $KibanaUrl).Host
    $tcp = New-Object System.Net.Sockets.TcpClient
    $conn = $tcp.BeginConnect($h, 443, $null, $null)
    $ok = $conn.AsyncWaitHandle.WaitOne(5000)
    $tcp.Close()
    if (-not $ok) { throw "Timeout após 5s" }
    Log "   Porta 443 acessível" Green
}

# 3 — Kibana status (sem auth)
Section "3. Kibana Status (sem autenticação)"
Test-Step "GET $KibanaUrl/api/status" {
    $r = Invoke-RestMethod -Uri "$KibanaUrl/api/status" -TimeoutSec 10
    Log "   Kibana version: $($r.version.number)" Green
    Log "   Status: $($r.status.overall.level)" Green
}

# 4 — Auth com API Key
Section "4. Autenticação com API Key"
Test-Step "GET $KibanaUrl/api/status (com API Key)" {
    $r = Invoke-RestMethod -Uri "$KibanaUrl/api/status" -Headers $headers -TimeoutSec 10
    Log "   Autenticado como: $($r.name)" Green
}

# 5 — Elasticsearch através do Kibana
Section "5. Elasticsearch via Kibana Proxy"
Test-Step "GET $KibanaUrl/api/console/proxy?path=/_cat/indices&method=GET" {
    $r = Invoke-RestMethod -Uri "$KibanaUrl/api/console/proxy?path=%2F_cat%2Findices%3Fv%3Dtrue&method=GET" -Headers $headers -TimeoutSec 15
    if ($r) {
        Log "   Indices recebidos:" Green
        ($r -split "`n") | Select-Object -First 20 | ForEach-Object { Log "     $_" }
    }
}

# 6 — Elasticsearch direto (porta 9200)
Section "6. Elasticsearch Direto (porta 9200)"
$esUrl = $KibanaUrl -replace "kibana\.", "elasticsearch." -replace ":5601", ":9200"
Log "   URL tentativa: $esUrl"
Test-Step "GET $esUrl/_cat/indices" {
    $r = Invoke-RestMethod -Uri "$esUrl/_cat/indices?v" -Headers @{ Authorization = "ApiKey $ApiKey" } -TimeoutSec 10
    Log "   Acesso direto ES OK" Green
    ($r -split "`n") | Select-Object -First 10 | ForEach-Object { Log "     $_" }
}

# 7 — Listar Data Views do Kibana
Section "7. Data Views (Kibana)"
Test-Step "GET $KibanaUrl/api/data_views" {
    $r = Invoke-RestMethod -Uri "$KibanaUrl/api/data_views" -Headers $headers -TimeoutSec 10
    Log "   Data Views encontrados: $($r.data_view.Count)" Green
    $r.data_view | Select-Object -First 10 | ForEach-Object { Log "     - $($_.title)  [id: $($_.id)]" }
}

# 8 — Listar TODOS os índices do ES
Section "8. Todos os indices Elasticsearch"
Test-Step "GET $esUrl/_cat/indices?v (lista completa)" {
    $r = Invoke-RestMethod -Uri "$esUrl/_cat/indices?v&s=index" -Headers @{ Authorization = "ApiKey $ApiKey" } -TimeoutSec 15
    ($r -split "`n") | ForEach-Object { Log "     $_" }
}

# 9 — Mapping do índice pilots mais recente (guardado em ficheiro separado)
Section "9. Mapping hgw-syslog-pilots (campos disponiveis)"
$mappingFile = "$PSScriptRoot\kibana-mapping.json"
Test-Step "GET $esUrl/hgw-syslog-pilots-*/_mapping -> $mappingFile" {
    $r = Invoke-RestMethod -Uri "$esUrl/hgw-syslog-pilots-28-04-2026/_mapping" -Headers @{ Authorization = "ApiKey $ApiKey" } -TimeoutSec 15
    $json = $r | ConvertTo-Json -Depth 20
    $json | Set-Content -Path $mappingFile -Encoding UTF8
    $props = ($r | Get-Member -MemberType NoteProperty | Select-Object -First 1).Name
    $fields = $r.$props.mappings.properties | Get-Member -MemberType NoteProperty | Select-Object -ExpandProperty Name
    Log "   Campos encontrados ($($fields.Count)) — guardado em kibana-mapping.json" Green
    $fields | ForEach-Object { Log "     - $_" }
}

# 10 — Amostra de 1 documento pilots (guardado em ficheiro separado)
Section "10. Amostra de documento (hgw-syslog-pilots)"
$sampleFile = "$PSScriptRoot\kibana-sample-doc.json"
Test-Step "GET $esUrl/hgw-syslog-pilots-28-04-2026/_search (1 doc) -> $sampleFile" {
    $body = '{"size":1,"query":{"match_all":{}}}'
    $r = Invoke-RestMethod -Uri "$esUrl/hgw-syslog-pilots-28-04-2026/_search" -Method POST -Headers @{ Authorization = "ApiKey $ApiKey"; "Content-Type" = "application/json" } -Body $body -TimeoutSec 15
    $doc = $r.hits.hits[0]._source
    $json = $doc | ConvertTo-Json -Depth 10
    $json | Set-Content -Path $sampleFile -Encoding UTF8
    Log "   Documento guardado em kibana-sample-doc.json" Green
    $doc | Get-Member -MemberType NoteProperty | ForEach-Object {
        Log "     $($_.Name): $($doc.($_.Name))"
    }
}

# 11 — Amostra de 1 documento framework
Section "11. Amostra de documento (hgw-syslog-framework)"
$sampleFwFile = "$PSScriptRoot\kibana-sample-framework.json"
Test-Step "GET $esUrl/hgw-syslog-framework-28.04.2026/_search (1 doc) -> $sampleFwFile" {
    $body = '{"size":1,"query":{"match_all":{}}}'
    $r = Invoke-RestMethod -Uri "$esUrl/hgw-syslog-framework-28.04.2026/_search" -Method POST -Headers @{ Authorization = "ApiKey $ApiKey"; "Content-Type" = "application/json" } -Body $body -TimeoutSec 15
    $doc = $r.hits.hits[0]._source
    $json = $doc | ConvertTo-Json -Depth 10
    $json | Set-Content -Path $sampleFwFile -Encoding UTF8
    Log "   Documento guardado em kibana-sample-framework.json" Green
    $doc | Get-Member -MemberType NoteProperty | ForEach-Object {
        Log "     $($_.Name): $($doc.($_.Name))"
    }
}

# Guardar log
Section "RESULTADO"
Log "A guardar log em: $LogFile"
$lines | Set-Content -Path $LogFile -Encoding UTF8
Log "Concluido. Envia o ficheiro '$LogFile' para analise." Green
Log ""
Read-Host "Prima Enter para fechar"
