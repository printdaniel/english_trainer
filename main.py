from app.database import init_db
from app.cli import run

if __name__ == "__main__":
    init_db()
    run()

