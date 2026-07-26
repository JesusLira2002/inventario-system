from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.security import require_admin
from app.models.usuario import Usuario
from app.core.database import get_db
from app.schemas.usuario import (
    UsuarioCreate,
    UsuarioUpdate,
    UsuarioResponse,
)
from app.services.usuario_service import (
    crear_usuario,
    listar_usuarios,
    obtener_usuario_por_id,
    actualizar_usuario,
)

router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"],
)


@router.post("/", response_model=UsuarioResponse)
def crear_nuevo_usuario(
    datos: UsuarioCreate,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(require_admin),
):
    return crear_usuario(db, datos)

@router.get("/", response_model=list[UsuarioResponse])
def obtener_usuarios(
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(require_admin),
):
    return listar_usuarios(db)

@router.get("/{usuario_id}", response_model=UsuarioResponse)
def obtener_usuario(
    usuario_id: int,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(require_admin),
):
    return obtener_usuario_por_id(db, usuario_id)

@router.patch("/{usuario_id}", response_model=UsuarioResponse)
def editar_usuario(
    usuario_id: int,
    datos: UsuarioUpdate,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(require_admin),
):
    return actualizar_usuario(
        db,
        usuario_id,
        datos
    )

