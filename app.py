from PyQt5 import QtCore, QtGui, QtWidgets, sip
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
import sys
from module import func,main,Ui_window
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
        btn.clicked.connect(lambda checked, i=i: threading.Thread(target=main.download_video, args=(data[i][0],ui.textBrowser,cursor)).start())
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
    center(MainWindow)
    ui.pushButton.clicked.connect(lambda: search(ui.lineEdit.text()))
    ui.lineEdit_2.setReadOnly(True);ui.lineEdit_2.setAlignment(Qt.AlignCenter)
    ui.lineEdit_2.setText(str(page))
    ui.pushButton_2.clicked.connect(prev_page)
    ui.pushButton_3.clicked.connect(next_page)
    ui.lineEdit.returnPressed.connect(lambda: search(ui.lineEdit.text()))
    ui.textBrowser.setOpenExternalLinks(True)
    cursor=ui.textBrowser.textCursor()
    #cursor.setPosition(0)  # 例如，从文本的开始位置
    #选择要删除的文本长度（这里假设删除5个字符）
    #cursor.insertText("插入的文字")
    #cursor.movePosition(QTextCursor.Left, QTextCursor.KeepAnchor, 5)
    #cursor.removeSelectedText()
    #cursor.insertHtml('1')
    #ui.textBrowser.append(f"<a href='https://v16m-default.akamaized.net/f4d6649c1ce4c4a27d88acf2a9ae8808/66fd6cad/video/tos/alisg/tos-alisg-ve-0051c001-sg/oYFuitXlqAjtBbsqEhNndNfBQnUfIycIDSUgQD/?a=2011&bti=MzhALjBg&ch=0&cr=0&dr=0&net=5&cd=0%7C0%7C0%7C0&br=3952&bt=1976&cs=0&ds=4&ft=XE5bCqT0mmjPD12_C0p73wU7C1JcMeF~O5&mime_type=video_mp4&qs=0&rc=NGc6ZGdmaDo4PDg0ZDdkNEBpM2dza2o5cmU6cDMzODYzNEAyNF5gYS4tXzMxMWEtNDIzYSNpYWloMmQ0a2lgLS1kMC1zcw%3D%3D&vvpl=1&l=202410020930403BCC31FBBFC2AF9E527C&btag=e000a8000'>https://v16m-default.akamaized.net/f4d6649c1ce4c4a27d88acf2a9ae8808/66fd6cad/video/tos/alisg/tos-alisg-ve-0051c001-sg/oYFuitXlqAjtBbsqEhNndNfBQnUfIycIDSUgQD/?a=2011&bti=MzhALjBg&ch=0&cr=0&dr=0&net=5&cd=0%7C0%7C0%7C0&br=3952&bt=1976&cs=0&ds=4&ft=XE5bCqT0mmjPD12_C0p73wU7C1JcMeF~O5&mime_type=video_mp4&qs=0&rc=NGc6ZGdmaDo4PDg0ZDdkNEBpM2dza2o5cmU6cDMzODYzNEAyNF5gYS4tXzMxMWEtNDIzYSNpYWloMmQ0a2lgLS1kMC1zcw%3D%3D&vvpl=1&l=202410020930403BCC31FBBFC2AF9E527C&btag=e000a8000</a>")
    MainWindow.show()
    sys.exit(app.exec_())