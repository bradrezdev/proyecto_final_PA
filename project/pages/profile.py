import reflex as rx
from ..theme import Custom_theme
from ..state import Login

def profile_page():
    profile = Login.profile_data
    # Lee en cada render el estado actual del usuario
    my_id = Login.logged_user_data.get("user_id")
    profile_id = profile.get("user_id")
    is_owner = (rx.cond(my_id == profile_id, True, False))

    return rx.cond(
        profile_id,
        rx.vstack(
            rx.heading(f"Perfil de {profile.get('username')}", size="4"),
            rx.divider(),
            rx.cond(
                is_owner,
                rx.vstack(
                    rx.text("Este es tu perfil. Puedes editar tus datos."),
                    rx.input(
                        placeholder="Nombre de usuario",
                        value=Login.edit_username,
                        on_change=lambda e: Login.set_edit_username(e),
                    ),
                    rx.input(
                        placeholder="Correo electrónico",
                        value=Login.edit_email,
                        on_change=lambda e: Login.set_edit_email(e),
                    ),
                    rx.button("Guardar cambios", on_click=Login.update_profile),
                    spacing="3"
                ),
                rx.vstack(
                    rx.text(f"Nombre de usuario: {profile.get('username')}"),
                    rx.text(f"Correo electrónico: {profile.get('email')}"),
                    rx.text(f"Título: {profile.get('title')}"),
                    rx.text(f"Estrellas: {profile.get('total_stars')}"),
                    spacing="2"
                )
            ),
            spacing="6",
            align="start",
            width="100%",
            max_width="540px",
            margin="0 auto",
            padding="2rem",
            on_mount=[Login.load_profile, Login.load_logged_user],
        ),
        rx.center(rx.heading("Cargando perfil..."), height="100vh")
    )