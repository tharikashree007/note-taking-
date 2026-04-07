from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class NoteSchema(BaseModel):
    title: str = Field(...)
    content: str = Field(...)
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

    class Config:
        json_schema_extra = {
            "example": {
                "title": "My Note",
                "content": "This is a note content."
            }
        }

class UpdateNoteModel(BaseModel):
    title: Optional[str]
    content: Optional[str]
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Updated Note",
                "content": "This is an updated note content."
            }
        }
