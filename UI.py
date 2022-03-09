import sys
import os
import shutil
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class MainForm(QWidget):
    def __init__(self, name = 'MainForm'):
        super(MainForm,self).__init__()
        self.cwd = os.getcwd() # 获取当前程序文件位置
        self.setWindowTitle("Markdown Format Converter")
        self.setWindowIcon( QIcon (self.cwd + '\\icon\\tiger.png'))
        self.resize(400,100)  
        # btn 1
        self.btn_chooseFile = QPushButton(self)  
        self.btn_chooseFile.setFont(QtGui.QFont('Comic Sans MS', 14))
        self.btn_chooseFile.setStyleSheet(
                                 "QPushButton{color:rgb(0,0,0)}" #按键前景色
                                 "QPushButton{background-color:rgb(202, 195, 187)}"  #按键背景色
                                 "QPushButton:hover{color:rgb(240, 235, 229)}" #光标移动到上面后的前景色
                                 "QPushButton{border-radius:6px}"  #圆角半径
                                 "QPushButton:pressed{background-color:rgb(180,180,180);border: None;}" #按下时的样式
                                 )
        # self.btn_chooseFile.setFixedSize(400,50)
        self.btn_chooseFile.move(100, 100)
        icon_img = QtGui.QIcon(self.cwd + '\\icon\\md.png')
        self.btn_chooseFile.setIcon(icon_img)
        self.btn_chooseFile.setObjectName("btn_chooseFile")  
        self.btn_chooseFile.setText("Choose a Markdown File")
        # btn 2
        self.btn_executeFile = QPushButton(self)  
        self.btn_executeFile.setFont(QtGui.QFont('Comic Sans MS', 14))
        self.btn_executeFile.setStyleSheet(
                                 "QPushButton{color:rgb(0,0,0)}" #按键前景色
                                 "QPushButton{background-color:rgb(193, 203, 215)}"  #按键背景色
                                 "QPushButton:hover{color:rgb(240, 235, 229)}" #光标移动到上面后的前景色
                                 "QPushButton{border-radius:6px}"  #圆角半径
                                 "QPushButton:pressed{background-color:rgb(180,180,180);border: None;}" #按下时的样式
                                 )
        # self.btn_executeFile.resize(self.btn_chooseFile.sizeHint()) 
        self.btn_executeFile.move(100, 100)
        icon_img = QtGui.QIcon(self.cwd + '\\icon\\100.png')
        self.btn_executeFile.setIcon(icon_img)
        self.btn_executeFile.setObjectName("btn_executeFile")  
        self.btn_executeFile.setText("Execute File Conversion")


        # 设置布局
        layout = QVBoxLayout()
        layout.addWidget(self.btn_chooseFile)
        layout.addWidget(self.btn_executeFile)
        self.setLayout(layout)

        #连接 信号 和 槽
        self.btn_chooseFile.clicked.connect(self.slot_btn_chooseFile)
        self.btn_executeFile.clicked.connect(self.slot_btn_executeFile)

    def slot_btn_chooseFile(self):
        fileName_choose, filetype = QFileDialog.getOpenFileName(self,  
                                    "选取文件",  
                                    self.cwd, # 起始路径 
                                    "Markdown Files (*.md);;PDF Files(*.pdf);;All Files (*)")   # 设置文件扩展名过滤,用双分号间隔

        if fileName_choose == "":
            print("\n取消选择")
            return

        print("\n你选择的文件为:")
        print(fileName_choose)
        #print(self.cwd+ '\\history')
        print("文件筛选器类型: ",filetype)

        shutil.copy(fileName_choose, self.cwd+ '\\source')
        
    def slot_btn_executeFile(self):

        os.system('python main.py')

if __name__=="__main__":
    app = QApplication(sys.argv)
    mainForm = MainForm('QFileDialog')
    mainForm.show()
    sys.exit(app.exec_())


