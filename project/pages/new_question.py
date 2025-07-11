import reflex as rx
from project.state import QuestionsState

def new_question():
    return rx.vstack(
        rx.heading("Haz una pregunta pública", size="2", margin_bottom="1rem"),

        # 1. Input del título
        rx.input(
            placeholder="Título de la pregunta",
            value=QuestionsState.title,
            on_change=QuestionsState.setTitle,
            width="63vw",
            margin_bottom="0.5rem",
        ),

        # 2. Textarea del cuerpo
        rx.text_area(
            placeholder="Cuerpo de la pregunta",
            value=QuestionsState.body,
            on_change=QuestionsState.setBody,
            width="63vw",
            height="200px",
            margin_bottom="0.5rem",
        ),

        # 3. Input de etiquetas
        rx.input(
            placeholder="Etiquetas (separadas por comas)",
            value=QuestionsState.tags_input,
            on_change=QuestionsState.setTagsInput,
            width="40vw",
            margin_bottom="1rem",
        ),

        # 4. Botón Publicar
        rx.button(
            "Publicar",
            on_click=QuestionsState.publish_question,
            width="20vw",
            height="48px",
            border_radius="8px",
        ),

        spacing="4",
        padding="2rem",
        bg=rx.color_mode_cond(light="white", dark="gray.800"),
        border_radius="12px",
    )