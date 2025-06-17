"""Proyecto Final | Programación Avanzada"""

import reflex as rx
from .pages.loggedindex import loggedindex
from .pages.signup import signup
from .pages.login import login

def index() -> rx.Component:
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
                rx.icon_button("search", border_radius="100px", width="48px", height="48px", margin_right="10px",),

                # Botón Registrarse
                rx.link(
                    rx.button(
                        "Registrarse",
                        border_radius="100px",
                        width="135px",
                        height="48px",
                    ),
                    href="/signup",
                ),

                # Botón Iniciar sesión
                rx.link(
                    rx.button(
                        rx.text("Iniciar sesión",color_scheme="violet",),
                        bg="none",
                        border_radius="100px",
                        width="135px",
                        height="48px",
                        #border="5px solid amber",
                    ),
                    margin_left="10px",
                    href="/login",
                ),
                
            # Propiedades contenedor botones Búsqueda, Registro e Inicio de sesión
            width="26vw",
            ),

        # Propiedades @Header
        justify="between",
        padding="4%",
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
                    rx.flex(

                        # Contiene el título de la pregunta + hora de creación
                        rx.hstack(
                        
                            rx.heading(
                                "[Título de pregunta]",
                                size="5",

                                #Propiedades @heading del título de pregunta
                            ),

                            rx.text(

                                "Hace 38 minutos",
                                size="1",

                                # Propiedades @text de tiempo de creación
                            ),
                            
                            # Propiedades @hstack de título de pregunta + hora de creación
                            justify="between",
                        ),

                        rx.text(
                            "Lorem ipsum dolor sit amet, consectetur adipiscing elit. In dictum sit amet felis in lobortis. Sed sed ipsum arcu. Donec sit amet gravida nulla. In sodales magna erat, at scelerisque magna suscipit et. Donec eu nulla nec lorem dictum maximus eget eget orci...",
                            
                            # Propiedades @text de pregunta
                        ),

                        # Contiene las etiquetas + nombre de quien preguntó + estrellas
                        rx.hstack(
                        
                            rx.container(
                                rx.text("Python", size="2"),

                                #Propiedades @container de la etiqueta
                                bg="#A7A7A7",
                                #width="auto",
                            ),

                            rx.link(

                                "[Nombre de usuario que pregunta]",
                                size="2",

                                # Propiedades @link del usuario quien pregunta
                            ),
                            
                            # Propiedades @Contiene las etiquetas + nombre de quien preguntó + estrellas
                            #justify="between",
                        ),

                        # Propiedades @Contiene título, texto de la pregunta, etc. envuelto en un contenedor
                        bg="#E3E3E3",
                        border_radius="20px",
                        width="63vw",
                        padding="22px",
                        direction="column",
                        spacing="2",
                    ),

                    rx.flex(

                        # Contiene el título de la pregunta + hora de creación
                        rx.hstack(
                        
                            rx.heading(
                                "[Título de pregunta]",
                                size="5",

                                #Propiedades @heading del título de pregunta
                            ),

                            rx.text(

                                "Hace 38 minutos",
                                size="1",

                                # Propiedades @text de tiempo de creación
                            ),
                            
                            # Propiedades @hstack de título de pregunta + hora de creación
                            justify="between",
                        ),

                        rx.text(
                            "Lorem ipsum dolor sit amet, consectetur adipiscing elit. In dictum sit amet felis in lobortis. Sed sed ipsum arcu. Donec sit amet gravida nulla. In sodales magna erat, at scelerisque magna suscipit et. Donec eu nulla nec lorem dictum maximus eget eget orci...",
                            
                            # Propiedades @text de pregunta
                        ),

                        # Contiene las etiquetas + nombre de quien preguntó + estrellas
                        rx.hstack(
                        
                            rx.container(
                                rx.text("Python", size="2"),

                                #Propiedades @container de la etiqueta
                                bg="#A7A7A7",
                                #width="auto",
                            ),

                            rx.link(

                                "[Nombre de usuario que pregunta]",
                                size="2",

                                # Propiedades @link del usuario quien pregunta
                            ),
                            
                            # Propiedades @Contiene las etiquetas + nombre de quien preguntó + estrellas
                            #justify="between",
                        ),

                        # Propiedades @Contiene título, texto de la pregunta, etc. envuelto en un contenedor
                        bg="#E3E3E3",
                        border_radius="20px",
                        width="63vw",
                        padding="22px",
                        direction="column",
                        spacing="2",
                    ),

                    rx.flex(

                        # Contiene el título de la pregunta + hora de creación
                        rx.hstack(
                        
                            rx.heading(
                                "[Título de pregunta]",
                                size="5",

                                #Propiedades @heading del título de pregunta
                            ),

                            rx.text(

                                "Hace 38 minutos",
                                size="1",

                                # Propiedades @text de tiempo de creación
                            ),
                            
                            # Propiedades @hstack de título de pregunta + hora de creación
                            justify="between",
                        ),

                        rx.text(
                            "Lorem ipsum dolor sit amet, consectetur adipiscing elit. In dictum sit amet felis in lobortis. Sed sed ipsum arcu. Donec sit amet gravida nulla. In sodales magna erat, at scelerisque magna suscipit et. Donec eu nulla nec lorem dictum maximus eget eget orci...",
                            
                            # Propiedades @text de pregunta
                        ),

                        # Contiene las etiquetas + nombre de quien preguntó + estrellas
                        rx.hstack(
                        
                            rx.container(
                                rx.text("Python", size="2"),

                                #Propiedades @container de la etiqueta
                                bg="#A7A7A7",
                                #width="auto",
                            ),

                            rx.link(

                                "[Nombre de usuario que pregunta]",
                                size="2",

                                # Propiedades @link del usuario quien pregunta
                            ),
                            
                            # Propiedades @Contiene las etiquetas + nombre de quien preguntó + estrellas
                            #justify="between",
                        ),

                        # Propiedades @Contiene título, texto de la pregunta, etc. envuelto en un contenedor
                        bg="#E3E3E3",
                        border_radius="20px",
                        width="63vw",
                        padding="22px",
                        direction="column",
                        spacing="2",
                    ),

                    rx.flex(

                        # Contiene el título de la pregunta + hora de creación
                        rx.hstack(
                        
                            rx.heading(
                                "[Título de pregunta]",
                                size="5",

                                #Propiedades @heading del título de pregunta
                            ),

                            rx.text(

                                "Hace 38 minutos",
                                size="1",

                                # Propiedades @text de tiempo de creación
                            ),
                            
                            # Propiedades @hstack de título de pregunta + hora de creación
                            justify="between",
                        ),

                        rx.text(
                            "Lorem ipsum dolor sit amet, consectetur adipiscing elit. In dictum sit amet felis in lobortis. Sed sed ipsum arcu. Donec sit amet gravida nulla. In sodales magna erat, at scelerisque magna suscipit et. Donec eu nulla nec lorem dictum maximus eget eget orci...",
                            
                            # Propiedades @text de pregunta
                        ),

                        # Contiene las etiquetas + nombre de quien preguntó + estrellas
                        rx.hstack(
                        
                            rx.container(
                                rx.text("Python", size="2"),

                                #Propiedades @container de la etiqueta
                                bg="#A7A7A7",
                                #width="auto",
                            ),

                            rx.link(

                                "[Nombre de usuario que pregunta]",
                                size="2",

                                # Propiedades @link del usuario quien pregunta
                            ),
                            
                            # Propiedades @Contiene las etiquetas + nombre de quien preguntó + estrellas
                            #justify="between",
                        ),

                        # Propiedades @Contiene título, texto de la pregunta, etc. envuelto en un contenedor
                        bg="#E3E3E3",
                        border_radius="20px",
                        width="63vw",
                        padding="22px",
                        direction="column",
                        spacing="2",
                    ),

                    rx.flex(

                        # Contiene el título de la pregunta + hora de creación
                        rx.hstack(
                        
                            rx.heading(
                                "[Título de pregunta]",
                                size="5",

                                #Propiedades @heading del título de pregunta
                            ),

                            rx.text(

                                "Hace 38 minutos",
                                size="1",

                                # Propiedades @text de tiempo de creación
                            ),
                            
                            # Propiedades @hstack de título de pregunta + hora de creación
                            justify="between",
                        ),

                        rx.text(
                            "Lorem ipsum dolor sit amet, consectetur adipiscing elit. In dictum sit amet felis in lobortis. Sed sed ipsum arcu. Donec sit amet gravida nulla. In sodales magna erat, at scelerisque magna suscipit et. Donec eu nulla nec lorem dictum maximus eget eget orci...",
                            
                            # Propiedades @text de pregunta
                        ),

                        # Contiene las etiquetas + nombre de quien preguntó + estrellas
                        rx.hstack(
                        
                            rx.container(
                                rx.text("Python", size="2"),

                                #Propiedades @container de la etiqueta
                                bg="#A7A7A7",
                                #width="auto",
                            ),

                            rx.link(

                                "[Nombre de usuario que pregunta]",
                                size="2",

                                # Propiedades @link del usuario quien pregunta
                            ),
                            
                            # Propiedades @Contiene las etiquetas + nombre de quien preguntó + estrellas
                            #justify="between",
                        ),

                        # Propiedades @Contiene título, texto de la pregunta, etc. envuelto en un contenedor
                        bg="#E3E3E3",
                        border_radius="20px",
                        width="63vw",
                        padding="22px",
                        direction="column",
                        spacing="2",
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


app = rx.App(theme=rx.theme(accent_color="violet"))
app.add_page(index, title="Página de inicio")
app.add_page(loggedindex, title="Página de inicio", route="/logged")
app.add_page(login, title="Iniciar sesión", route="/login")
app.add_page(signup, title="Crear nueva cuenta", route="sign_up")