#  조회 페이지

from PySide6.QtWidgets import (QWidget, QFormLayout, QLineEdit, QTextEdit, QPushButton,QHBoxLayout,QMessageBox)
from PySide6.QtCore import Signal

class ViewPage(QWidget):
    request_list = Signal()
    request_edit = Signal(int)
    request_delete = Signal(int)
    
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.current_post_id = None

        layout = QFormLayout()

        self.title = QLineEdit()
        self.author = QLineEdit()
        self.created = QLineEdit()
        self.updated = QLineEdit()
        self.content = QTextEdit()

        for w in [self.title, self.author, self.created, self.updated, self.content]:
            w.setReadOnly(True)

        btn_edit = QPushButton("수정")
        btn_delete = QPushButton("삭제")
        btn_back = QPushButton("목록")
        

        btn_edit.clicked.connect(self.go_edit)
        btn_delete.clicked.connect(self.go_delete)
        btn_back.clicked.connect(self.request_list.emit)
        

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(btn_edit)
        btn_layout.addWidget(btn_delete)
        btn_layout.addWidget(btn_back)

        layout.addRow("제목", self.title)
        layout.addRow("작성자", self.author)
        layout.addRow("작성일", self.created)
        layout.addRow("수정일", self.updated)
        layout.addRow("내용", self.content)
        layout.addRow(btn_layout)

        self.setLayout(layout)

    def load_post(self, post_id):
        self.current_post_id = post_id
        post = self.db.get_post(post_id)

        self.title.setText(post["title"])
        self.author.setText(post["author"])
        self.created.setText(post["created_at"])
        self.updated.setText(post["updated_at"])
        self.content.setText(post["content"])

    def go_edit(self):
        self.request_edit.emit(self.current_post_id)
        
    def go_delete(self):
        if not self.confirm_delete():
            return
              
        self.request_delete.emit(self.current_post_id)
        
    def confirm_delete(self):
        reply = QMessageBox.question(self, "삭제 확인", "정말로 이 게시글을 삭제하시겠습니까?",
                                     QMessageBox.Yes | QMessageBox.No
                                     )
        
        return reply == QMessageBox.Yes
