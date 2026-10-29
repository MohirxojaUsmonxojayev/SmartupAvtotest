# Allure hisobotini generatsiya qilib brauzerda ochadi.
# Ishlatilishi:
#   1) Testlarni --alluredir bilan ishga tushiring:
#        pytest tests/online tests/xtrade --alluredir=allure-results
#   2) Hisobotni oching:
#        .\scripts\allure-report.ps1
$ErrorActionPreference = "Stop"
$root = Split-Path $PSScriptRoot -Parent
Set-Location $root

# Java (JAVA_HOME) ni topish — Allure Java ilovasi.
if (-not $env:JAVA_HOME -or -not (Test-Path "$env:JAVA_HOME\bin\java.exe")) {
    $jdk = Get-ChildItem "C:\Program Files\Microsoft" -Directory -Filter "jdk-*" -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($jdk) { $env:JAVA_HOME = $jdk.FullName }
}
if (-not $env:JAVA_HOME) { throw "Java topilmadi. OpenJDK o'rnating: winget install Microsoft.OpenJDK.21" }
$env:PATH = "$env:JAVA_HOME\bin;$env:PATH"

# Bitta self-contained HTML hisobot (file:// orqali ochiladi, server shart emas).
allure generate allure-results -o allure-report --single-file --clean
Start-Process "allure-report\index.html"
Write-Output "Ochildi: allure-report\index.html"
