from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from core.config import settings
from repositories.note import Folder, Note
from repositories.repository import Repository
from repositories.user import User

# Cliente MongoDB
client = AsyncIOMotorClient(settings.database_url)

# Banco de dados
database = client.textly


# Função para inicializar Beanie
async def init_database():
    await init_beanie(
        database=database, document_models=[User, Repository, Folder, Note]
    )
