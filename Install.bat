@echo off
echo ============================================
echo   SecureVault - Installation
echo ============================================
echo.

python -m venv .venv

call .venv\Scripts\activate.bat

echo.
echo Installing dependencies...
pip install -r requirements.txt

echo.
echo ============================================
echo   Installation complete!
echo   Run "Run.bat" to start SecureVault.
echo ============================================
pause
