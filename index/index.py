"""Proyecto Final | Programación Avanzada"""

import reflex as rx
from rxconfig import config
from index.state import State
from .signup import signup
from .login import login

def index() -> rx.Component:
    # Contenedor principal
    return rx.vstack(
        
        # Contenedor Header | Logo + Search, Login, Signup
        rx.hstack(
            
            rx.image(src="/logotipo.png", width="200px", height="auto"),

            rx.box(   
                # Botón Búsqueda
                rx.icon_button("search", border_radius="100px", width="48px", height="48px", margin_right="10px",),

                # Botón Registrarse
                rx.link(
                    rx.button(
                        "Registrarse",
                        border_radius="100px",
                        width="135px",
                        height="48px",
                    ),
                    href="/signup",
                ),

                # Botón Iniciar sesión
                rx.link(
                    rx.button(
                        "Iniciar sesión",
                        bg="white",
                        border_radius="100px",
                        width="135px",
                        height="48px",
                        border="5px solid purple",
                    ),
                    href="/login",
                ),
                
            # Propiedades contenedor botones Búsqueda, Registro e Inicio de sesión

            ),

        # Propiedades @Header
        justify="between",
        padding="4%",
        width="100%",
        ),

        # Propiedades contenedor principal
        height="100vh",
        max_width="1920",
        width="100%",
    )


app = rx.App(theme=rx.theme(accent_color="amber"))
app.add_page(index, title="Página de inicio")
app.add_page(login, title="Iniciar sesión")
app.add_page(signup, title="Crear nueva cuenta")