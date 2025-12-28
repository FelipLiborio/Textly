from pydantic import BaseSettings
from dotenv import load_dotenv

# Carregar variáveis do .env
load_dotenv()

class Settings(BaseSettings):
    database_url: str
    secret_key: str
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7

    class Config:
        env_file = ".env"

# Instância global
settings = Settings()