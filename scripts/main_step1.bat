@echo off
rem prepare data

setlocal

rem Get the project root directory (parent of scripts/)
pushd "%~dp0.."
set "PROJECT_ROOT=%CD%"

cd data
rem python get_daily_price.py
python get_interdaily_price.py
if errorlevel 1 goto :error
python merge_jsonl.py
if errorlevel 1 goto :error
cd ..

popd
goto :eof

:error
echo ❌ An error occurred.
pause
exit /b 1
