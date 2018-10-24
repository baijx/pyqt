# -*- coding: utf-8 -*-
import sys
import datetime
import uuid

from PyQt5.QtWidgets import *
from PyQt5.QtSql import QSqlDatabase, QSqlQueryModel, QSqlQuery

def create_table_and_init():
    db = QSqlDatabase.addDatabase('QSQLITE')
    db.setDatabaseName('./database.db')
    if not db.open():
        return False
    query = QSqlQuery()
    query.exec("SELECT COUNT(*) FROM SQLITE_MASTER WHERE TYPE = 'table' AND NAME = '%s'" % ('T_KINDS'))
    if query.next():
        if int(query.value(0)) == 0:
            query.exec("CREATE TABLE T_KINDS(ID TEXT, NAME TEXT)")
            query.exec("INSERT INTO T_KINDS VALUES('1','Java')")
            query.exec("INSERT INTO T_KINDS VALUES('2','Oracle')")
            query.exec("INSERT INTO T_KINDS VALUES('3','Linux')")
            query.exec("INSERT INTO T_KINDS VALUES('4','Html')")
            query.exec("INSERT INTO T_KINDS VALUES('5','Python')")
            query.exec("INSERT INTO T_KINDS VALUES('6','Sqlite')")

    query.exec("SELECT COUNT(*) FROM SQLITE_MASTER WHERE TYPE = 'table' AND NAME = '%s'" % ('T_TIPS'))
    if query.next():
        if int(query.value(0)) == 0:
            query.exec("CREATE TABLE T_TIPS(ID TEXT, RELATED_KIND_ID TEXT, TITLE TEXT, CONTENT TEXT, CREATE_TIME TIMESTAMP, REVIEW_TIME TIMESTAMP, REVIEW_COUNT INTEGER)")
    db.close()
    return True

class INote(QWidget):
    def __init__(self):
        super(INote, self).__init__()

        self.review_btn = None
        self.manage_btn = None
        self.left_kind_cbx = None

        self.table_view = None
        self.table_data_model = None
        self.total_page_label = None
        self.current_page = 0
        self.total_page = 0
        self.total_recrod_count = 0
        self.page_record_count = 100

        self.prev_btn = None
        self.next_btn = None

        self.tip_id = None
        self.title = None
        self.right_kind_cbx = None
        self.save_btn = None
        self.update_btn = None
        self.delete_btn = None
        self.container = None

        self.kinds = []

        self.db = None

        self.init_ui()
        self.init_data()

        self.left_kind_cbx.activated.connect(self.on_left_kind_cbx_activate)
        self.table_view.clicked.connect(self.on_table_view_clicked)
        self.save_btn.clicked.connect(self.on_save_btn_clicked)
        self.update_btn.clicked.connect(self.on_update_btn_clicked)
        self.delete_btn.clicked.connect(self.on_delete_btn_clicked)

    def closeEvent(self, event):
        # 关闭数据库
        self.db.close()

    def init_ui(self):
        self.review_btn = QPushButton()
        self.review_btn.setText("review")
        self.manage_btn = QPushButton()
        self.manage_btn.setText("manage")

        self.left_kind_cbx = QComboBox()

        self.table_view = QTableView()
        self.table_view.horizontalHeader().setStretchLastSection(True)
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.prev_btn = QPushButton()
        self.prev_btn.setText("prev")
        self.next_btn = QPushButton()
        self.next_btn.setText("next")

        self.tip_id = QLineEdit();
        self.tip_id.hide()

        self.title = QLineEdit()

        self.right_kind_cbx = QComboBox()

        self.save_btn = QPushButton()
        self.save_btn.setText("save")

        self.update_btn = QPushButton()
        self.update_btn.setText("update")

        self.delete_btn = QPushButton()
        self.delete_btn.setText("delete")

        self.container = QTextEdit()

        # left box
        left_mgr_btn_box = QHBoxLayout()
        left_mgr_btn_box.addWidget(self.review_btn)
        left_mgr_btn_box.addWidget(self.manage_btn)

        left_page_btn_box = QHBoxLayout()
        left_page_btn_box.addWidget(self.prev_btn)
        left_page_btn_box.addWidget(self.next_btn)

        left_box = QVBoxLayout()
        left_box.addLayout(left_mgr_btn_box)
        left_box.addWidget(self.left_kind_cbx)
        left_box.addWidget(self.table_view)
        left_box.addLayout(left_page_btn_box)

        # right box
        right_title_box = QHBoxLayout()
        right_title_box.addWidget(self.tip_id)
        right_title_box.addWidget(self.title)
        right_title_box.addWidget(self.right_kind_cbx)
        right_title_box.addWidget(self.save_btn)
        right_title_box.addWidget(self.update_btn)
        right_title_box.addWidget(self.delete_btn)

        right_box = QVBoxLayout()
        right_box.addLayout(right_title_box, 1)
        right_box.addWidget(self.container, 500)

        # main box
        main_box = QHBoxLayout()
        main_box.addLayout(left_box)
        main_box.addLayout(right_box, 1)

        self.setLayout(main_box)
        self.setWindowTitle('inote')
        self.resize(800, 600)

    def init_data(self):
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName('./database.db')
        self.db.open()

        self.get_all_kinds()
        for option in self.kinds:
            self.left_kind_cbx.addItem(option[1], option[0])
            self.left_kind_cbx.setCurrentIndex(-1)
            self.right_kind_cbx.addItem(option[1], option[0])
            self.right_kind_cbx.setCurrentIndex(-1)

        self.table_data_model = QSqlQueryModel(self)
        self.update_table_data()

    def update_table_data(self):
        sql = "SELECT ID, TITLE FROM T_TIPS"
        kind_id = self.left_kind_cbx.currentData()
        if kind_id:
            sql_where = " WHERE RELATED_KIND_ID = '%s'" % (kind_id)
            sql = sql + sql_where
        print(sql)
        self.table_data_model.setQuery(sql)
        self.table_view.setModel(self.table_data_model)
        _TITLE_COLUMN_NUM = 1
        for i in range(self.table_data_model.columnCount()):
            if i != _TITLE_COLUMN_NUM:
                self.table_view.setColumnHidden(i, True)

    def get_all_kinds(self):
        query = QSqlQuery()
        sql = "SELECT ID, NAME FROM T_KINDS"
        query.exec(sql)
        while (query.next()):
            option = [query.value(0), query.value(1)]
            self.kinds.append(option)

    def on_left_kind_cbx_activate(self):
        self.update_table_data()

    def on_table_view_clicked(self, target):
        _TABLE_ID_COLUMN = 0
        id = self.table_data_model.index(target.row(), _TABLE_ID_COLUMN).data()
        query = QSqlQuery()
        sql = "SELECT ID, RELATED_KIND_ID, TITLE, CONTENT FROM T_TIPS WHERE ID = '%s'" % (id)
        query.exec(sql)
        while (query.next()):
            self.tip_id.setText(query.value(0))
            related_kind_id = query.value(1)
            kind_cbx_text = ''
            for option in self.kinds:
                if related_kind_id == option[0]:
                    kind_cbx_text = option[1]
                    break
            if kind_cbx_text == '':
                self.right_kind_cbx.setCurrentIndex(-1)
            else:
                self.right_kind_cbx.setCurrentText(kind_cbx_text)
            self.title.setText(query.value(2))
            self.container.setText(query.value(3))
            break

    def on_save_btn_clicked(self):
        id = uuid.uuid1()
        title = self.title.text()
        if title == '':
            return
        kind_id = self.right_kind_cbx.currentData()
        content = self.container.toPlainText()
        create_time = datetime.datetime.now()
        sql = "INSERT INTO T_TIPS VALUES ('%s','%s','%s','%s', '%s', '', '0')" % (
            id, kind_id, title, content, create_time)
        print(sql)
        self.db.exec_(sql)
        self.db.commit()
        self.clear_left_content()
        self.update_table_data()

    def on_update_btn_clicked(self):
        id = self.tip_id.text()
        if id == '':
            return
        kind_id = self.right_kind_cbx.currentData()
        title = self.title.text()
        content = self.container.toPlainText()
        sql = "UPDATE T_TIPS SET RELATED_KIND_ID = '%s', TITLE = '%s', CONTENT = '%s' WHERE ID = '%s'" % (
            kind_id, title, content, id)
        print(sql)
        self.db.exec_(sql)
        self.db.commit()
        self.clear_left_content()
        self.update_table_data()

    def on_delete_btn_clicked(self):
        id = self.tip_id.text()
        if id == '':
            return
        confirm = QMessageBox.question(
            self,
            '提示',
            '是否删除？',
            QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            sql = "DELETE FROM T_TIPS WHERE ID = '%s'" % (id)
            print(sql)
            self.db.exec_(sql)
            self.db.commit()
            self.clear_left_content()
            self.clear_right_content()
            self.update_table_data()

    def clear_left_content(self):
        self.left_kind_cbx.setCurrentIndex(-1)

    def clear_right_content(self):
        self.tip_id.setText("")
        self.title.setText("")
        self.right_kind_cbx.setCurrentIndex(-1)
        self.container.setText("")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    if create_table_and_init():
        inote = INote()
        inote.show()
    sys.exit(app.exec_())
