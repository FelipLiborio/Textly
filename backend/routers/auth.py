from fastapi import APIRouter, Response, HTTPException, Request
from services.auth import AuthService
from schemas.user import UserCreate, UserLogin
from core.config import settings

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/me")
async def get_me(request: Request, response: Response):
    access_token = request.cookies.get("access_token")
    if not access_token:
        raise HTTPException(status_code=401, detail="Access token missing")

    service = AuthService()
    user = await service.get_current_user(access_token)
    return {"user": user}


@router.post("/register")
async def register(user: UserCreate, response: Response):
    service = AuthService()
    tokens = await service.register(user)
    # Set cookies
    response.set_cookie(
        key="access_token",
        value=tokens.access_token,
        httponly=True,
        secure=settings.cookie_secure,
        samesite="strict",
    )
    response.set_cookie(
        key="refresh_token",
        value=tokens.refresh_token,
        httponly=True,
        secure=settings.cookie_secure,
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
        secure=settings.cookie_secure,
        samesite="strict",
    )
    response.set_cookie(
        key="refresh_token",
        value=tokens.refresh_token,
        httponly=True,
        secure=settings.cookie_secure,
        samesite="strict",
    )
    return {"message": "Logged in successfully"}


@router.post("/refresh")
async def refresh(request: Request, response: Response):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token missing")

    service = AuthService()
    tokens = await service.refresh(refresh_token)

    # Set new cookies
    response.set_cookie(
        key="access_token",
        value=tokens.access_token,
        httponly=True,
        secure=settings.cookie_secure,
        samesite="strict",
    )
    response.set_cookie(
        key="refresh_token",
        value=tokens.refresh_token,
        httponly=True,
        secure=settings.cookie_secure,
        samesite="strict",
    )
    return {"message": "Tokens refreshed"}


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return {"message": "Logged out"}
