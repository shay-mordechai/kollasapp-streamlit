#app/core/database_manager.py
import sqlite3
import os
from contextlib import contextmanager

DB_PATH = "kollas.db"

class DatabaseManager:
    @staticmethod
    @contextmanager
    def get_connection():
        conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        conn.row_factory = sqlite3.Row  # Access columns by name
        try:
            yield conn
        finally:
            conn.close()

    @staticmethod
    def init_db():
        """Creates tables if they don't exist."""
        with DatabaseManager.get_connection() as conn:
            cursor = conn.cursor()
            # Songs Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS songs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    file_path TEXT UNIQUE,  -- Relative path from mount root
                    filename TEXT,
                    title TEXT,
                    cantor TEXT DEFAULT 'Unknown',
                    origin TEXT DEFAULT 'Unknown',
                    category TEXT DEFAULT 'General',
                    lyrics TEXT,
                    status TEXT DEFAULT 'unverified', -- unverified, pending, verified
                    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            # Create Index for fast search
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_search ON songs(title, cantor, lyrics);")
            conn.commit()

    @staticmethod
    def search_songs(query=None, limit=50, offset=0, only_verified=True):
        """Highly optimized search query."""
        sql = "SELECT * FROM songs WHERE 1=1"
        params = []

        if only_verified:
            sql += " AND status = 'verified'"

        if query:
            sql += " AND (title LIKE ? OR cantor LIKE ? OR lyrics LIKE ?)"
            wildcard = f"%{query}%"
            params.extend([wildcard, wildcard, wildcard])

        sql += " ORDER BY title ASC LIMIT ? OFFSET ?"
        params.extend([limit, offset])

        with DatabaseManager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, params)
            return [dict(row) for row in cursor.fetchall()]

    @staticmethod
    def get_song_by_id(song_id):
        with DatabaseManager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM songs WHERE id = ?", (song_id,))
            row = cursor.fetchone()
            return dict(row) if row else None

    @staticmethod
    def update_song_metadata(song_id, title, cantor, origin, lyrics, status="pending"):
        with DatabaseManager.get_connection() as conn:
            conn.execute("""
                UPDATE songs
                SET title = ?, cantor = ?, origin = ?, lyrics = ?, status = ?
                WHERE id = ?
            """, (title, cantor, origin, lyrics, status, song_id))
            conn.commit()

    @staticmethod
    def get_pending_reviews():
        with DatabaseManager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM songs WHERE status = 'pending' ORDER BY added_at DESC")
            return [dict(row) for row in cursor.fetchall()]
