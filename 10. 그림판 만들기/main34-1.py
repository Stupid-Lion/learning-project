import sys 
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtWidgets import QPushButton


ui_path = r"./paintshop.ui"
form_class = uic.loadUiType(ui_path)[0] 


class WindowClass(QMainWindow, form_class) : 
    def __init__(self) :
        super().__init__()
        self.setupUi(self)


if __name__ == "__main__" :
    app = QApplication(sys.argv) 
    myWindow = WindowClass() 
    myWindow.show() 
    app.exec_()