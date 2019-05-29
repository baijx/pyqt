# -*- coding: utf-8 -*-
import sys
import html
import datetime

from PyQt5 import sip
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtSql import QSqlDatabase, QSqlQuery


class Review(QWidget):
    def __init__(self, parent=None):
        super(Review, self).__init__(parent)

        # review param
        self.review_id_dict = None
        self.review_total_num = 0
        self.review_pass_num = 0
        self.review_cursor = 0
        self.review_current_id = None
        self.review_current_title = None
        self.review_current_kind = None
        self.review_current_count = None
        self.review_current_container = None

        # welcome page
        self.welcome_box = None
        self.summary_label = None
        self.start_btn = None
        self.exit_btn = None

        # review page
        self.review_box = None
        self.nav_box = None
        self.title_label = None
        self.progress_label = None
        self.container = None
        self.shadow_box = None
        self.view_btn = None
        self.container = None
        self.rember_box = None
        self.yes_btn = None
        self.no_btn = None

        # complete page
        self.complete_box = None
        self.complete_label = None
        self.exit_completely = False

        self.db = None

        self.init_db()
        self.init_ui()
        self.init_listener()

    def init_db(self):
        self.db = QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName('./database.db')
        self.db.open()

    def init_ui(self):
        welcome_box = self.welcome_box = QVBoxLayout()

        summary_label = self.summary_label = QLabel()
        summary_label.setAlignment(Qt.AlignCenter)
        self.get_reivew_id_dict()
        size = len(self.review_id_dict)
        if size > 0:
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

        nav_box = self.nav_box = QHBoxLayout()
        title_label = self.title_label = QLabel()
        progress_lable = self.progress_label = QLabel()
        nav_box.addWidget(title_label, 1)
        nav_box.addWidget(progress_lable)

        view_btn = self.view_btn = QPushButton()
        view_btn.setText('点击查看内容')
        self.view_btn.clicked.connect(self.on_view_btn_clicked)
        container = self.container = QTextEdit()
        container.setDisabled(True)
        yes_btn = self.yes_btn = QPushButton()
        yes_btn.setText('记得')
        yes_btn.clicked.connect(self.on_yes_btn_clicked)
        yes_btn.hide()
        no_btn = self.no_btn = QPushButton()
        no_btn.setText('不记得')
        no_btn.clicked.connect(self.on_no_btn_clicked)
        no_btn.hide()
        rember_box = self.rember_box = QHBoxLayout()
        rember_box.addWidget(yes_btn)
        rember_box.addWidget(no_btn)

        review_box.addLayout(nav_box)
        review_box.addWidget(container)
        review_box.addWidget(view_btn)
        review_box.addLayout(rember_box)
        self.setLayout(self.review_box)
        self.review_tips()

    def init_complete_ui(self):
        complete_box = self.complete_box = QVBoxLayout()

        complete_label = self.complete_label = QLabel()
        complete_label.setAlignment(Qt.AlignCenter)
        complete_label.setText('恭喜您已完成本轮复习！')
        complete_box.addWidget(complete_label)
        self.exit_btn = QPushButton()
        self.exit_btn.setText('退出复习')
        self.exit_btn.clicked.connect(self.on_exit_btn_clicked)
        complete_box.addWidget(self.exit_btn)

        self.setLayout(complete_box)

    def get_reivew_id_dict(self):
        self.review_id_dict = {}
        query = QSqlQuery()
        # review_count_sql = "SELECT T.Id FROM T_TIPS T WHERE T.REVIEW_TIME < DATETIME(CURRENT_TIMESTAMP,'LOCALTIME')
        # AND T.ID = 'f8ac57c8-34f2-11e9-92ef-005056c00008'"
        review_count_sql = "SELECT T.Id FROM T_TIPS T WHERE T.REVIEW_TIME < DATETIME(CURRENT_TIMESTAMP,'LOCALTIME')"
        query.exec(review_count_sql)
        while query.next():
            self.review_id_dict[query.value(0)] = False

    def get_review_tip_by_id(self, id):
        query = QSqlQuery()
        sql = "SELECT T.ID, T.TITLE, K.NAME, T.CONTENT, T.REVIEW_COUNT from T_TIPS T, T_KINDS K WHERE" \
              " T.RELATED_KIND_ID = K.ID AND T.ID = '%s'" % id
        query.exec(sql)
        while query.next():
            self.review_current_id = query.value(0)
            self.review_current_title = query.value(1)
            self.review_current_kind = query.value(2)
            self.review_current_container = query.value(3)
            self.review_current_count = query.value(4) + 1

    def get_next_review_tip_id(self, dict, cursor):
        left = None
        right = None
        for i in range(len(dict)):
            if i <= cursor and left is None and list(dict.values())[i] == False:
                left = list(dict.keys())[i]
            if i > cursor and right is None and list(dict.values())[i] == False:
                right = list(dict.keys())[i]

        if self.review_cursor + 1 < len(self.review_id_dict):
            self.review_cursor += 1
        else:
            self.review_cursor = 0

        if right is not None:
            return right
        elif left is not None:
            return left
        else:
            return None

    def init_listener(self):
        if self.start_btn:
            self.start_btn.clicked.connect(self.on_start_btn_clicked)
        if self.exit_btn:
            self.exit_btn.clicked.connect(self.on_exit_btn_clicked)
        pass

    def on_start_btn_clicked(self):
        self.delete_welcome_box()
        self.init_review_ui()

    def on_exit_btn_clicked(self):
        self.exit_completely = True
        self.close()

    def on_view_btn_clicked(self):
        self.container.setDisabled(False)
        self.container.setPlainText(html.unescape(self.review_current_container))
        self.view_btn.hide()
        self.yes_btn.show()
        self.no_btn.show()

    def on_yes_btn_clicked(self):
        # 标记dictionary通过状态
        self.review_id_dict[self.review_current_id] = True
        # 修改数据库
        review_time = datetime.datetime.now() + datetime.timedelta(days=pow(2, self.review_current_count))
        sql = "UPDATE T_TIPS SET REVIEW_TIME = '%s', REVIEW_COUNT = '%s' WHERE ID = '%s'" % \
              (review_time, self.review_current_count, self.review_current_id)
        self.db.exec_(sql)
        self.db.commit()

        # 复习下一个
        self.review_pass_num += 1
        if self.review_pass_num == len(self.review_id_dict):
            self.delete_review_box()
            self.init_complete_ui()
        else:
            self.container.clear()
            self.container.setDisabled(True)
            self.view_btn.show()
            self.yes_btn.hide()
            self.no_btn.hide()
            self.review_tips()

    def on_no_btn_clicked(self):
        self.container.clear()
        self.container.setDisabled(True)
        self.view_btn.show()
        self.yes_btn.hide()
        self.no_btn.hide()
        self.review_tips()

    def review_tips(self):
        self.review_current_id = self.get_next_review_tip_id(self.review_id_dict, self.review_cursor)
        if self.review_current_id is not None:
            self.get_review_tip_by_id(self.review_current_id)
            self.title_label.setText(self.review_current_kind + ': ' + self.review_current_title)
            progress = str(self.review_pass_num + 1) + '/' + str(len(self.review_id_dict))
            self.progress_label.setText(progress)

    def delete_welcome_box(self):
        sip.delete(self.start_btn);
        sip.delete(self.summary_label);
        sip.delete(self.welcome_box);

    def delete_review_box(self):
        self.title_label.hide()
        self.progress_label.hide()
        self.container.hide()
        sip.delete(self.review_box)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    review = Review()
    review.show()
    sys.exit(app.exec_())
