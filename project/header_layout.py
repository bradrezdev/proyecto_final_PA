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
                                rx.input(
                                    placeholder="Buscar por tema",
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