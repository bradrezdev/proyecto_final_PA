import reflex as rx
from ..state import Login
from ..state import QuestionsState

def question_page() -> rx.Component:
    return rx.vstack(
        rx.cond(
            QuestionsState.question,
            rx.vstack(
                rx.heading(QuestionsState.question.title, size="3"),
                rx.text(QuestionsState.question.body),
                rx.text(f"Preguntado por: {QuestionsState.question_username}"),
                # Etiquetas
                rx.hstack(
                    rx.foreach(QuestionsState.tags, lambda tag: rx.badge(tag.tag_name)),
                ),
                rx.divider(),

                # Respuestas
                rx.heading("Respuestas", size="2"),
                rx.cond(
                    QuestionsState.answers,
                    rx.foreach(
                        QuestionsState.answers,
                        lambda answer: rx.box(
                            rx.text(answer.body),
                            rx.text(f"Respondido por: {answer.user_id}", size="3", color="gray"),
                            bg="#fafafa",
                            border_radius="8px",
                            padding="8px",
                            margin_bottom="6px",
                        )
                    ),
                    rx.text("No hay respuestas aún.")
                ),
                rx.divider(),

                # Formulario de respuesta
                rx.text_area(
                    value=QuestionsState.answer_body,
                    on_change=QuestionsState.set_answer_body,
                    placeholder="Escribe tu respuesta...",
                    width="100%",
                    min_height="70px"
                ),
                rx.button(
                    "Responder",
                    on_click=QuestionsState.post_answer(Login.logged_user_data["user_id"]),
                    disabled=~QuestionsState.answer_body.bool()
                )
            ),
            rx.heading("Cargando pregunta...")
        ),
        on_mount=[Login.load_logged_user,
                  QuestionsState.load_question_detail],
        padding="2rem",
        max_width="800px",
        margin="0 auto"
    )