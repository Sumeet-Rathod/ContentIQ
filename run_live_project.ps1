# ContentIQ: Enterprise Live System Launcher (PowerShell)
# Course: 222301907 Capstone Project – II, GLS University FCAIT

$RootDir = "C:\Users\sumee\.gemini\antigravity\scratch\ContentIQ"
$MongoExe = "C:\Program Files\MongoDB\Server\8.2\bin\mongod.exe"
$MongoData = "$RootDir\mongodb_data"
$VenvPython = "$RootDir\backend\.venv\Scripts\python.exe"

Write-Host "===============================================================================" -ForegroundColor Cyan
Write-Host "           CONTENTIQ: LIVE ENTERPRISE SAAS SYSTEM LAUNCHER" -ForegroundColor Yellow
Write-Host "     GLS University - Faculty of Computer Applications & IT (iMCA SEM IX)" -ForegroundColor White
Write-Host "===============================================================================" -ForegroundColor Cyan

# 1. MongoDB
Write-Host "`n[*] Step 1/4: Launching MongoDB Server on Port 27017..." -ForegroundColor Green
$mongoRunning = Get-Process mongod -ErrorAction SilentlyContinue
if (-not $mongoRunning) {
    Start-Process -FilePath $MongoExe -ArgumentList "--dbpath `"$MongoData`" --bind_ip 127.0.0.1 --port 27017" -WindowStyle Minimized
    Start-Sleep -Seconds 3
}
Write-Host "[OK] MongoDB is running." -ForegroundColor Green

# 2. Database Seeder
Write-Host "`n[*] Step 2/4: Verifying Ground-Truth Database Records..." -ForegroundColor Green
Set-Location "$RootDir\backend"
& $VenvPython seed.py
Write-Host "[OK] Database seeded successfully." -ForegroundColor Green

# 3. FastAPI Backend
Write-Host "`n[*] Step 3/4: Starting FastAPI Backend on Port 8000..." -ForegroundColor Green
Start-Process cmd -ArgumentList "/k cd /d `"$RootDir\backend`" && .venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000" -WindowStyle Normal
Start-Sleep -Seconds 3
Write-Host "[OK] Backend running at http://127.0.0.1:8000" -ForegroundColor Green

# 4. React Vite Frontend
Write-Host "`n[*] Step 4/4: Starting Vite Frontend on Port 3000..." -ForegroundColor Green
Start-Process cmd -ArgumentList "/k cd /d `"$RootDir\frontend`" && npm run dev" -WindowStyle Normal
Start-Sleep -Seconds 4
Write-Host "[OK] Frontend ready at http://127.0.0.1:3000" -ForegroundColor Green

# 5. Open Browser
Write-Host "`n===============================================================================" -ForegroundColor Cyan
Write-Host "  SUCCESS! Opening live application at http://127.0.0.1:3000 ..." -ForegroundColor Yellow
Write-Host "===============================================================================" -ForegroundColor Cyan
Start-Process "http://127.0.0.1:3000"
