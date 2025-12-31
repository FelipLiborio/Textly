from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class NoteCreate(BaseModel):
    title: str
    content: str
    parent_id: str


class NoteUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None


class NoteResponse(BaseModel):
    id: str
    repository_id: str
    title: str
    content: str
    parent_id: str
    created_at: str
    updated_at: str


class NoteMetadata(BaseModel):
    id: str
    repository_id: str
    title: str
    parent_id: str
    created_at: str
    updated_at: str
