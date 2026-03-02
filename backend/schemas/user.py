
from pydantic import BaseModel, EmailStr, Field


# Para criar usuário
class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., max_length=72)

# Para resposta (sem senha)
class UserResponse(BaseModel):
    id: str
    email: EmailStr
    created_at: str 

# Para login
class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(..., max_length=72)

# Token response
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"