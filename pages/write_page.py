#  글쓰기 페이지

from PySide6.QtWidgets import (QWidget, QFormLayout, QLineEdit, QTextEdit, QPushButton,QHBoxLayout, QMessageBox)
from PySide6.QtCore import Signal

class WritePage(QWidget):
    request_list = Signal()
    request_save = Signal(str, str, str)
    
    def __init__(self, db):
        super().__init__()
        self.db = db
        
        self.layout = QFormLayout(self)
        
        self.input_title = QLineEdit()
        self.input_content = QTextEdit()
        self.input_author = QLineEdit()
        
        self.btn_save = QPushButton("저장")
        self.btn_cancel = QPushButton("취소")

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.btn_save)
        btn_layout.addWidget(self.btn_cancel)
        
        self.layout.addRow("제목", self.input_title)
        self.layout.addRow("내용", self.input_content)
        self.layout.addRow("작성자", self.input_author)
        self.layout.addRow(btn_layout)
        
        self.btn_save.clicked.connect(self.on_save)
        self.btn_cancel.clicked.connect(self.on_cancel)
        
    def on_save(self):
        if not self.validate_inputs():
            return
        
        title = self.input_title.text()
        content = self.input_content.toPlainText()
        author = self.input_author.text()
        
        self.request_save.emit(title, content, author)
        self.clear_fields()
        
    def validate_inputs(self):
        if not self.input_title.text().strip():
            QMessageBox.warning(self, "입력 오류", "제목을 입력하세요.")
            return False
        
        if not self.input_content.toPlainText().strip():
            QMessageBox.warning(self, "입력 오류", "내용을 입력하세요")
            return False
        
        return True
            
    def on_cancel(self):
        self.clear_fields()
        self.request_list.emit()
        
    def clear_fields(self):
        self.input_title.clear()
        self.input_content.clear()
        self.input_author.clear()

