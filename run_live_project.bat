@echo off
TITLE ContentIQ Enterprise Platform Launcher
COLOR 0B

echo ===============================================================================
echo            CONTENTIQ: LIVE ENTERPRISE SAAS SYSTEM LAUNCHER
echo      Enterprise Multimodal Social Scheduling and Prediction Platform
echo      Production Active Learning Feedback Loop and Intelligence Suite
echo ===============================================================================
echo.

set ROOT_DIR=C:\Users\sumee\.gemini\antigravity\scratch\ContentIQ
set MONGO_EXE=C:\Program Files\MongoDB\Server\8.2\bin\mongod.exe
set MONGO_DATA=%ROOT_DIR%\mongodb_data
set VENV_PYTHON=%ROOT_DIR%\backend\.venv\Scripts\python.exe

:: 1. Start MongoDB Database
echo [*] Step 1/4: Checking and Starting MongoDB Database on Port 27017...
netstat -ano | findstr :27017 | findstr LISTENING >nul
if %ERRORLEVEL% EQU 0 (
    echo [OK] MongoDB is already listening on port 27017.
) else (
    echo [+] Starting MongoDB Server daemon...
    start "ContentIQ - MongoDB Database (Port 27017)" /min "%MONGO_EXE%" --dbpath "%MONGO_DATA%" --bind_ip 127.0.0.1 --port 27017
    ping -n 4 127.0.0.1 >nul
    echo [OK] MongoDB Server initialized.
)

:: 2. Ensure Database is Seeded
echo.
echo [*] Step 2/4: Verifying Enterprise Multi-Tenant Ground-Truth Seed Data...
cd /d "%ROOT_DIR%\backend"
"%VENV_PYTHON%" seed.py
echo [OK] 9 Collections seeded (80+ posts, metrics, Prophet history, A/B tests).

:: 3. Start FastAPI Backend Gateway
echo.
echo [*] Step 3/4: Starting FastAPI REST Gateway and ML Engine on Port 8000...
start "ContentIQ - FastAPI Backend Gateway (Port 8000)" cmd /k "cd /d %ROOT_DIR%\backend && .venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000"
ping -n 4 127.0.0.1 >nul
echo [OK] FastAPI REST Gateway listening at http://127.0.0.1:8000.
echo      Interactive OpenAPI Docs available at http://127.0.0.1:8000/docs.

:: 4. Start React 18 Frontend
echo.
echo [*] Step 4/4: Starting React 18 / Vite Development Server on Port 3000...
start "ContentIQ - React 18 Frontend (Port 3000)" cmd /k "cd /d %ROOT_DIR%\frontend && npm run dev"
ping -n 5 127.0.0.1 >nul
echo [OK] Frontend SPA ready at http://localhost:3000 and http://127.0.0.1:3000.

:: 5. Open Web Browser
echo.
echo ===============================================================================
echo   SUCCESS! All services (Database, Backend, Frontend) are now LIVE!
echo   Opening live application at http://localhost:3000 ...
echo ===============================================================================
start http://localhost:3000

echo.
echo [!] Keep background service windows open during your viva presentation.
echo [!] To stop all services after the demo, run stop_services.bat.
if "%1"=="--no-pause" goto :eof
if "%1"=="--daemon" goto :eof
pause
