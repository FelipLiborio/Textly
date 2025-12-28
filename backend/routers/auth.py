from fastapi import APIRouter, Response, HTTPException
from services.auth import AuthService
from schemas.user import UserCreate, UserLogin
from core.auth import verify_token, create_access_token, create_refresh_token
from repositories.user import UserRepository

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register")
async def register(user: UserCreate, response: Response):
    service = AuthService()
    tokens = await service.register(user)
    # Set cookies
    response.set_cookie(
        key="access_token",
        value=tokens.access_token,
        httponly=True,
        secure=False, 
        samesite="strict",
    )
    response.set_cookie(
        key="refresh_token",
        value=tokens.refresh_token,
        httponly=True,
        secure=False,
        samesite="strict",
    )
    return {"message": "Registered successfully"}


@router.post("/login")
async def login(user: UserLogin, response: Response):
    service = AuthService()
    tokens = await service.login(user)
    # Set cookies
    response.set_cookie(
        key="access_token",
        value=tokens.access_token,
        httponly=True,
        secure=False,
        samesite="strict",
    )
    response.set_cookie(
        key="refresh_token",
        value=tokens.refresh_token,
        httponly=True,
        secure=False,
        samesite="strict",
    )
    return {"message": "Logged in successfully"}


@router.post("/refresh")
async def refresh(response: Response):
    refresh_token = response.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token missing")

    payload = verify_token(refresh_token)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    user_id = payload.get("sub")
    repo = UserRepository()
    user = await repo.get_user_by_id(int(user_id))
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    # Generate new tokens
    data = {"sub": str(user.id)}
    access = create_access_token(data)
    refresh_new = create_refresh_token(data)

    # Set new cookies
    response.set_cookie(
        key="access_token", value=access, httponly=True, secure=False, samesite="strict"
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_new,
        httponly=True,
        secure=False,
        samesite="strict",
    )
    return {"message": "Tokens refreshed"}


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return {"message": "Logged out"}
