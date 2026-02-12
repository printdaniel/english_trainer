from pathlib import Path
import sqlite3


# Base directory del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent

# Carpeta donde se guarda la base de datos
DATA_DIR = BASE_DIR / "data"

# Ruta final del archivo .db
DB_PATH = DATA_DIR / "english_trainer.db"


def get_connection():
    """Return a SQLite connection."""
    return sqlite3.connect(DB_PATH)


def init_db():
    """
    Initialize the SQLite database and create all required tables
    if they do not already exist.
    """

    # Crear carpeta data si no existe
    DATA_DIR.mkdir(exist_ok=True)

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
            words_written INTEGER DEFAULT 0
        );
    """)

    conn.commit()
    conn.close()

