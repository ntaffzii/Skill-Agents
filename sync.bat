@echo off
setlocal
chcp 65001 >nul

set "REPO_ROOT=%~dp0"
set "SCRIPT_PATH=%REPO_ROOT%scripts\sync_skills.py"

if exist "%REPO_ROOT%.venv\Scripts\python.exe" (
    "%REPO_ROOT%.venv\Scripts\python.exe" -c "import sys" >nul 2>&1
    if not errorlevel 1 (
        "%REPO_ROOT%.venv\Scripts\python.exe" "%SCRIPT_PATH%" %*
        goto :done
    )
)

where py >nul 2>&1
if not errorlevel 1 (
    py -3 -c "import sys" >nul 2>&1
    if not errorlevel 1 (
        py -3 "%SCRIPT_PATH%" %*
        goto :done
    )
)

for %%P in (python python3) do (
    where %%P >nul 2>&1
    if not errorlevel 1 (
        %%P -c "import sys" >nul 2>&1
        if not errorlevel 1 (
            %%P "%SCRIPT_PATH%" %*
            goto :done
        )
    )
)

where uv >nul 2>&1
if not errorlevel 1 (
    uv run --project "%REPO_ROOT%" python "%SCRIPT_PATH%" %*
    goto :done
)

echo [ERROR] Python 3.12+ not found. Please install Python or uv, or download the standalone release from GitHub Releases.
set "EXIT_CODE=1"
if "%~1"=="" pause
exit /b %EXIT_CODE%

:done
set "EXIT_CODE=%ERRORLEVEL%"
if "%~1"=="" pause
exit /b %EXIT_CODE%
