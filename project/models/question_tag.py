"""Se encarga de la información entre app y DB | tabla question_tag"""

import reflex as rx
from sqlmodel import Field

class QuestionTag(rx.Model, table=True):
    question_id: int = Field(foreign_key="questions.question_id", primary_key=True)
    tag_id: int = Field(foreign_key="tags.tag_id", primary_key=True)