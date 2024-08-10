import Ui_window
from PyQt5 import QtCore, QtGui, QtWidgets, sip
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFontMetrics, QIcon
from PyQt5.QtWidgets import *
import sys
import func
import main
import threading
import os
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = r'./.venv/Lib/site-packages/PyQt5/Qt5/plugins/platforms'
def center(win):
    """
    centers a window on the screen
    :param win: the window to center
    """
    win.move((QtWidgets.QApplication.desktop().width() - win.width()) // 2,
             (QtWidgets.QApplication.desktop().height() - win.height()) // 2)
def search(txt):
    data=func.get_base_url(txt)
    print(data)
    widget=QWidget()#创建widget
    layout = QGridLayout()#创建布局
    widget.setLayout(layout)
    for i in range(len(data)):
        btn=QPushButton(f"{data[i][1]}")
        layout.addWidget(btn)
        btn.clicked.connect(lambda checked, i=i: threading.Thread(target=main.download_video, args=(data[i][0],)).start())
    ui.scrollArea.setWidget(widget)
if __name__ == '__main__':
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling) 
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_window.Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.setFixedSize(MainWindow.width(), MainWindow.height()); 
    MainWindow.show()
    center(MainWindow)
    ui.pushButton.clicked.connect(lambda: search(ui.lineEdit.text()))
    sys.exit(app.exec_())