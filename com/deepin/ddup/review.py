# -*- coding: utf-8 -*-
import sys
from PyQt5 import sip
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtSql import QSqlDatabase, QSqlQueryModel, QSqlQuery
#class Review(QDialog):
class Review(QWidget):
    def __init__(self, parent=None):
        super(Review, self).__init__(parent)
        self.init_fields()
        self.init_db()
        self.init_ui()
        self.init_listener()

    def init_fields(self):
        self.db = None

        self.review_id_list = None

        self.welcome_box = None
        self.summary_label = None
        self.start_btn = None
        self.exit_btn = None

        self.review_box = None
        self.title_label = None
        self.kind_label = None
        self.progress_label = None
        self.shadow_box = None
        self.view_btn = None
        self.container = None
        self.yes_btn = None
        self.no_btn = None

    def init_db(self):
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName('./database.db')
        self.db.open()

    def init_ui(self):
        welcome_box = self.welcome_box = QVBoxLayout()

        summary_label = self.summary_label = QLabel()
        summary_label.setAlignment(Qt.AlignCenter)
        self.get_reivew_id_list()
        size = len(self.review_id_list)
        if(size > 0):
            summary_label.setText('本轮您有' + str(size) + '个知识点要复习')
            welcome_box.addWidget(summary_label)
            self.start_btn = QPushButton()
            self.start_btn.setText('开始复习')
            welcome_box.addWidget(self.start_btn)
        else:
            summary_label.setText('恭喜您目前没有要复习的知识点')
            welcome_box.addWidget(summary_label)
            self.exit_btn = QPushButton()
            self.exit_btn.setText('退出复习')
            welcome_box.addWidget(self.exit_btn)

        self.setLayout(welcome_box)
        self.setWindowTitle('ireview')
        self.resize(800, 600)

    def init_review_ui(self):
        review_box = self.review_box = QVBoxLayout()

        title_label = self.title_label = QLabel()
        title_label.setText('hello')
        review_box.addWidget(title_label)

        self.setLayout(self.review_box)


    def get_reivew_id_list(self):
        self.review_id_list = []
        query = QSqlQuery()
        review_count_sql = "SELECT T.Id FROM T_TIPS T WHERE T.REVIEW_TIME < DATETIME(CURRENT_TIMESTAMP,'LOCALTIME');"
        query.exec(review_count_sql)
        while (query.next()):
            self.review_id_list.append(query.value(0))


    def init_listener(self):
        if(self.start_btn):
            self.start_btn.clicked.connect(self.on_start_btn_clicked)
        if(self.exit_btn):
            self.exit_btn.clicked.connect(self.on_exit_btn_clicked)
        pass

    def on_start_btn_clicked(self):
        self.delete_welcome_box()
        self.init_review_ui()

        #self.setLayout(self.review_box)
        #self.setWindowTitle('ireview')
        #self.resize(800, 600)

    def on_exit_btn_clicked(self):
        self.close()


    def delete_welcome_box(self):
        sip.delete(self.start_btn);
        sip.delete(self.summary_label);
        sip.delete(self.welcome_box);


if __name__ == '__main__':
    app = QApplication(sys.argv)
    review = Review()
    review.show()
    sys.exit(app.exec_())