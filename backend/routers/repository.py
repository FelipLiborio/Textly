from fastapi import APIRouter, Depends
from services.repository import RepositoryService
from services.folder import FolderService
from services.note import NoteService
from schemas.repository import (
    RepositoryCreate,
    RepositoryResponse,
    RepositoryUpdate,
    RepositoryDetailResponse,
)
from schemas.folder import FolderResponse
from schemas.note import NoteMetadata
from typing import List
from core.auth import get_current_user

router = APIRouter(prefix="/repositories", tags=["repositories"])


@router.post("/", response_model=RepositoryResponse)
async def create_repository(
    repo: RepositoryCreate, current_user: dict = Depends(get_current_user)
):
    service = RepositoryService()
    created_repo = await service.create_repository(current_user["sub"], repo)
    return RepositoryResponse(
        id=str(created_repo.id),
        user_id=created_repo.user_id,
        name=created_repo.name,
        description=created_repo.description,
        created_at=created_repo.created_at.isoformat(),
    )


@router.get("/", response_model=List[RepositoryResponse])
async def get_user_repositories(current_user: dict = Depends(get_current_user)):
    service = RepositoryService()
    repos = await service.get_user_repositories(current_user["sub"])
    return [
        RepositoryResponse(
            id=str(r.id),
            user_id=r.user_id,
            name=r.name,
            description=r.description,
            created_at=r.created_at.isoformat(),
        )
        for r in repos
    ]


@router.get("/{repo_id}", response_model=RepositoryDetailResponse)
async def get_repository(repo_id: str, current_user: dict = Depends(get_current_user)):
    # Verificar se repositório pertence ao usuário
    repo_service = RepositoryService()
    repo = await repo_service.get_repository(current_user["sub"], repo_id)

    # Pegar folders
    folder_service = FolderService()
    folders = await folder_service.get_repository_folders(current_user["sub"], repo_id)

    # Pegar notes (metadata apenas)
    note_service = NoteService()
    notes = await note_service.get_repository_notes_metadata(
        current_user["sub"], repo_id
    )

    return RepositoryDetailResponse(
        repository=RepositoryResponse(
            id=str(repo.id),
            user_id=repo.user_id,
            name=repo.name,
            description=repo.description,
            created_at=repo.created_at.isoformat(),
        ),
        folders=[
            FolderResponse(
                id=str(f.id),
                repository_id=f.repository_id,
                name=f.name,
                parent_id=f.parent_id,
                created_at=f.created_at.isoformat(),
                updated_at=f.updated_at.isoformat(),
            )
            for f in folders
        ],
        notes=[
            NoteMetadata(
                id=str(n.id),
                repository_id=n.repository_id,
                title=n.title,
                parent_id=n.parent_id,
                created_at=n.created_at.isoformat(),
                updated_at=n.updated_at.isoformat(),
            )
            for n in notes
        ],
    )


@router.put("/{repo_id}", response_model=RepositoryResponse)
async def update_repository(
    repo_id: str,
    repo_update: RepositoryUpdate,
    current_user: dict = Depends(get_current_user),
):
    service = RepositoryService()
    updated_repo = await service.update_repository(
        current_user["sub"], repo_id, repo_update
    )
    return RepositoryResponse(
        id=str(updated_repo.id),
        user_id=updated_repo.user_id,
        name=updated_repo.name,
        description=updated_repo.description,
        created_at=updated_repo.created_at.isoformat(),
    )


@router.delete("/{repo_id}")
async def delete_repository(
    repo_id: str, current_user: dict = Depends(get_current_user)
):
    service = RepositoryService()
    await service.delete_repository(current_user["sub"], repo_id)
    return {"message": "Repository deleted successfully"}
