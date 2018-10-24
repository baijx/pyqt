__author__ = 'baijx'
import sys
# from com.deepin.qt.hello import Ui_MainWindow
from com.deepin.qt.hello import Ui_Form
from PyQt5.QtWidgets import QApplication, QMainWindow
if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_Form()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())