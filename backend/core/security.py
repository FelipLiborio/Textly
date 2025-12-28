from fastapi import Depends, HTTPException, Request
from core.auth import verify_token
from repositories.user import UserRepository


async def get_current_user(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Access token missing")

    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid access token")

    user_id = payload.get("sub")
    repo = UserRepository()
    user = await repo.get_user_by_id(int(user_id))
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user
