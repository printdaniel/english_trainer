from app.database import get_connection
from datetime import datetime


class Vocabulary:
    """Model for managing vocabulary words"""

    @staticmethod
    def add_word(word: str, translation: str = None, example: str = None, level: str = None):
        """Add a new word to the vocabulary database"""
        conn = get_connection()
        cursor = conn.cursor()

        today = datetime.today().strftime("%Y-%m-%d")

        cursor.execute("""
            INSERT INTO vocabulary (word, translation, example_sentence, level, next_review)
            VALUES (?, ?, ?, ?, ?)
        """, (word, translation, example, level, today))

        conn.commit()
        conn.close()

    @staticmethod
    def get_all_words():
        """Retrieve all words from the database"""
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, word, translation, example_sentence, level, next_review,
                   interval, repetitions
            FROM vocabulary
            ORDER BY word
        """)

        words = cursor.fetchall()
        conn.close()

        return words

    @staticmethod
    def get_word_by_id(word_id: int):
        """Get a specific word by its ID"""
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, word, translation, example_sentence, level, next_review,
                   interval, ease_factor, repetitions
            FROM vocabulary
            WHERE id = ?
        """, (word_id,))

        word = cursor.fetchone()
        conn.close()

        return word

    @staticmethod
    def get_random_word():
        """Get a random word for practice"""
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, word, translation, example_sentence, level, next_review,
                   interval, ease_factor, repetitions
            FROM vocabulary
            ORDER BY RANDOM()
            LIMIT 1
        """)

        word = cursor.fetchone()
        conn.close()

        return word

    @staticmethod
    def delete_word(word_id: int):
        """Delete a word from the database"""
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM vocabulary WHERE id = ?", (word_id,))

        conn.commit()
        conn.close()

    @staticmethod
    def get_due_words(limit: int = 10):
        """Get words that are due for review today"""
        conn = get_connection()
        cursor = conn.cursor()

        today = datetime.today().strftime("%Y-%m-%d")

        cursor.execute("""
            SELECT id, word, translation, example_sentence, level
            FROM vocabulary
            WHERE next_review <= ?
            ORDER BY next_review
            LIMIT ?
        """, (today, limit))

        rows = cursor.fetchall()
        conn.close()

        # Convert rows to dictionaries
        words = []
        for row in rows:
            words.append({
                'id': row[0],
                'word': row[1],
                'translation': row[2],
                'example_sentence': row[3],
                'level': row[4]
            })

        return words
