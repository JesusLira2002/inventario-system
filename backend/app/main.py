from fastapi import FastAPI
from app.core.config import settings
from app.core.database import test_connection


print(settings.DATABASE_HOST)

test_connection()

app = FastAPI(
    title="Sistema de Inventarios",
    description="API desarrollada con FastAPI",
    version="1.0.0",
)


@app.get("/")
def root():
    return {
        "mensaje": "Bienvenido al Sistema de Inventarios"
    }