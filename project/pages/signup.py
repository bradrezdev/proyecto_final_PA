"""Proyecto Final | Programación Avanzada | Sign up Page"""

import reflex as rx
from rxconfig import config
from ..state import Signup
from ..theme import Custom_theme
#from ..models.users import Users

def signup() -> rx.Component:
    # Contenedor principal
    return rx.flex(
        
        # Contenedor izquierdo | Formulario
        rx.vstack(
            
            rx.image(src="/logotipo.png", width="200px", height="auto"),

            # Formulario de inicio de sesión.
            rx.form(
                
                # Inputs del formulario.
                rx.vstack(

                    rx.heading("Crea una cuenta", size="8",),

                    rx.text("Únete a la red de apoyo más grande para estudiantes y programadores:"),
                    
                    rx.text("Nombre de usuario"),

                    rx.input(
                        placeholder="Escribe un nombre de usuario válido",
                        type="text",
                        value=Signup.username,
                        on_change=Signup.setUsername,
                        reset_on_submit= True,
                        required=True,
                        style={"border": "1px solid black"},
                        border_color=rx.color_mode_cond(
                            light=Custom_theme().light_colors()["primary"],
                            dark=Custom_theme().dark_colors()["primary"]
                        ),
                        border_radius="8px",
                        height="40px",
                        width="25vw",
                    ),

                    rx.text("Correo electrónico"),

                    rx.input(
                        placeholder="Escribe tu correo electrónico",
                        type="email",
                        value=Signup.email,
                        on_change=Signup.setEmail,
                        reset_on_submit= True,
                        required=True,
                        style={"border": "1px solid black"},
                        border_color=rx.color_mode_cond(
                            light=Custom_theme().light_colors()["primary"],
                            dark=Custom_theme().dark_colors()["primary"]
                        ),
                        border_radius="8px",
                        height="40px",
                        width="25vw"
                    ),

                    rx.hstack(

                        rx.vstack(
                            rx.text("Contraseña"),

                            rx.input(
                                placeholder="Escribe tu contraseña",
                                type="password",
                                value=Signup.password,
                                on_change=Signup.setPassword,
                                reset_on_submit= True,
                                required=True,
                                style={"border": "1px solid black"},
                                border_color=rx.color_mode_cond(
                                    light=Custom_theme().light_colors()["primary"],
                                    dark=Custom_theme().dark_colors()["primary"]
                                ),
                                border_radius="8px",
                                height="40px",
                                width="100%"
                            ),
                            width="12.25vw"
                        ),

                        rx.vstack(
                            rx.text("Confirmar contraseña"),

                            rx.input(
                                placeholder="Confirma tu contraseña",
                                type="password",
                                value=Signup.confirm_password,
                                on_change=Signup.setConfirmPassword,
                                reset_on_submit= True,
                                required=True,
                                style={"border": "1px solid black"},
                                border_color=rx.color_mode_cond(
                                    light=Custom_theme().light_colors()["primary"],
                                    dark=Custom_theme().dark_colors()["primary"]
                                ),
                                border_radius="8px",
                                height="40px",
                                width="100%"
                            ),
                            width="12.25vw"
                        ),
                        spacing="2"
                    ),

                    rx.hstack(

                        rx.checkbox("Al registrar los detalles de tu cuenta, aceptas nuestros términos y condiciones.", size="2"),

                    ),

                    rx.button(
                        "Registrarse",
                        type="submit",
                        height="47px",
                        width="25vw",
                        bg=rx.color_mode_cond(
                            light=Custom_theme().light_colors()["primary"],
                            dark=Custom_theme().dark_colors()["primary"]
                        ),
                        border_radius="8px",
                    ),

                    rx.hstack(
                        rx.spacer(),
                        rx.text("Ya tienes una cuenta?",size="1"),
                        rx.link("Inicia sesión",color=rx.color_mode_cond(
                            light=Custom_theme().light_colors()["primary"],
                            dark=Custom_theme().dark_colors()["primary"]
                        ),href="/login",size="1"),
                        rx.spacer(),
                    # Propiedades de hstack "¿NO tienes una cuenta?
                    spacing="1",
                    width="100%",
                    ),
                ),

                # Propiedades @Formulario de registro.
                on_submit=Signup.signup_user,
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
        rx.center(
            rx.image(src="/image_signup.png", width="80%", height="auto", align="center"),
            width="50%",
        ),

        # Propiedades contenedor principal
        height="100vh",
        max_width="1920",
        width="100%",
    )