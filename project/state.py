"""Proyecto Final | Programación Avanzada | state"""

import reflex as rx
from .models.users import Users

class State(rx.State):
    pass

class Signup(rx.State):
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
    def signup_user(self):
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

    @rx.event
    def show_info(self):
        print(self.email)
        print(self.password)
        print(self.username)