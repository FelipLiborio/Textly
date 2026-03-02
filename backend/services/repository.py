
from fastapi import HTTPException

from repositories.repository import Repository, RepositoryRepository
from repositories.user import UserRepository


class RepositoryService:
    def __init__(self):
        self.repo = RepositoryRepository()
        self.user_repo = UserRepository()

    async def create_repository(self, user_id: str, repo_data) -> Repository:
        # Verificar se o usuário existe
        user = await self.user_repo.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return await self.repo.create_repository(user_id, repo_data.name, repo_data.description)

    async def get_user_repositories(self, user_id: str) -> list[Repository]:
        return await self.repo.get_repositories_by_user(user_id)

    # pega o repository pelo id e verifica se pertence ao user_id, muito reutilizado
    async def get_repository(self, user_id: str, repo_id: str) -> Repository:
        repository = await self.repo.get_repository_by_id(repo_id)
        if not repository:
            raise HTTPException(status_code=404, detail="Repository not found")
        if repository.user_id != user_id:
            raise HTTPException(status_code=403, detail="Access denied")
        return repository

    async def update_repository(self, user_id: str, repo_id: str, repo_data) -> Repository:
        await self.get_repository(user_id, repo_id)
        updated = await self.repo.update_repository(repo_id, repo_data.name, repo_data.description)
        if not updated:
            raise HTTPException(status_code=500, detail="Failed to update repository")
        return updated

    async def delete_repository(self, user_id: str, repo_id: str):
        await self.get_repository(user_id, repo_id)
        success = await self.repo.delete_repository(repo_id)
        if not success:
            raise HTTPException(status_code=500, detail="Failed to delete repository")