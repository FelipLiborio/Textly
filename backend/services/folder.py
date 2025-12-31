from fastapi import HTTPException, status
from services.repository import RepositoryService
from repositories.note import FolderRepository, Folder
from typing import List


class FolderService:
    def __init__(self):
        self.repo_service = RepositoryService()
        self.folder_repo = FolderRepository()

    async def create_folder(self, user_id: str, repo_id: str, folder_data) -> Folder:
        # Verificar se repositório existe e pertence ao usuário
        await self.repo_service.get_repository(user_id, repo_id)

        # Verificar se parent_id existe e pertence ao mesmo repositório
        if folder_data.parent_id:
            parent = await self.folder_repo.get_folder_by_id(folder_data.parent_id)
            if not parent or parent.repository_id != repo_id:
                raise HTTPException(status_code=404, detail="Parent folder not found")

        return await self.folder_repo.create_folder(
            repo_id, folder_data.name, folder_data.parent_id
        )

    async def get_repository_folders(self, user_id: str, repo_id: str) -> List[Folder]:
        # Verificar se repositório existe e pertence ao usuário
        await self.repo_service.get_repository(user_id, repo_id)
        return await self.folder_repo.get_folders_by_repository(repo_id)

    async def get_root_folders(self, user_id: str, repo_id: str) -> List[Folder]:
        # Verificar se repositório existe e pertence ao usuário
        await self.repo_service.get_repository(user_id, repo_id)
        # Só pastas raiz (parent_id = None)
        return await Folder.find(
            Folder.repository_id == repo_id, Folder.parent_id == None
        ).to_list()

    async def get_child_folders(
        self, user_id: str, repo_id: str, parent_id: str
    ) -> List[Folder]:
        # Verificar se repositório existe e pertence ao usuário
        await self.repo_service.get_repository(user_id, repo_id)
        # Verificar se parent_id existe e pertence ao repo
        parent = await self.folder_repo.get_folder_by_id(parent_id)
        if not parent or parent.repository_id != repo_id:
            raise HTTPException(status_code=404, detail="Parent folder not found")
        # Filhos diretos
        return await Folder.find(
            Folder.repository_id == repo_id, Folder.parent_id == parent_id
        ).to_list()

    async def update_folder(
        self, user_id: str, repo_id: str, folder_id: str, name: str
    ) -> Folder:
        # Verificar se repositório pertence ao usuário
        await self.repo_service.get_repository(user_id, repo_id)

        folder = await self.folder_repo.get_folder_by_id(folder_id)
        if not folder or folder.repository_id != repo_id:
            raise HTTPException(status_code=404, detail="Folder not found")

        updated = await self.folder_repo.update_folder(folder_id, name)
        if not updated:
            raise HTTPException(status_code=500, detail="Failed to update folder")
        return updated

    async def delete_folder(self, user_id: str, repo_id: str, folder_id: str):
        # Verificar se repositório pertence ao usuário
        await self.repo_service.get_repository(user_id, repo_id)

        folder = await self.folder_repo.get_folder_by_id(folder_id)
        if not folder or folder.repository_id != repo_id:
            raise HTTPException(status_code=404, detail="Folder not found")

        # Verificar se tem filhos e decidir o que fazer
        success = await self.folder_repo.delete_folder(folder_id)
        if not success:
            raise HTTPException(status_code=500, detail="Failed to delete folder")
