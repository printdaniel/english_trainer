import argparse
from app.models.vocabulary import Vocabulary


def run():
    parser = argparse.ArgumentParser(
        description="English Trainer CLI"
    )

    subparsers = parser.add_subparsers(dest="command")

    # -----------------------
    # Add word command
    # -----------------------
    add_parser = subparsers.add_parser("add", help="Add a new word")
    add_parser.add_argument("word", type=str, help="Word in English")
    add_parser.add_argument("-t", "--translation", type=str, help="Translation")
    add_parser.add_argument("-e", "--example", type=str, help="Example sentence")
    add_parser.add_argument("-l", "--level", type=str, help="Difficulty level")

    # -----------------------
    # List words command
    # -----------------------
    subparsers.add_parser("list", help="List all words")
    subparsers.add_parser("practice", help="Practice random vocabulary word")



    # -----------------------
    # Delete word command
    # -----------------------
    delete_parser = subparsers.add_parser("delete", help="Delete word by ID")
    delete_parser.add_argument("id", type=int, help="Word ID")

    args = parser.parse_args()

    if args.command == "add":
        Vocabulary.add_word(
            args.word,
            args.translation,
            args.example,
            args.level
        )
        print("Word added successfully.")

    elif args.command == "list":
        words = Vocabulary.get_all_words()
        for w in words:
            print(w)

    elif args.command == "delete":
        Vocabulary.delete_word(args.id)
        print("Word deleted successfully.")

    elif args.command == "practice":
        word = Vocabulary.get_random_word()

        if not word:
            print("No words available. Add some first.")
            return

        word_id, english, translation, example, level, *_ = word

        print(f"\nTranslate this word: {english}")
        user_answer = input("Your answer: ").strip()

        if translation and user_answer.lower() == translation.lower():
            print("Correct!")
        else:
            print(f"Incorrect. Correct answer: {translation}")

    else:
        parser.print_help()

