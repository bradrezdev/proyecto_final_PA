import reflex as rx
from .state import Login
from .state import QuestionsState
from .state import SearchUIState
from .theme import Custom_theme

def header():
    return rx.flex(
                # Contenedor del logo
                rx.button(
                    rx.image(src="/logotipo.png", width="200px", height="auto"),
                    bg="none",
                    cursor="pointer",
                    on_click=lambda: rx.redirect("/"),
                ),
                rx.flex(
                    # Botón Búsqueda
                    rx.icon_button(
                        "search",
                        on_click=SearchUIState.toggle_search_box,
                        bg=rx.color_mode_cond(
                            light=Custom_theme().light_colors()["primary"],
                            dark=Custom_theme().dark_colors()["primary"]),
                        border_radius="100px",
                        cursor="pointer",
                        width="48px",
                        height="48px",
                        margin_right="24px",
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
                                rx.flex(
                                    rx.input(
                                        placeholder="Buscar por tema",
                                        bg="#FFFFFF",

                                        padding="0 16px",
                                        border_radius="100px",
                                        height="48px",
                                        width="40%",
                                        on_change=QuestionsState.set_search_term,
                                    ),
                                    rx.icon(
                                        "x",
                                        on_click=[
                                            SearchUIState.toggle_search_box,
                                            QuestionsState.set_search_term("")
                                        ],
                                        cursor="pointer",
                                        width="40px",
                                        height="40px",
                                        margin_left="16px",
                                    ),
                                    direction="row",
                                    width="100%",
                                    margin_bottom="32px",
                                    justify="center",
                                    align="center",
                                ),
                                rx.scroll_area(
                                    rx.flex(
                                        rx.cond(
                                            QuestionsState.search_term,
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
                                                        light="#FFFFFF",
                                                        dark="#000000"
                                                    ),
                                                    cursor="pointer",
                                                    border_radius="20px",
                                                    padding="20px",
                                                    direction="column",
                                                    spacing="3",
                                                    on_click=[
                                                        lambda: rx.redirect(f"/question/{question.question_id}"),
                                                        QuestionsState.set_search_term(""),
                                                        SearchUIState.toggle_search_box
                                                    ]
                                                ),
                                            ),
                                        ),
                                        margin="0 auto",
                                        direction="column",
                                        width="70%",
                                        spacing="5",
                                    ),
                                    padding_bottom="128px",
                                ),
                                position="fixed",
                                top="50%",
                                left="50%",
                                transform="translate(-50%, -50%)",
                                width="100vw",
                                height="100vh",
                                #bg="rgba(200, 200, 200, 0.6)",
                                backdrop_filter="blur(30px)",
                                padding_top="48px",
                                z_index="100",
                            )
                        )
                    ),
                    
                    rx.cond(
                        Login.logged_user_data,

                        # ------------------ BLOQUE SI EL USUARIO ESTÁ LOGUEADO ------------------
                        rx.flex(
                            # Nombre de usuario
                            rx.flex(
                                rx.link(
                                    rx.text(Login.logged_user_data["username"], size="4"),
                                    href=f"/profile/{Login.logged_user_data['user_id']}"
                                ),
                                #rx.text(Login.logged_user_data["title"]),
                                direction="column",
                                padding="0 32px 0 32px",
                                justify="center",
                            ),
                            rx.button(
                                "Cerrar sesión",
                                on_click=Login.logout,
                                cursor="pointer",
                                bg=rx.color_mode_cond(
                                    light=Custom_theme().light_colors()["primary"],
                                    dark=Custom_theme().dark_colors()["primary"],
                                ),
                                height="40px",
                                border_radius="12px",
                            ),
                            bg=rx.color_mode_cond(
                                light=Custom_theme().light_colors()["background"],
                                dark=Custom_theme().dark_colors()["background"],
                            ),
                            border_radius="20px",
                            spacing="3",
                            padding="20px",
                            ),
                        # ------------------ BLOQUE SI **NO** HAY SESIÓN ------------------
                        rx.hstack(
                            # Botón “Registrarse”
                            rx.link(
                                rx.button(
                                    "Registrarse",
                                    bg=rx.color_mode_cond(
                                        light=Custom_theme().light_colors()["primary"],
                                        dark=Custom_theme().dark_colors()["primary"],
                                    ),
                                    border_radius="100px",
                                    width="135px",
                                    height="48px",
                                    cursor="pointer",
                                ),
                                margin_left="7rem",
                                href="/sign_up",
                            ),
                            # Botón “Iniciar sesión”
                            rx.link( 
                                rx.button(
                                    rx.text(
                                        "Iniciar sesión",
                                        color=rx.color_mode_cond(
                                            light=Custom_theme().light_colors()["primary"],
                                            dark=Custom_theme().dark_colors()["primary"],
                                        ),
                                    ),
                                    cursor="pointer",
                                    bg="none",
                                    border_radius="100px",
                                    width="135px",
                                    height="48px",
                                    border="2px solid",
                                    border_color=rx.color_mode_cond(
                                        light=Custom_theme().light_colors()["primary"],
                                        dark=Custom_theme().dark_colors()["primary"],
                                    ),
                                ),
                                href="/login",
                                margin_left="1rem",
                            ),
                            spacing="2",
                        ),
                    ),
                    align="center",
                ),
                align="center",
                justify="between",
                direction="row",
                margin="64px 0 64px 0",
                width="100%",
            ),