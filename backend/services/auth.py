from fastapi import HTTPException, status
from repositories.user import UserRepository
from core.auth import create_access_token, create_refresh_token
from schemas.user import UserCreate, UserLogin, Token


class AuthService:
    async def register(self, user_data: UserCreate) -> Token:
        repo = UserRepository()
        # Verificar se email já existe
        existing = await repo.get_user_by_email(user_data.email)
        if existing:
            raise HTTPException(status_code=400, detail="Email already registered")

        # Criar usuário
        user = await repo.create_user(user_data.email, user_data.password)

        # Gerar tokens
        data = {"sub": str(user.id)}
        access = create_access_token(data)
        refresh = create_refresh_token(data)

        return Token(access_token=access, refresh_token=refresh)

    async def login(self, login_data: UserLogin) -> Token:
        repo = UserRepository()
        user = await repo.get_user_by_email(login_data.email)
        if not user or not repo.verify_password(
            login_data.password, user.password_hash
        ):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        # Gerar tokens
        data = {"sub": str(user.id)}
        access = create_access_token(data)
        refresh = create_refresh_token(data)

        return Token(access_token=access, refresh_token=refresh)
