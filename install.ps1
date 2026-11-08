<#
.SYNOPSIS
    Official 1-Line Native Windows Installer for Antigravity RTL & Persian Typography.
.DESCRIPTION
    Zero-dependency installer. Automatically downloads, links, and hot-reloads
    Antigravity RTL into Google Antigravity 2.0 without requiring npm, git, or python.
.EXAMPLE
    irm https://raw.githubusercontent.com/yasin-saeedi/antigravity-rtl/main/install.ps1 | iex
#>

$ErrorActionPreference = 'Stop'

Write-Host ""
Write-Host "  ==================================================" -ForegroundColor Cyan
Write-Host "    Antigravity RTL & Persian Typography Installer" -ForegroundColor Cyan
Write-Host "  ==================================================" -ForegroundColor Cyan
Write-Host ""

$pluginsDir = Join-Path $HOME ".gemini\config\plugins"
$targetDir  = Join-Path $pluginsDir "antigravity-rtl"
$repoZipUrl = "https://github.com/yasin-saeedi/antigravity-rtl/archive/refs/heads/main.zip"
$tempZip    = Join-Path $env:TEMP "antigravity-rtl-main.zip"
$tempExtract= Join-Path $env:TEMP "antigravity-rtl-extract"

# 1. Prepare Target Directory
if (-not (Test-Path $pluginsDir)) {
    New-Item -ItemType Directory -Path $pluginsDir -Force | Out-Null
}

$sourceDir = $null

if ($PSScriptRoot -and (Test-Path (Join-Path $PSScriptRoot "plugin.json"))) {
    Write-Host "  [*] Using local repository package..." -ForegroundColor Gray
    $sourceDir = $PSScriptRoot
} else {
    Write-Host "  [*] Downloading latest release from GitHub..." -ForegroundColor Yellow
    try {
        [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.SecurityProtocolType]::Tls12
        Invoke-WebRequest -Uri $repoZipUrl -OutFile $tempZip -UseBasicParsing
    } catch {
        Write-Host "  [-] Failed to download archive: $_" -ForegroundColor Red
        exit 1
    }

    Write-Host "  [*] Extracting plugin files..." -ForegroundColor Yellow
    if (Test-Path $tempExtract) {
        Remove-Item $tempExtract -Recurse -Force -ErrorAction SilentlyContinue
    }
    Expand-Archive -Path $tempZip -DestinationPath $tempExtract -Force
    $sourceDir = Join-Path $tempExtract "antigravity-rtl-main"
}

# 2. Deploy to Plugins Directory
Write-Host "  [*] Installing to: $targetDir" -ForegroundColor Gray
if (Test-Path $targetDir) {
    Remove-Item $targetDir -Recurse -Force -ErrorAction SilentlyContinue
}
New-Item -ItemType Directory -Path $targetDir -Force | Out-Null

$itemsToCopy = @("plugin.json", "package.json", "sidecars", "src", "scripts", "bin")
foreach ($item in $itemsToCopy) {
    $srcItem = Join-Path $sourceDir $item
    if (Test-Path $srcItem) {
        Copy-Item -Path $srcItem -Destination $targetDir -Recurse -Force
    }
}

# 3. Clean up temp files if downloaded
if (Test-Path $tempZip) { Remove-Item $tempZip -Force -ErrorAction SilentlyContinue }
if (Test-Path $tempExtract) { Remove-Item $tempExtract -Recurse -Force -ErrorAction SilentlyContinue }

# 4. Trigger Instant Live Hot-Reload if Antigravity is running
$installScript = Join-Path $targetDir "scripts\install-plugin.js"
if (Test-Path $installScript) {
    try {
        $hasNode = Get-Command node -ErrorAction SilentlyContinue
        if ($hasNode) {
            Start-Process node -ArgumentList "`"$installScript`"" -NoNewWindow -Wait
        } else {
            $antigravityExe = "$env:LOCALAPPDATA\Programs\antigravity\Antigravity.exe"
            if (Test-Path $antigravityExe) {
                $env:ELECTRON_RUN_AS_NODE = "1"
                $env:ELECTRON_NO_ASAR = "1"
                Start-Process $antigravityExe -ArgumentList "`"$installScript`"" -NoNewWindow -Wait
            }
        }
    } catch {}
}

Write-Host "  --------------------------------------------------" -ForegroundColor DarkGray
Write-Host "  [+] Antigravity RTL installed successfully!" -ForegroundColor Green
Write-Host "  [i] Open Antigravity to enjoy native RTL and Persian fonts." -ForegroundColor White
Write-Host ""
