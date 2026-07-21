from pydantic import BaseModel, EmailStr


class UsuarioCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    nombre_completo: str | None = None
    rol: str = "usuario"


class UsuarioResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    nombre_completo: str | None
    rol: str
    activo: bool

    model_config = {
        "from_attributes": True
    }