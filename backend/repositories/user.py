from beanie import Document
from pydantic import EmailStr
from datetime import datetime
from passlib.context import CryptContext
from connections.mongo import database

# Contexto para hash de senha
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(Document):
    email: EmailStr
    password_hash: str
    created_at: datetime = datetime.utcnow()

    class Settings:
        name = "users"

class UserRepository:
    async def create_user(self, email: str, password: str) -> User:
        hashed = pwd_context.hash(password)
        user = User(email=email, password_hash=hashed)
        await user.insert()
        return user

    async def get_user_by_email(self, email: str) -> User | None:
        return await User.find_one(User.email == email)

    async def get_user_by_id(self, user_id: str) -> User | None:
        return await User.get(user_id)

    def verify_password(self, plain: str, hashed: str) -> bool:
        return pwd_context.verify(plain, hashed)