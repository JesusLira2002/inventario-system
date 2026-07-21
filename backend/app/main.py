from fastapi import FastAPI
from app.core.config import settings
from app.core.database import test_connection

from app.routers.usuarios import router as usuarios_router
from app.routers.auth import router as auth_router


print(settings.DATABASE_HOST)

test_connection()

app = FastAPI(
    title="Sistema de Inventarios",
    description="API (desarrollada con FastAPI)",
    version="1.0.1",
)

app.include_router(usuarios_router)
app.include_router(auth_router)

@app.get("/")
def root():
    return {
        "mensaje": "Bienvenido a los Inventarios"
    }