@echo off

REM Check if Mosquitto is already installed
where mosquitto >nul 2>nul
if %errorlevel% equ 0 (
    echo Mosquitto is already installed. Skipping download.
    exit /B
)

REM Set the URL for the Mosquitto installer
set MOSQUITTO_INSTALLER_URL=https://mosquitto.org/files/binary/win64/mosquitto-2.0.11-install-windows-x64.exe

REM Set the path for the downloaded installer
set INSTALLER_PATH=%TEMP%\mosquitto_installer.exe

REM Download the Mosquitto installer
curl -o %INSTALLER_PATH% %MOSQUITTO_INSTALLER_URL%

REM Rest of the script (installing Mosquitto)...
