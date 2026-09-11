<#
Run the experiment: every cell, every model in models.txt, one command.

    $env:OPENROUTER_API_KEY = 'sk-or-...'
    powershell -ExecutionPolicy Bypass -File .\run.ps1 -WhatIf
    powershell -ExecutionPolicy Bypass -File .\run.ps1 -Epochs 20

-Epochs N     epochs per cell (default 20)
-Models a,b   run only these
-WhatIf       print the plan and stop. Price it with: python cost.py --epochs N

Build both images first:
    docker build -f adapters/docker/Dockerfile -t honeypot-scaffold .
    docker build -f adapters/docker/Dockerfile --build-arg FIXTURE_MODE=noclaim -t honeypot-scaffold-noclaim .

An arm whose logs already exist is skipped, so an interrupted batch resumes.
#>
[CmdletBinding()]
param([int] $Epochs = 20, [string[]] $Models, [switch] $WhatIf)

$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot
$Out = 'logs\all'
$Python = if ($env:PYTHON) { $env:PYTHON } else { 'python' }

$roster = if ($Models) { $Models } else {
    Get-Content models.txt | ForEach-Object { $_.Trim() } | Where-Object { $_ -and -not $_.StartsWith('#') }
}
$cells = [int](& $Python -c "import json;print(len(json.load(open('variants.json'))['variants']))")
$perModel = $cells * $Epochs
Write-Host "$cells cells x $Epochs epochs = $perModel episodes per model"

if (-not $WhatIf) {
    if (-not $env:OPENROUTER_API_KEY) { Write-Host 'OPENROUTER_API_KEY is not set' -ForegroundColor Red; exit 2 }
    foreach ($img in 'honeypot-scaffold', 'honeypot-scaffold-noclaim') {
        docker image inspect $img > $null
        if ($LASTEXITCODE -ne 0) { Write-Host "$img is not built" -ForegroundColor Red; exit 2 }
    }
    & $Python check.py > $null
    if ($LASTEXITCODE -ne 0) { Write-Host 'check.py failed -- run it to see why' -ForegroundColor Red; exit 2 }
    New-Item -ItemType Directory -Force -Path $Out | Out-Null
}

foreach ($model in $roster) {
    $dest = Join-Path $Out ($model -replace '[/:.]', '_')
    if ((Test-Path $dest) -and (Get-ChildItem $dest -File -ErrorAction SilentlyContinue)) {
        Write-Host "skip  $model  (logs present)" -ForegroundColor DarkYellow
        continue
    }
    Write-Host "=== $model ===" -ForegroundColor Green
    if ($WhatIf) { continue }

    New-Item -ItemType Directory -Force -Path $dest | Out-Null
    # The task path must be relative: Inspect globs it, and Python 3.14 rejects
    # an absolute glob.
    & $Python -m inspect_ai eval 'adapters/inspect/inspect_task.py' `
        --model "openrouter/$model" --epochs $Epochs --log-dir $dest

    # inspect can exit 0 having run nothing, so count what actually landed.
    # Nothing at all: delete the directory so the skip above does not skip it.
    $n = [int](& $Python -c "
import glob
from inspect_ai.log import read_eval_log
print(sum(1 for f in glob.glob(r'$dest/*.eval') for s in (read_eval_log(f).samples or []) if not s.error))")
    if ($n -eq 0) {
        Write-Host "FAILED $model -- no episodes" -ForegroundColor Red
        Add-Content (Join-Path $Out 'failed.txt') $model
        Remove-Item -Recurse -Force $dest -ErrorAction SilentlyContinue
    } elseif ($n -lt $perModel) {
        Write-Host "SHORT  $model -- $n of $perModel, kept" -ForegroundColor DarkYellow
        Add-Content (Join-Path $Out 'failed.txt') $model
    } else {
        Write-Host "done   $model -- $n episodes" -ForegroundColor DarkGreen
    }
}

if ($WhatIf) { Write-Host "`nplan only. Price it:  $Python cost.py --epochs $Epochs" }
else { Write-Host "`nthen:  $Python scrub.py $Out; $Python report.py $Out" }
