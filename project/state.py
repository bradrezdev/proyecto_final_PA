"""Proyecto Final | Programación Avanzada | state"""

import reflex as rx
import bcrypt
import pytz
import jwt
import os
import datetime
from dotenv import load_dotenv
from typing import List
from sqlmodel import select
from .models.users import Users
from .models.titles import Titles
from .models.tags import Tags
from .models.questions import Questions
from .models.answers import Answers
from .models.question_tag import QuestionTag


class State(rx.State):
    pass

class Signup(rx.State):
    username: str = ""
    email: str = ""
    password: str = ""
    confirm_password: str = ""

    @rx.event
    def setUsername(self, input_username):
        self.username = input_username

    @rx.event
    def setEmail(self, input_email):
        self.email = input_email

    @rx.event
    def setPassword(self, input_password):
        self.password = input_password

    @rx.event
    def setConfirmPassword(self, input_confirm_password):
        self.confirm_password = input_confirm_password

    def search_user(self):
        with rx.session() as session:
            signed_up_user = session.exec(
                select(Users).where(
                    Users.email == self.email
                )
            ).first()
        return signed_up_user

    @rx.event
    def signup_user(self):
        signed_up_user = self.search_user()

        if self.confirm_password != self.password:
            return print("Las contraseñas no coinciden.")
        elif signed_up_user:
            return print("El usuario ya existe.")
        else:
            new_user = Users.create_user(
                id=None,
                username=self.username,
                user_email=self.email,
                user_password=self.password
            )

            with rx.session() as session:
                session.add(new_user)
                session.commit()

            return rx.redirect("/login", replace=True)

class Login(rx.State):
    username: str = ""
    email: str = ""
    password: str = ""
    auth_token: str = rx.Cookie(name="auth_token", secure=False, same_site="lax")
    logged_user_data: dict = {}

    @rx.event
    def setEmail(self, input_email):
        self.email = input_email

    @rx.event
    def setPassword(self, input_password):
        self.password = input_password

    @rx.event
    def login_user(self):
        load_dotenv()
        jwt_secret_key = os.environ.get("JWT_SECRET_KEY")

        try:
            with rx.session() as session:
                user = session.exec(
                    Users.select().where(
                        Users.email == self.email,
                    )
                ).first()

                if user and bcrypt.checkpw(self.password.encode(), user.password.encode()):
                    login_token = {
                        "id": user.user_id,
                        "username": user.username,
                        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
                    }

                    token = jwt.encode(
                        login_token,
                        jwt_secret_key,
                        algorithm="HS256",
                    )

                    if isinstance(token, bytes):
                        token = token.decode()

                    self.auth_token = token

                    return rx.redirect("/dashboard", replace=True)
                else:
                    print("Correo electrónico no encontrado o contraseña incorrecta.")
                    return rx.redirect("/login", replace=True)

        except Exception as e:
            print(f"Error al iniciar sesión: {e}")
            return rx.redirect("/login", replace=True)

    @rx.event
    def load_logged_user(self):
        token = self.auth_token
        if not token or "." not in token:
            return

        try:
            payload = jwt.decode(
                token,
                os.environ["JWT_SECRET_KEY"],
                algorithms=["HS256"],
            )
        except jwt.ExpiredSignatureError:
            self.auth_token = ""
            return
        except Exception:
            return

        user_id = payload.get("id")
        with rx.session() as session:
            user = session.exec(
                select(Users).where(Users.user_id == user_id)
            ).first()

        if user:
            self.logged_user_data = {
                "user_id": user.user_id,
                "username": user.username,
                "email": user.email,
                "total_stars": user.total_stars,
                "title": user.get_title(),
            }
        
class SearchUIState(rx.State):
    show_search_box: bool = False

    @rx.event
    def toggle_search_box(self):
        self.show_search_box = not self.show_search_box

class SearchState(rx.State):
    show_search: bool = False
    search_term: str = ""

    @rx.event
    def toggle_search(self):
        self.show_search = not self.show_search
        if not self.show_search:
            self.search_term = ""

class QuestionsState(rx.State):
    current_user_id: int | None = None

    @rx.event
    def load_current_user(self):
        try:
            # Obtener el token desde la cookie (no desde client_storage)
            token = rx.Cookie(name="auth_token", secure=False, same_site="lax")
            if not token or "." not in token:
                return

            payload = jwt.decode(
                token,
                os.environ["JWT_SECRET_KEY"],
                algorithms=["HS256"],
            )
            self.current_user_id = payload.get("id")
        except jwt.ExpiredSignatureError:
            self.current_user_id = None
        except Exception as e:
            self.current_user_id = None


    # ==========================
    # --- Estado general de preguntas y formulario ---
    # ==========================
    # Pregunta nueva (formulario)
    title: str = ""
    body: str = ""
    tags_input: str = ""
    
    # Estado de carga y lista de preguntas
    is_loading: bool = False
    questions: list[Questions] = []

    # ==========================
    # --- Estado de detalle de pregunta seleccionada ---
    # ==========================
    selected_question_id: int | None = None  # Cambiar question_id por selected_question_id
    question: Questions | None = None        # Objeto pregunta seleccionada
    question_username: str = ""       # Agregar campo separado para username
    tags: list[Tags] = []             # Lista de tags de la pregunta seleccionada
    answers: list[Answers] = []       # Respuestas de la pregunta seleccionada

    # Respuesta nueva (formulario)
    answer_body: str = ""

    # ==========================
    # --- Utilidades privadas ---
    # ==========================
    def _format_datetime(self, dt):
        """Convierte un datetime (con o sin zona) a hora local CDMX."""
        import pytz, datetime
        local_tz = pytz.timezone("America/Mexico_City")
        if isinstance(dt, str):
            utc_dt = datetime.datetime.fromisoformat(dt)
        else:
            utc_dt = dt
        if utc_dt.tzinfo is None:
            utc_dt = utc_dt.replace(tzinfo=pytz.utc)
        return utc_dt.astimezone(local_tz)

    # ==========================
    # --- Setters para formularios ---
    # ==========================
    @rx.event
    def setTitle(self, input_title: str):
        """Actualiza el título de la pregunta nueva."""
        self.title = input_title

    @rx.event
    def setBody(self, input_body: str):
        """Actualiza el cuerpo de la pregunta nueva."""
        self.body = input_body

    @rx.event
    def setTagsInput(self, input_tags: str):
        """Actualiza el input de etiquetas para pregunta nueva."""
        self.tags_input = input_tags

    @rx.event
    def set_answer_body(self, body: str):
        """Actualiza el cuerpo de la respuesta a publicar."""
        self.answer_body = body

    # ==========================
    # --- Publicar nueva pregunta ---
    # ==========================
    @rx.event
    def publish_question(self):
        """Guarda una nueva pregunta con sus tags, limpia el formulario y redirige al dashboard."""
        with rx.session() as session:
            # 1. Crear la pregunta
            user_id = None  # Aquí deberías obtener el user_id del usuario logueado

            new_question = Questions(
                title=self.title,
                body=self.body,
                user_id=self.user_id,
            )
            session.add(new_question)
            session.commit()
            print(f"Pregunta publicada: {new_question.title}")

            # 2. Procesar etiquetas (tags)
            tags = [t.strip() for t in self.tags_input.split(",") if t.strip()]
            for name in tags:
                tag = session.exec(
                    select(Tags).where(Tags.tag_name == name)
                ).first()
                if not tag:
                    tag = Tags(tag_name=name)
                    session.add(tag)
                    session.commit()
                # Relacionar pregunta y etiqueta
                question_tag = QuestionTag(
                    question_id=new_question.question_id,
                    tag_id=tag.tag_id
                )
                session.add(question_tag)
            session.commit()

            # 3. Limpiar campos y redirigir
            self.title = ""
            self.body = ""
            self.tags_input = ""
            return rx.redirect("/dashboard", replace=True)

    # ==========================
    # --- Cargar todas las preguntas (lista general) ---
    # ==========================
    @rx.event
    def load_questions(self):
        """Carga todas las preguntas de la base de datos (con fechas locales)."""
        self.is_loading = True
        with rx.session() as session:
            results = session.exec(select(Questions)).all()
            # Ajustar fechas
            for question in results:
                question.created_at = self._format_datetime(question.created_at)
            self.questions = list(results)
            self.is_loading = False

    # ==========================
    # --- Buscar preguntas ---
    # ==========================
    @rx.event
    def search_questions(self, term: str):
        """Busca preguntas que coincidan con el término en título o cuerpo."""
        with rx.session() as session:
            results = session.exec(select(Questions)).all()
            term_lower = term.lower()
            filtered = []
            for question in results:
                if term_lower in question.title.lower() or term_lower in question.body.lower():
                    question.created_at = self._format_datetime(question.created_at)
                    filtered.append(question)
            self.questions = filtered

    # ==========================
    # --- Cargar detalle de pregunta (con tags y respuestas) ---
    # ==========================
# --- Cargar detalle de pregunta (sin argumento) ---
    @rx.event
    def load_question_detail(self):
        """Carga el detalle de la pregunta cuyo ID viene en la URL."""
        question_id = self.router.page.params.get("question_id")
        if question_id:
            self.load_question(int(question_id))

    # ==========================
    # --- Cargar detalle de pregunta (con tags y respuestas) ---
    # ==========================
    @rx.event
    def load_question(self, question_id: int):
        """Carga una pregunta por ID junto con sus tags y respuestas."""
        with rx.session() as session:
            q = session.exec(
                select(Questions).where(Questions.question_id == question_id)
            ).first()
            if q:
                q.created_at = self._format_datetime(q.created_at)
                # --- Buscar el username ---
                user = session.exec(select(Users).where(Users.user_id == q.user_id)).first()
                self.question_username = user.username if user else "Desconocido"
                # --- Guardar el objeto Questions directamente ---
                self.question = q
                self.selected_question_id = question_id
            else:
                self.question = None
                self.question_username = ""

            # Buscar respuestas asociadas
            answers = session.exec(
                select(Answers).where(Answers.question_id == question_id)
            ).all()
            # Ajustar fechas de respuestas si tienen fecha
            for answer in answers:
                if hasattr(answer, "created_at"):
                    answer.created_at = self._format_datetime(answer.created_at)
            self.answers = list(answers)

    # ==========================
    # --- Publicar respuesta ---
    # ==========================
    @rx.event
    def post_answer(self, user_id: int):
        print("[DEBUG] Entrando a post_answer")
        print(f"[DEBUG] answer_body: {self.answer_body}")
        print(f"[DEBUG] selected_question_id: {self.selected_question_id}")

        if not self.answer_body or not self.selected_question_id:
            print("[WARN] Campos vacíos: respuesta o pregunta no seleccionada")
            return

        print(f"[DEBUG] user_id: {user_id} (type: {type(user_id)})")

        # Validación robusta
        if user_id is None or str(user_id).lower() in ["none", "null", ""]:
            print("[ERROR] user_id es inválido. Redirigiendo a login.")
            return rx.redirect("/login", replace=True)

        with rx.session() as session:
            try:
                new_answer = Answers(
                    body=self.answer_body,
                    question_id=self.selected_question_id,
                    user_id=user_id,
                    created_at=datetime.datetime.now(),
                )
                session.add(new_answer)
                session.commit()
            except Exception as e:
                print(f"[ERROR] Falló la inserción en DB: {e}")
                session.rollback()
                return

            self.answer_body = ""

            answers = session.exec(
                select(Answers).where(
                    Answers.question_id == self.selected_question_id
                )
            ).all()

            for answer in answers:
                if hasattr(answer, "created_at"):
                    answer.created_at = self._format_datetime(answer.created_at)

            self.answers = list(answers)
            print("[DEBUG] Respuesta guardada exitosamente")

            print("[WARN] Campos vacíos: respuesta o pregunta no seleccionada")
            return

        login_data = Login.logged_user_data
        print(f"[DEBUG] login_data: {login_data}")

        try:
            user_id = login_data["user_id"]
        except Exception as e:
            print(f"[ERROR] No se pudo obtener user_id: {e}")
            return rx.redirect("/login", replace=True)

        print(f"[DEBUG] user_id: {user_id} (type: {type(user_id)})")

        # Validación robusta
        if user_id is None or str(user_id).lower() in ["none", "null", ""]:
            print("[ERROR] user_id es inválido. Redirigiendo a login.")
            return rx.redirect("/login", replace=True)

        with rx.session() as session:
            try:
                new_answer = Answers(
                    body=self.answer_body,
                    question_id=self.selected_question_id,
                    user_id=user_id,
                    created_at=datetime.datetime.now(),
                )
                session.add(new_answer)
                session.commit()
            except Exception as e:
                print(f"[ERROR] Falló la inserción en DB: {e}")
                session.rollback()
                return

            self.answer_body = ""

            answers = session.exec(
                select(Answers).where(
                    Answers.question_id == self.selected_question_id
                )
            ).all()

            for answer in answers:
                if hasattr(answer, "created_at"):
                    answer.created_at = self._format_datetime(answer.created_at)

            self.answers = list(answers)
            print("[DEBUG] Respuesta guardada exitosamente")