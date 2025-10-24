import base64
from bson import ObjectId, Binary

def safe_value(value):
    if isinstance(value, ObjectId):
        return str(value)
    elif isinstance(value, (bytes, Binary)):
        # safely convert binary data to base64 string
        return base64.b64encode(value).decode('utf-8')
    else:
        return value

def chatSerializer(chat) -> dict:
    return {
        "_id": safe_value(chat.get("_id")),
        "chat_id": safe_value(chat.get("chat_id")),
        "chat_name": safe_value(chat.get("chat_name")),
        "collection_name": safe_value(chat.get("collection_name")),
        "chat_history": safe_value(chat.get("chat_history")),
        "created_at": safe_value(chat.get("created_at")),
        "modified_at": safe_value(chat.get("modified_at")),
    }
