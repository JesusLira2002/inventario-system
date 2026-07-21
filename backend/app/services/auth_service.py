from sqlalchemy.orm import Session

from app.models.usuario import Usuario
from app.core.security import verify_password, create_access_token


def autenticar_usuario(
    db: Session,
    username: str,
    password: str
):
    usuario = (
        db.query(Usuario)
        .filter(Usuario.username == username)
        .first()
    )

    if not usuario:
        return None

    if not verify_password(password, usuario.password_hash):
        return None

    if not usuario.activo:
        return None

    access_token = create_access_token(
        {"sub": usuario.username}
    )

    return access_token