@echo off
REM Run the existing fixture across the model roster (Windows).
REM
REM   set OPENROUTER_API_KEY=sk-or-...
REM   tools\run_multimodel.cmd [epochs] [roster]
REM
REM For a capped key use the budget roster (three non-Claude models, ~$10):
REM   tools\run_multimodel.cmd 10 tools\models-smoke.txt
REM Price it first: python tools\estimate_cost.py --roster <roster>
REM
REM Defaults to 10 epochs: 7 variants x 10 = 70 episodes per model.
REM The key is read from the environment and never echoed or written to disk.

setlocal enabledelayedexpansion

set "ROOT=%~dp0.."
set "EPOCHS=%~1"
if "%EPOCHS%"=="" set "EPOCHS=10"
set "ROSTER=%~2"
if "%ROSTER%"=="" set "ROSTER=%ROOT%\tools\models.txt"
set "OUT=%ROOT%\logs\multimodel"

REM Invoke the CLI as a module, not as the bare `inspect` console script.
REM pip installs that script into a Scripts\ directory that is frequently not
REM on PATH, which fails every model in the roster with "not recognized as an
REM internal or external command". `python -m inspect_ai` is the same entry
REM point (inspect_ai/__main__.py) and is guaranteed to resolve to whichever
REM interpreter actually has the package. Override with:  set PYTHON=py -3.11
set "PY=%PYTHON%"
if "%PY%"=="" set "PY=python"

if "%OPENROUTER_API_KEY%"=="" (
  echo OPENROUTER_API_KEY is not set.
  echo   cmd: set OPENROUTER_API_KEY=sk-or-...
  exit /b 2
)

echo validating roster...
%PY% "%ROOT%\tools\check_models.py" "%ROSTER%"
if errorlevel 1 (
  echo roster has unknown ids -- fix tools\models.txt before running.
  exit /b 2
)

if not exist "%OUT%" mkdir "%OUT%"

REM Comments and blanks are stripped by findstr BEFORE the loop. Doing it
REM inside the loop is unsafe: a ")" in a comment line closes the FOR block
REM early, and this roster's comments contain parentheses.
for /f "usebackq tokens=* delims= " %%M in (`findstr /v /r /c:"^ *#" /c:"^ *$" "%ROSTER%"`) do (
  set "LINE=%%M"
  set "LINE=!LINE: =!"
  if not "!LINE!"=="" (
    set "SLUG=!LINE:/=_!"
    set "SLUG=!SLUG::=_!"
    set "SLUG=!SLUG:.=_!"
    set "DEST=%OUT%\!SLUG!"

    if exist "!DEST!\*" (
      echo skip  !LINE!  -- logs already present, delete to rerun
    ) else (
      echo.
      echo === !LINE! : %EPOCHS% epochs ===
      if not exist "!DEST!" mkdir "!DEST!"
      %PY% -m inspect_ai eval "%ROOT%\adapters\inspect\inspect_task.py" --model "openrouter/!LINE!" --epochs %EPOCHS% --log-dir "!DEST!"
      if errorlevel 1 (
        echo FAILED !LINE! -- continuing with the rest of the roster
        echo !LINE!>> "%OUT%\failed.txt"
      ) else (
        echo done  !LINE!
      )
    )
  )
)

echo.
echo all models attempted. report with:
echo   python tools\report_multimodel.py logs\multimodel --baseline logs
endlocal
