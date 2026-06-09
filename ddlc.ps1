<#
.SYNOPSIS
    DDLC After Story - Project Toolbox (Windows PowerShell)

.DESCRIPTION
    Unified command-line interface for all project tools.

.PARAMETER Command
    The command to execute:
      detect         - Check toolchain completeness
      build-content  - Build game content (sprites, BG, audio)
      build          - Configure + compile the game
      run            - Build and launch the game
      bundle         - Full packaging pipeline
      clean          - Remove build artifacts and caches
      clean-all      - Remove everything including content/
      help           - Show this help message

.EXAMPLE
    .\ddlc.ps1 detect
    .\ddlc.ps1 build
    .\ddlc.ps1 bundle --skip-check
#>

param(
    [Parameter(Position = 0)]
    [string]$Command = "help",

    [Parameter(Position = 1, ValueFromRemainingArguments = $true)]
    [string[]]$ExtraArgs = @()
)

$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ProjectRoot

$Python = if ($env:PYTHON) { $env:PYTHON } else { "python" }
$BuildDir = if ($env:BUILD_DIR) { $env:BUILD_DIR } else { "build" }
$BuildType = if ($env:BUILD_TYPE) { $env:BUILD_TYPE } else { "Release" }
$Jobs = if ($env:JOBS) { $env:JOBS } else {
    (Get-CimInstance Win32_Processor -ErrorAction SilentlyContinue |
        Measure-Object -Property NumberOfLogicalProcessors -Sum).Sum
    if (-not $?) { 2 }
}

function Write-Header {
    Write-Host ""
    Write-Host "  ╔══════════════════════════════════════════════════════╗" -ForegroundColor Cyan
    Write-Host "  ║        DDLC After Story — Project Toolbox           ║" -ForegroundColor Cyan
    Write-Host "  ╚══════════════════════════════════════════════════════╝" -ForegroundColor Cyan
    Write-Host ""
}

function Show-Help {
    Write-Header
    Write-Host "  Usage: " -NoNewline
    Write-Host ".\ddlc.ps1 <command> [args...]" -ForegroundColor White
    Write-Host ""
    Write-Host "  Commands:" -ForegroundColor White
    Write-Host "    detect         " -ForegroundColor Green -NoNewline
    Write-Host "Check toolchain completeness"
    Write-Host "    build-content  " -ForegroundColor Green -NoNewline
    Write-Host "Build game content (sprites, BG, audio)"
    Write-Host "    build          " -ForegroundColor Green -NoNewline
    Write-Host "Configure + compile the game"
    Write-Host "    run            " -ForegroundColor Green -NoNewline
    Write-Host "Build and launch the game"
    Write-Host "    bundle         " -ForegroundColor Green -NoNewline
    Write-Host "Full packaging pipeline"
    Write-Host "    clean          " -ForegroundColor Green -NoNewline
    Write-Host "Remove build artifacts and caches"
    Write-Host "    clean-all      " -ForegroundColor Green -NoNewline
    Write-Host "Remove everything including content/"
    Write-Host ""
    Write-Host "  Environment:" -ForegroundColor White
    Write-Host "    `$env:PYTHON      Python executable  (default: python)"
    Write-Host "    `$env:BUILD_DIR   Build directory     (default: build)"
    Write-Host "    `$env:BUILD_TYPE  CMake build type    (default: Release)"
    Write-Host "    `$env:JOBS        Parallel jobs       (default: auto)"
    Write-Host ""
}

function Invoke-Detect {
    Write-Host "Running toolchain detection..." -ForegroundColor Cyan
    & $Python tools/compile/detection.py @ExtraArgs
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}

function Invoke-BuildContent {
    Write-Host "Building game content..." -ForegroundColor Cyan
    & $Python tools/build_content.py @ExtraArgs
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}

function Invoke-Build {
    Write-Host "Configuring CMake..." -ForegroundColor Cyan

    $cmakeArgs = @("-S", ".", "-B", $BuildDir, "-DCMAKE_BUILD_TYPE=$BuildType")

    if (Get-Command ninja -ErrorAction SilentlyContinue) {
        $cmakeArgs += @("-G", "Ninja")
    }

    & cmake @cmakeArgs
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

    Write-Host "Building ($Jobs jobs)..." -ForegroundColor Cyan
    & cmake --build $BuildDir --config $BuildType --parallel $Jobs
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

    Write-Host "Build complete!" -ForegroundColor Green
}

function Invoke-Run {
    Invoke-Build

    $exe = Join-Path $BuildDir "bin\ddlc_afterstory.exe"
    if (-not (Test-Path $exe)) {
        $found = Get-ChildItem -Path $BuildDir -Recurse -Filter "ddlc_afterstory.exe" -ErrorAction SilentlyContinue | Select-Object -First 1
        if ($found) { $exe = $found.FullName }
    }

    if (-not (Test-Path $exe)) {
        Write-Host "ERROR: Executable not found after build." -ForegroundColor Red
        exit 1
    }

    Write-Host "Launching: $exe" -ForegroundColor Green
    & $exe
}

function Invoke-Bundle {
    Write-Host "Starting packaging pipeline..." -ForegroundColor Cyan
    & $Python tools/bundle/package.py --build-type $BuildType --jobs $Jobs @ExtraArgs
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}

function Invoke-Clean {
    Write-Host "Cleaning workspace..." -ForegroundColor Cyan
    & $Python tools/clean/clean.py @ExtraArgs
}

function Invoke-CleanAll {
    Write-Host "Cleaning workspace (including content/)..." -ForegroundColor Yellow
    & $Python tools/clean/clean.py --all @ExtraArgs
}

switch ($Command.ToLower()) {
    "detect"        { Invoke-Detect }
    "build-content" { Invoke-BuildContent }
    "build"         { Invoke-Build }
    "run"           { Invoke-Run }
    "bundle"        { Invoke-Bundle }
    "clean"         { Invoke-Clean }
    "clean-all"     { Invoke-CleanAll }
    { $_ -in "help", "--help", "-h" } { Show-Help }
    default {
        Write-Host "Unknown command: $Command" -ForegroundColor Red
        Write-Host "Run '.\ddlc.ps1 help' for usage."
        exit 1
    }
}
