from fastapi import FastAPI
from beanie import init_beanie
from connections.mongo import database
from repositories.user import User
from routers.auth import router as auth_router

app = FastAPI(title="Textly API", version="1.0.0")

@app.on_event("startup")
async def startup_event():
    await init_beanie(database=database, document_models=[User])

app.include_router(auth_router)

@app.get("/")
async def root():
    return {"message": "Textly API is running"}