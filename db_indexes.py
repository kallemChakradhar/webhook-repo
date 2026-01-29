from config import collection
from pymongo.errors import DuplicateKeyError

try:
    collection.create_index(
        [("request_id", 1), ("action", 1), ("timestamp", 1)],
        unique=True
    )
    print("MongoDB indexes created successfully")
except Exception as e:
    print("Index already exists or duplicates found:", e)
