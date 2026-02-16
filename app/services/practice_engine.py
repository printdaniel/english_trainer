from datetime import date
import time

class PracticeSession:
    def __init__(self, srs_service, db):
        self.srs = srs_service
        self.db = db
        self.reviewed = 0
        self.correct = 0
        self.incorrect = 0
        self.start_time = None

    def run(self, limit=10):
        self.start_time = time.time()

        words = self.srs.get_due_words(limit)

        if not words:
            print("No words due for review.")
            return

        print(f"\nStarting session ({len(words)} words)\n")

        for i, word in enumerate(words, 1):
            self.review_word(word, i, len(words))

        self.finish()

    def review_word(self, word, index, total):
        print(f"\nWord {index}/{total}: {word['word']}")
        answer = input("Your answer: ")

        is_correct = answer.strip().lower() == word['translation'].lower()

        if is_correct:
            print("✓ Correct")
            self.correct += 1
        else:
            print(f"✗ Incorrect (correct: {word['translation']})")
            self.incorrect += 1

        self.reviewed += 1
        self.srs.update_word_review(word['id'], is_correct)

    def finish(self):
        duration = int(time.time() - self.start_time)

        accuracy = 0
        if self.reviewed > 0:
            accuracy = (self.correct / self.reviewed) * 100

        print("\nSession complete")
        print("-----------------")
        print(f"Reviewed: {self.reviewed}")
        print(f"Correct: {self.correct}")
        print(f"Incorrect: {self.incorrect}")
        print(f"Accuracy: {accuracy:.2f}%")
        print(f"Duration: {duration} seconds")

        self.save_progress(accuracy, duration)

    def save_progress(self, accuracy, duration):
        today = date.today()

        query = """
        INSERT INTO daily_progress
        (date, words_reviewed, words_correct, accuracy, session_duration)
        VALUES (?, ?, ?, ?, ?)
        """

        self.db.execute(query, (
            today,
            self.reviewed,
            self.correct,
            accuracy,
            duration
        ))

