@echo off
REM Windows equivalent of tools/preflight.sh.  Run:  tools\preflight.cmd
setlocal EnableDelayedExpansion
set FRONTEND_BAD=0

where docker >nul 2>&1
if errorlevel 1 (echo docker                             MISSING) else (
  for /f "tokens=1,2 delims=," %%v in ('docker --version') do echo docker                             %%v
)

docker info >nul 2>&1
if errorlevel 1 (
  echo docker daemon                      NOT RUNNING -- start Docker Desktop
) else (
  echo docker daemon                      running
)

REM The scaffold pins a buildkit frontend fetched from Docker Hub. It exists
REM only for COPY --chmod, which modern buildkit supports natively.
docker pull -q docker/dockerfile:1.4 >nul 2>&1
if errorlevel 1 (
  echo buildkit frontend                  UNREACHABLE -- see note below
  set FRONTEND_BAD=1
) else (
  echo buildkit frontend                  reachable
)

set INSPECT_V=
for /f "delims=" %%v in ('python -c "import inspect_ai; print(inspect_ai.__version__)" 2^>nul') do set INSPECT_V=%%v
if "!INSPECT_V!"=="" (
  echo inspect-ai                         MISSING -- pip install inspect-ai
) else (
  echo inspect-ai                         !INSPECT_V!
)

if defined ANTHROPIC_API_KEY (
  echo provider api key                   set
) else if defined OPENAI_API_KEY (
  echo provider api key                   set
) else (
  echo provider api key                   unset -- needed only to run an episode
)

echo.
if "!FRONTEND_BAD!"=="1" (
  echo The frontend pin on line 1 of adapters\docker\Dockerfile is unreachable.
  echo It is inherited from the scaffold and buys nothing on modern Docker.
  echo To drop it:
  echo.
  echo     powershell -Command "(Get-Content adapters\docker\Dockerfile ^| Select-Object -Skip 1) ^| Set-Content adapters\docker\Dockerfile"
  echo.
)
endlocal
exit /b 0
