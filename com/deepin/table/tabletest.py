# -*- coding: utf-8 -*-
import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class Ddup(QWidget):
    def __init__(self):
        super(Ddup, self).__init__()

        tableview = QTableView()
        dm = QStandardItemModel(100, 5)
        dm.setHeaderData(0, Qt.Horizontal, "编号")
        dm.setHeaderData(1, Qt.Horizontal, "姓名")
        dm.setHeaderData(2, Qt.Horizontal, "性别")
        dm.setHeaderData(3, Qt.Horizontal, "年龄")
        dm.setHeaderData(4, Qt.Horizontal, "院系")
        tableview.setModel(dm)
        tableview.horizontalHeader().setStretchLastSection(True)
        tableview.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # main box
        mbox = QHBoxLayout()
        mbox.addWidget(tableview)

        self.setLayout(mbox)
        self.setWindowTitle('ddup')
        self.resize(800, 600)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ddup = Ddup()
    ddup.show()
    sys.exit(app.exec_())
