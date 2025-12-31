from fastapi import FastAPI
from connections.mongo import init_database
from routers.auth import router as auth_router
from routers.repository import router as repository_router
from routers.folder import router as folder_router
from routers.note import router as note_router

app = FastAPI(title="Textly API", version="1.0.0")


@app.on_event("startup")
async def startup_event():
    await init_database()


app.include_router(auth_router)
app.include_router(repository_router)
app.include_router(folder_router)
app.include_router(note_router)


@app.get("/")
async def root():
    return {"message": "Textly API is running"}
