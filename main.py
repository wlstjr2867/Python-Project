import sys
from PySide6.QtWidgets import QApplication, QStackedWidget

from db.db_manager import DBManager
from pages.list_page import ListPage
from pages.write_page import WritePage
from pages.view_page import ViewPage
from pages.edit_page import EditPage

# 앱 시작
def main() : 
    app = QApplication(sys.argv)
    
    # 페이지 컨테이너
    stack = QStackedWidget()
    stack.resize(700, 500)
    
    # DB 매니저
    db = DBManager()
    
    # 페이지 생성
    list_page = ListPage(db)
    write_page = WritePage(db)
    view_page = ViewPage(db)
    edit_page = EditPage(db)
    
    # 페이지 등록
    stack.addWidget(list_page)   # 0 (목록)
    stack.addWidget(write_page)  # 1 (작성)
    stack.addWidget(view_page)   # 2 (조회)
    stack.addWidget(edit_page)   # 3 (수정)
    
    # 최초 목록 로딩
    list_page.load_posts(db.get_posts())

    # 페이지 전환 연결 (Signal -> Slot)
    # list_page안에서 request_write 시그널 발생 후 1로 이동 (목록 -> 작성)
    list_page.request_write.connect(lambda: stack.setCurrentIndex(1))
    
    # 목록 -> 조회
    list_page.request_view.connect(
        lambda post_id: (
            # 조회 페이지에 데이터 세팅 (post_id를 받아 해당 글 조회)
            view_page.load_post(post_id),
            # 조회 페이지로 이동
            stack.setCurrentIndex(2)
        )
    )
    
    # 조회 -> 목록
    view_page.request_list.connect(lambda: stack.setCurrentIndex(0))
    
    # 조회 -> 수정
    view_page.request_edit.connect(
        lambda post_id: (
            edit_page.load_post(post_id),
            stack.setCurrentIndex(3)
        )
    )
    
    # 조회 -> 삭제
    view_page.request_delete.connect(
        lambda post_id:(
            db.delete_post(post_id),
            list_page.load_posts(db.get_posts()),
            stack.setCurrentIndex(0)
        )
    )
    
    # 작성 -> 저장 -> 목록
    write_page.request_save.connect(
        lambda title, content, author: (
            db.write_post(title, content, author),
            list_page.load_posts(db.get_posts()),
            stack.setCurrentIndex(0)
        )
    )
    
    # 작성 -> 목록
    write_page.request_list.connect(lambda: stack.setCurrentIndex(0))
    
    # 수정 -> 저장 후 조회
    edit_page.request_view.connect(
        lambda post_id : (
            view_page.load_post(post_id),
            stack.setCurrentIndex(2)
        )
    )
    
    # 시작페이지
    stack.setCurrentIndex(0)
    stack.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
