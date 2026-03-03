
from pydantic import BaseModel


class FolderCreate(BaseModel):
    name: str
    parent_id: str | None = None


class FolderUpdate(BaseModel):
    name: str | None = None


class FolderResponse(BaseModel):
    id: str
    repository_id: str
    name: str
    parent_id: str | None = None
    created_at: str
    updated_at: str
