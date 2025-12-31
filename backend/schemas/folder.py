from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class FolderCreate(BaseModel):
    name: str
    parent_id: Optional[str] = None


class FolderUpdate(BaseModel):
    name: Optional[str] = None


class FolderResponse(BaseModel):
    id: str
    repository_id: str
    name: str
    parent_id: Optional[str] = None
    created_at: str
    updated_at: str
