"""Se encarga de la información entre app y DB | tabla tags"""

import reflex as rx
from sqlmodel import Field

class Tags(rx.Model, table=True):
    tag_id: int = Field(default=None, primary_key=True)
    tag_name: str = Field(unique=True, index=True)