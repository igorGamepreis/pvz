@echo off
setlocal

python --version >nul 2>&1
if %errorlevel% == 0 (
    echo Python is already installed.
    goto end
) else (
    echo Python is not installed. Installing Python...

    :: Download Python installer
    set PYTHON_INSTALLER_URL=https://www.python.org/ftp/python/3.11.4/python-3.11.4-amd64.exe
    set PYTHON_INSTALLER=python-installer.exe

    :: Check if curl is available
    curl --version >nul 2>&1
    if %errorlevel% == 0 (
        curl -o %PYTHON_INSTALLER% %PYTHON_INSTALLER_URL%
    ) else (
        echo curl is not available. Please install curl or download the Python installer manually.
        goto end
    )

    %PYTHON_INSTALLER% /quiet InstallAllUsers=1 PrependPath=1

    python --version >nul 2>&1
    if %errorlevel% == 0 (
        echo Python installation succeeded.
    ) else (
        echo Python installation failed. Please install Python manually.
    )
)
:end
echo you can close this now
pause >nul
endlocal