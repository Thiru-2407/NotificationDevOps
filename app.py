from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

notifications = []
next_id = 1


@app.route("/")
def index():
    return render_template("index.html", notifications=notifications)


@app.route("/add", methods=["POST"])
def add_notification():
    global next_id

    title = request.form.get("title", "").strip()
    message = request.form.get("message", "").strip()

    if title and message:
        notifications.append({
            "id": next_id,
            "title": title,
            "message": message,
            "created_at": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        })
        next_id += 1

    return redirect(url_for("index"))


@app.route("/delete/<int:notification_id>", methods=["POST"])
def delete_notification(notification_id):
    notifications[:] = [
        item for item in notifications
        if item["id"] != notification_id
    ]
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)