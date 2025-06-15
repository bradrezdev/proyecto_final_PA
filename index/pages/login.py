"""Proyecto Final | Programación Avanzada | Log in Page"""

import reflex as rx
from ..state import Login
from rxconfig import config


def login() -> rx.Component:
    # Contenedor principal
    return rx.flex(
        
        # Contenedor izquierdo | Formulario
        rx.vstack(
            
            rx.image(src="/logotipo.png", width="200px", height="auto"),

            # Formulario de inicio de sesión.
            rx.form(
                
                # Inputs del formulario.
                rx.vstack(

                    rx.heading("Bienvenido de vuelta", size="8",),

                    rx.text("Qué gusto volverte a ver. Por favor, ingresa los datos de tu cuenta:"),
                    
                    rx.spacer(),

                    rx.text("Correo electrónico"),

                    rx.input(
                        placeholder="Escribe tu correo electrónico",
                        name="email",
                        style={"border": "1px solid black"},
                        type="email",
                        on_change=lambda value: Login.setEmail(Login(), value),

                        border_radius="8px",
                        height="40px",
                        width="25vw",
                    ),

                    rx.text("Contraseña"),

                    rx.input(
                        placeholder="Escribe tu contraseña",
                        name="password",
                        style={"border": "1px solid black"},
                        type="password",
                        on_change=lambda value: Login.setPassword(Login(), value),

                        border_radius="8px",
                        height="40px",
                        width="25vw",
                    ),

                    rx.text("Olvidé mi contraseña", size="1",),
                    
                    rx.link(
                        rx.button("Iniciar sesión", height="47px", width="25vw", border_radius="8px",),
                        href="/loggedindex",
                    ),

                    rx.hstack(
                        rx.spacer(),
                        rx.text("¿No tienes una cuenta?",size="1"),
                        rx.link("Crear una cuenta", href="/signup",size="1"),
                        rx.spacer(),
                    # Propiedades de hstack "¿NO tienes una cuenta?
                    spacing="1",
                    width="100%",
                    ),
                ),

                # Propiedades @Formulario de inicio de sesión.
                padding="20%",
                width="100%",
            ),

            # Propiedades @Contenedor izquierdo | Formulario
            #bg="blue",
            justify="center",
            padding="4%",
            width="50%",
        ),

        # Contenedor derecho | Imagen
        rx.box(
            bg="red",
            width="50%",
        ),

        # Propiedades contenedor principal
        height="100vh",
        max_width="1920",
        width="100%",
    )