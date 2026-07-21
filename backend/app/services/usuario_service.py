from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate
from app.core.security import get_password_hash


def crear_usuario(db: Session, datos: UsuarioCreate) -> Usuario:

    #El usuario existe?
    usuario_existente = (
        db.query(Usuario)
        .filter(Usuario.username == datos.username)
        .first()
    )

    if usuario_existente:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El nombre de usuario ya está registrado"
        )

    #El email existe?
    email_existente = (
        db.query(Usuario)
        .filter(Usuario.email == datos.email)
        .first()
    )

    if email_existente:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El correo electrónico ya está registrado"
        )

    #Si el usuario y el email no existen, se ejecuta esto:
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