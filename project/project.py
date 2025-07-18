"""Proyecto Final | Programación Avanzada | index"""

import reflex as rx
from .pages.signup import signup
from .pages.login import login
from .pages.profile import profile_page
from .pages.new_question import new_question
from .pages.question import question_page
from .header_layout import header
from .theme import Custom_theme
from .state import Login
from .state import QuestionsState

def project() -> rx.Component:
    return rx.cond(
        QuestionsState.is_loading,
        rx.center(
            rx.skeleton(
                rx.box(
                    height="90vh",
                    width="90vw",
                    bg="rgba(200, 200, 200, 0.4)",
                    border_radius="32px"
                ),
                height="90vh",
                width="90vw"
            )
        ),
        # Aquí empieza todo el contenido real.
        rx.vstack(

            # Contenedor Header | Logo + Search, Login, Signup
            header(),

            rx.flex(
                rx.heading("Últimas preguntas"),
                rx.button("Nueva pregunta", on_click=lambda: rx.redirect("/new_question"), bg=rx.color_mode_cond(
                    light=Custom_theme().light_colors()["primary"],
                    dark=Custom_theme().dark_colors()["primary"],
                ),
                height="40px",
                width="12%",
                border_radius="12px",
                cursor="pointer",
            ),
            justify="between",
            margin="4% 0 2% 0",
            width="100%",
        ),
        rx.hstack(
                rx.flex(
                    rx.foreach(
                        QuestionsState.questions,
                        lambda question: rx.flex(
                            rx.hstack(
                                rx.heading(
                                    question.title,
                                    size="5",
                                ),
                                rx.moment(
                                    question.created_at, from_now=True,
                                    size="1",
                                ),
                                justify="between",
                            ),
                            rx.text(
                                question.body[:400] + "..."
                            ),
                            bg=rx.color_mode_cond(
                                light=Custom_theme().light_colors()["background"],
                                dark=Custom_theme().dark_colors()["background"]
                            ),
                            cursor="pointer",
                            border_radius="20px",
                            padding="20px",
                            direction="column",
                            spacing="3",
                            on_click=lambda: rx.redirect(f"/question/{question.question_id}"),
                        )
                    ),
                    direction="column",
                    width="100%",
                    spacing="5",
                ),
                width="100%",
                margin_bottom="128px",
            ),
            padding="0 20px 0 20px",
            max_width="1280px",
            margin="0 auto",
            on_mount=[
                Login.load_logged_user,  # Cargar datos del usuario logueado
                Login.load_profile,  # Cargar perfil del usuario logueado
                QuestionsState.load_questions,  # Cargar preguntas
            ]
        ),
    )


app = rx.App(theme=rx.theme(
    light=Custom_theme().light_colors(),
    dark=Custom_theme().dark_colors(),
    appearance="inherit",
))
app.add_page(
    project,
    title="Página de inicio",
    route="/",
    on_load=[QuestionsState.load_questions, Login.load_logged_user,]
)
app.add_page(
    new_question,
    title="Nueva pregunta",
    route="/new_question",
)
app.add_page(
    question_page,
    title="Detalle de pregunta", 
    route="/question/[question_id]",
    on_load=QuestionsState.load_questions
)
app.add_page(profile_page,
    title="Perfil de usuario | [username]",
    route="/profile/[user_id]",
    on_load=Login.load_profile,
)
app.add_page(login,
    title="Iniciar sesión",
    route="/login"
)
app.add_page(signup,
    title="Crear nueva cuenta",
    route="/sign_up"
)