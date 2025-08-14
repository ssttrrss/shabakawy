@echo off
REM Shabakawy Windows Installer
REM This script installs Shabakawy on Windows systems

setlocal enabledelayedexpansion

REM Set title and colors
title Shabakawy Windows Installer v1.0
color 0B

echo ========================================
echo     Shabakawy Windows Installer v1.0
echo ========================================
echo.

REM Check if running as administrator
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo [ERROR] This script must be run as Administrator
    echo Please right-click and select "Run as administrator"
    echo.
    pause
    exit /b 1
)

echo [INFO] Running as Administrator - OK
echo.

REM Function to print colored output
:print_status
echo [INFO] %~1
goto :eof

:print_success
echo [SUCCESS] %~1
goto :eof

:print_warning
echo [WARNING] %~1
goto :eof

:print_error
echo [ERROR] %~1
goto :eof

REM Check Windows version
echo [INFO] Checking Windows version...
for /f "tokens=4-5 delims=. " %%i in ('ver') do set VERSION=%%i.%%j
echo [INFO] Windows version: %VERSION%

REM Check if Python is installed
echo [INFO] Checking Python installation...
python --version >nul 2>&1
if %errorLevel% equ 0 (
    for /f "tokens=2" %%i in ('python --version') do set PYTHON_VERSION=%%i
    echo [SUCCESS] Python %PYTHON_VERSION% is already installed
    goto :install_deps
)

REM Python not found, offer to download
echo [WARNING] Python is not installed
echo.
echo Python is required to run Shabakawy.
echo Please download and install Python from: https://www.python.org/downloads/
echo.
echo Make sure to check "Add Python to PATH" during installation.
echo.
echo After installing Python, run this installer again.
echo.
pause
exit /b 1

:install_deps
echo.
echo [INFO] Installing Python dependencies...

REM Upgrade pip
echo [INFO] Upgrading pip...
python -m pip install --upgrade pip

REM Install required packages
echo [INFO] Installing required packages...
python -m pip install PyQt5 scapy psutil requests selenium beautifulsoup4 lxml cryptography paramiko netifaces

if %errorLevel% neq 0 (
    echo [ERROR] Failed to install Python dependencies
    echo Please check your internet connection and try again
    pause
    exit /b 1
)

echo [SUCCESS] Python dependencies installed successfully
echo.

REM Check if Git is installed
echo [INFO] Checking Git installation...
git --version >nul 2>&1
if %errorLevel% neq 0 (
    echo [WARNING] Git is not installed
    echo Please download and install Git from: https://git-scm.com/download/win
    echo.
    echo After installing Git, run this installer again.
    echo.
    pause
    exit /b 1
)

echo [SUCCESS] Git is available
echo.

REM Clone repository
echo [INFO] Cloning Shabakawy repository...
if exist "shabakawy" (
    echo [WARNING] Shabakawy directory already exists, removing...
    rmdir /s /q "shabakawy"
)

git clone https://github.com/ssttrrss/shabakawy.git

if not exist "shabakawy" (
    echo [ERROR] Failed to clone repository
    echo Please check your internet connection and try again
    pause
    exit /b 1
)

echo [SUCCESS] Repository cloned successfully
echo.

REM Create executable batch file
echo [INFO] Creating executable...
cd shabakawy

echo @echo off > run.bat
echo cd /d "%%~dp0" >> run.bat
echo python run.py %%* >> run.bat

echo [SUCCESS] Executable created successfully
echo.

REM Create desktop shortcut
echo [INFO] Creating desktop shortcut...
set DESKTOP=%USERPROFILE%\Desktop
if exist "%DESKTOP%\Shabakawy.lnk" del "%DESKTOP%\Shabakawy.lnk"

REM Create VBS script to create shortcut
echo Set oWS = WScript.CreateObject("WScript.Shell") > CreateShortcut.vbs
echo sLinkFile = "%DESKTOP%\Shabakawy.lnk" >> CreateShortcut.vbs
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> CreateShortcut.vbs
echo oLink.TargetPath = "%~dp0run.bat" >> CreateShortcut.vbs
echo oLink.WorkingDirectory = "%~dp0" >> CreateShortcut.vbs
echo oLink.Description = "Shabakawy Network Security Monitor" >> CreateShortcut.vbs
echo oLink.IconLocation = "%~dp0icon.ico" >> CreateShortcut.vbs
echo oLink.Save >> CreateShortcut.vbs

cscript //nologo CreateShortcut.vbs
del CreateShortcut.vbs

echo [SUCCESS] Desktop shortcut created
echo.

REM Create start menu shortcut
echo [INFO] Creating start menu shortcut...
set STARTMENU=%APPDATA%\Microsoft\Windows\Start Menu\Programs
if not exist "%STARTMENU%" mkdir "%STARTMENU%"

if exist "%STARTMENU%\Shabakawy.lnk" del "%STARTMENU%\Shabakawy.lnk"

REM Create VBS script for start menu shortcut
echo Set oWS = WScript.CreateObject("WScript.Shell") > CreateStartMenuShortcut.vbs
echo sLinkFile = "%STARTMENU%\Shabakawy.lnk" >> CreateStartMenuShortcut.vbs
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> CreateStartMenuShortcut.vbs
echo oLink.TargetPath = "%~dp0run.bat" >> CreateStartMenuShortcut.vbs
echo oLink.WorkingDirectory = "%~dp0" >> CreateStartMenuShortcut.vbs
echo oLink.Description = "Shabakawy Network Security Monitor" >> CreateStartMenuShortcut.vbs
echo oLink.IconLocation = "%~dp0icon.ico" >> CreateStartMenuShortcut.vbs
echo oLink.Save >> CreateStartMenuShortcut.vbs

cscript //nologo CreateStartMenuShortcut.vbs
del CreateStartMenuShortcut.vbs

echo [SUCCESS] Start menu shortcut created
echo.

REM Create configuration directory
echo [INFO] Creating configuration...
set CONFIGDIR=%APPDATA%\Shabakawy
if not exist "%CONFIGDIR%" mkdir "%CONFIGDIR%"

REM Create default configuration file
echo [network] > "%CONFIGDIR%\shabakawy.conf"
echo scan_interval = 30 >> "%CONFIGDIR%\shabakawy.conf"
echo packet_capture_timeout = 60 >> "%CONFIGDIR%\shabakawy.conf"
echo max_devices = 100 >> "%CONFIGDIR%\shabakawy.conf"
echo. >> "%CONFIGDIR%\shabakawy.conf"
echo [security] >> "%CONFIGDIR%\shabakawy.conf"
echo ddos_threshold = 1000 >> "%CONFIGDIR%\shabakawy.conf"
echo mitm_detection = true >> "%CONFIGDIR%\shabakawy.conf"
echo auto_block = true >> "%CONFIGDIR%\shabakawy.conf"
echo. >> "%CONFIGDIR%\shabakawy.conf"
echo [router] >> "%CONFIGDIR%\shabakawy.conf"
echo default_gateway = 192.168.1.1 >> "%CONFIGDIR%\shabakawy.conf"
echo admin_port = 80 >> "%CONFIGDIR%\shabakawy.conf"
echo timeout = 30 >> "%CONFIGDIR%\shabakawy.conf"
echo. >> "%CONFIGDIR%\shabakawy.conf"
echo [gui] >> "%CONFIGDIR%\shabakawy.conf"
echo theme = light >> "%CONFIGDIR%\shabakawy.conf"
echo auto_refresh = true >> "%CONFIGDIR%\shabakawy.conf"
echo notifications = true >> "%CONFIGDIR%\shabakawy.conf"

echo [SUCCESS] Configuration created
echo.

REM Create log directory
echo [INFO] Creating log directory...
set LOGDIR=%APPDATA%\Shabakawy\logs
if not exist "%LOGDIR%" mkdir "%LOGDIR%"

echo [SUCCESS] Log directory created
echo.

REM Check installation
echo [INFO] Checking installation...

REM Test Python dependencies
python -c "import PyQt5, scapy, psutil, requests, selenium; print('All dependencies available')" >nul 2>&1
if %errorLevel% neq 0 (
    echo [ERROR] Some Python dependencies are missing
    echo Please run: python -m pip install PyQt5 scapy psutil requests selenium
    pause
    exit /b 1
)

REM Check if executable exists
if not exist "run.bat" (
    echo [ERROR] Executable file not found
    pause
    exit /b 1
)

echo [SUCCESS] Installation check completed successfully
echo.

REM Create firewall rules
echo [INFO] Setting up Windows Firewall...
netsh advfirewall firewall add rule name="Shabakawy Outbound DNS" dir=out action=allow protocol=UDP localport=any remoteport=53 >nul 2>&1
netsh advfirewall firewall add rule name="Shabakawy Outbound HTTP" dir=out action=allow protocol=TCP localport=any remoteport=80 >nul 2>&1
netsh advfirewall firewall add rule name="Shabakawy Outbound HTTPS" dir=out action=allow protocol=TCP localport=any remoteport=443 >nul 2>&1

echo [SUCCESS] Firewall rules configured
echo.

REM Create uninstaller
echo [INFO] Creating uninstaller...
echo @echo off > uninstall.bat
echo echo Shabakawy Uninstaller >> uninstall.bat
echo echo. >> uninstall.bat
echo echo This will remove Shabakawy from your system. >> uninstall.bat
echo echo. >> uninstall.bat
echo set /p confirm="Are you sure? (y/N): " >> uninstall.bat
echo if /i "%%confirm%%"=="y" ( >> uninstall.bat
echo     echo Removing Shabakawy... >> uninstall.bat
echo     if exist "%%APPDATA%%\Shabakawy" rmdir /s /q "%%APPDATA%%\Shabakawy" >> uninstall.bat
echo     if exist "%%USERPROFILE%%\Desktop\Shabakawy.lnk" del "%%USERPROFILE%%\Desktop\Shabakawy.lnk" >> uninstall.bat
echo     if exist "%%APPDATA%%\Microsoft\Windows\Start Menu\Programs\Shabakawy.lnk" del "%%APPDATA%%\Microsoft\Windows\Start Menu\Programs\Shabakawy.lnk" >> uninstall.bat
echo     echo Shabakawy removed successfully. >> uninstall.bat
echo     echo You can now delete this folder manually. >> uninstall.bat
echo ) else ( >> uninstall.bat
echo     echo Uninstall cancelled. >> uninstall.bat
echo ) >> uninstall.bat
echo pause >> uninstall.bat

echo [SUCCESS] Uninstaller created
echo.

REM Show completion message
echo.
echo ========================================
echo     Shabakawy Installation Complete!
echo ========================================
echo.
echo Installation completed successfully!
echo.
echo To run Shabakawy:
echo   Double-click the desktop shortcut
echo   Or run: run.bat
echo.
echo Configuration file: %CONFIGDIR%\shabakawy.conf
echo Log files: %LOGDIR%
echo.
echo For more information, see the README.md file
echo.
echo To uninstall, run: uninstall.bat
echo.

REM Go back to parent directory
cd ..

pause
exit /b 0
