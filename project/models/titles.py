"""Se encarga de la información entre app y DB | tabla titles"""

import reflex as rx
from sqlmodel import Field
from typing import Optional

class Titles(rx.Model, table=True):
    title_id: int = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    min_stars: int

    # (Opcional) Puedes agregar un método para asignar el título según estrellas