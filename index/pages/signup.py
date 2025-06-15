"""Proyecto Final | Programación Avanzada | Sign up Page"""

import reflex as rx
from rxconfig import config

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
                        name="username",
                        style={"border": "1px solid black"},
                        border_radius="8px",
                        height="40px",
                        width="25vw",
                    ),

                    rx.text("Correo electrónico"),

                    rx.input(
                        placeholder="Escribe tu correo electrónico",
                        name="email",
                        style={"border": "1px solid black"},
                        type="email",
                        border_radius="8px",
                        height="40px",
                        width="25vw"
                    ),

                    rx.hstack(

                        rx.vstack(
                            rx.text("Contraseña"),

                            rx.input(
                                placeholder="Escribe tu contraseña",
                                name="password",
                                style={"border": "1px solid black"},
                                type="password",
                                border_radius="8px",
                                height="40px",
                                width="100%"
                            ),
                        ),

                        rx.vstack(
                            rx.text("Confirmar contraseña"),

                            rx.input(
                                placeholder="Confirma tu contraseña",
                                name="password",
                                style={"border": "1px solid black"},
                                type="password",
                                border_radius="8px",
                                height="40px",
                                width="100%"
                            ),
                        ),

                    ),

                    rx.hstack(

                        rx.checkbox("Al registrar los detalles de tu cuenta, aceptas nuestros términos y condiciones.", size="2"),

                    ),

                    rx.button("Registrarse", height="47px", width="25vw", border_radius="8px",),

                    rx.hstack(
                        rx.spacer(),
                        rx.text("Ya tienes una cuenta?",size="1"),
                        rx.link("Inicia sesión", href="/login",size="1"),
                        rx.spacer(),
                    # Propiedades de hstack "¿NO tienes una cuenta?
                    spacing="1",
                    width="100%",
                    ),
                ),

                # Propiedades @Formulario de registro.
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