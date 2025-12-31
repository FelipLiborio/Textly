from beanie import Document
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from core.utils import validate_object_id


class Folder(Document):
    repository_id: str
    name: str
    parent_id: Optional[str] = None  # None para pastas raiz do repositório
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()

    class Settings:
        name = "folders"


class Note(Document):
    repository_id: str
    title: str
    content: str
    parent_id: str  # Sempre deve ter uma pasta pai
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()

    class Settings:
        name = "notes"


class FolderRepository:
    async def create_folder(
        self, repository_id: str, name: str, parent_id: Optional[str] = None
    ) -> Folder:
        folder = Folder(repository_id=repository_id, name=name, parent_id=parent_id)
        await folder.insert()
        return folder

    async def get_folders_by_repository(self, repository_id: str) -> List[Folder]:
        return await Folder.find(Folder.repository_id == repository_id).to_list()

    async def get_folder_by_id(self, folder_id: str) -> Optional[Folder]:
        object_id = validate_object_id(folder_id)
        if not object_id:
            return None
        return await Folder.get(object_id)

    async def update_folder(self, folder_id: str, name: str) -> Optional[Folder]:
        object_id = validate_object_id(folder_id)
        if not object_id:
            return None
        folder = await Folder.get(object_id)
        if folder:
            folder.name = name
            folder.updated_at = datetime.utcnow()
            await folder.save()
        return folder

    async def delete_folder(self, folder_id: str) -> bool:
        object_id = validate_object_id(folder_id)
        if not object_id:
            return False
        folder = await Folder.get(object_id)
        if folder:
            await folder.delete()
            return True
        return False


class NoteRepository:
    async def create_note(
        self, repository_id: str, title: str, content: str, parent_id: str
    ) -> Note:
        note = Note(
            repository_id=repository_id,
            title=title,
            content=content,
            parent_id=parent_id,
        )
        await note.insert()
        return note

    async def get_notes_by_repository(self, repository_id: str) -> List[Note]:
        return await Note.find(Note.repository_id == repository_id).to_list()

    async def get_note_by_id(self, note_id: str) -> Optional[Note]:
        object_id = validate_object_id(note_id)
        if not object_id:
            return None
        return await Note.get(object_id)

    async def update_note(
        self, note_id: str, title: str, content: str
    ) -> Optional[Note]:
        object_id = validate_object_id(note_id)
        if not object_id:
            return None
        note = await Note.get(object_id)
        if note:
            note.title = title
            note.content = content
            note.updated_at = datetime.utcnow()
            await note.save()
        return note

    async def delete_note(self, note_id: str) -> bool:
        object_id = validate_object_id(note_id)
        if not object_id:
            return False
        note = await Note.get(object_id)
        if note:
            await note.delete()
            return True
        return False
