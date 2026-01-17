@echo off
rem Start AI-Trader Web UI

setlocal

rem Get the project root directory (parent of scripts/)
pushd "%~dp0.."
set "PROJECT_ROOT=%CD%"

echo 🌐 Starting Web UI server...
echo.
echo Press Ctrl+C to stop the server
echo.

cd docs
python -m http.server 8888

popd
goto :eof
