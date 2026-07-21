from sqlalchemy.orm import Session

from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate
from app.core.security import get_password_hash


def crear_usuario(db: Session, datos: UsuarioCreate) -> Usuario:
    nuevo_usuario = Usuario(
        username=datos.username,
        email=datos.email,
        password_hash=get_password_hash(datos.password),
        nombre_completo=datos.nombre_completo,
        rol=datos.rol,
        activo=True,
    )

    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)

    return nuevo_usuario