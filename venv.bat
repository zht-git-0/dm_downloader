@echo off
set PATH=../python;%PATH%
python -m venv .venv
call .venv\Scripts\activate
python.exe -m pip install --upgrade pip
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
playwright install
echo have been completed!you can click start.bat
pause