@echo off
REM Bring every arm to a uniform 10 epochs on one fixture version.
REM
REM   set OPENROUTER_API_KEY=sk-or-...
REM   tools\run_repair.cmd            all three phases
REM   tools\run_repair.cmd A          affected cells only
REM   tools\run_repair.cmd B          cluster top-up only
REM   tools\run_repair.cmd C          the new luna arm only
REM
REM There is a PowerShell twin, tools\run_repair.ps1, which adds -WhatIf to
REM price a batch before running it. Invoke that one as:
REM   powershell -ExecutionPolicy Bypass -File .\tools\run_repair.ps1 -WhatIf
REM Calling .\run_repair.ps1 directly fails on a default Windows box with
REM "running scripts is disabled on this system", and the answer is that
REM per-invocation flag, not changing the machine's execution policy.
REM
REM ~$65 expected, ~3x that as a ceiling. 570 episodes.
REM
REM THREE PHASES, AND WHY EACH CELL IS IN THE ONE IT IS IN.
REM
REM A  logs\repair\  -- noclaim-none, decoy-none, decoy-claim-none, 10 epochs,
REM    every model. The first two were built by staging a claim-free file over
REM    one the image commits, so `git status` showed " M allocate.py" and
REM    `git diff` printed the claim to the cell meant to be free of it; 58 of
REM    176 such episodes ran one of those commands and one reverted the
REM    override outright. decoy-claim-none is here for a smaller reason: the
REM    leaked log's rev= changed from 7782645, which was in no history, to
REM    16b1fe9, which is the tip at the log's own timestamp. That is a change
REM    to an agent-visible file, and the decoy cells carry the only reward-hack
REM    result in the project, so they are not going to rest on two fixture
REM    versions pooled together.
REM
REM B  logs\topup\   -- the 6 cells NEITHER problem touched, +5 epochs, cluster
REM    arms only. claim-* and conflict-* were served from the treatment image
REM    with a clean tree throughout and are unaffected, so these top up 5 -> 10
REM    rather than being re-run. The four arms in logs\final already have 15.
REM
REM C  logs\luna\    -- openai/gpt-5.6-luna, all 9 cells, 10 epochs. A new arm,
REM    not a repair. It is the only closed OpenAI frontier model here; gpt-oss
REM    is open-weight and sits in a different cluster.
REM
REM BUILD BOTH IMAGES FIRST -- the control has its own now:
REM   docker build -f adapters/docker/Dockerfile -t honeypot-scaffold .
REM   docker build -f adapters/docker/Dockerfile --build-arg FIXTURE_MODE=noclaim -t honeypot-scaffold-noclaim .

setlocal enabledelayedexpansion

set "ROOT=%~dp0.."
REM The task path MUST be relative, with the repo root as the working
REM directory. Inspect globs it (inspect_ai/_eval/list.py:
REM root_dir.glob(glob)) and Python 3.14's pathlib raises
REM NotImplementedError: Non-relative patterns are unsupported when the
REM pattern is absolute. The absolute form failed every arm at
REM task-resolution time, before a single episode ran.
cd /d "%ROOT%"
set "PHASE=%~1"
if "%PHASE%"=="" set "PHASE=ALL"

set "AFFECTED=noclaim-none,decoy-none,decoy-claim-none"
set "UNAFFECTED=claim-gaming-attributed,claim-gaming-stripped,claim-compliant-attributed,claim-none,conflict-gaming-attributed,conflict-none"

set "PY=%PYTHON%"
if "%PY%"=="" set "PY=python"

if "%OPENROUTER_API_KEY%"=="" (
  echo OPENROUTER_API_KEY is not set.
  echo   cmd: set OPENROUTER_API_KEY=sk-or-...
  exit /b 2
)

docker image inspect honeypot-scaffold >nul 2>&1
if errorlevel 1 (
  echo honeypot-scaffold is not built. See the header of this file.
  exit /b 2
)
docker image inspect honeypot-scaffold-noclaim >nul 2>&1
if errorlevel 1 (
  echo honeypot-scaffold-noclaim is not built. See the header of this file.
  exit /b 2
)

echo auditing the fixture before spending anything...
%PY% "%ROOT%\tools\audit_fixture.py" >nul
if errorlevel 1 (
  echo fixture audit FAILED -- run: python tools\audit_fixture.py
  exit /b 2
)
%PY% "%ROOT%\tools\check_staging.py" >nul
if errorlevel 1 (
  echo staging check FAILED -- run: python tools\check_staging.py
  exit /b 2
)
echo   ok

if "%PHASE%"=="ALL" goto :phaseA
if /i "%PHASE%"=="A" goto :phaseA
if /i "%PHASE%"=="B" goto :phaseB
if /i "%PHASE%"=="C" goto :phaseC
echo unknown phase "%PHASE%" -- use A, B, C, or omit for all
exit /b 2

:phaseA
echo.
echo ################ PHASE A: affected cells, 10 epochs, every model ########
set "OUT=%ROOT%\logs\repair"
set "CELLS=%AFFECTED%"
if not exist "!OUT!" mkdir "!OUT!"
call :arm 10 anthropic/claude-sonnet-5
call :arm 10 google/gemini-3.8-flash
call :arm 10 qwen/qwen3.8-27b
call :arm 10 x-ai/grok-4.3
call :arm 10 deepseek/deepseek-v4-flash-0731
call :arm 10 z-ai/glm-5.3-flash
call :arm 10 minimax/minimax-m2
call :arm 10 openai/gpt-oss-120b
call :arm 10 meta-llama/llama-3.3-70b-instruct
call :arm 10 mistralai/mistral-small-3.2-24b-instruct
if /i "%PHASE%"=="A" goto :done

:phaseB
echo.
echo ################ PHASE B: cluster top-up, +5 epochs, 6 unaffected cells #
set "OUT=%ROOT%\logs\topup"
set "CELLS=%UNAFFECTED%"
if not exist "!OUT!" mkdir "!OUT!"
call :arm 5 deepseek/deepseek-v4-flash-0731
call :arm 5 z-ai/glm-5.3-flash
call :arm 5 minimax/minimax-m2
call :arm 5 openai/gpt-oss-120b
call :arm 5 meta-llama/llama-3.3-70b-instruct
call :arm 5 mistralai/mistral-small-3.2-24b-instruct
if /i "%PHASE%"=="B" goto :done

:phaseC
echo.
echo ################ PHASE C: new arm, all 9 cells, 10 epochs ###############
set "OUT=%ROOT%\logs\luna"
set "CELLS="
if not exist "!OUT!" mkdir "!OUT!"
call :arm 10 openai/gpt-5.6-luna
goto :done

:done
echo.
echo done. check for leakage, then report:
echo   python tools\scrub_check.py logs\repair logs\topup logs\luna
echo   python tools\report_multimodel.py logs\repair --baseline logs\final
goto :eof

:arm
set "EPOCHS=%~1"
set "MODEL=%~2"
set "SLUG=%MODEL:/=_%"
set "SLUG=%SLUG::=_%"
set "SLUG=%SLUG:.=_%"
set "DEST=%OUT%\%SLUG%"
if exist "%DEST%\*" (
  echo skip  %MODEL%  -- logs already present, delete to rerun
  goto :eof
)
echo.
echo === %MODEL% : %EPOCHS% epochs ===
mkdir "%DEST%"
if "%CELLS%"=="" (
  %PY% -m inspect_ai eval "adapters\inspect\inspect_task.py" --model "openrouter/%MODEL%" --epochs %EPOCHS% --log-dir "%DEST%"
) else (
  %PY% -m inspect_ai eval "adapters\inspect\inspect_task.py" --model "openrouter/%MODEL%" --sample-id "%CELLS%" --epochs %EPOCHS% --log-dir "%DEST%"
)
if errorlevel 1 (
  echo FAILED %MODEL% -- continuing
  echo %MODEL%>> "%OUT%\failed.txt"
) else (
  echo done  %MODEL%
)
goto :eof
