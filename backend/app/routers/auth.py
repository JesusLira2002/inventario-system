from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.auth import LoginRequest, Token
from app.services.auth_service import autenticar_usuario


router = APIRouter(
    tags=["Autenticación"]
)


@router.post("/login", response_model=Token)
def login(
    datos: LoginRequest,
    db: Session = Depends(get_db)
):
    access_token = autenticar_usuario(
        db,
        datos.username,
        datos.password
    )

    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos"
        )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }