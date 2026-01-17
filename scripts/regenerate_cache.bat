@echo off
rem Regenerate Frontend Cache
rem Run this script after updating trading data to regenerate the pre-computed cache files

setlocal

echo ========================================
echo Regenerating Frontend Cache
echo ========================================
echo.

rem Get the project root directory (parent of scripts/)
pushd "%~dp0.."
set "PROJECT_ROOT=%CD%"

rem Try to find Python
where python >nul 2>nul
if %errorlevel% equ 0 (
    set "PYTHON=python"
) else (
    where python3 >nul 2>nul
    if %errorlevel% equ 0 (
        set "PYTHON=python3"
    ) else (
        echo Error: Python not found. Please ensure Python is installed and in your PATH.
        pause
        exit /b 1
    )
)

echo Using Python: %PYTHON%
echo.

rem Run the cache generation script
echo Running cache generation script...
%PYTHON% scripts/precompute_frontend_cache.py

echo.
echo ========================================
echo Cache regeneration complete!
echo ========================================
echo.
echo Generated files:
echo   - docs/data/us_cache.json
echo   - docs/data/cn_cache.json
echo.
echo These files will be automatically used by the frontend for faster loading.
echo Commit these files to your repository for GitHub Pages deployment.

popd
goto :eof
