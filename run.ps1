<#
Run the experiment: every cell, every model in models.txt, one command.

    $env:OPENROUTER_API_KEY = 'sk-or-...'
    powershell -ExecutionPolicy Bypass -File .\run.ps1 -WhatIf
    powershell -ExecutionPolicy Bypass -File .\run.ps1 -Epochs 20

-Epochs N     epochs per cell (default 20)
-Models a,b   run only these
-Append       add N more epochs to an arm that already has logs, instead of
              skipping it. The new run lands as a second .eval file in the same
              directory and report.py reads them together.
-WhatIf       print the plan and stop. Price it with: python cost.py --epochs N

Build both images first:
    docker build -f adapters/docker/Dockerfile -t honeypot-scaffold .
    docker build -f adapters/docker/Dockerfile --build-arg FIXTURE_MODE=noclaim -t honeypot-scaffold-noclaim .

An arm whose logs already exist is skipped, so an interrupted batch resumes.
#>
[CmdletBinding()]
param([int] $Epochs = 20, [string[]] $Models, [switch] $Append, [switch] $WhatIf)

$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot
$Out = 'logs\all'
$Python = if ($env:PYTHON) { $env:PYTHON } else { 'python' }

# inspect can exit 0 having run nothing, so what landed is counted, not trusted.
function Count-Episodes([string] $dir) {
    [int](& $Python -c "
import glob
from inspect_ai.log import read_eval_log
print(sum(1 for f in glob.glob(r'$dir/*.eval') for s in (read_eval_log(f).samples or []) if not s.error))")
}

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
    # The key's own spend counter, before and after every arm, so the ledger
    # shows what OpenRouter actually billed next to what the tokens compute to.
    & $Python cost.py --billed --note 'before batch' --ledger (Join-Path $Out 'ledger.txt')
}

foreach ($model in $roster) {
    $dest = Join-Path $Out ($model -replace '[/:.]', '_')
    $before = 0
    if ((Test-Path $dest) -and (Get-ChildItem $dest -File -ErrorAction SilentlyContinue)) {
        if (-not $Append) {
            Write-Host "skip  $model  (logs present; -Append to add epochs)" -ForegroundColor DarkYellow
            continue
        }
        if (-not $WhatIf) { $before = Count-Episodes $dest }
    }
    Write-Host "=== $model ===" -ForegroundColor Green
    if ($WhatIf) { continue }

    New-Item -ItemType Directory -Force -Path $dest | Out-Null
    # The task path must be relative: Inspect globs it, and Python 3.14 rejects
    # an absolute glob.
    & $Python -m inspect_ai eval 'adapters/inspect/inspect_task.py' `
        --model "openrouter/$model" --epochs $Epochs --log-dir $dest

    $n = Count-Episodes $dest
    $new = $n - $before
    if ($new -eq 0) {
        Write-Host "FAILED $model -- no new episodes" -ForegroundColor Red
        Add-Content (Join-Path $Out 'failed.txt') $model
        # An empty directory would be skipped next time; one with earlier logs stays.
        if ($before -eq 0) { Remove-Item -Recurse -Force $dest -ErrorAction SilentlyContinue }
    } elseif ($new -lt $perModel) {
        Write-Host "SHORT  $model -- $new of $perModel new, kept ($n total)" -ForegroundColor DarkYellow
        Add-Content (Join-Path $Out 'failed.txt') $model
    } else {
        Write-Host "done   $model -- $new new episodes, $n total" -ForegroundColor DarkGreen
    }
    & $Python cost.py --billed --note "after $model" --ledger (Join-Path $Out 'ledger.txt')
}

if ($WhatIf) { Write-Host "`nplan only. Price it:  $Python cost.py --epochs $Epochs" }
else {
    Write-Host ''
    & $Python cost.py --spent $Out
    Write-Host "`nthen:  $Python scrub.py $Out; $Python report.py $Out"
}
