@echo off
chcp 65001 >nul

:: MinerU 启动脚本 - 同时启动后端和前端服务

:: ===== 1. 启动后端 (使用 conda MinerUv2 环境) =====
start "MinerU Backend" cmd /k "cd /d H:\Git\MinerU\backend && call E:\Anaconda\Scripts\activate.bat MinerUv2 && set PYTHONNOUSERSITE=1 && python main.py"

:: 等待 3 秒
timeout /t 3 >nul

:: ===== 2. 启动前端 =====
start "MinerU Frontend" cmd /k "cd /d H:\Git\MinerU\frontend && npm run dev -- --host 0.0.0.0 --port 3000 --strictPort"

set "LAN_IP="
for /f "usebackq delims=" %%i in (`powershell -NoProfile -Command "$ip=(Get-NetIPAddress -AddressFamily IPv4 -InterfaceAlias 'Wi-Fi' -ErrorAction SilentlyContinue | Where-Object { $_.IPAddress -notlike '169.254*' -and $_.IPAddress -ne '127.0.0.1' } | Select-Object -First 1 -ExpandProperty IPAddress); if(-not $ip){$ip=(Get-NetIPAddress -AddressFamily IPv4 | Where-Object { $_.IPAddress -notlike '169.254*' -and $_.IPAddress -ne '127.0.0.1' } | Select-Object -First 1 -ExpandProperty IPAddress)}; $ip"`) do set "LAN_IP=%%i"
if not defined LAN_IP set "LAN_IP=localhost"

echo.
echo ✅ MinerU 启动脚本已执行
echo    后端: http://%LAN_IP%:8267
echo    前端: http://%LAN_IP%:3000
echo    请检查弹出的两个窗口是否有报错
echo.
pause
