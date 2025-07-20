@echo off
REM 创建虚拟环境（如已存在则跳过）
if not exist .venv (
    python -m venv .venv
)

REM 使用清华源安装依赖
REM .venv\Scripts\pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

REM 4. 用pythonw.exe后台无窗口启动Flask服务
start /b .venv\Scripts\pythonw.exe app.py

REM 等待2秒，确保服务启动
ping 127.0.0.1 -n 3 >nul

REM 打开网页
start  http://127.0.0.1:5055

REM 关闭当前cmd窗口
exit 