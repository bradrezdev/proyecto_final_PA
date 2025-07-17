import reflex as rx
from ..header_layout import header
from ..state import Login
from ..state import QuestionsState
from ..state import Stars
from ..theme import Custom_theme

def question_page() -> rx.Component:
    return rx.vstack(

        # Contenedor Header | Logo + Search, Login, Signup
        header(),

        rx.cond(
            QuestionsState.question,
            rx.vstack(
                rx.heading(QuestionsState.question.title),
                rx.text(QuestionsState.question.body),
                rx.text("Preguntado por: ", rx.link(QuestionsState.question_user['username'], href=f'/profile/{QuestionsState.question_user['user_id']}'), size="3", color="gray"),
                rx.divider(),

                # Respuestas
                rx.heading("Respuestas", size="2"),
                rx.cond(
                    QuestionsState.answers,
                    rx.foreach(
                        QuestionsState.answers,
                        lambda answer, i: rx.box(
                            rx.text(answer.body),
                            rx.text("Respondido por: ", rx.link(QuestionsState.answers_user[i]['username'], href=f'/profile/{QuestionsState.answers_user[i]['user_id']}', color=rx.color_mode_cond(light=Custom_theme().light_colors()["text"], dark=Custom_theme().dark_colors()["text"])), size="3", color="gray", margin_right="16px"),
                            rx.divider(margin_top="16px"),
                            border_radius="20px",
                            padding="10px 20px 10px 20px",
                            width="100%",
                        )
                    ),
                    rx.text("No hay respuestas aún.", margin_bottom="16px"),
                ),
                rx.vstack(
                    # Formulario de respuesta
                    rx.text(f"Estás respondiendo como {Login.logged_user_data['username']}"),
                    rx.text_area(
                        value=QuestionsState.answer_body,
                        on_change=QuestionsState.set_answer_body,
                        placeholder="Escribe tu respuesta...",
                        
                        border_radius="20px",
                        padding="10px",
                        width="100%",
                        auto_height=True,
                        min_height="100px",
                        max_height="200px",
                    ),
                    rx.button(
                        "Responder",
                        on_click=QuestionsState.post_answer(Login.logged_user_data["user_id"]),
                        disabled=~QuestionsState.answer_body.bool(),
                        bg=rx.color_mode_cond(
                            light=Custom_theme().light_colors()["primary"],
                            dark=Custom_theme().dark_colors()["primary"],
                        ),
                        border_radius="8px",
                        padding="10px",
                        width="15%",
                        height="40px",
                    ),
                    margin="0 auto",
                    width="100%",
                ),
                margin="0 auto",
                margin_bottom="128px",
                width="100%",
                on_mount=[
                    Login.load_logged_user,
                    QuestionsState.load_question_detail
                ],
            ),
            rx.heading(
                "Cargando pregunta...",
                height="100%",
                margin="0 auto",
            ),
        ),
        margin="0 auto",
        max_width="1280px",
    )