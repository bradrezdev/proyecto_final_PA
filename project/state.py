"""Proyecto Final | Programación Avanzada | state"""

import reflex as rx
from .models.users import Users

class State(rx.State):
    pass

class Signup(rx.State):
    
    @classmethod
    def setEmail(cls, input_email):
        cls.email = input_email

    @rx.event
    def setPassword(cls, input_password):
        cls.password = input_password

    @rx.event
    def setUsername(cls, input_username):
        cls.username = input_username

    @rx.event
    def signup_user(self):
        try:
            #Abre y cierra la comunicación de manera automática para evitar filtración de información
            with rx.session() as channel:
                channel.add(
                    Users.create_user(
                        id=None,  # El ID se autogenera
                        username=self.username,
                        user_email=self.email,
                        user_password=self.password,
                        user_stars=0
                    )
                )
                
                # Le indica que guardará cambios en la DB.
                channel.commit() 
        except:
            print("Algo falló")

    @rx.event
    def show_info(self):
        print(self.email)
        print(self.password)
        print(self.username)