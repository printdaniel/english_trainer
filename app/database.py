from pathlib import Path
import sqlite3
import sys


# =============================
# Paths
# =============================

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "english_trainer.db"


# =============================
# Connection
# =============================

def get_connection():
    """Return a configured SQLite connection."""
    try:
        # Ensure data directory exists before connecting
        DATA_DIR.mkdir(parents=True, exist_ok=True)

        conn = sqlite3.connect(str(DB_PATH), timeout=10.0)
        conn.row_factory = sqlite3.Row  # Allows dict-like row access
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}", file=sys.stderr)
        raise


# =============================
# Database Initialization
# =============================

def init_db():
    """
    Initialize database and ensure all tables and columns exist.
    """
    try:
        # Ensure directory exists
        DATA_DIR.mkdir(parents=True, exist_ok=True)

        conn = get_connection()
        cursor = conn.cursor()

        # -----------------------------
        # Vocabulary Table
        # -----------------------------
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS vocabulary (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                word TEXT NOT NULL,
                translation TEXT,
                example_sentence TEXT,
                level TEXT,
                next_review TEXT,
                interval INTEGER DEFAULT 0,
                ease_factor REAL DEFAULT 2.5,
                repetitions INTEGER DEFAULT 0
            );
        """)

        # -----------------------------
        # Grammar Topics Table
        # -----------------------------
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS grammar_topics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                difficulty TEXT,
                mastery_score INTEGER DEFAULT 0
            );
        """)

        # -----------------------------
        # Writing Practice Table
        # -----------------------------
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS writing_practice (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                topic TEXT,
                text TEXT NOT NULL,
                word_count INTEGER,
                feedback TEXT
            );
        """)

        # -----------------------------
        # Speaking Sessions Table
        # -----------------------------
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS speaking_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                topic TEXT,
                duration_minutes INTEGER,
                notes TEXT
            );
        """)

        # -----------------------------
        # Daily Progress Table
        # -----------------------------
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS daily_progress (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                words_reviewed INTEGER DEFAULT 0,
                words_correct INTEGER DEFAULT 0,
                minutes_spoken INTEGER DEFAULT 0,
                words_written INTEGER DEFAULT 0,
                accuracy REAL DEFAULT 0,
                session_duration INTEGER DEFAULT 0
            );
        """)

        # Commit table creation first
        conn.commit()

        # -----------------------------
        # Migration Safety (Add missing columns if DB already exists)
        # -----------------------------
        ensure_column(cursor, "daily_progress", "accuracy", "REAL DEFAULT 0")
        ensure_column(cursor, "daily_progress", "session_duration", "INTEGER DEFAULT 0")

        # Commit migrations
        conn.commit()
        conn.close()

    except Exception as e:
        print(f"Error initializing database: {e}", file=sys.stderr)
        raise


# =============================
# Schema Utilities
# =============================

def ensure_column(cursor, table_name, column_name, column_definition):
    """
    Ensure a column exists in a table (basic migration support).
    """
    try:
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = [row[1] for row in cursor.fetchall()]

        if column_name not in columns:
            cursor.execute(
                f"ALTER TABLE {table_name} "
                f"ADD COLUMN {column_name} {column_definition};"
            )
    except Exception as e:
        # Column might already exist, that's okay
        pass
