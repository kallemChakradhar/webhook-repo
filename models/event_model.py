from datetime import datetime

def build_event(data):
    return {
        "request_id": data["request_id"],
        "author": data["author"],
        "action": data["action"],
        "from_branch": data["from_branch"],
        "to_branch": data["to_branch"],
        "timestamp": datetime.fromisoformat(data["timestamp"].replace("Z", "+00:00")),  # REAL datetime
        "created_at": datetime.utcnow()
    }
