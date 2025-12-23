# DB 매니저

import sqlite3
from datetime import datetime


class DBManager:
    # DBManager 객체 생성 시 실행되는 생성자
    def __init__(self, db_path="board.db"):
        # SQLite DB 파일에 연결 (없으면 자동생성)
        self.conn = sqlite3.connect(db_path)
        # 조회 결과를 dict 처럼 사용하기 위해 설정
        self.conn.row_factory = sqlite3.Row
        # SQL 실행을 위한 커서 객체
        self.cur = self.conn.cursor()
        # 테이블이 없으면 생성
        self.create_table()

    # 게시글 테이블 생성
    def create_table(self):
        # posts 테이블이 없을 경우 생성
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            author TEXT,
            created_at TEXT,
            updated_at TEXT
        )
        """)
        # 테이블 생성 반영
        self.conn.commit()

    # 목록 조회
    def get_posts(self):
        self.cur.execute("""
        SELECT id, title, created_at
        FROM posts
        ORDER BY id DESC
        """)
        # 여러 행을 리스트 형태로 반환
        return self.cur.fetchall()

    # 단건 조회
    def get_post(self, post_id):
        # 특정 id에 해당하는 게시글 조회
        self.cur.execute("""
        SELECT *
        FROM posts
        WHERE id = ?
        """, (post_id,)) # SQL Injection 방지용 바인딩
        
        # 한 행만 가져옴
        row = self.cur.fetchone()
        
        # 결과가 있으면 dict로 변환해서 반환
        return dict(row) if row else None

    # 게시글 저장
    def write_post(self, title, content, author):
        # 제목이나 내용이 비어 있으면 저장x
        if not title.strip() or not content.strip():
            return False  # 유효성 검사 (과제 8번)

        # 현재 시간 문자열 생성
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.cur.execute("""
        INSERT INTO posts (title, content, author, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?)
        """, (title, content, author, now, now))

        # DB에 실제 반영
        self.conn.commit()
        # 저장 성공
        return True

    # 게시글 수정
    def update_post(self, post_id, title, content):
        if not title.strip() or not content.strip():
            return False

        # 수정 시간 갱신
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 해당 id 게시글 수정
        self.cur.execute("""
        UPDATE posts
        SET title = ?, content = ?, updated_at = ?
        WHERE id = ?
        """, (title, content, now, post_id))

        self.conn.commit()
        return True

    # 게시글 삭제
    def delete_post(self, post_id):
        # 특정 id 게시글 삭제
        self.cur.execute("""
        DELETE FROM posts
        WHERE id = ?
        """, (post_id,))
        self.conn.commit()

    def close(self):
        # 프로그램 종료시 DB 연결 해제
        self.conn.close()