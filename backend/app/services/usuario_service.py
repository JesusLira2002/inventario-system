from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate
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

def listar_usuarios(db: Session) -> list[Usuario]:
    return db.query(Usuario).all()

def obtener_usuario_por_id(
    db: Session,
    usuario_id: int
) -> Usuario:

    usuario = (
        db.query(Usuario)
        .filter(Usuario.id == usuario_id)
        .first()
    )

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )

    return usuario

def actualizar_usuario(
    db: Session,
    usuario_id: int,
    datos: UsuarioUpdate
) -> Usuario:

    usuario = obtener_usuario_por_id(db, usuario_id)

    # Validar username
    if datos.username is not None:
        existe = (
            db.query(Usuario)
            .filter(
                Usuario.username == datos.username,
                Usuario.id != usuario_id
            )
            .first()
        )

        if existe:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="El nombre de usuario ya está registrado"
            )

        usuario.username = datos.username

    # Validar email
    if datos.email is not None:
        existe = (
            db.query(Usuario)
            .filter(
                Usuario.email == datos.email,
                Usuario.id != usuario_id
            )
            .first()
        )

        if existe:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="El correo electrónico ya está registrado"
            )

        usuario.email = datos.email

    # Actualizar contraseña
    if datos.password is not None:
        usuario.password_hash = get_password_hash(datos.password)

    # Nombre completo
    if datos.nombre_completo is not None:
        usuario.nombre_completo = datos.nombre_completo

    # Rol
    if datos.rol is not None:
        usuario.rol = datos.rol

    # Estado
    if datos.activo is not None:
        usuario.activo = datos.activo

    db.commit()
    db.refresh(usuario)

    return usuario