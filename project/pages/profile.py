import reflex as rx
from ..header_layout import header
from ..theme import Custom_theme
from ..state import Login
from ..state import QuestionsState

def profile_page():
    profile = Login.profile_data
    # Lee en cada render el estado actual del usuario
    my_id = Login.logged_user_data.get("user_id")
    profile_id = profile.get("user_id")
    is_owner = (rx.cond(my_id == profile_id, True, False))

    return rx.vstack(
        # Contenedor Header | Logo + Search, Login, Signup
        header(),

        rx.cond(
            profile_id,
            rx.vstack(
            rx.heading("Perfil de usuario", size="4"),
            rx.divider(),
            rx.cond(
                is_owner,
                rx.flex(
                    rx.vstack(
                        rx.text("Nombre de usuario", margin_bottom="16px"),
                        rx.text("Correo electrónico", margin_bottom="12px"),
                        rx.text("Miembro desde", margin_bottom="12px"),
                        width="30%"
                    ),
                    rx.vstack(
                        rx.input(
                            placeholder="Nombre de usuario",
                            value=Login.edit_username,
                            on_change=lambda e: Login.set_edit_username(e),
                            required=True,
                            text_align="right",
                            border_radius="8px",
                            padding_right="8px",
                            width="60%",
                            margin_bottom="8px",
                        ),
                        rx.text(profile.get('email'), margin_bottom="12px"),
                        rx.text(profile.get('created_at'), margin_bottom="20px"),
                        rx.button(
                            "Guardar cambios",
                            bg=rx.color_mode_cond(
                                light=Custom_theme().light_colors()["primary"],
                                dark=Custom_theme().dark_colors()["primary"],
                            ),
                            cursor="pointer",
                            on_click=Login.update_profile),
                        align="end",
                        width="70%",
                    ),
                    justify="between",
                    width="100%",
                ),
                rx.flex(
                    rx.vstack(
                        rx.text("Nombre de usuario", margin_bottom="16px"),
                        rx.text("Correo electrónico", margin_bottom="12px"),
                        rx.text("Miembro desde", margin_bottom="12px"),
                        width="30%"
                    ),
                    rx.vstack(
                        rx.text(profile.get('username'), margin_bottom="16px"),
                        rx.text(profile.get('email'), margin_bottom="12px"),
                        rx.text(profile.get('created_at'), margin_bottom="20px"),
                        align="end",
                        width="70%",
                    ),
                    justify="between",
                    width="100%",
                )
            ),
            rx.divider(),
            rx.cond(
                is_owner,
                rx.heading("Mis preguntas", size="3"),
                rx.heading(f"Preguntas de {profile.get('username')}", size="3"),
            ),
            rx.hstack(
                rx.foreach(
                    QuestionsState.questions,
                    lambda question: rx.flex(
                        rx.hstack(
                            rx.heading(
                                question.title,
                                size="5",
                            ),
                            rx.moment(
                                question.created_at,
                                from_now=True,
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
                        width="100%",
                    )
                ),
                direction="column",
                width="100%",
                spacing="5",
            ),
            spacing="6",
            align="start",
            width="100%",
            #max_width="80%",
            margin="0 auto",
            margin_bottom="128px",
            on_mount=[
                Login.load_profile,
                Login.load_logged_user,
                QuestionsState.load_user_questions(profile.get("user_id")),
            ],
        ),
        rx.heading(
            "Cargando perfil...",
            height="100%",
            margin="0 auto",
        )
    ),
    max_width="1280px",
    margin="0 auto",
)