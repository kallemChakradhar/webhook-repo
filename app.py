from flask import Flask, render_template, jsonify
from config import collection
from utils.time_utils import format_github_time
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/events")
def get_events():
    events = list(collection.find().limit(50))

    priority = {
        "PULL_REQUEST": 3,
        "MERGE": 2,
        "PUSH": 1
    }


    def safe_time(e):
        ts = e.get("timestamp")
        if isinstance(ts, datetime):
            return ts
        try:
            return datetime.fromisoformat(str(ts).replace("Z", "+00:00"))
        except:
            return datetime.min

    def safe_created(e):
        ca = e.get("created_at")
        if isinstance(ca, datetime):
            return ca
        return datetime.min

    #SAFE SORTING (latest first)
    events.sort(
        key=lambda e: (
            safe_time(e),
            priority.get(e.get("action", ""), 0),
            safe_created(e)
        ),
        reverse=True
    )

    result = []

    for e in events:
        action = e.get("action", "")
        author = e.get("author", "unknown")
        from_branch = e.get("from_branch", "")
        to_branch = e.get("to_branch", "")

        if action == "PUSH":
            text = f'{author} pushed to {to_branch} on {format_github_time(safe_time(e))}'
        elif action == "PULL_REQUEST":
            text = f'{author} submitted a pull request from {from_branch} to {to_branch} on {format_github_time(safe_time(e))}'
        elif action == "MERGE":
            text = f'{author} merged branch {from_branch} to {to_branch} on {format_github_time(safe_time(e))}'
        else:
            continue

        result.append({
            "type": action,
            "message": text
        })

    return jsonify(result[:20])


if __name__ == "__main__":
    app.run(debug=True, port=5000)
