@echo off
setlocal
set "SCRIPT_DIR=%~dp0"
call "%SCRIPT_DIR%..\TrenTorch_CLI\bin\tren.cmd" %*
exit /b %ERRORLEVEL%
