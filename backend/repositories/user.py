from datetime import datetime

import bcrypt
from beanie import Document
from pydantic import EmailStr


class User(Document):
    email: EmailStr
    password_hash: str
    created_at: datetime = datetime.utcnow()

    class Settings:
        name = "users"

class UserRepository:
    async def create_user(self, email: str, password: str) -> User:
        # Hash da senha com bcrypt
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password_bytes, salt).decode('utf-8')
        user = User(email=email, password_hash=hashed)
        await user.insert()
        return user

    async def get_user_by_email(self, email: str) -> User | None:
        return await User.find_one(User.email == email)

    async def get_user_by_id(self, user_id: str) -> User | None:
        return await User.get(user_id)

    def verify_password(self, plain: str, hashed: str) -> bool:
        # Verificar senha com bcrypt
        plain_bytes = plain.encode('utf-8')
        hashed_bytes = hashed.encode('utf-8')
        return bcrypt.checkpw(plain_bytes, hashed_bytes)