from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from .folder import FolderResponse
from .note import NoteMetadata


class RepositoryCreate(BaseModel):
    name: str
    description: Optional[str] = None


class RepositoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class RepositoryResponse(BaseModel):
    id: str
    user_id: str
    name: str
    description: Optional[str] = None
    created_at: str


class RepositoryDetailResponse(BaseModel):
    repository: RepositoryResponse
    folders: List[FolderResponse]
    notes: List[NoteMetadata]
