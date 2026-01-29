import hashlib
import hmac
import os
from flask import Blueprint, request, jsonify
from config import collection
from services.github_parser import parse_github_event
from models.event_model import build_event

webhook_bp = Blueprint("webhook", __name__)

SECRET = os.getenv("WEBHOOK_SECRET", "mysecret")

def verify_signature(payload, signature):
    mac = hmac.new(SECRET.encode(), payload, hashlib.sha256).hexdigest()
    return hmac.compare_digest(mac, signature)

@webhook_bp.route("/webhook", methods=["POST"])
def github_webhook():
    event_type = request.headers.get("X-GitHub-Event")
    payload = request.json

    if event_type not in ["push", "pull_request"]:
        return jsonify({"message": "Event ignored"}), 200

    data = parse_github_event(payload, event_type)

    if not data:
        return jsonify({"message": "Invalid event"}), 400

    try:
        event_doc = build_event(data)
        collection.insert_one(event_doc)
        print("✅ Event stored")
    except Exception:
        print("⚠️ Duplicate ignored")

    return jsonify({"message": "Webhook processed"}), 200
