import os
from motor.motor_asyncio import AsyncIOMotorClient

# Provide default localhost fallback if URI is not set
MONGO_DETAILS = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = AsyncIOMotorClient(MONGO_DETAILS)
database = client.note_taking_db
note_collection = database.get_collection("notes")

# Helper function to parse the mongo document
def note_helper(note) -> dict:
    return {
        "id": str(note["_id"]),
        "title": note["title"],
        "content": note["content"],
        "created_at": note.get("created_at"),
        "updated_at": note.get("updated_at")
    }
