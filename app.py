
from flask import Flask, render_template
import sqlite3
import os

app = Flask(__name__)

DB_PATH = os.environ.get("DB_PATH", "notifications.db")


def get_db():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    os.makedirs(os.path.dirname(os.path.abspath(DB_PATH)), exist_ok=True)

    with get_db() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS notifications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                message TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)


@app.route("/")
def index():
    with get_db() as connection:
        notifications = connection.execute(
            "SELECT id, title, message, created_at "
            "FROM notifications ORDER BY id DESC"
        ).fetchall()

    return render_template(
        "index.html",
        notifications=notifications
    )


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=False)
