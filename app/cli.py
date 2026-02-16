import argparse
import sys
from datetime import date

# Relative imports since this file is in app/
from .models.vocabulary import Vocabulary
from .services.srs import SRS
from .services.practice_engine import PracticeSession


def run():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="English Trainer CLI - Learn English in 30 days",
        epilog="Example: python main.py add hello -t hola -e 'Hello, how are you?'"
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # -----------------------
    # Add word command
    # -----------------------
    add_parser = subparsers.add_parser(
        "add",
        help="Add a new word to your vocabulary"
    )
    add_parser.add_argument("word", type=str, help="Word in English")
    add_parser.add_argument("-t", "--translation", type=str, help="Translation")
    add_parser.add_argument("-e", "--example", type=str, help="Example sentence")
    add_parser.add_argument("-l", "--level", type=str,
                           choices=["beginner", "intermediate", "advanced"],
                           help="Difficulty level")

    # -----------------------
    # List words command
    # -----------------------
    list_parser = subparsers.add_parser(
        "list",
        help="List all words in your vocabulary"
    )

    # -----------------------
    # Practice command (simple version)
    # -----------------------
    practice_parser = subparsers.add_parser(
        "practice",
        help="Practice with a random word (simple mode)"
    )

    # -----------------------
    # Session command (full practice session)
    # -----------------------
    session_parser = subparsers.add_parser(
        "session",
        help="Start a practice session with multiple words"
    )
    session_parser.add_argument(
        "-n", "--number",
        type=int,
        default=10,
        help="Number of words to practice (default: 10)"
    )

    # -----------------------
    # Delete word command
    # -----------------------
    delete_parser = subparsers.add_parser(
        "delete",
        help="Delete a word by ID"
    )
    delete_parser.add_argument("id", type=int, help="Word ID to delete")

    # -----------------------
    # Stats command
    # -----------------------
    stats_parser = subparsers.add_parser(
        "stats",
        help="Show your learning statistics"
    )

    # -----------------------
    # Parse and execute
    # -----------------------
    args = parser.parse_args()

    if args.command == "add":
        try:
            Vocabulary.add_word(
                args.word,
                args.translation,
                args.example,
                args.level
            )
            print(f"✓ Word '{args.word}' added successfully!")
            sys.exit(0)
        except Exception as e:
            print(f"✗ Error adding word: {e}", file=sys.stderr)
            sys.exit(1)

    elif args.command == "list":
        try:
            words = Vocabulary.get_all_words()

            if not words:
                print("No words in your vocabulary yet. Add some with 'add' command!")
                sys.exit(0)

            print(f"\n{'='*70}")
            print(f"  Your Vocabulary ({len(words)} words)")
            print(f"{'='*70}\n")

            for w in words:
                word_id, word, translation, example, level, next_review, interval, reps = w
                print(f"[{word_id}] {word}")
                if translation:
                    print(f"    → {translation}")
                if level:
                    print(f"    Level: {level}")
                if next_review:
                    print(f"    Next review: {next_review} (interval: {interval} days, reps: {reps})")
                print()

            sys.exit(0)
        except Exception as e:
            print(f"✗ Error listing words: {e}", file=sys.stderr)
            sys.exit(1)

    elif args.command == "delete":
        try:
            word = Vocabulary.get_word_by_id(args.id)
            if word:
                Vocabulary.delete_word(args.id)
                print(f"✓ Word deleted successfully!")
            else:
                print(f"✗ Word with ID {args.id} not found.")
            sys.exit(0)
        except Exception as e:
            print(f"✗ Error deleting word: {e}", file=sys.stderr)
            sys.exit(1)

    elif args.command == "practice":
        try:
            # Simple random word practice (original)
            word = Vocabulary.get_random_word()

            if not word:
                print("No words available. Add some first with 'add' command!")
                sys.exit(0)

            word_id, english, translation, example, level, *_ = word

            print(f"\n{'='*50}")
            print(f"  Translate this word: {english}")
            print(f"{'='*50}")

            if example:
                print(f"Example: {example}\n")

            user_answer = input("Your answer: ").strip()

            if translation and user_answer.lower() == translation.lower():
                print("✓ Correct!")
                SRS.update_word_review(word_id, True)
            else:
                print(f"✗ Incorrect. Correct answer: {translation}")
                SRS.update_word_review(word_id, False)

            sys.exit(0)
        except KeyboardInterrupt:
            print("\n\nPractice cancelled.")
            sys.exit(0)
        except Exception as e:
            print(f"✗ Error during practice: {e}", file=sys.stderr)
            sys.exit(1)

    elif args.command == "session":
        try:
            # Full practice session with progress tracking
            srs = SRS()
            session = PracticeSession(srs)
            session.run(limit=args.number)
            sys.exit(0)
        except KeyboardInterrupt:
            print("\n\nSession cancelled.")
            sys.exit(0)
        except Exception as e:
            print(f"✗ Error during session: {e}", file=sys.stderr)
            sys.exit(1)

    elif args.command == "stats":
        try:
            from .database import get_connection
            conn = get_connection()
            cursor = conn.cursor()

            # Get total words
            cursor.execute("SELECT COUNT(*) FROM vocabulary")
            total_words = cursor.fetchone()[0]

            # Get today's stats
            today = date.today().strftime("%Y-%m-%d")
            cursor.execute("""
                SELECT words_reviewed, words_correct, accuracy, session_duration
                FROM daily_progress
                WHERE date = ?
            """, (today,))

            today_stats = cursor.fetchone()

            print(f"\n{'='*50}")
            print("  Your Statistics")
            print(f"{'='*50}")
            print(f"  Total vocabulary: {total_words} words")

            if today_stats:
                reviewed, correct, accuracy, duration = today_stats
                print(f"\n  Today's practice:")
                print(f"    Reviewed: {reviewed} words")
                print(f"    Correct: {correct}")
                print(f"    Accuracy: {accuracy:.1f}%")
                print(f"    Time: {duration} seconds")
            else:
                print("\n  No practice today yet. Start with 'session' command!")

            print(f"{'='*50}\n")

            conn.close()
            sys.exit(0)
        except Exception as e:
            print(f"✗ Error showing stats: {e}", file=sys.stderr)
            sys.exit(1)

    else:
        parser.print_help()
        sys.exit(0)


if __name__ == "__main__":
    run()
