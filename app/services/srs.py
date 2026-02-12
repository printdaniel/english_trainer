from datetime import datetime, timedelta
from app.database import get_connection


class SRS:

    @staticmethod
    def update_word_review(word_id: int, correct: bool):
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

