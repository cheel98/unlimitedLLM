@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo.
echo ========================================
echo    🚀 Unlimited Agent 启动器
echo ========================================
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误: 未找到Python，请先安装Python 3.8+
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM 检查依赖是否安装
if not exist "requirements.txt" (
    echo ❌ 错误: 未找到requirements.txt文件
    pause
    exit /b 1
)

REM 检查是否首次运行
if not exist "models" (
    echo 🔧 首次运行，正在安装依赖...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ 依赖安装失败
        pause
        exit /b 1
    )
    echo ✅ 依赖安装完成
    echo.
)

REM 启动程序
echo 🚀 正在启动 Unlimited Agent...
echo.
python run.py

REM 程序结束后暂停
echo.
echo 程序已退出
pause