from datetime import datetime, timedelta
from app.database import get_connection


class SRS:
    """Spaced Repetition System for vocabulary learning"""

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

    @staticmethod
    def update_word_review(word_id: int, correct: bool):
        """Update word review based on SRS algorithm"""
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT repetitions, interval, ease_factor
            FROM vocabulary
            WHERE id = ?
        """, (word_id,))

        result = cursor.fetchone()

        if not result:
            conn.close()
            return

        repetitions, interval, ease_factor = result

        today = datetime.today()

        if correct:
            repetitions += 1

            if repetitions == 1:
                interval = 1
            elif repetitions == 2:
                interval = 3
            else:
                interval = int(interval * ease_factor)

            next_review = today + timedelta(days=interval)

        else:
            repetitions = 0
            interval = 1
            next_review = today + timedelta(days=1)

        cursor.execute("""
            UPDATE vocabulary
            SET repetitions = ?, interval = ?, next_review = ?
            WHERE id = ?
        """, (repetitions, interval, next_review.strftime("%Y-%m-%d"), word_id))

        conn.commit()
        conn.close()
