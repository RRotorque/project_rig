@echo off
:: BatchGotAdmin
:-------------------------------------
REM  --> Check for permissions
>nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"

REM --> If error flag set, we do not have admin.
if '%errorlevel%' NEQ '0' (
    echo Requesting administrative privileges...
    goto UACPrompt
) else ( goto gotAdmin )

:UACPrompt
    echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
    echo UAC.ShellExecute "%~s0", "", "", "runas", 1 >> "%temp%\getadmin.vbs"

    "%temp%\getadmin.vbs"
    exit /B

:gotAdmin
    if exist "%temp%\getadmin.vbs" ( del "%temp%\getadmin.vbs" )

:: Change the working directory to the Mosquitto program files directory
cd /d "C:\Program Files\Mosquitto"

:: Check if the config file exists
if not exist .\testconfig.txt (
    echo Error: Config file not found. Please make sure the file exists.
    pause
    exit /B
)

:: Run mosquitto with the provided config file
mosquitto -v -c .\testconfig.txt

:: Pause to keep the command window open
pause
