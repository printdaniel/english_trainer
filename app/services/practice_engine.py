from datetime import date
import time
from app.database import get_connection


class PracticeSession:
    """Handle practice sessions with progress tracking"""

    def __init__(self, srs_service):
        self.srs = srs_service
        self.reviewed = 0
        self.correct = 0
        self.incorrect = 0
        self.start_time = None

    def run(self, limit=10):
        """Run a practice session with a specified number of words"""
        self.start_time = time.time()

        words = self.srs.get_due_words(limit)

        if not words:
            print("\n✓ No words due for review. Great job!")
            return

        print(f"\n{'='*50}")
        print(f"  Starting Practice Session ({len(words)} words)")
        print(f"{'='*50}\n")

        for i, word in enumerate(words, 1):
            self.review_word(word, i, len(words))

        self.finish()

    def review_word(self, word, index, total):
        """Review a single word and check the answer"""
        print(f"\n[{index}/{total}] Translate: {word['word']}")

        if word['example_sentence']:
            print(f"   Example: {word['example_sentence']}")

        answer = input("   Your answer: ").strip()

        is_correct = answer.lower() == word['translation'].lower()

        if is_correct:
            print("   ✓ Correct!")
            self.correct += 1
        else:
            print(f"   ✗ Incorrect (correct answer: {word['translation']})")
            self.incorrect += 1

        self.reviewed += 1
        self.srs.update_word_review(word['id'], is_correct)

    def finish(self):
        """Finish the session and display statistics"""
        duration = int(time.time() - self.start_time)

        accuracy = 0
        if self.reviewed > 0:
            accuracy = (self.correct / self.reviewed) * 100

        print(f"\n{'='*50}")
        print("  Session Complete!")
        print(f"{'='*50}")
        print(f"  Reviewed:  {self.reviewed} words")
        print(f"  Correct:   {self.correct}")
        print(f"  Incorrect: {self.incorrect}")
        print(f"  Accuracy:  {accuracy:.1f}%")
        print(f"  Duration:  {duration} seconds")
        print(f"{'='*50}\n")

        self.save_progress(accuracy, duration)

    def save_progress(self, accuracy, duration):
        """Save session progress to the database"""
        conn = get_connection()
        cursor = conn.cursor()
        today = date.today().strftime("%Y-%m-%d")

        # Check if there's already a record for today
        cursor.execute("""
            SELECT id, words_reviewed, words_correct
            FROM daily_progress
            WHERE date = ?
        """, (today,))

        existing = cursor.fetchone()

        if existing:
            # Update existing record
            cursor.execute("""
                UPDATE daily_progress
                SET words_reviewed = words_reviewed + ?,
                    words_correct = words_correct + ?,
                    accuracy = ?,
                    session_duration = session_duration + ?
                WHERE date = ?
            """, (self.reviewed, self.correct, accuracy, duration, today))
        else:
            # Insert new record
            cursor.execute("""
                INSERT INTO daily_progress
                (date, words_reviewed, words_correct, accuracy, session_duration)
                VALUES (?, ?, ?, ?, ?)
            """, (today, self.reviewed, self.correct, accuracy, duration))

        conn.commit()
        conn.close()
