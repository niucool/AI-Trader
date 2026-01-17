@echo off
setlocal

rem Get the project root directory (parent of scripts/)
pushd "%~dp0.."
set "PROJECT_ROOT=%CD%"

echo 🤖 Now starting the cryptocurrencies trading agent...

python main.py configs/default_crypto_config.json
if errorlevel 1 goto :error

echo ✅ AI-Trader stopped

popd
goto :eof

:error
echo ❌ An error occurred.
pause
exit /b 1
