#  수정 페이지

from PySide6.QtWidgets import (QWidget, QFormLayout, QLineEdit, QTextEdit, QPushButton,QHBoxLayout)
from PySide6.QtCore import Signal

class EditPage(QWidget):
    request_view = Signal(int)
    request_list = Signal()

    # 생성자
    def __init__(self, db):
        super().__init__()
        self.db = db
        # 현재 수정 중인 게시글 ID 저장용
        self.current_post_id = None

        # 레이아웃 생성
        layout = QFormLayout()

        # 입력 위젯
        self.title = QLineEdit()
        self.author = QLineEdit()
        self.content = QTextEdit()

        # 버튼 생성
        btn_save = QPushButton("저장")
        btn_cancel = QPushButton("취소")

        # 연결 설정
        btn_save.clicked.connect(self.save)
        btn_cancel.clicked.connect(self.cancel)

        # 버튼 가로 설정
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(btn_save)
        btn_layout.addWidget(btn_cancel)
        
        # 레이아웃 구성
        layout.addRow("제목", self.title)
        layout.addRow("작성자", self.author)
        layout.addRow("내용", self.content)
        layout.addRow(btn_layout)

        # 레이아웃을 이 페이지에 적용
        self.setLayout(layout)

    def load_post(self, post_id):
        # 현재 수정중인 Id 저장
        self.current_post_id = post_id
        # DB 에서 데이터 가져오기
        post = self.db.get_post(post_id)

        # 기존 내용을 입력창에 세팅
        self.title.setText(post["title"])
        self.author.setText(post["author"])
        self.content.setText(post["content"])

    def save(self):
        # DB 매너지의 함수를 호출하여 실제 데이터베이스 수정
        self.db.update_post(
            self.current_post_id,
            self.title.text(),
            self.content.toPlainText()
        )
        # 수정 완료 후 다시 조회 페이지로 이동
        self.request_view.emit(self.current_post_id)

    def cancel(self):
        # DB 작업 없이 바로 조회 페이자로 복귀
        self.request_view.emit(self.current_post_id)