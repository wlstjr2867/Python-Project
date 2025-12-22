#  수정 페이지

from PySide6.QtWidgets import (QWidget, QFormLayout, QLineEdit, QTextEdit, QPushButton,QHBoxLayout)
from PySide6.QtCore import Signal

class EditPage(QWidget):
    request_view = Signal(int)
    request_list = Signal()

    def __init__(self, db):
        super().__init__()
        self.db = db
        self.current_post_id = None

        layout = QFormLayout()

        self.title = QLineEdit()
        self.author = QLineEdit()
        self.content = QTextEdit()

        btn_save = QPushButton("저장")
        btn_cancel = QPushButton("취소")

        btn_save.clicked.connect(self.save)
        btn_cancel.clicked.connect(self.cancel)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(btn_save)
        btn_layout.addWidget(btn_cancel)

        layout.addRow("제목", self.title)
        layout.addRow("작성자", self.author)
        layout.addRow("내용", self.content)
        layout.addRow(btn_layout)

        self.setLayout(layout)

    def load_post(self, post_id):
        self.current_post_id = post_id
        post = self.db.get_post(post_id)

        self.title.setText(post["title"])
        self.author.setText(post["author"])
        self.content.setText(post["content"])

    def save(self):
        self.db.update_post(
            self.current_post_id,
            self.title.text(),
            self.content.toPlainText()
        )
        self.request_view.emit(self.current_post_id)

    def cancel(self):
        self.request_view.emit(self.current_post_id)