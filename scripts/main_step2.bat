@echo off
setlocal

rem Get the project root directory (parent of scripts/)
pushd "%~dp0.."
set "PROJECT_ROOT=%CD%"

echo 🔧 Now starting MCP services...
cd agent_tools
python start_mcp_services.py
if errorlevel 1 goto :error
cd ..

popd
goto :eof

:error
echo ❌ An error occurred.
pause
exit /b 1
