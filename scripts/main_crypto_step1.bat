@echo off
rem A-share data preparation
setlocal

rem Get the project root directory (parent of scripts/)
pushd "%~dp0.."
set "PROJECT_ROOT=%CD%"

cd data
if not exist "crypto" mkdir "crypto"
cd crypto

echo Current dir: %CD%
echo Running: python get_daily_price_crypto.py
python get_daily_price_crypto.py
if errorlevel 1 goto :error

echo Current dir: %CD%
echo Running: python merge_crypto_jsonl.py
python merge_crypto_jsonl.py
if errorlevel 1 goto :error

rem # for tushare
rem echo Current dir: %CD%
rem echo Running: python get_daily_price_tushare.py
rem python get_daily_price_tushare.py
rem echo Current dir: %CD%
rem echo Running: python merge_jsonl_tushare.py
rem python merge_jsonl_tushare.py

cd ..\..

popd
goto :eof

:error
echo ❌ An error occurred.
pause
exit /b 1
