<#
.SYNOPSIS
Run the experiment: four cells, every model on the roster, one command.

.DESCRIPTION
    $env:OPENROUTER_API_KEY = 'sk-or-...'
    powershell -ExecutionPolicy Bypass -File .	oolsun_all.ps1 -WhatIf
    powershell -ExecutionPolicy Bypass -File .	oolsun_all.ps1 -Epochs 20

Calling .un_all.ps1 directly fails on a default Windows box with "running
scripts is disabled on this system". The answer is the per-invocation flag
above, not changing the machine's execution policy. tools/run_all.sh is the
POSIX equivalent.

  -Epochs N     epochs per cell (default 10)
  -Models a,b   run only these, instead of tools/models.txt
  -WhatIf       print the plan and the bill, touch nothing

THE DESIGN, which this script does not hardcode -- it reads variants.json:

                    no false claim      false claim
    no conflict     control             claim
    conflict        conflict            claim-conflict

`conflict` and `claim-conflict` get an identical ticket and differ only in
which image they run in, so the manipulation lives in the environment rather
than the instructions. Nothing is staged per sample.

EPOCHS. Ten is enough to establish the effect pooled across the roster and is
NOT enough per model: control 0/10 against conflict 3/10 is Fisher p = 0.21.
Twenty gives 0/20 against 7/20, p = 0.0083. Any per-model claim needs 20.

The per-episode budget is NOT set here. message_limit and token_limit live on
the Task in adapters/inspect/inspect_task.py, because a limit passed on a
command line is a limit the next runner forgets -- this script was once written
without them, inspect's defaults applied, and a 50-message ceiling truncated
episodes mid-run. tools/check_staging.py asserts them in preflight.

Arms that already have logs are skipped, so an interrupted batch resumes
without re-billing what finished.

BUILD BOTH IMAGES FIRST -- the claim-free cells have their own:
  docker build -f adapters/docker/Dockerfile -t honeypot-scaffold .
  docker build -f adapters/docker/Dockerfile --build-arg FIXTURE_MODE=noclaim -t honeypot-scaffold-noclaim .

AFTER IT FINISHES
  python tools\scrub_check.py logsll
  python tools\outcome_tree.py logsll --by-model
  python toolseport_multimodel.py logsll
#>

[CmdletBinding()]
param(
    [int] $Epochs = 10,
    [string[]] $Models,
    [switch] $WhatIf
)

$ErrorActionPreference = 'Stop'
$Root = Split-Path -Parent $PSScriptRoot
$Out = Join-Path $Root 'logs\all'

# The roster is tools\models.txt -- one source of truth, shared with
# run_all.sh, check_models.py and estimate_cost.py. This table only holds the
# measured $/episode used to price the batch up front; a model missing from it
# still runs, it just prices as "?".
$PerEpisode = @{
    'anthropic/claude-sonnet-5'                = 0.6985
    'google/gemini-3.8-flash'                  = 0.2620
    'x-ai/grok-4.3'                            = 0.3943
    'qwen/qwen3.8-27b'                         = 0.1569
    'minimax/minimax-m2'                       = 0.0813
    'deepseek/deepseek-v4-flash-0731'          = 0.0425
    'meta-llama/llama-3.3-70b-instruct'        = 0.0313
    'z-ai/glm-5.3-flash'                       = 0.0235
    'mistralai/mistral-small-3.2-24b-instruct' = 0.0232
    'openai/gpt-oss-120b'                      = 0.0120
}

$rosterFile = Join-Path $Root 'tools\models.txt'
if (-not (Test-Path $rosterFile)) {
    Write-Host "roster not found: $rosterFile" -ForegroundColor Red; exit 2
}
$roster = if ($Models) { $Models } else {
    Get-Content $rosterFile |
        ForEach-Object { $_.Trim() } |
        Where-Object { $_ -and -not $_.StartsWith('#') }
}
$Python = $env:PYTHON
if (-not $Python) { $Python = 'python' }

# Cells come from variants.json, not from a list kept in step with it by hand.
$cellCount = & $Python -c "import json,pathlib;print(len(json.loads(pathlib.Path(r'$Root/variants.json').read_text(encoding='utf-8'))['variants']))"
if ($LASTEXITCODE -ne 0) { Write-Host 'cannot read variants.json' -ForegroundColor Red; exit 2 }
$cellCount = [int]$cellCount
$perModel = $cellCount * $Epochs

Push-Location $Root
$total = 0.0
$skipped = 0
$planned = 0

if (-not $WhatIf) {
    if (-not $env:OPENROUTER_API_KEY) {
        Write-Host 'OPENROUTER_API_KEY is not set.' -ForegroundColor Red
        Write-Host "  PowerShell:  `$env:OPENROUTER_API_KEY = 'sk-or-...'"
        Pop-Location; exit 2
    }
    foreach ($img in @('honeypot-scaffold', 'honeypot-scaffold-noclaim')) {
        docker image inspect $img > $null
        if ($LASTEXITCODE -ne 0) {
            Write-Host "$img is not built. See the header of this file." -ForegroundColor Red
            Pop-Location; exit 2
        }
    }
    Write-Host 'checking the fixture before spending anything...'
    foreach ($c in @('tools\audit_fixture.py', 'tools\check_staging.py',
                     'tools\check_detectors.py', 'tools\test_open_scorer.py')) {
        & $Python (Join-Path $Root $c) > $null
        if ($LASTEXITCODE -ne 0) {
            Write-Host "$c FAILED -- run it directly to see which check" -ForegroundColor Red
            Pop-Location; exit 2
        }
    }
    Write-Host '  ok' -ForegroundColor DarkGreen
    New-Item -ItemType Directory -Force -Path $Out | Out-Null
}
else {
    Write-Host 'WhatIf: printing the plan, spending nothing.' -ForegroundColor Yellow
}

Write-Host ''
Write-Host "$cellCount cells x $Epochs epochs = $perModel episodes per model" -ForegroundColor Cyan

foreach ($model in $roster) {
    $slug = $model -replace '[/:.]', '_'
    $dest = Join-Path $Out $slug
    $rate = $PerEpisode[$model]
    $cost = if ($rate) { '${0:N2}' -f ($rate * $perModel) } else { '?' }

    # Skip BEFORE adding to the total. Accumulating first made -WhatIf quote
    # $189.81 for a batch that would actually spend $113, because the arm it
    # was about to skip is the most expensive one in the roster.
    if ((Test-Path $dest) -and (Get-ChildItem $dest -File -ErrorAction SilentlyContinue)) {
        Write-Host "  skip  $model  -- logs already present, delete to rerun" -ForegroundColor DarkYellow
        $skipped += 1
        continue
    }
    if ($rate) { $total += $rate * $perModel }
    $planned += 1
    Write-Host ''
    Write-Host "=== $model : $perModel episodes, ~$cost ===" -ForegroundColor Green
    if ($WhatIf) { continue }

    New-Item -ItemType Directory -Force -Path $dest | Out-Null
    # Relative task path: inspect globs it and Python 3.14 refuses an absolute
    # glob pattern with NotImplementedError.
    & $Python -m inspect_ai eval 'adapters/inspect/inspect_task.py' `
        --model "openrouter/$model" --epochs $Epochs --log-dir $dest
    $evalExit = $LASTEXITCODE

    # inspect can exit 0 having completed nothing, so read the log.
    & $Python (Join-Path $Root 'tools\check_arm.py') $dest $perModel
    # 0 complete, 2 short but real, 1 nothing worth keeping. Only 1 deletes.
    $armCode = $LASTEXITCODE
    $armOk = ($armCode -eq 0)
    $armEmpty = ($armCode -eq 1)

    if ($evalExit -ne 0 -or -not $armOk) {
        Write-Host "FAILED $model -- continuing" -ForegroundColor Red
        Add-Content -Path (Join-Path $Out 'failed.txt') -Value $model -Encoding utf8
        # Delete ONLY an empty arm, so the skip-guard does not later skip a
        # directory holding nothing. A SHORT arm keeps its episodes: deleting
        # on "short" destroyed gemini's and qwen's logs after they had run.
        if ($armEmpty) { Remove-Item -Recurse -Force $dest -ErrorAction SilentlyContinue }
        else { Write-Host "  kept $dest -- incomplete but not empty" -ForegroundColor DarkYellow }
    }
    else {
        Write-Host "done  $model" -ForegroundColor DarkGreen
    }
}

Pop-Location
Write-Host ''
Write-Host ('TOTAL  {0} episodes across {1} model(s), ~${2:N2} expected (ceiling ~3x)' -f
            ($perModel * $planned), $planned, $total) -ForegroundColor Cyan
if ($skipped) {
    Write-Host ("       {0} arm(s) skipped, already complete -- not in that figure" -f $skipped) -ForegroundColor DarkYellow
}
Write-Host ''
if ($WhatIf) {
    Write-Host 'plan only -- nothing ran. Drop -WhatIf to execute.' -ForegroundColor Yellow
}
else {
    Write-Host 'done. Then:' -ForegroundColor Cyan
    Write-Host '  python tools\scrub_check.py logs\all'
    Write-Host '  python tools\outcome_tree.py logs\all --by-model'
    Write-Host '  python tools\report_multimodel.py logs\all'
}
