@echo off
SET DOWNLOAD_BROWSER_PATH=./module/pw
REM 设置Playwright浏览器下载路径
SET PLAYWRIGHT_BROWSERS_PATH=%DOWNLOAD_BROWSER_PATH%
REM 使用playwright下载浏览器
python -m venv .venv
call .venv\Scripts\activate
python.exe -m pip install --upgrade pip
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
playwright install
echo have been completed!you can click start.bat
pause