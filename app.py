from flask import Flask, render_template, request
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
    return render_template("index.html", success=None)


@app.route("/add", methods=["POST"])
def add_notification():
    title = request.form.get("title", "").strip()
    message = request.form.get("message", "").strip()

    if not title or not message:
        return render_template(
            "index.html",
            success="Please enter both a title and a message."
        ), 400

    with get_db() as connection:
        connection.execute(
            "INSERT INTO notifications (title, message) VALUES (?, ?)",
            (title, message)
        )

    return render_template(
        "index.html",
        success="Alert submitted successfully!"
    )


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=False)