from fastapi import APIRouter, Body, HTTPException
from fastapi.encoders import jsonable_encoder
from models import NoteSchema, UpdateNoteModel
from database import note_collection, note_helper
from bson.objectid import ObjectId
from datetime import datetime

router = APIRouter()


# ✅ Create note
@router.post("/")
async def add_note(note: NoteSchema = Body(...)):
    note = jsonable_encoder(note)
    new_note = await note_collection.insert_one(note)
    created_note = await note_collection.find_one({"_id": new_note.inserted_id})
    return note_helper(created_note)


# ✅ Get all notes (IMPORTANT FOR .map())
@router.get("/")
async def get_notes():
    notes = []
    async for note in note_collection.find():
        notes.append(note_helper(note))
    return notes   # ✔ MUST ALWAYS BE ARRAY


# ✅ Get single note
@router.get("/{id}")
async def get_note(id: str):
    note = await note_collection.find_one({"_id": ObjectId(id)})
    if note:
        return note_helper(note)
    raise HTTPException(status_code=404, detail="Note not found")


# ✅ Update note
@router.put("/{id}")
async def update_note(id: str, req: UpdateNoteModel = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}

    if req:
        req["updated_at"] = datetime.utcnow()

        update_result = await note_collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": req}
        )

        if update_result.modified_count == 1:
            updated_note = await note_collection.find_one({"_id": ObjectId(id)})
            if updated_note:
                return note_helper(updated_note)

    existing_note = await note_collection.find_one({"_id": ObjectId(id)})
    if existing_note:
        return note_helper(existing_note)

    raise HTTPException(status_code=404, detail="Note not found")


# ✅ Delete note
@router.delete("/{id}")
async def delete_note(id: str):
    delete_result = await note_collection.delete_one({"_id": ObjectId(id)})

    if delete_result.deleted_count == 1:
        return {"message": "Note deleted successfully"}

    raise HTTPException(status_code=404, detail="Note not found")