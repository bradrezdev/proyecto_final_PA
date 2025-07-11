"""Proyecto Final | Programación Avanzada | index"""

import reflex as rx
from .pages.logged_index import logged_index
from .pages.signup import signup
from .pages.login import login
from .pages.new_question import new_question
from .pages.question import question_page
from .theme import Custom_theme
from .state import Login
from .state import SearchState
from .state import SearchUIState
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
            rx.flex(
                # Contenedor del logo
                rx.box(
                    rx.image(src="/logotipo.png", width="200px", height="auto"),
                    width="74vw",
                ),
                rx.box(
                    # Botón Búsqueda
                    rx.icon_button(
                        "search",
                        on_click=SearchUIState.toggle_search_box,
                        bg=rx.color_mode_cond(
                            light=Custom_theme().light_colors()["primary"],
                            dark=Custom_theme().dark_colors()["primary"]),
                        border_radius="100px",
                        width="48px",
                        height="48px",
                        margin_right="10px",
                    ),
                    rx.cond(
                        SearchUIState.show_search_box,
                        rx.fragment(
                            rx.box(
                                on_click=SearchUIState.toggle_search_box,
                                position="fixed",
                                top="0",
                                left="0",
                                width="100vw",
                                height="100vh",
                                z_index="99",
                            ),
                            rx.box(
                                rx.input(
                                    placeholder="Buscar por tema o etiqueta",
                                    bg="#FFFFFF",
                                    margin="0 auto",
                                    padding="0 16px",
                                    border_radius="100px",
                                    height="48px",
                                    width="40%",
                                    on_change=lambda e: QuestionsState.search_questions(e),
                                ),
                                rx.vstack(
                                    rx.foreach(
                                        QuestionsState.questions,
                                        lambda question: rx.box(
                                            rx.text(question.title),
                                            rx.text(question.body[:100] + "..."),
                                            bg=rx.color_mode_cond(
                                                light=Custom_theme().light_colors()["background"],
                                                dark=Custom_theme().dark_colors()["background"]
                                            ),
                                            border_radius="20px",
                                            width="63vw",
                                            padding="22px",
                                            direction="column",
                                            spacing="2",
                                        )
                                    ),
                                    padding="2rem",
                                    spacing="2",
                                    align_items="start"
                                ),
                                position="fixed",
                                top="50%",
                                left="50%",
                                transform="translate(-50%, -50%)",
                                width="95vw",
                                height="95vh",
                                bg="rgba(175, 175, 175, 0.3)",
                                box_shadow="0 4px 8px rgba(175, 175, 175, 0.3)",
                                backdrop_filter="blur(10px)",
                                border_radius="64px",
                                padding_top="48px",
                                z_index="100",
                            )
                        )
                    ),
                    rx.link(
                        rx.button(
                            "Registrarse",
                            bg=rx.color_mode_cond(
                                light=Custom_theme().light_colors()["primary"],
                                dark=Custom_theme().dark_colors()["primary"]
                            ),
                            border_radius="100px",
                            width="135px",
                            height="48px",
                        ),
                        href="/sign_up",
                    ),
                    rx.link(
                        rx.button(
                            rx.text("Iniciar sesión",color=rx.color_mode_cond(
                                light=Custom_theme().light_colors()["primary"],
                                dark=Custom_theme().dark_colors()["primary"]
                            )),
                            bg="none",
                            border_radius="100px",
                            width="135px",
                            height="48px",
                            border="2px solid",
                            border_color=rx.color_mode_cond(
                                light=Custom_theme().light_colors()["primary"],
                                dark=Custom_theme().dark_colors()["primary"]
                        )
                        ),
                        margin_left="1rem",
                        href="/login",
                    ),
                    width="25rem",
                ),
                justify="between",
                padding="3%",
                width="100%",
            ),
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
                            on_click=lambda: rx.redirect(f"/question/{question.question_id}"),  # Usar question.question_id
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
            height="100vh",
            max_width="100%",
            width="100%",
        )
    )


app = rx.App(theme=rx.theme(
    light=Custom_theme().light_colors(),
    dark=Custom_theme().dark_colors(),
    appearance="inherit",
))
app.add_page(project, title="Página de inicio", route="/", on_load=QuestionsState.load_questions)
app.add_page(new_question, title="Nueva pregunta", route="/new_question")
app.add_page(
    question_page,
    title="Detalle de pregunta", 
    route="/question/[question_id]",  # Usar corchetes para parámetros dinámicos
    on_load=QuestionsState.load_questions
)
app.add_page(
    logged_index,
    title="Página de inicio",
    route="/dashboard",
    on_load=QuestionsState.load_questions,
)
app.add_page(login, title="Iniciar sesión", route="/login")
app.add_page(signup, title="Crear nueva cuenta", route="/sign_up")