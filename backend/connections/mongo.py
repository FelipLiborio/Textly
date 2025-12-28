from motor.motor_asyncio import AsyncIOMotorClient
from core.config import settings

# Cliente MongoDB
client = AsyncIOMotorClient(settings.database_url)

# Banco de dados
database = client.textly