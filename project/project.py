"""Proyecto Final | Programación Avanzada | index"""

import reflex as rx
from .pages.logged_index import logged_index
from .pages.signup import signup
from .pages.login import login
from .theme import Custom_theme
from .state import SearchState
from .state import SearchUIState
from .state import QuestionsState



def project() -> rx.Component:
    # Contenedor principal
    return rx.vstack(
        
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
                    # Propiedades @icon_button del botón Búsqueda
                    border_radius="100px",
                    width="48px",
                    height="48px",
                    margin_right="10px",
                ),
                # Propiedades @vstack del botón Búsqueda
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

                # Botón Registrarse
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

                # Botón Iniciar sesión
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
                    
                    # Propiedades @link del botón Iniciar sesión
                    margin_left="10px",
                    href="/login",
                ),
                
            # Propiedades contenedor botones Búsqueda, Registro e Inicio de sesión
            width="18vw",
            ),

        # Propiedades @Header
        justify="between",
        padding="3%",
        width="100%",
        ),

        # Contenedor títulos | Últimas preguntas + Top Developers
        rx.flex(

            rx.box(
                rx.heading("Última preguntas"),
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

        # Contenedor Main | Preguntas + Top Developers
        rx.hstack(
            
            # Contenedor vstak de preguntas
            rx.vstack(

                    # Contiene título, texto de la pregunta, etc. envuelto en un contenedor
                    rx.foreach(
                        QuestionsState.questions,
                        lambda question: rx.flex(
                            
                            # Título y hora de creación de la pregunta.
                            rx.hstack(
                                rx.heading(
                                    question["title"],
                                    size="5",
                                ),
                                rx.moment(
                                    question["created_at"], from_now=True,
                                    size="1",
                                ),
                                justify="between",
                            ),
                            rx.text(
                                question.body[:200] + "..."
                            ),
                            # Aquí podrías agregar etiquetas y usuario si lo tienes relacionado
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
                    
                # Propiedades vstack de los contenedores de preguntas
                width="63vw",
                spacing="4",
            ),

            # Contenedor de los contenedores de los Top Developers
            rx.flex(
                
                # Contiene todos los elementos del Developer (imagen, nombre, título, estrellas)
                rx.flex(
                    
                    # Contendor de la imagen del Developer
                    rx.box(
                        
                        # Propiedades box de imagen
                        height="56px",
                        width="56px",
                        border_radius="100px",
                        bg="#FFFFFF",
                    ),

                    # Contenedor de cada Desarrollador
                    rx.flex(

                        rx.text(
                            "[Nombre de Desarrollador]",
                            size="4",
                        ),

                        rx.text(
                            "[Título de Desarrollador]",
                            size="2",
                        ),
                        # Propiedades flex de nombre + título
                        direction="column",
                    ),
                    # Propiedades flex de imagen + nombre + título
                    bg=rx.color_mode_cond(
                        light=Custom_theme().light_colors()["background"],
                        dark=Custom_theme().dark_colors()["background"]
                    ),
                    border_radius="20px",
                    spacing="3",
                    padding="20px",
                ),

                rx.flex(
                    
                    # Contendor de la imagen del Developer
                    rx.box(
                        
                        # Propiedades box de imagen
                        height="56px",
                        width="56px",
                        border_radius="100px",
                        bg="#FFFFFF",
                    ),

                    # Contenedor de cada Desarrollador
                    rx.flex(

                        rx.text(
                            "[Nombre de Desarrollador]",
                            size="4",
                        ),

                        rx.text(
                            "[Título de Desarrollador]",
                            size="2",
                        ),
                        # Propiedades flex de nombre + título
                        direction="column",
                    ),
                    bg="#979797",
                    border_radius="20px",
                    spacing="3",
                    padding="20px",
                ),

                rx.flex(
                    
                    # Contendor de la imagen del Developer
                    rx.box(
                        
                        # Propiedades box de imagen
                        height="56px",
                        width="56px",
                        border_radius="100px",
                        bg="#FFFFFF",
                    ),

                    # Contenedor de cada Desarrollador
                    rx.flex(

                        rx.text(
                            "[Nombre de Desarrollador]",
                            size="4",
                        ),

                        rx.text(
                            "[Título de Desarrollador]",
                            size="2",
                        ),
                        # Propiedades flex de nombre + título
                        direction="column",
                    ),
                    bg="#979797",
                    border_radius="20px",
                    spacing="3",
                    padding="20px",
                ),

                rx.flex(
                    
                    # Contendor de la imagen del Developer
                    rx.box(
                        
                        # Propiedades box de imagen
                        height="56px",
                        width="56px",
                        border_radius="100px",
                        bg="#FFFFFF",
                    ),

                    # Contenedor de cada Desarrollador
                    rx.flex(

                        rx.text(
                            "[Nombre de Desarrollador]",
                            size="4",
                        ),

                        rx.text(
                            "[Título de Desarrollador]",
                            size="2",
                        ),
                        # Propiedades flex de nombre + título
                        direction="column",
                    ),
                    bg="#979797",
                    border_radius="20px",
                    spacing="3",
                    padding="20px",
                ),

                rx.flex(
                    
                    # Contendor de la imagen del Developer
                    rx.box(
                        
                        # Propiedades box de imagen
                        height="56px",
                        width="56px",
                        border_radius="100px",
                        bg="#FFFFFF",
                    ),

                    # Contenedor de cada Desarrollador
                    rx.flex(

                        rx.text(
                            "[Nombre de Desarrollador]",
                            size="4",
                        ),

                        rx.text(
                            "[Título de Desarrollador]",
                            size="2",
                        ),
                        # Propiedades flex de nombre + título
                        direction="column",
                    ),
                    bg="#979797",
                    border_radius="20px",
                    spacing="3",
                    padding="20px",
                ),

                # Propiedades de @Contenedor de los contenedores de los Top Developers
                direction="column",
                spacing="4",
                width="27vw",
            ),
        
        # Propiedades @Contenedor Main | Preguntas + Top Developers
        justify="between",
        padding_left="4%",
        padding_right="4%",
        width="100%",
        ),

        # Propiedades contenedor principal vstack
        height="100vh",
        max_width="100%",
        width="100%",
    )


app = rx.App(theme=rx.theme(
    light=Custom_theme().light_colors(),
    dark=Custom_theme().dark_colors(),
    appearance="inherit",
))
app.add_page(project, title="Página de inicio", route="/", on_load=QuestionsState.load_questions)
app.add_page(logged_index, title="Página de inicio", route="/dashboard")
app.add_page(login, title="Iniciar sesión", route="/login")
app.add_page(signup, title="Crear nueva cuenta", route="/sign_up")