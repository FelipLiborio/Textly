from datetime import datetime

from beanie import Document

from core.utils import validate_object_id


class Repository(Document):
    user_id: str
    name: str
    description: str | None = None
    created_at: datetime = datetime.utcnow()

    class Settings:
        name = "repositories"

class RepositoryRepository:
    async def create_repository(self, user_id: str, name: str, description: str | None = None) -> Repository:
        repo = Repository(user_id=user_id, name=name, description=description)
        await repo.insert()
        return repo

    async def get_repositories_by_user(self, user_id: str) -> list[Repository]:
        return await Repository.find(Repository.user_id == user_id).to_list()

    async def get_repository_by_id(self, repo_id: str) -> Repository | None:
        object_id = validate_object_id(repo_id)
        if not object_id:
            return None
        return await Repository.get(object_id)

    async def update_repository(self, repo_id: str, name: str, description: str | None = None) -> Repository | None:
        object_id = validate_object_id(repo_id)
        if not object_id:
            return None
        repo = await Repository.get(object_id)
        if repo:
            repo.name = name
            repo.description = description
            await repo.save()
        return repo

    async def delete_repository(self, repo_id: str) -> bool:
        object_id = validate_object_id(repo_id)
        if not object_id:
            return False
        repo = await Repository.get(object_id)
        if repo:
            await repo.delete()
            return True
        return False