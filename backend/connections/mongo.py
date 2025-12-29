from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from core.config import settings
from repositories.user import User
from repositories.repository import Repository

# Cliente MongoDB
client = AsyncIOMotorClient(settings.database_url)

# Banco de dados
database = client.textly

# Função para inicializar Beanie
async def init_database():
    await init_beanie(database=database, document_models=[User, Repository])