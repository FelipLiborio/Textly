
from pydantic import BaseModel


class NoteCreate(BaseModel):
    title: str
    content: str
    parent_id: str


class NoteUpdate(BaseModel):
    title: str | None = None
    content: str | None = None


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
