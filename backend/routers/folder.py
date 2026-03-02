
from fastapi import APIRouter, Depends

from core.auth import get_current_user
from schemas.folder import FolderCreate, FolderResponse, FolderUpdate
from services.folder import FolderService

router = APIRouter(prefix="/repositories/{repo_id}/folders", tags=["folders"])


@router.post("/", response_model=FolderResponse)
async def create_folder(
    repo_id: str, folder: FolderCreate, current_user: dict = Depends(get_current_user)
):
    service = FolderService()
    created_folder = await service.create_folder(current_user["sub"], repo_id, folder)
    return FolderResponse(
        id=str(created_folder.id),
        repository_id=created_folder.repository_id,
        name=created_folder.name,
        parent_id=created_folder.parent_id,
        created_at=created_folder.created_at.isoformat(),
        updated_at=created_folder.updated_at.isoformat(),
    )


@router.get("/", response_model=list[FolderResponse])
async def get_folders(repo_id: str, current_user: dict = Depends(get_current_user)):
    service = FolderService()
    folders = await service.get_repository_folders(current_user["sub"], repo_id)
    return [
        FolderResponse(
            id=str(f.id),
            repository_id=f.repository_id,
            name=f.name,
            parent_id=f.parent_id,
            created_at=f.created_at.isoformat(),
            updated_at=f.updated_at.isoformat(),
        )
        for f in folders
    ]


@router.put("/{folder_id}", response_model=FolderResponse)
async def update_folder(
    repo_id: str,
    folder_id: str,
    folder_update: FolderUpdate,
    current_user: dict = Depends(get_current_user),
):
    service = FolderService()
    updated_folder = await service.update_folder(
        current_user["sub"], repo_id, folder_id, folder_update.name
    )
    return FolderResponse(
        id=str(updated_folder.id),
        repository_id=updated_folder.repository_id,
        name=updated_folder.name,
        parent_id=updated_folder.parent_id,
        created_at=updated_folder.created_at.isoformat(),
        updated_at=updated_folder.updated_at.isoformat(),
    )


@router.delete("/{folder_id}")
async def delete_folder(
    repo_id: str, folder_id: str, current_user: dict = Depends(get_current_user)
):
    service = FolderService()
    await service.delete_folder(current_user["sub"], repo_id, folder_id)
    return {"message": "Folder deleted successfully"}
