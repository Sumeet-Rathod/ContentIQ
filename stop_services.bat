@echo off
TITLE Stop ContentIQ Services
COLOR 0C

echo ===============================================================================
echo               CONTENTIQ: SHUTTING DOWN LIVE DEMO SERVICES
echo ===============================================================================
echo.

echo [*] Stopping Vite Frontend (Port 3000)...
for /f "tokens=5" %%a in ('netstat -aon ^| find ":3000" ^| find "LISTENING"') do taskkill /f /pid %%a >nul 2>&1

echo [*] Stopping FastAPI Backend (Port 8000)...
for /f "tokens=5" %%a in ('netstat -aon ^| find ":8000" ^| find "LISTENING"') do taskkill /f /pid %%a >nul 2>&1

echo [*] Stopping MongoDB Database (Port 27017)...
taskkill /f /im mongod.exe >nul 2>&1

echo [OK] All ContentIQ demo processes stopped cleanly.
timeout /t 3
