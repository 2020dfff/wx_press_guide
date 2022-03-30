import sys
import os
import premailer
import shutil
from mistune import Markdown
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *



def pack_html(html, style='default_style.css'):
        head = """<!DOCTYPE html><html lang="zh-cn">
             <head>
             <meta charset="UTF-8">
             <title>output</title>
             <link rel="stylesheet" type="text/css" href="{style}">
             </head>
             <body>\n""".format(style=style)

        bottom = """\n</body>\n</html>"""
        return head + html + bottom


def convert_all(src='source', dst='html_output', style='default_style.css'):
        for file in os.listdir(src):

            if file.endswith('.md'):
                for hisfile in os.listdir('history'):
                    if hisfile==file:
                        print('已有重名文件，请重新命名要转换的文件或在html_output和history文件夹下删除重名文件')
                        return

                with open('{src}/{fn}'.format(src=src, fn=file), 'r', encoding='utf-8') as mdfile:
                    mdstr = mdfile.read()
                            
                md = Markdown()
                raw_html = md(mdstr)

                # for mdfile in os.walk({src})
                #     if 
                result = premailer.transform(pack_html(raw_html, style))

                with open('{dst}/{fn}.html'.format(dst=dst, fn=file[:-3]),
                        'w', encoding='utf-8') as htmlfile:
                    htmlfile.write(result)
                
                os.rename('{src}/{fn}'.format(src=src, fn=file), 'history/{fn}'.format(fn=file))
                print('成功：转换后的.html文件保存在html_output文件夹中')
                print('在history文件中查看转换完毕的.md源文件')


class MainForm(QWidget):
    def __init__(self, name = 'MainForm'):
        super(MainForm,self).__init__()
        self.cwd = os.getcwd() # 获取当前程序文件位置
        self.setWindowTitle("Markdown2VX Press Guide")
        self.setWindowIcon( QIcon (self.cwd + '\\icon\\tiger.ico'))
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
        
    # def slot_btn_executeFile(self):
    #     os.system('python md2html.py')


    def slot_btn_executeFile(self):
        try:
            convert_all(src='source', dst='html_output', style='default_style.css')
        except:
            input('错误：运行前请将所有要转换的.md文件放入source文件夹中'
                  '按回车键结束程序：')


        # os.system('python md2html.py')


if __name__=="__main__":
    app = QApplication(sys.argv)
    mainForm = MainForm('QFileDialog')
    mainForm.show()
    sys.exit(app.exec_())


