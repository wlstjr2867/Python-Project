#  조회 페이지

from PySide6.QtWidgets import (QWidget, QFormLayout, QLineEdit, QTextEdit, QPushButton,QHBoxLayout,QMessageBox)
from PySide6.QtCore import Signal

class ViewPage(QWidget):
    request_list = Signal()
    request_edit = Signal(int)
    request_delete = Signal(int)
    
    # 생성자
    def __init__(self, db):
        super().__init__()
        self.db = db
        # 현재 조회 중인 게시글 ID 저장용
        self.current_post_id = None

        # 레이아웃 생성
        layout = QFormLayout()

        # 조회용 입력 위젯 생성
        self.title = QLineEdit()
        self.author = QLineEdit()
        self.created = QLineEdit()
        self.updated = QLineEdit()
        self.content = QTextEdit()

        # for문을 사용해 읽기 전용으로 설정
        for w in [self.title, self.author, self.created, self.updated, self.content]:
            w.setReadOnly(True)

        # 버튼 설정
        btn_edit = QPushButton("수정")
        btn_delete = QPushButton("삭제")
        btn_back = QPushButton("목록")
        
        # 연결 설정
        btn_edit.clicked.connect(self.go_edit)
        btn_delete.clicked.connect(self.go_delete)
        btn_back.clicked.connect(self.request_list.emit)
        
        # 버튼 가로 설정
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(btn_edit)
        btn_layout.addWidget(btn_delete)
        btn_layout.addWidget(btn_back)

        # 레이아웃 구성
        layout.addRow("제목", self.title)
        layout.addRow("작성자", self.author)
        layout.addRow("작성일", self.created)
        layout.addRow("수정일", self.updated)
        layout.addRow("내용", self.content)
        # 버튼 줄 추가
        layout.addRow(btn_layout)
        # 레이아웃을 이 페이지에 적용
        self.setLayout(layout)

    def load_post(self, post_id):
        # 현재 게시글 Id 저장
        self.current_post_id = post_id
        # DB에서 게시글 단건 조회
        post = self.db.get_post(post_id)

        # 데이터를 각 필드에 표시
        self.title.setText(post["title"])
        self.author.setText(post["author"])
        self.created.setText(post["created_at"])
        self.updated.setText(post["updated_at"])
        self.content.setText(post["content"])

    def go_edit(self):
        self.request_edit.emit(self.current_post_id)
        
    def go_delete(self):
        # 삭제 확인 팝업에서 
        if not self.confirm_delete():
            return # No를 누르면 중단
        
        # Yes를 누르면 메인에게 삭제 요청 신호
        self.request_delete.emit(self.current_post_id)
        
    def confirm_delete(self):
        # 표준 메세지 박스 활용
        reply = QMessageBox.question(self, "삭제 확인", "정말로 이 게시글을 삭제하시겠습니까?",
                                     QMessageBox.Yes | QMessageBox.No
                                     )
        
        return reply == QMessageBox.Yes # Yes면 True, No면 False 반환
