from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

# Temporary storage for v1; shared persistent storage will be added
# when we configure the complete three-version system.
notifications = []


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

    notifications.append({
        "id": len(notifications) + 1,
        "title": title,
        "message": message,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

    return render_template(
        "index.html",
        success="Alert submitted successfully!"
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)