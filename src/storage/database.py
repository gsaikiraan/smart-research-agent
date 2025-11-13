"""Database storage for research data."""

import sqlite3
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional


class ResearchDatabase:
    """SQLite database for storing research results."""

    def __init__(self, db_path: Path):
        """
        Initialize database connection.

        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _init_db(self):
        """Initialize database schema."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Research sessions table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS research_sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    topic TEXT NOT NULL,
                    depth TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    completed_at TIMESTAMP,
                    status TEXT DEFAULT 'in_progress',
                    summary TEXT,
                    report_path TEXT
                )
            """)

            # Sources table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS sources (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id INTEGER,
                    title TEXT,
                    url TEXT,
                    content TEXT,
                    relevance_score REAL,
                    retrieved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (session_id) REFERENCES research_sessions (id)
                )
            """)

            # Findings table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS findings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id INTEGER,
                    finding TEXT NOT NULL,
                    source_ids TEXT,
                    confidence REAL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (session_id) REFERENCES research_sessions (id)
                )
            """)

            conn.commit()

    def create_session(self, topic: str, depth: str) -> int:
        """
        Create a new research session.

        Args:
            topic: Research topic
            depth: Research depth (quick, standard, deep)

        Returns:
            Session ID
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO research_sessions (topic, depth) VALUES (?, ?)",
                (topic, depth),
            )
            conn.commit()
            return cursor.lastrowid

    def add_source(
        self,
        session_id: int,
        title: str,
        url: str,
        content: str,
        relevance_score: float = 0.0,
    ):
        """Add a source to a research session."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO sources
                   (session_id, title, url, content, relevance_score)
                   VALUES (?, ?, ?, ?, ?)""",
                (session_id, title, url, content, relevance_score),
            )
            conn.commit()

    def add_finding(
        self,
        session_id: int,
        finding: str,
        source_ids: List[int],
        confidence: float = 0.0,
    ):
        """Add a finding to a research session."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO findings
                   (session_id, finding, source_ids, confidence)
                   VALUES (?, ?, ?, ?)""",
                (session_id, finding, json.dumps(source_ids), confidence),
            )
            conn.commit()

    def complete_session(
        self, session_id: int, summary: str, report_path: Optional[str] = None
    ):
        """Mark a research session as completed."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """UPDATE research_sessions
                   SET status = 'completed',
                       completed_at = CURRENT_TIMESTAMP,
                       summary = ?,
                       report_path = ?
                   WHERE id = ?""",
                (summary, report_path, session_id),
            )
            conn.commit()

    def get_session(self, session_id: int) -> Optional[Dict[str, Any]]:
        """Get a research session by ID."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM research_sessions WHERE id = ?", (session_id,)
            )
            row = cursor.fetchone()
            return dict(row) if row else None

    def list_sessions(self, limit: int = 10) -> List[Dict[str, Any]]:
        """List recent research sessions."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(
                """SELECT * FROM research_sessions
                   ORDER BY created_at DESC
                   LIMIT ?""",
                (limit,),
            )
            return [dict(row) for row in cursor.fetchall()]
