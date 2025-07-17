"""Se encarga de la información entre app y DB | tabla users"""

import reflex as rx

# Librería que contiene funciones extra para darle formato a la tabla
from sqlmodel import Field # <- Permite personalizar de manera estricta las columnas
from sqlmodel import desc # <- Permite ordenar los resultados de la consulta
from sqlmodel import func # <- Permite usar funciones de SQL como NOW() para obtener la fecha actual
import bcrypt # <- Permite encriptar la contraseña del usuario
from datetime import datetime, timezone # <- Permite manejar fechas y horas con zona horaria


# Emula cómo se ve una tabla de la DB.
class Users(rx.Model, table=True):
    user_id: int = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    email: str = Field(unique=True, index=True)
    password: str
    #total_stars: int = Field(default=0)
    created_at: datetime = Field(
    default_factory=lambda: datetime.now(timezone.utc),
    sa_column_kwargs={"server_default": func.now()},
)
    #title_id: int = Field(default=1, foreign_key="titles.title_id")

    @classmethod
    def create_user(cls, id, username, user_email, user_password):
        coded_password = user_password.encode()
        hashed_password = bcrypt.hashpw(coded_password, bcrypt.gensalt())
        return cls(
            user_id=id,
            username=username,
            email=user_email,
            password=hashed_password.decode(),
        )