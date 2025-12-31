from fastapi import HTTPException, status
from services.repository import RepositoryService
from services.folder import FolderService
from repositories.note import NoteRepository, Note
from typing import List


class NoteService:
    def __init__(self):
        self.repo_service = RepositoryService()
        self.folder_service = FolderService()
        self.note_repo = NoteRepository()

    async def create_note(self, user_id: str, repo_id: str, note_data) -> Note:
        # Verificar se repositório existe e pertence ao usuário
        await self.repo_service.get_repository(user_id, repo_id)

        # Verificar se parent_id existe e pertence ao mesmo repositório
        parent = await self.folder_service.folder_repo.get_folder_by_id(
            note_data.parent_id
        )
        if not parent or parent.repository_id != repo_id:
            raise HTTPException(status_code=404, detail="Parent folder not found")

        return await self.note_repo.create_note(
            repo_id, note_data.title, note_data.content, note_data.parent_id
        )

    async def get_repository_notes(self, user_id: str, repo_id: str) -> List[Note]:
        # Verificar se repositório existe e pertence ao usuário
        await self.repo_service.get_repository(user_id, repo_id)
        return await self.note_repo.get_notes_by_repository(repo_id)

    async def get_repository_notes_metadata(
        self, user_id: str, repo_id: str
    ) -> List[Note]:
        # Verificar se repositório existe e pertence ao usuário
        await self.repo_service.get_repository(user_id, repo_id)
        # Retorna apenas metadata (sem content)
        notes = await self.note_repo.get_notes_by_repository(repo_id)
        # Remover content de cada note
        for note in notes:
            note.content = None
        return notes

    async def update_note(
        self, user_id: str, repo_id: str, note_id: str, note_data
    ) -> Note:
        # Verificar se repositório pertence ao usuário
        await self.repo_service.get_repository(user_id, repo_id)

        note = await self.note_repo.get_note_by_id(note_id)
        if not note or note.repository_id != repo_id:
            raise HTTPException(status_code=404, detail="Note not found")

        # Atualizar apenas campos fornecidos
        update_data = {}
        if note_data.title is not None:
            update_data["title"] = note_data.title
        if note_data.content is not None:
            update_data["content"] = note_data.content

        if update_data:
            updated = await self.note_repo.update_note(note_id, **update_data)
            if not updated:
                raise HTTPException(status_code=500, detail="Failed to update note")
            return updated
        return note

    async def delete_note(self, user_id: str, repo_id: str, note_id: str):
        # Verificar se repositório pertence ao usuário
        await self.repo_service.get_repository(user_id, repo_id)

        note = await self.note_repo.get_note_by_id(note_id)
        if not note or note.repository_id != repo_id:
            raise HTTPException(status_code=404, detail="Note not found")

        success = await self.note_repo.delete_note(note_id)
        if not success:
            raise HTTPException(status_code=500, detail="Failed to delete note")
