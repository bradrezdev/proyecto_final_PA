"""Proyecto Final | Programación Avanzada | Log in Page"""

import reflex as rx
from rxconfig import config
from index.state import State

def login() -> rx.Component:
    # Contenedor principal
    return rx.flex(
        
        # Contenedor izquierdo | Formulario
        rx.vstack(
            
            rx.image(src="/logotipo.png", width="200px", height="auto"),

            """
            # Mensajes de error y éxito
            rx.cond(
                State.error_message != "",
                rx.callout(
                    State.error_message,
                    icon="alert_triangle",
                    color_scheme="red",
                    width="25vw",
                ),
            ),
            
            rx.cond(
                State.success_message != "",
                rx.callout(
                    State.success_message,
                    icon="check",
                    color_scheme="green",
                    width="25vw",
                ),
            ),
            """,

            # Formulario de inicio de sesión
            rx.form(
                
                # Inputs del formulario
                rx.vstack(

                    rx.heading("Bienvenido de vuelta", size="8"),

                    rx.text("Qué gusto volverte a ver. Por favor, ingresa los datos de tu cuenta:"),
                    
                    rx.spacer(),

                    rx.text("Correo electrónico"),
                    rx.input(
                        placeholder="Escribe tu correo electrónico",
                        value=State.login_email,
                        on_change=State.set_login_email,
                        name="email",
                        type="email",
                        style={"border": "1px solid black"},
                        border_radius="8px",
                        height="40px",
                        width="25vw",
                        required=True,
                    ),

                    rx.text("Contraseña"),
                    rx.input(
                        placeholder="Escribe tu contraseña",
                        value=State.login_password,
                        on_change=State.set_login_password,
                        name="password",
                        type="password",
                        style={"border": "1px solid black"},
                        border_radius="8px",
                        height="40px",
                        width="25vw",
                        required=True,
                    ),

                    rx.link("Olvidé mi contraseña", href="/reset-password", size="1"),
                    
                    rx.button(
                        rx.cond(
                            State.loading,
                            rx.hstack(
                                rx.spinner(size="1"),
                                rx.text("Iniciando sesión..."),
                                spacing="2",
                            ),
                            rx.text("Iniciar sesión"),
                        ),
                        on_click=State.handle_login,
                        disabled=State.loading,
                        height="47px",
                        width="25vw",
                        type="submit",
                        border_radius="8px",
                    ),

                    rx.hstack(
                        rx.spacer(),
                        rx.text("¿No tienes una cuenta?", size="1"),
                        rx.link("Crear una cuenta", href="/signup", size="1"),
                        rx.spacer(),
                        spacing="1",
                        width="100%",
                    ),
                ),

                # Propiedades del formulario
                on_submit=State.handle_login,
                reset_on_submit=False,
                padding="20%",
                width="100%",
            ),

            # Propiedades del contenedor izquierdo
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