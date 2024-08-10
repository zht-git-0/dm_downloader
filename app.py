from PyQt5 import QtCore, QtGui, QtWidgets, sip
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFontMetrics, QIcon
from PyQt5.QtWidgets import *
import sys
from model import func,main,Ui_window
import threading
import os
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = r'./.venv/Lib/site-packages/PyQt5/Qt5/plugins/platforms'
def center(win):
    """
    居中
    """
    win.move((QtWidgets.QApplication.desktop().width() - win.width()) // 2,
             (QtWidgets.QApplication.desktop().height() - win.height()) // 2)
def search(txt,p=1):
    global page
    page=p
    ui.lineEdit_2.setText(str(p))
    if txt=="":
        return
    data=func.get_base_url(txt,p)
    widget=QWidget()#创建widget
    layout = QGridLayout()#创建布局
    widget.setLayout(layout)
    for i in range(len(data)):
        btn=QPushButton(f"{data[i][1]}")
        layout.addWidget(btn)
        btn.clicked.connect(lambda checked, i=i: threading.Thread(target=main.download_video, args=(data[i][0],)).start())
    ui.scrollArea.setWidget(widget)
def next_page():
    global page
    page+=1
    ui.lineEdit_2.setText(str(page))
    search(ui.lineEdit.text(),page)
def prev_page():
    global page
    if page==1:
        return
    page-=1
    ui.lineEdit_2.setText(str(page))
    search(ui.lineEdit.text(),page)
if __name__ == '__main__':
    page=1
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling) 
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_window.Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.setFixedSize(MainWindow.width(), MainWindow.height()); 
    MainWindow.show()
    center(MainWindow)
    ui.pushButton.clicked.connect(lambda: search(ui.lineEdit.text()))
    ui.lineEdit_2.setReadOnly(True);ui.lineEdit_2.setAlignment(Qt.AlignCenter)
    ui.lineEdit_2.setText(str(page))
    ui.pushButton_2.clicked.connect(prev_page)
    ui.pushButton_3.clicked.connect(next_page)
    ui.lineEdit.returnPressed.connect(lambda: search(ui.lineEdit.text()))
    sys.exit(app.exec_())