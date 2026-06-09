# Clean build artifacts and temporary files (Windows PowerShell)
$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = (Resolve-Path (Join-Path $ScriptDir "..\..")).Path

Write-Host "=== Clean Workspace (PowerShell) ==="
Write-Host "  Project root: $ProjectRoot"
Write-Host ""

$removed = 0

function Remove-ItemSafe {
    param([string]$Path)
    if (Test-Path $Path) {
        $isDir = (Get-Item $Path).PSIsContainer
        $label = if ($isDir) { "DIR " } else { "FILE" }
        Write-Host "  Removing ${label}: $Path"
        Remove-Item -Path $Path -Recurse -Force
        $script:removed++
    }
}

$topDirs = @("build", "bin", "target", "bundle", ".cache")
foreach ($d in $topDirs) {
    Remove-ItemSafe (Join-Path $ProjectRoot $d)
}

Get-ChildItem -Path $ProjectRoot -Directory -Filter "cmake-build-*" -ErrorAction SilentlyContinue |
    ForEach-Object { Remove-ItemSafe $_.FullName }

# Recursive __pycache__ cleanup (skip third_party)
Get-ChildItem -Path $ProjectRoot -Directory -Recurse -Filter "__pycache__" -ErrorAction SilentlyContinue |
    Where-Object { $_.FullName -notlike "*\third_party\*" } |
    ForEach-Object { Remove-ItemSafe $_.FullName }

# Recursive .pyc / .pyo cleanup (skip third_party)
Get-ChildItem -Path $ProjectRoot -File -Recurse -Include "*.pyc", "*.pyo" -ErrorAction SilentlyContinue |
    Where-Object { $_.FullName -notlike "*\third_party\*" } |
    ForEach-Object { Remove-ItemSafe $_.FullName }

Write-Host ""
if ($removed -eq 0) {
    Write-Host "  Nothing to clean - workspace is already tidy."
} else {
    Write-Host "  Removed $removed item(s)."
}
