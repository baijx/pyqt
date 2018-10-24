#coding=utf-8
from PyQt5.QtWidgets import *
import sys

class GridLayout(QWidget):
    def __init__(self):
        super(GridLayout, self).__init__()
        button1 = QPushButton("1")
        button2 = QPushButton("2")
        button2.resize(300, 30)
        button3 = QPushButton("3")
        button4 = QPushButton("4")
        button4.resize(300, 30)

        grid = QGridLayout()
        grid.addWidget(button1, 0, 0)
        grid.addWidget(button2, 0, 1)
        grid.addWidget(button3, 1, 0)
        grid.addWidget(button4, 1, 1)

        self.setLayout(grid)
        self.setWindowTitle('box layout')
        self.resize(400, 300)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = GridLayout()
    window.show()
    sys.exit(app.exec_())