
from pydantic import BaseModel

from .folder import FolderResponse
from .note import NoteMetadata


class RepositoryCreate(BaseModel):
    name: str
    description: str | None = None


class RepositoryUpdate(BaseModel):
    name: str | None = None
    description: str | None = None


class RepositoryResponse(BaseModel):
    id: str
    user_id: str
    name: str
    description: str | None = None
    created_at: str


class RepositoryDetailResponse(BaseModel):
    repository: RepositoryResponse
    folders: list[FolderResponse]
    notes: list[NoteMetadata]
