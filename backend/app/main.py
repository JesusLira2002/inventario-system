from fastapi import FastAPI
from app.config import DATABASE_HOST

print(f"Servidor de base de datos: {DATABASE_HOST}")

app = FastAPI(
    title="Sistema de Inventarios",
    description="API desarrollada con FastAPI",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "mensaje": " Bienvenido al Sistema de Inventarios "
    }