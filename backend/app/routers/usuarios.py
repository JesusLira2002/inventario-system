from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.security import require_admin
from app.models.usuario import Usuario
from app.core.database import get_db
from app.schemas.usuario import UsuarioCreate, UsuarioResponse
from app.services.usuario_service import crear_usuario


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