import sys
import os
import shutil
from PyQt5.QtWidgets import *

class MainForm(QWidget):
    def __init__(self, name = 'MainForm'):
        super(MainForm,self).__init__()
        self.setWindowTitle("选择文件")
        self.cwd = os.getcwd() # 获取当前程序文件位置
        self.resize(300,200)  
        # btn 1
        self.btn_chooseFile = QPushButton(self)  
        self.btn_chooseFile.setObjectName("btn_chooseFile")  
        self.btn_chooseFile.setText("选取文件并保存至source目录下")
        # btn 2
        self.btn_executeFile = QPushButton(self)  
        self.btn_executeFile.setObjectName("btn_executeFile")  
        self.btn_executeFile.setText("执行文件转换")

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
        
        shutil.copyfile(fileName_choose, self.cwd+ '\\source')

        if fileName_choose == "":
            print("\n取消选择")
            return

        print("\n你选择的文件为:")
        print(fileName_choose)
        #print(self.cwd+ '\\history')
        print("文件筛选器类型: ",filetype)
        
        #path = r"E:/Desktop/秃头文件/●应用软件课程设计/Individual Assignment/wx_press_guide/source"

       


    def slot_btn_executeFile(self):

        os.system('python main.py')

        #fileName_choose, filetype = QFileDialog.getSaveFileName(self,  
        #                            "文件保存",  
        #                            self.cwd, # 起始路径 
        #                            "All Files (*);;Markdown Files (*.md)")  # 设置文件扩展名过滤,用双分号间隔

        #if fileName_choose == "":
        #    print("\n取消选择")
        #    return

        #print("\n你选择要保存的文件为:")
        #print(fileName_choose)
        #print("文件筛选器类型: ",filetype)

if __name__=="__main__":
    app = QApplication(sys.argv)
    mainForm = MainForm('QFileDialog')
    mainForm.show()
    sys.exit(app.exec_())


