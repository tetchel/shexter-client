@echo off
::set LOGFILE=shexterd.log
::call :LOG > %LOGFILE% 2>&1
::exit \B

:: :LOG
python %~dp0shexterd.py %*