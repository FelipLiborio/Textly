from pydantic import BaseModel, EmailStr
from typing import Optional

# Para criar usuário
class UserCreate(BaseModel):
    email: EmailStr
    password: str

# Para resposta (sem senha)
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: str  

    class Config:
        from_attributes = True 

# Para login
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Token response
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"