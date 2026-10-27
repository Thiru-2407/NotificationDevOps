
from flask import Flask, render_template, redirect, url_for
import os
import psycopg
from psycopg.rows import dict_row

app = Flask(__name__)


def get_db():
    return psycopg.connect(
        host=os.environ.get("DB_HOST", "localhost"),
        dbname=os.environ.get("DB_NAME", "notifications"),
        user=os.environ.get("DB_USER", "notification_user"),
        password=os.environ.get("DB_PASSWORD", "devops-demo-password-2026"),
        row_factory=dict_row,
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
    with get_db() as connection:
        notifications = connection.execute(
            "SELECT id, title, message, created_at "
            "FROM notifications ORDER BY id DESC"
        ).fetchall()

    return render_template(
        "index.html",
        notifications=notifications,
        success=None
    )


@app.route("/delete/<int:notification_id>", methods=["POST"])
def delete_notification(notification_id):
    with get_db() as connection:
        connection.execute(
            "DELETE FROM notifications WHERE id = %s",
            (notification_id,)
        )

    with get_db() as connection:
        notifications = connection.execute(
            "SELECT id, title, message, created_at "
            "FROM notifications ORDER BY id DESC"
        ).fetchall()

    return render_template(
        "index.html",
        notifications=notifications,
        success="Alert deleted successfully!"
    )


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=False)
