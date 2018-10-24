#coding=utf-8
from PyQt5.QtWidgets import *
import sys

class HLayout(QWidget):
    def __init__(self):
        super(HLayout, self).__init__()
        button1 = QPushButton("1")
        button2 = QPushButton("2")
        button3 = QPushButton("3")
        button4 = QPushButton("4")
        button5 = QPushButton("5")

        hbox = QHBoxLayout()
        # hbox.addStretch() #先加stretch相当于在左侧加了个弹簧，全屏时弹簧会将元素弹到右侧
        hbox.addWidget(button1)
        hbox.addWidget(button2)
        hbox.addWidget(button3)
        hbox.addWidget(button4, 3)
        hbox.addWidget(button5, 4)
        # 权重系数自己的理解是当宽度有空余需要填充时，没有权重的默认大小，有权重的按权重平分剩余的部分

        self.setLayout(hbox)
        self.setWindowTitle('box layout')
        self.resize(400, 300)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = HLayout()
    window.show()
    sys.exit(app.exec_())