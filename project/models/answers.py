"""Se encarga de la información entre app y DB | tabla answers"""

import reflex as rx
from sqlmodel import Field
from datetime import datetime, timezone
from sqlmodel import func

class Answers(rx.Model, table=True):
    answer_id: int = Field(default=None, primary_key=True)
    question_id: int = Field(foreign_key="questions.question_id")  # FK to questions
    user_id: int = Field(foreign_key="users.user_id")      # FK to users
    body: str
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column_kwargs={"server_default": func.now()},
    )