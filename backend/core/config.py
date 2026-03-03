from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# Carregar variáveis do .env
load_dotenv()

class Settings(BaseSettings):
    database_url: str
    secret_key: str
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    cookie_secure: bool = False  # True para HTTPS em produção

    class Config:
        env_file = ".env"

# Instância global
settings = Settings()