#  글쓰기 페이지

from PySide6.QtWidgets import (QWidget, QFormLayout, QHBoxLayout, QLineEdit, QTextEdit, QPushButton, QMessageBox)
from PySide6.QtCore import Signal

class WritePage(QWidget):
    request_list = Signal()
    #(제목, 내용, 작성자) 3개의 문자열 전달
    request_save = Signal(str, str, str)
    
    # 생성자
    def __init__(self, db):
        super().__init__()
        self.db = db
        
        # 레이아웃 설정 (Form 구조)
        self.layout = QFormLayout(self)
        
        # 입력 생성
        self.input_title = QLineEdit() # 한 줄 입력 위젯 (text()사용)
        self.input_content = QTextEdit() # 여러 줄 입력 위젯 (toPlainText()사용)
        self.input_author = QLineEdit()
        
        # 버튼 생성 및 배치
        self.btn_save = QPushButton("저장")
        self.btn_cancel = QPushButton("취소")

        # 버튼을 가로로 배치하는 레이아웃
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.btn_save)
        btn_layout.addWidget(self.btn_cancel)
        
        # 폼 레이아웃에 항목 추가
        self.layout.addRow("제목", self.input_title)
        self.layout.addRow("내용", self.input_content)
        self.layout.addRow("작성자", self.input_author)
        # 버튼들을 가로로 묶은 레이아웃을 한 행으로 추가
        self.layout.addRow(btn_layout)
        
        # 버튼 클릭시 동작 연결
        self.btn_save.clicked.connect(self.on_save)
        self.btn_cancel.clicked.connect(self.on_cancel)
        
    def on_save(self):
        # 입력값 유효성 검사
        if not self.validate_inputs():
            return
        
        # 입력값 가져오기
        title = self.input_title.text()
        content = self.input_content.toPlainText()
        author = self.input_author.text()
        
        self.request_save.emit(title, content, author)
        # 입력창 초기화
        self.clear_fields()
    
    # 입력값 검증 함수
    def validate_inputs(self):
        # 제목이 비어있는지 확인 (strip()으로 공백만 있는 경우도 체크)
        if not self.input_title.text().strip():
            QMessageBox.warning(self, "입력 오류", "제목을 입력하세요.")
            return False
        
        if not self.input_content.toPlainText().strip():
            QMessageBox.warning(self, "입력 오류", "내용을 입력하세요")
            return False
        
        if not self.input_author.text().strip():
            QMessageBox.warning(self, "입력 오류", "작성자를 입력하세요")
            return False
            
        return True
    
    # 취소 버튼 클릭시 실행        
    def on_cancel(self):
        # 입력창 초기화
        self.clear_fields()
        self.request_list.emit()
    
    # 모든 입력창 초기화
    def clear_fields(self):
        self.input_title.clear()
        self.input_content.clear()
        self.input_author.clear()

