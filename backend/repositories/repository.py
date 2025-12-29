from beanie import Document
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class Repository(Document):
    user_id: str
    name: str
    description: Optional[str] = None
    created_at: datetime = datetime.utcnow()

    class Settings:
        name = "repositories"

class RepositoryRepository:
    async def create_repository(self, user_id: str, name: str, description: Optional[str] = None) -> Repository:
        repo = Repository(user_id=user_id, name=name, description=description)
        await repo.insert()
        return repo

    async def get_repositories_by_user(self, user_id: str) -> List[Repository]:
        return await Repository.find(Repository.user_id == user_id).to_list()

    async def get_repository_by_id(self, repo_id: str) -> Optional[Repository]:
        return await Repository.get(repo_id)

    async def update_repository(self, repo_id: str, name: str, description: Optional[str] = None) -> Optional[Repository]:
        repo = await Repository.get(repo_id)
        if repo:
            repo.name = name
            repo.description = description
            await repo.save()
        return repo

    async def delete_repository(self, repo_id: str) -> bool:
        repo = await Repository.get(repo_id)
        if repo:
            await repo.delete()
            return True
        return False