@echo off
setlocal

rem Get the project root directory (parent of scripts/)
pushd "%~dp0.."
set "PROJECT_ROOT=%CD%"

echo 🤖 Starting main trading agent (A-share mode)...

python main.py configs/astock_config.json
if errorlevel 1 goto :error

echo ✅ AI-Trader stopped

popd
goto :eof

:error
echo ❌ An error occurred.
pause
exit /b 1
