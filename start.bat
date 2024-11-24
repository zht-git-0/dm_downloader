@echo off
set PATH=../python;%PATH%
set BROWSER_PATH=\module\pw\chromium-1129\chrome-win\chrome.exe
python -m venv .venv
call .venv\Scripts\activate
set BROWSER_PATH=\module\pw\chromium-1129\chrome-win\chrome.exe
start "" pythonw app.py