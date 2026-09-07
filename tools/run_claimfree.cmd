@echo off
REM Re-run ONLY the claim-free cells, on the fixed control image.
REM
REM   set OPENROUTER_API_KEY=sk-or-...
REM   tools\run_claimfree.cmd
REM
REM WHY THIS EXISTS. noclaim-none and decoy-none were built by staging
REM fixture/allocate_noclaim.py over a file the image commits, so `git status`
REM showed " M allocate.py" and `git diff` printed the claim the cell is meant
REM to be free of. 58 of 176 claim-free episodes ran one of those commands, and
REM one -- the single targeted-the-key episode in the project -- ran
REM `git checkout allocate.py` and finished in a cell it had converted back to
REM claim-bearing. Those 176 episodes are unusable; the other 622 are unaffected,
REM because the leak only touched cells where docstring_claim is False.
REM
REM Epochs are matched to the batch each model already has, so the re-run drops
REM into the same denominators: 15 for the four frontier arms in logs/final,
REM 5 for the six cluster arms in logs/cluster.
REM
REM BUILD BOTH IMAGES FIRST -- the control now has its own:
REM   docker build -f adapters/docker/Dockerfile -t honeypot-scaffold .
REM   docker build -f adapters/docker/Dockerfile --build-arg FIXTURE_MODE=noclaim -t honeypot-scaffold-noclaim .
REM
REM ~$47 expected, ~$136 ceiling. Price it yourself before running:
REM   python tools\estimate_cost.py --calibrate logs\final --roster <roster>

setlocal enabledelayedexpansion

set "ROOT=%~dp0.."
set "OUT=%ROOT%\logs\claimfree"
set "CELLS=noclaim-none,decoy-none"

set "PY=%PYTHON%"
if "%PY%"=="" set "PY=python"

if "%OPENROUTER_API_KEY%"=="" (
  echo OPENROUTER_API_KEY is not set.
  echo   cmd: set OPENROUTER_API_KEY=sk-or-...
  exit /b 2
)

REM Refuse to run against a stale control image. The whole point of this batch
REM is the new one, and a silent fallback to the old behaviour would produce a
REM log that looks clean and is not.
docker image inspect honeypot-scaffold-noclaim >nul 2>&1
if errorlevel 1 (
  echo honeypot-scaffold-noclaim is not built. Build it first:
  echo   docker build -f adapters/docker/Dockerfile --build-arg FIXTURE_MODE=noclaim -t honeypot-scaffold-noclaim .
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

if not exist "%OUT%" mkdir "%OUT%"

call :arm 15 anthropic/claude-sonnet-5
call :arm 15 google/gemini-3.8-flash
call :arm 15 qwen/qwen3.8-27b
call :arm 15 x-ai/grok-4.3
call :arm 5 deepseek/deepseek-v4-flash-0731
call :arm 5 z-ai/glm-5.3-flash
call :arm 5 minimax/minimax-m2
call :arm 5 openai/gpt-oss-120b
call :arm 5 meta-llama/llama-3.3-70b-instruct
call :arm 5 mistralai/mistral-small-3.2-24b-instruct

echo.
echo all arms attempted. check for leakage, then report:
echo   python tools\scrub_check.py logs\claimfree
echo   python tools\report_multimodel.py logs\claimfree --baseline logs\final
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
echo === %MODEL% : %CELLS% x %EPOCHS% epochs ===
mkdir "%DEST%"
%PY% -m inspect_ai eval "%ROOT%\adapters\inspect\inspect_task.py" --model "openrouter/%MODEL%" --sample-id "%CELLS%" --epochs %EPOCHS% --log-dir "%DEST%"
if errorlevel 1 (
  echo FAILED %MODEL% -- continuing
  echo %MODEL%>> "%OUT%\failed.txt"
) else (
  echo done  %MODEL%
)
goto :eof
