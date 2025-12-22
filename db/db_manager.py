# DB 매니저

import sqlite3
from datetime import datetime


class DBManager:
    def __init__(self, db_path="board.db"):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self.cur = self.conn.cursor()
        self.create_table()

    def create_table(self):
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
        self.conn.commit()

    # 목록 조회
    def get_posts(self):
        self.cur.execute("""
        SELECT id, title, created_at
        FROM posts
        ORDER BY id DESC
        """)
        return self.cur.fetchall()

    # 단건 조회
    def get_post(self, post_id):
        self.cur.execute("""
        SELECT *
        FROM posts
        WHERE id = ?
        """, (post_id,))
        row = self.cur.fetchone()
        return dict(row) if row else None

    # 게시글 저장
    def write_post(self, title, content, author):
        if not title.strip() or not content.strip():
            return False  # 유효성 검사 (과제 8번)

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.cur.execute("""
        INSERT INTO posts (title, content, author, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?)
        """, (title, content, author, now, now))

        self.conn.commit()
        return True

    # 게시글 수정
    def update_post(self, post_id, title, content):
        if not title.strip() or not content.strip():
            return False

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.cur.execute("""
        UPDATE posts
        SET title = ?, content = ?, updated_at = ?
        WHERE id = ?
        """, (title, content, now, post_id))

        self.conn.commit()
        return True

    # 게시글 삭제
    def delete_post(self, post_id):
        self.cur.execute("""
        DELETE FROM posts
        WHERE id = ?
        """, (post_id,))
        self.conn.commit()

    def close(self):
        self.conn.close()