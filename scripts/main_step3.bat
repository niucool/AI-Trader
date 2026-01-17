@echo off
setlocal

rem Get the project root directory (parent of scripts/)
pushd "%~dp0.."
set "PROJECT_ROOT=%CD%"

echo 🤖 Now starting the main trading agent...

rem Please create the config file first!!

rem python main.py configs/default_day_config.json #run daily config
python main.py configs/default_hour_config.json
if errorlevel 1 goto :error

echo ✅ AI-Trader stopped

popd
goto :eof

:error
echo ❌ An error occurred.
pause
exit /b 1
