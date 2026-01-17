@echo off
rem AI-Trader Main Launch Script
rem Used to start the complete trading environment

setlocal

echo 🚀 Launching AI Trader Environment...

rem Get the project root directory (parent of scripts/)
pushd "%~dp0.."
set "PROJECT_ROOT=%CD%"

echo 📊 Now getting and merging price data...
cd data
python get_daily_price.py
if errorlevel 1 goto :error
python merge_jsonl.py
if errorlevel 1 goto :error
cd ..

echo 🔧 Now starting MCP services...
cd agent_tools
start "AI-Trader MCP Services" python start_mcp_services.py
cd ..

rem Waiting for MCP services to start
timeout /t 2 /nobreak >nul

echo 🤖 Now starting the main trading agent...
python main.py configs/default_config.json
if errorlevel 1 goto :error

echo ✅ AI-Trader stopped

echo 🔄 Starting web server...
cd docs
python -m http.server 8888
if errorlevel 1 goto :error

echo ✅ Web server started
popd
goto :eof

:error
echo ❌ An error occurred.
pause
exit /b 1
