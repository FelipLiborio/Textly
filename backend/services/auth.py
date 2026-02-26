from fastapi import HTTPException, status
from repositories.user import UserRepository
from core.auth import create_access_token, create_refresh_token, verify_token
from schemas.user import UserCreate, UserLogin, Token


class AuthService:
    async def register(self, user_data: UserCreate) -> Token:
        repo = UserRepository()
        # Verificar se email já existe
        existing = await repo.get_user_by_email(user_data.email)
        if existing:
            raise HTTPException(status_code=409, detail="Email already registered")

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

    async def refresh(self, refresh_token: str) -> Token:
        # Validar refresh token
        payload = verify_token(refresh_token)
        if not payload or payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid refresh token")

        # Buscar usuário
        user_id = payload.get("sub")
        repo = UserRepository()
        user = await repo.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        # Gerar novos tokens
        data = {"sub": str(user.id)}
        access = create_access_token(data)
        refresh = create_refresh_token(data)

        return Token(access_token=access, refresh_token=refresh)
    
    async def get_current_user(self, token: str):
        '''Este método pode ser implementado para extrair o usuário atual do token de acesso.'''
        payload = verify_token(token)
        if not payload:
            raise HTTPException(status_code=401, detail="Invalid token")
        user_id = payload.get("sub")
        repo = UserRepository()
        user = await repo.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        return user
        
