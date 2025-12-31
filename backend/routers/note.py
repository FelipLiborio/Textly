from fastapi import APIRouter, Depends
from services.note import NoteService
from schemas.note import NoteCreate, NoteUpdate, NoteResponse, NoteMetadata
from typing import List
from core.auth import get_current_user

router = APIRouter(prefix="/repositories/{repo_id}/notes", tags=["notes"])


@router.post("/", response_model=NoteResponse)
async def create_note(
    repo_id: str, note: NoteCreate, current_user: dict = Depends(get_current_user)
):
    service = NoteService()
    created_note = await service.create_note(current_user["sub"], repo_id, note)
    return NoteResponse(
        id=str(created_note.id),
        repository_id=created_note.repository_id,
        title=created_note.title,
        content=created_note.content,
        parent_id=created_note.parent_id,
        created_at=created_note.created_at.isoformat(),
        updated_at=created_note.updated_at.isoformat(),
    )


@router.get("/", response_model=List[NoteMetadata])
async def get_notes(repo_id: str, current_user: dict = Depends(get_current_user)):
    service = NoteService()
    notes = await service.get_repository_notes_metadata(current_user["sub"], repo_id)
    return [
        NoteMetadata(
            id=str(n.id),
            repository_id=n.repository_id,
            title=n.title,
            parent_id=n.parent_id,
            created_at=n.created_at.isoformat(),
            updated_at=n.updated_at.isoformat(),
        )
        for n in notes
    ]


@router.get("/{note_id}", response_model=NoteResponse)
async def get_note(
    repo_id: str, note_id: str, current_user: dict = Depends(get_current_user)
):
    service = NoteService()
    # Verificar se repositório pertence ao usuário
    await service.repo_service.get_repository(current_user["sub"], repo_id)

    note = await service.note_repo.get_note_by_id(note_id)
    if not note or note.repository_id != repo_id:
        from fastapi import HTTPException

        raise HTTPException(status_code=404, detail="Note not found")

    return NoteResponse(
        id=str(note.id),
        repository_id=note.repository_id,
        title=note.title,
        content=note.content,
        parent_id=note.parent_id,
        created_at=note.created_at.isoformat(),
        updated_at=note.updated_at.isoformat(),
    )


@router.put("/{note_id}", response_model=NoteResponse)
async def update_note(
    repo_id: str,
    note_id: str,
    note_update: NoteUpdate,
    current_user: dict = Depends(get_current_user),
):
    service = NoteService()
    updated_note = await service.update_note(
        current_user["sub"], repo_id, note_id, note_update
    )
    return NoteResponse(
        id=str(updated_note.id),
        repository_id=updated_note.repository_id,
        title=updated_note.title,
        content=updated_note.content,
        parent_id=updated_note.parent_id,
        created_at=updated_note.created_at.isoformat(),
        updated_at=updated_note.updated_at.isoformat(),
    )


@router.delete("/{note_id}")
async def delete_note(
    repo_id: str, note_id: str, current_user: dict = Depends(get_current_user)
):
    service = NoteService()
    await service.delete_note(current_user["sub"], repo_id, note_id)
    return {"message": "Note deleted successfully"}


@router.get("/{note_id}/content")
async def get_note_content(
    repo_id: str, note_id: str, current_user: dict = Depends(get_current_user)
):
    """Retorna apenas o conteúdo da nota (para lazy loading)"""
    service = NoteService()
    # Verificar se repositório pertence ao usuário
    await service.repo_service.get_repository(current_user["sub"], repo_id)

    note = await service.note_repo.get_note_by_id(note_id)
    if not note or note.repository_id != repo_id:
        from fastapi import HTTPException

        raise HTTPException(status_code=404, detail="Note not found")

    return {"content": note.content}
