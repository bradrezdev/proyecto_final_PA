"""Se encarga de la información entre app y DB | tabla questions"""

import reflex as rx
from sqlmodel import Field
from typing import Optional
from datetime import datetime, timezone
from sqlmodel import func

class Questions(rx.Model, table=True):
    question_id: int = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.user_id")   # Relación con usuario
    title: str = Field(index=True)
    body: str
    tag_id: str = Field(default=None, foreign_key="tags.tag_id")  # Relación con tags
    created_at: datetime = Field(
    default_factory=lambda: datetime.now(timezone.utc),
    sa_column_kwargs={"server_default": func.now()},
    )
    # La relación de tags se hace con la tabla question_tag (no aquí como texto)