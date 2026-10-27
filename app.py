
from flask import Flask, render_template, request
import os
import psycopg

app = Flask(__name__)


def get_db():
    return psycopg.connect(
        host=os.environ.get("DB_HOST", "localhost"),
        dbname=os.environ.get("DB_NAME", "notifications"),
        user=os.environ.get("DB_USER", "notification_user"),
        password=os.environ.get("DB_PASSWORD", "devops-demo-password-2026"),
    )


def init_db():
    with get_db() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS notifications (
                id SERIAL PRIMARY KEY,
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
            "INSERT INTO notifications (title, message) VALUES (%s, %s)",
            (title, message)
        )

    return render_template(
        "index.html",
        success="Alert submitted successfully!"
    )


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=False)
