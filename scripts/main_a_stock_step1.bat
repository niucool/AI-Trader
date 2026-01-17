@echo off
rem A-share data preparation
setlocal

rem Get the project root directory (parent of scripts/)
pushd "%~dp0.."
set "PROJECT_ROOT=%CD%"

cd data\A_stock

rem for alphavantage
python get_daily_price_alphavantage.py
if errorlevel 1 goto :error
python merge_jsonl_alphavantage.py
if errorlevel 1 goto :error

rem for tushare
rem python get_daily_price_tushare.py
rem python merge_jsonl_tushare.py

cd ..\..

popd
goto :eof

:error
echo ❌ An error occurred.
pause
exit /b 1
