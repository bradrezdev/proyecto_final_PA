"""Proyecto Final | Programación Avanzada | Index sin inicio de sesión"""

import reflex as rx
from rxconfig import config
from ..theme import Custom_theme
from ..state import Login
from ..state import SearchState
from ..state import SearchUIState
from ..state import QuestionsState

def logged_index() -> rx.Component:
    # Contenedor principal
    return rx.vstack(

        # Contenedor Header | Logo + Search, Login, Signup
        rx.flex(
            
            # Contenedor del logo
            rx.box(
                
                rx.image(src="/logotipo.png", width="200px", height="auto"),
                width="100%",

            ),

            # Contenedor del usuario que inició sesión
            rx.flex(
                    
                # Contendor de la imagen del Developer
                rx.box(
                    
                    # Propiedades box de imagen
                    height="56px",
                    width="56px",
                    border_radius="100px",
                    bg="#FFFFFF",
                ),

                # Contenedor nombre + título
                rx.flex(

                    rx.text(
                            Login.logged_user_data.get("username"),
                        size="4",
                    ),

                    rx.text(
                            Login.logged_user_data.get("title"),
                        size="2",
                    ),
                    # Propiedades flex de nombre + título
                    direction="column",
                ),
                bg=rx.color_mode_cond(
                    light=Custom_theme().light_colors()["background"],
                    dark=Custom_theme().dark_colors()["background"]
                ),
                border_radius="20px",
                spacing="3",
                padding="20px",
                on_click=lambda: rx.redirect(f"/profile/{Login.logged_user_data.get('user_id')}"),
                width="36vw",
            ),

        # Propiedades @Header
        justify="between",
        padding="4%",
        width="100%",
        ),

        # Contenedor títulos | Últimas preguntas + Top Developers
        rx.flex(

            rx.box(
                rx.heading("Últimas preguntas"),
                width="63vw",
                ),

            rx.box(
                rx.heading("Top Developers"),
                width="27vw",
            ),

        justify="between",
        padding_left="4%",
        padding_right="4%",
        padding_top="4%",
        padding_bottom="1%",
        width="100%",
        ),

        # Contenedor Main | Preguntas + Top Developers
        rx.hstack(
                rx.flex(
                    rx.foreach(
                        QuestionsState.questions,
                        lambda question: rx.flex(
                            rx.hstack(
                                rx.heading(
                                    question.title,  # Cambiar question["title"] por question.title
                                    size="5",
                                ),
                                rx.moment(
                                    question.created_at, from_now=True,  # Cambiar question["created_at"] por question.created_at
                                    size="1",
                                ),
                                justify="between",
                            ),
                            rx.text(
                                question.body[:200] + "..."
                            ),
                            bg=rx.color_mode_cond(
                                light=Custom_theme().light_colors()["background"],
                                dark=Custom_theme().dark_colors()["background"]
                            ),
                            border_radius="20px",
                            width="63vw",
                            padding="22px",
                            direction="column",
                            spacing="2",
                            on_click=lambda: rx.redirect(f"/question/{question.question_id}"),
                        )
                    ),
                    direction="column",
                    width="63vw",
                    spacing="4",
                ),
                rx.flex(
                    rx.flex(
                        rx.box(
                            height="56px",
                            width="56px",
                            border_radius="100px",
                            bg="#FFFFFF",
                        ),
                        rx.flex(
                            rx.text(
                                "[Nombre de Desarrollador]",
                                size="4",
                            ),
                            rx.text(
                                "[Título de Desarrollador]",
                                size="2",
                            ),
                            direction="column",
                        ),
                        bg=rx.color_mode_cond(
                            light=Custom_theme().light_colors()["background"],
                            dark=Custom_theme().dark_colors()["background"]
                        ),
                        border_radius="20px",
                        spacing="3",
                        padding="20px",
                    ),
                    rx.flex(
                        rx.box(
                            height="56px",
                            width="56px",
                            border_radius="100px",
                            bg="#FFFFFF",
                        ),
                        rx.flex(
                            rx.text(
                                "[Nombre de Desarrollador]",
                                size="4",
                            ),
                            rx.text(
                                "[Título de Desarrollador]",
                                size="2",
                            ),
                            direction="column",
                        ),
                        bg="#979797",
                        border_radius="20px",
                        spacing="3",
                        padding="20px",
                    ),
                    rx.flex(
                        rx.box(
                            height="56px",
                            width="56px",
                            border_radius="100px",
                            bg="#FFFFFF",
                        ),
                        rx.flex(
                            rx.text(
                                "[Nombre de Desarrollador]",
                                size="4",
                            ),
                            rx.text(
                                "[Título de Desarrollador]",
                                size="2",
                            ),
                            direction="column",
                        ),
                        bg="#979797",
                        border_radius="20px",
                        spacing="3",
                        padding="20px",
                    ),
                    rx.flex(
                        rx.box(
                            height="56px",
                            width="56px",
                            border_radius="100px",
                            bg="#FFFFFF",
                        ),
                        rx.flex(
                            rx.text(
                                "[Nombre de Desarrollador]",
                                size="4",
                            ),
                            rx.text(
                                "[Título de Desarrollador]",
                                size="2",
                            ),
                            direction="column",
                        ),
                        bg="#979797",
                        border_radius="20px",
                        spacing="3",
                        padding="20px",
                    ),
                    rx.flex(
                        rx.box(
                            height="56px",
                            width="56px",
                            border_radius="100px",
                            bg="#FFFFFF",
                        ),
                        rx.flex(
                            rx.text(
                                "[Nombre de Desarrollador]",
                                size="4",
                            ),
                            rx.text(
                                "[Título de Desarrollador]",
                                size="2",
                            ),
                            direction="column",
                        ),
                        bg="#979797",
                        border_radius="20px",
                        spacing="3",
                        padding="20px",
                    ),
                    direction="column",
                    spacing="4",
                    width="27vw",
                ),
                justify="between",
                padding_left="4%",
                padding_right="4%",
                width="100%",
            ),

        # Propiedades contenedor principal vstack
        on_mount=[Login.load_logged_user, Login.load_profile],
        height="100vh",
        max_width="1920",
        width="100%",
    )