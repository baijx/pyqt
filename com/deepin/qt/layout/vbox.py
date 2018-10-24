#coding=utf-8
from PyQt5.QtWidgets import *
import sys

class VLayout(QWidget):
    def __init__(self):
        super(VLayout, self).__init__()
        button1 = QPushButton("1")
        button2 = QPushButton("2")
        button3 = QPushButton("3")
        button4 = QPushButton("4")
        button5 = QPushButton("5")

        vbox = QVBoxLayout()
        vbox.addWidget(button1)
        vbox.addWidget(button2)
        vbox.addWidget(button3)
        vbox.addWidget(button4)
        vbox.addWidget(button5)

        self.setLayout(vbox)
        self.setWindowTitle('box layout')
        self.resize(400, 300)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = VLayout()
    window.show()
    sys.exit(app.exec_())