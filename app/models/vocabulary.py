from app.database import get_connection


class Vocabulary:
    """Model for vocabulary CRUD operations."""

    @staticmethod
    def add_word(word: str, translation: str = None, example_sentence: str = None, level: str = None):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO vocabulary (word, translation, example_sentence, level)
            VALUES (?, ?, ?, ?)
        """, (word, translation, example_sentence, level))

        conn.commit()
        conn.close()

    @staticmethod
    def get_all_words():
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM vocabulary")
        rows = cursor.fetchall()

        conn.close()
        return rows

    @staticmethod
    def delete_word(word_id: int):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM vocabulary WHERE id = ?", (word_id,))
        conn.commit()
        conn.close()

    @staticmethod
    def update_word(word_id: int, word: str, translation: str, example_sentence: str, level: str):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE vocabulary
            SET word = ?, translation = ?, example_sentence = ?, level = ?
            WHERE id = ?
        """, (word, translation, example_sentence, level, word_id))

        conn.commit()
        conn.close()

    @staticmethod
    def get_random_word():
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""SELECT * FROM vocabulary
                        WHERE next_review IS NULL OR next_review <= date('now')
                        ORDER BY RANDOM()
                        LIMIT 1""")

        word = cursor.fetchone()

        conn.close()
        return word


