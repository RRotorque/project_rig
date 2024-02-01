@echo off

REM Set the execution policy
powershell -Command "Set-ExecutionPolicy RemoteSigned -Force"

REM Respond 'Y' to confirmation prompt
echo Y | set /p="."
powershell -Command "& {}"

REM Set the path for the script directory
set SCRIPT_DIR=%~dp0

REM Set the path to the Mosquitto installation directory
set MOSQUITTO_DIR=C:\Program Files\Mosquitto

REM Run the installer silently
start /wait %TEMP%\mosquitto_installer.exe /S

REM Run the Mosquitto start script
call "%SCRIPT_DIR%install_mosquitto.bat"

REM Create a configuration file for Mosquitto
echo listener 1883 > "%MOSQUITTO_DIR%\mosquitto.conf"

REM Display Mosquitto version
"%MOSQUITTO_DIR%\mosquitto.exe" -v
