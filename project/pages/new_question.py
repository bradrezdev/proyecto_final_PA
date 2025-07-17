import reflex as rx
from ..header_layout import header
from ..state import Login
from ..theme import Custom_theme
from project.state import QuestionsState

def new_question():
    return rx.vstack(

        # Contenedor Header | Logo + Search, Login, Signup
        header(),

        rx.heading("Haz una pregunta pública", margin_bottom="32px"),

        # 1. Input del título
        rx.text("Título de la pregunta", size="2", margin_bottom="2px"),
        rx.input(
            placeholder="Escribe el título de tu pregunta aquí...",
            value=QuestionsState.title,
            on_change=QuestionsState.setTitle,
            border_radius="12px",
            height="48px",
            margin_bottom="16px",
            padding_left="8px",
            width="100%",
            required=True,
        ),

        # 2. Cuerpo
        rx.text("Describe tu pregunta aquí. Entre más detalles, mejor.", size="2", margin_bottom="2px"),
        rx.text_area(
            placeholder="Escribe tu pregunta aquí...",
            value=QuestionsState.body,
            on_change=QuestionsState.setBody,
            border_radius="12px",
            auto_height=True,
            min_height="200px",
            max_height="400px",
            margin_bottom="16px",
            padding="8px 0 0 8px",
            size="2",
            width="100%",
            required=True,
        ),

        # 3. Botón Publicar
        rx.cond(
            QuestionsState.title.bool() & QuestionsState.body.bool(),
            rx.button(
                "Publicar pregunta",
                on_click=QuestionsState.publish_question(Login.logged_user_data["user_id"]),
                border_radius="8px",
                bg=rx.color_mode_cond(
                    light=Custom_theme().light_colors()["primary"],
                    dark=Custom_theme().dark_colors()["primary"],
                ),
                cursor="pointer",
                height="40px",
                padding="10px",
                width="15%",
            ),
        ),
        on_mount=[
            Login.load_logged_user,  # Cargar datos del usuario logueado
        ],
        margin="0 auto",
        max_width="1280px",
    )