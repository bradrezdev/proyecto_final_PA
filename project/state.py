"""Proyecto Final | Programación Avanzada | state"""

import reflex as rx
import bcrypt
from typing import List
from .models.users import Users
from project.models.users import Users
from project.models.titles import Titles
from project.models.tags import Tags
from project.models.questions import Questions
from project.models.answers import Answers
from project.models.question_tag import QuestionTag
from sqlmodel import select
from datetime import datetime
import pytz


class State(rx.State):
    pass

class Signup(rx.State):
    username: str = ""
    email: str = ""
    password: str = ""
    confirm_password: str = ""

    @rx.event
    def setUsername(self, input_username):
        self.username = input_username

    @rx.event
    def setEmail(self, input_email):
        self.email = input_email

    @rx.event
    def setPassword(self, input_password):
        self.password = input_password

    @rx.event
    def setConfirmPassword(self, input_confirm_password):
        self.confirm_password = input_confirm_password

    def search_user(self):
        with rx.session() as session:
            signed_up_user = session.exec(
                select(Users).where(
                    Users.email == self.email
                )
            ).first()
        return signed_up_user
    
    @rx.event
    def signup_user(self):
        signed_up_user = self.search_user()

        if self.confirm_password != self.password:
            return print("Las contraseñas no coinciden.")
        elif signed_up_user:
            return print("El usuario ya existe.")
        else:
            # Si el usuario no existe, crea un nuevo usuario.
            new_user = Users.create_user(
                id=None,
                username=self.username,
                user_email=self.email,
                user_password=self.password
            )
            
            # Abre una sesión para interactuar con la base de datos y la cierra al finalizar.
            with rx.session() as session:
                # Crea el usuario nuevo en la base de datos.
                session.add(new_user)
                # Guarda los cambios en la base de datos.
                session.commit()

            # Redirige al usuario a la página de inicio de sesión.
            return rx.redirect("/login", replace=True)
    
class Login(rx.State):
    email: str = ""
    password: str = ""
    username: str = ""

    @rx.event
    def setEmail(self, input_email):
        self.email = input_email

    @rx.event
    def setPassword(self, input_password):
        self.password = input_password

    @rx.event
    def setUsername(self, input_username):
        self.username = input_username

    @rx.event
    def login_user(self):
        try:
            with rx.session() as session:
                user = session.exec(
                    Users.select().where(
                        Users.email == self.email,
                    )
                ).first()

                if user and bcrypt.checkpw(self.password.encode(), user.password.encode()):
                    # Si el usuario existe, redirige a la página de inicio.
                    return rx.redirect("/dashboard", replace=True)
                else:
                    # Si el usuario no existe, redirige a la página de inicio de sesión.
                    print("Usuario no encontrado o contraseña incorrecta.")
                    return rx.redirect("/login", replace=True)
                
        except Exception as e:
            print(f"Error al iniciar sesión: {e}")
            return rx.redirect("/login", replace=True)

class SearchUIState(rx.State):
    show_search_box: bool = False

    @rx.event
    def toggle_search_box(self):
        self.show_search_box = not self.show_search_box

class SearchState(rx.State):
    show_search: bool = False

    @rx.event
    def toggle_search(self):
        self.show_search = not self.show_search

class QuestionsState(rx.State):
    questions: list[Questions] = []

    @rx.event
    def load_questions(self):
        with rx.session() as session:
            results = session.exec(select(Questions)).all()
            local_tz = pytz.timezone("America/Mexico_City")  # Pon aquí tu zona local

            for question in results:
                # Si tu fecha es string, conviértela primero a datetime
                if isinstance(question.created_at, str):
                    utc_dt = datetime.fromisoformat(question.created_at)
                else:
                    utc_dt = question.created_at

                # Ponle la zona UTC si aún no la tiene
                if utc_dt.tzinfo is None:
                    utc_dt = utc_dt.replace(tzinfo=pytz.utc)

                # Convierte a hora local
                local_dt = utc_dt.astimezone(local_tz)
                question.created_at = local_dt.isoformat()

            self.questions = results