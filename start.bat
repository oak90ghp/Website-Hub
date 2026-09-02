@echo off
REM Cilent Website - Windows 快速启动脚本
REM 这个脚本可以直接双击运行

echo.
echo ╔════════════════════════════════════════╗
echo ║   Cilent Website - 本地网站托管        ║
echo ║                                        ║
echo ║   正在启动程序...                     ║
echo ╚════════════════════════════════════════╝
echo.

REM 检查 Python 是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo ✗ 错误：未检测到 Python
    echo.
    echo 请先安装 Python，下载地址：https://www.python.org
    echo.
    pause
    exit /b 1
)

echo ✓ Python 已就绪
echo.

REM 启动主程序
python main.py

if errorlevel 1 (
    echo.
    echo ✗ 程序启动失败
    echo.
    pause
    exit /b 1
)
