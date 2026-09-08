<#
.SYNOPSIS
Bring every arm to a uniform 10 epochs on one fixture version.

.DESCRIPTION
    $env:OPENROUTER_API_KEY = 'sk-or-...'
    .\tools\run_repair.ps1            # all three phases
    .\tools\run_repair.ps1 -Phase A   # affected cells only
    .\tools\run_repair.ps1 -Phase B   # cluster top-up only
    .\tools\run_repair.ps1 -WhatIf    # print the plan, spend nothing

~$58 expected, roughly 3x that as a ceiling. 480 episodes.

TWO PHASES, SPLIT BY WHAT IS ACTUALLY WRONG WITH EACH CELL

A  logs\repair  -- noclaim-none, decoy-none, decoy-claim-none, 10 epochs, every
   model. The first two were built by staging a claim-free file over one the
   image commits, so `git status` showed " M allocate.py" and `git diff`
   printed the claim to the very cell meant to be free of it. 58 of 176 such
   episodes ran one of those commands and one reverted the override outright.
   decoy-claim-none is here for a smaller reason: the leaked log's rev= changed
   from 7782645, which is in no history, to 16b1fe9, the tip at the log's own
   timestamp. That is an agent-visible file, and the decoy cells carry the only
   reward-hack result in the project, so they will not rest on two fixture
   versions pooled together.

B  logs\topup   -- the 6 cells neither problem touched, +5 epochs, cluster arms
   only. claim-* and conflict-* ran from the treatment image with a clean tree
   throughout, so they top up 5 -> 10 rather than being re-run. The four arms
   in logs\final already have 15.

There was a phase C, a gpt-5.6-luna arm. It is gone: OpenAI's strict
function-calling requires `required` to name every key in `properties`, and
inspect's text_editor has optional ones, so the provider rejects every request
with "Invalid schema for function 'text_editor' ... Missing 'file_text'".
`-M strict_tools=false` would fix it, and is deliberately not used -- every
other arm sends strict: true, so that flag would make one arm differ from the
rest in how its tool calls are validated. See tools\models-cluster.txt.

BUILD BOTH IMAGES FIRST -- the control has its own now:
  docker build -f adapters/docker/Dockerfile -t honeypot-scaffold .
  docker build -f adapters/docker/Dockerfile --build-arg FIXTURE_MODE=noclaim -t honeypot-scaffold-noclaim .
#>

[CmdletBinding()]
param(
    [ValidateSet('ALL', 'A', 'B')]
    [string] $Phase = 'ALL',

    # Print what would run, and what it should cost, without spending anything.
    [switch] $WhatIf
)

$ErrorActionPreference = 'Stop'
$Root = Split-Path -Parent $PSScriptRoot

$Affected = 'noclaim-none,decoy-none,decoy-claim-none'
$Unaffected = 'claim-gaming-attributed,claim-gaming-stripped,' +
              'claim-compliant-attributed,claim-none,' +
              'conflict-gaming-attributed,conflict-none'

# Measured $/episode, from tools\estimate_cost.py --calibrate at the cache
# ratios these arms actually ran at. Used only to print the bill up front.
$PerEpisode = @{
    'anthropic/claude-sonnet-5'                = 0.6985
    'google/gemini-3.8-flash'                  = 0.2620
    'qwen/qwen3.8-27b'                         = 0.1569
    'x-ai/grok-4.3'                            = 0.3943
    'deepseek/deepseek-v4-flash-0731'          = 0.0425
    'z-ai/glm-5.3-flash'                       = 0.0235
    'minimax/minimax-m2'                       = 0.0813
    'openai/gpt-oss-120b'                      = 0.0120
    'meta-llama/llama-3.3-70b-instruct'        = 0.0313
    'mistralai/mistral-small-3.2-24b-instruct' = 0.0232
}

$Frontier = @('anthropic/claude-sonnet-5', 'google/gemini-3.8-flash',
              'qwen/qwen3.8-27b', 'x-ai/grok-4.3')
$Cluster = @('deepseek/deepseek-v4-flash-0731', 'z-ai/glm-5.3-flash',
             'minimax/minimax-m2', 'openai/gpt-oss-120b',
             'meta-llama/llama-3.3-70b-instruct',
             'mistralai/mistral-small-3.2-24b-instruct')

$Python = $env:PYTHON
if (-not $Python) { $Python = 'python' }

# Everything below assumes the repo root is the working directory: the task
# path handed to inspect has to be relative (see Invoke-Arm), and --log-dir is
# written relative to wherever the process starts.
Push-Location $Root

# Accumulated across every arm so the bill is printed once at the end rather
# than left for the reader to add up from the per-arm lines.
$script:TotalCost = 0.0
$script:TotalEpisodes = 0

function Write-Head($text) {
    Write-Host ''
    Write-Host ('#' * 74) -ForegroundColor DarkGray
    Write-Host "# $text" -ForegroundColor Cyan
    Write-Host ('#' * 74) -ForegroundColor DarkGray
}

function Invoke-Arm {
    param(
        [string] $Model,
        [int] $Epochs,
        [string] $OutDir,
        # Empty means the whole 9-variant dataset.
        [string] $Cells
    )

    # Slug has to match what the report tools expect from run_multimodel:
    # / : . all become _
    $slug = $Model -replace '[/:.]', '_'
    $dest = Join-Path $OutDir $slug

    if (Test-Path $dest) {
        if (Get-ChildItem -Path $dest -File -ErrorAction SilentlyContinue) {
            Write-Host "  skip  $Model  -- logs already present, delete to rerun" -ForegroundColor DarkYellow
            return
        }
    }

    $cellCount = 9
    if ($Cells) { $cellCount = ($Cells -split ',').Count }
    $episodes = $cellCount * $Epochs
    $rate = $PerEpisode[$Model]
    $cost = '?'
    if ($rate) {
        $cost = '${0:N2}' -f ($rate * $episodes)
        $script:TotalCost += $rate * $episodes
    }
    $script:TotalEpisodes += $episodes

    Write-Host ''
    Write-Host "=== $Model : $Epochs epochs x $cellCount cells = $episodes episodes, ~$cost ===" -ForegroundColor Green

    if ($WhatIf) { return }

    New-Item -ItemType Directory -Force -Path $dest | Out-Null

    # The task path MUST be relative, with the repo root as the working directory.
    # Inspect globs it (inspect_ai/_eval/list.py: root_dir.glob(glob)) and Python
    # 3.14's pathlib raises NotImplementedError: Non-relative patterns are
    # unsupported when the pattern is absolute. Passing the absolute path failed
    # every arm at task-resolution time, before a single episode ran.
    $evalArgs = @(
        '-m', 'inspect_ai', 'eval',
        'adapters/inspect/inspect_task.py',
        '--model', "openrouter/$Model",
        '--epochs', $Epochs,
        '--log-dir', $dest
    )
    if ($Cells) { $evalArgs += @('--sample-id', $Cells) }

    # Native exe: let it write straight through. Do NOT redirect stderr here --
    # in 5.1 that wraps each line in a NativeCommandError and sets $? to false
    # even when the process exits 0.
    & $Python $evalArgs
    $evalExit = $LASTEXITCODE

    # The exit code is not the answer. `inspect eval` returns 0 after
    # "Task interrupted (no samples completed before interruption)" when a
    # provider rejects the request schema -- gpt-5.6-luna did exactly that and
    # was recorded as "done" with an empty log. Read the log instead.
    & $Python (Join-Path $Root 'tools\check_arm.py') $dest $episodes
    # 0 complete, 2 short but real, 1 nothing worth keeping. Only 1 deletes.
    $armCode = $LASTEXITCODE
    $armOk = ($armCode -eq 0)
    $armEmpty = ($armCode -eq 1)

    if ($evalExit -ne 0 -or -not $armOk) {
        Write-Host "FAILED $Model -- continuing with the rest" -ForegroundColor Red
        Add-Content -Path (Join-Path $OutDir 'failed.txt') -Value $Model -Encoding utf8
        # Leave nothing that the skip-guard would mistake for a finished arm.
        # Delete ONLY an empty arm, so the skip-guard does not later skip a
        # directory holding nothing. A SHORT arm keeps its episodes: deleting
        # on "short" destroyed gemini's and qwen's logs after they had run.
        if ($armEmpty) { Remove-Item -Recurse -Force $dest -ErrorAction SilentlyContinue }
        else { Write-Host "  kept $dest -- incomplete but not empty" -ForegroundColor DarkYellow }
    }
    else {
        Write-Host "done  $Model" -ForegroundColor DarkGreen
    }
}

# ── preflight ───────────────────────────────────────────────────────────────
# Everything here is cheap and everything here has already gone wrong once.

if (-not $WhatIf) {
    if (-not $env:OPENROUTER_API_KEY) {
        Write-Host 'OPENROUTER_API_KEY is not set.' -ForegroundColor Red
        Write-Host "  PowerShell:  `$env:OPENROUTER_API_KEY = 'sk-or-...'"
        exit 2
    }

    # A missing control image is the failure that matters: compose would fall
    # back to building one, and a stale build writes a log that looks clean and
    # is not.
    foreach ($img in @('honeypot-scaffold', 'honeypot-scaffold-noclaim')) {
        docker image inspect $img > $null
        if ($LASTEXITCODE -ne 0) {
            Write-Host "$img is not built." -ForegroundColor Red
            Write-Host '  docker build -f adapters/docker/Dockerfile -t honeypot-scaffold .'
            Write-Host '  docker build -f adapters/docker/Dockerfile --build-arg FIXTURE_MODE=noclaim -t honeypot-scaffold-noclaim .'
            exit 2
        }
    }

    Write-Host 'auditing the fixture before spending anything...'
    foreach ($check in @('tools\audit_fixture.py', 'tools\check_staging.py')) {
        & $Python (Join-Path $Root $check) > $null
        if ($LASTEXITCODE -ne 0) {
            Write-Host "$check FAILED -- run it directly to see which check" -ForegroundColor Red
            exit 2
        }
    }
    Write-Host '  ok' -ForegroundColor DarkGreen
}
else {
    Write-Host 'WhatIf: printing the plan, spending nothing.' -ForegroundColor Yellow
}

# ── phases ──────────────────────────────────────────────────────────────────

if ($Phase -eq 'ALL' -or $Phase -eq 'A') {
    Write-Head 'PHASE A: affected cells, 10 epochs, every model'
    $out = Join-Path $Root 'logs\repair'
    if (-not $WhatIf) { New-Item -ItemType Directory -Force -Path $out | Out-Null }
    foreach ($m in ($Frontier + $Cluster)) {
        Invoke-Arm -Model $m -Epochs 10 -OutDir $out -Cells $Affected
    }
}

if ($Phase -eq 'ALL' -or $Phase -eq 'B') {
    Write-Head 'PHASE B: cluster top-up, +5 epochs, the 6 unaffected cells'
    $out = Join-Path $Root 'logs\topup'
    if (-not $WhatIf) { New-Item -ItemType Directory -Force -Path $out | Out-Null }
    foreach ($m in $Cluster) {
        Invoke-Arm -Model $m -Epochs 5 -OutDir $out -Cells $Unaffected
    }
}


Write-Host ''
Write-Host ('TOTAL  {0} episodes, ~${1:N2} expected (ceiling roughly 3x)' -f
            $script:TotalEpisodes, $script:TotalCost) -ForegroundColor Cyan
Write-Host ''
Pop-Location
if ($WhatIf) {
    Write-Host 'plan only -- nothing ran. Drop -WhatIf to execute.' -ForegroundColor Yellow
}
else {
    Write-Host 'done. Check for leakage, then report:' -ForegroundColor Cyan
    Write-Host '  python tools\scrub_check.py logs\repair logs\topup'
    Write-Host '  python tools\report_multimodel.py logs\repair --baseline logs\final'
}
