#  메인 페이지 (목록)

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QListWidget, QListWidgetItem, QPushButton)
from PySide6.QtCore import Qt, Signal

class ListPage(QWidget):
    request_view = Signal(int)
    request_write = Signal()
    
    # 생성자
    def __init__(self, db):
        super().__init__()
        self.db = db
        
        # 기본 레이아웃을 세로 방향으로 설정 (QVBoxLayout = 세로 방향 레이아웃)
        self.layout = QVBoxLayout(self)
        
        self.title_label = QLabel("게시글 목록")
        # 가운데 설정
        self.title_label.setAlignment(Qt.AlignCenter)
        # 목록을 표시할 리스트 위젯
        self.list_widget = QListWidget()
        
        self.btn_write = QPushButton("글쓰기")

        # 레이아웃 추가 항목
        self.layout.addWidget(self.title_label)
        self.layout.addWidget(self.list_widget)
        self.layout.addWidget(self.btn_write)
        
        # 리스트 클릭시 실행될 함수 연결
        self.list_widget.itemClicked.connect(self.on_item_clicked)
        # 버튼 클릭시 실행될 함수 연결
        self.btn_write.clicked.connect(self.on_write_clicked)
        
    def load_posts(self, posts):
        
        # 기존 리스트 초기화 (중복방지)
        self.list_widget.clear()
        
        # posts의 형태
        for post_id, title, created_at in posts:
            # 화면에 보여지는 문자열 생성
            item = QListWidgetItem(f"{title} | {created_at}")
            # post_id를 아이템에 숨겨서 저장
            item.setData(Qt.UserRole, post_id)
            # 리스트에 아이템(게시물 하나) 추가
            self.list_widget.addItem(item)
            
    def on_item_clicked(self, item):
        # 클릭한 아이템에서 숨겨둔 게시글 id 가져오기
        post_id = item.data(Qt.UserRole)
        # request_view에 post_id를 전송
        self.request_view.emit(post_id)
        
    def on_write_clicked(self):
        # 글쓰기 버튼 클릭시 request_write로 전송 (시그널 발생)
        self.request_write.emit()
