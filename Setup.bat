@echo off
setlocal

set "shortcut=%~dp0\Piano Control.lnk"
set "target=%~dp0\scripts\main.py"
set "pip=%~dp0\scripts\pip.exe"

if not exist "%shortcut%" (
    echo Shortcut does not exist: %shortcut%
    pause
    exit /b 1
)

if not exist "%target%" (
    echo Target file does not exist: %target%
    pause
    exit /b 1
)

echo Installing required packages...
"%pip%" install aubio pyaudio numpy ahk || (
    echo Failed to install required packages!
    pause
    exit /b 1
)

echo Updating shortcut target...
powershell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%shortcut%'); $Shortcut.TargetPath = '%target%'; $Shortcut.Save()"

if not exist "%shortcut%" (
    echo Shortcut not updated: %shortcut%
    pause
    exit /b 1
)

echo Shortcut updated successfully: %shortcut%
pause
exit /b 0
