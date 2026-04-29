@echo off
chcp 65001 >nul
title Kibana Fields
powershell -NoProfile -ExecutionPolicy Bypass -Command ^
  "$api = 'VnRiRzA1MEJCaUZzOS1KcGE3QTc6a290Yldtc20zSTk5Y0JnQ3RIMXRBdw=='; $es = 'https://elasticsearch.i9.clg.nos.pt'; $h = @{Authorization=\"ApiKey $api\"}; $out = '%~dp0'; Invoke-RestMethod \"$es/hgw-syslog-pilots-28-04-2026/_mapping\" -Headers $h | ConvertTo-Json -Depth 20 | Set-Content \"${out}fields-mapping.json\" -Encoding UTF8; (Invoke-RestMethod \"$es/hgw-syslog-pilots-28-04-2026/_search\" -Method POST -Headers ($h + @{'Content-Type'='application/json'}) -Body '{\"size\":1,\"query\":{\"match_all\":{}}}').hits.hits[0]._source | ConvertTo-Json -Depth 10 | Set-Content \"${out}fields-sample.json\" -Encoding UTF8; (Invoke-RestMethod \"$es/hgw-syslog-framework-28.04.2026/_search\" -Method POST -Headers ($h + @{'Content-Type'='application/json'}) -Body '{\"size\":1,\"query\":{\"match_all\":{}}}').hits.hits[0]._source | ConvertTo-Json -Depth 10 | Set-Content \"${out}fields-framework.json\" -Encoding UTF8; Write-Host 'OK - traz os 3 ficheiros JSON'"
pause
