from pydantic import BaseModel
from typing import Optional
from datetime import datetime

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