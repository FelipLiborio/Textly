from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from connections.mongo import init_database
from routers.auth import router as auth_router
from routers.repository import router as repository_router
from routers.folder import router as folder_router
from routers.note import router as note_router

app = FastAPI(title="Textly API", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://172.20.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
