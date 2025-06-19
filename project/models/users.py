"""Se encarga de la información entre app y DB | tabla users"""

import reflex as rx

# Librería que contiene funciones extra para darle formato a la tabla
from sqlmodel import Field # <- Permite personalizar de manera estricta las columnas

import bcrypt # <- Permite encriptar la contraseña del usuario


# Emula cómo se ve una tabla de la DB.
class Users(rx.Model, table=True):
    user_id: int = Field(default=None, primary_key=True)
    username: str
    email: str
    password: str
    total_stars: int

    @classmethod
    def create_user(cls, id, username, user_email, user_password, user_stars=0):

        # Hashear la contraseña del usuario.
        coded_password = user_password.encode()
        hashed_password = bcrypt.hashpw(coded_password, bcrypt.gensalt())


        return cls(user_id=id, username=username, email=user_email, password=hashed_password.decode(), total_stars=user_stars)