@echo off
python -m venv .venv
call .venv\Scripts\activate
python.exe -m pip install --upgrade pip
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
playwright install
set QT_PLUGIN_PATH=D:\python\脚本\动漫\.venv\Lib\site-packages\PyQt5\Qt5\plugins
python app.py