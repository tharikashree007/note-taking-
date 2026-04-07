from fastapi import APIRouter, Body, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List
from models import NoteSchema, UpdateNoteModel
from database import note_collection, note_helper
from bson.objectid import ObjectId
from datetime import datetime

router = APIRouter()

@router.post("/", response_description="Add new note")
async def add_note(note: NoteSchema = Body(...)):
    note = jsonable_encoder(note)
    new_note = await note_collection.insert_one(note)
    created_note = await note_collection.find_one({"_id": new_note.inserted_id})
    return note_helper(created_note)

@router.get("/", response_description="Get all notes")
async def get_notes():
    notes = []
    async for note in note_collection.find():
        notes.append(note_helper(note))
    return notes

@router.get("/{id}", response_description="Get a single note")
async def get_note(id: str):
    if (note := await note_collection.find_one({"_id": ObjectId(id)})) is dict:
        return note_helper(note)
    raise HTTPException(status_code=404, detail=f"Note {id} not found")

@router.put("/{id}", response_description="Update a note")
async def update_note(id: str, req: UpdateNoteModel = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    if len(req) >= 1:
        req["updated_at"] = datetime.utcnow()
        update_result = await note_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": req}
        )
        if update_result.modified_count == 1:
            if (
                updated_note := await note_collection.find_one({"_id": ObjectId(id)})
            ) is not None:
                return note_helper(updated_note)
    if (existing_note := await note_collection.find_one({"_id": ObjectId(id)})) is not None:
        return note_helper(existing_note)
    raise HTTPException(status_code=404, detail=f"Note {id} not found")

@router.delete("/{id}", response_description="Delete a note")
async def delete_note(id: str):
    delete_result = await note_collection.delete_one({"_id": ObjectId(id)})
    if delete_result.deleted_count == 1:
        return {"message": "Note deleted successfully"}
    raise HTTPException(status_code=404, detail=f"Note {id} not found")
