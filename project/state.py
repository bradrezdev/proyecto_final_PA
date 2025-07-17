"""Proyecto Final | Programación Avanzada | state"""

import reflex as rx
import bcrypt
import pytz
import jwt
import os
import datetime
from dotenv import load_dotenv
from sqlmodel import select
from .models.users import Users
from .models.questions import Questions
from .models.answers import Answers


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
    is_logged: bool = True

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

                    return rx.redirect("/", replace=True)
                else:
                    print("Correo electrónico no encontrado o contraseña incorrecta.")
                    return rx.redirect("/login", replace=True)

        except Exception as e:
            print(f"Error al iniciar sesión: {e}")
            return rx.redirect("/login", replace=True)

    @rx.event
    def check_login(self):
        """Verifica si el usuario ya está logueado y redirige si es necesario"""
        if self.auth_token:
            self.is_logged = False

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
            }

    profile_data: dict = {}
    edit_username: str = ""
    edit_email: str = ""

    @rx.event
    def load_profile(self):
        """Carga el detalle del perfil según la URL."""
        user_id = self.router.page.params.get("user_id")
        if not user_id:
            self.profile_data = {}
            return

        with rx.session() as session:
            user = session.exec(select(Users).where(Users.user_id == int(user_id))).first()
            if user:
                # Guardamos los datos que queremos mostrar/editar
                self.profile_data = {
                    "user_id": user.user_id,
                    "username": user.username,
                    "email": user.email,
                }
                # Cuando entras a tu propio perfil, precarga inputs
                logged_id = self.logged_user_data.get("user_id")
                if str(logged_id) == str(user.user_id):
                    self.edit_username = user.username
                    self.edit_email = user.email
            else:
                self.profile_data = {}

    @rx.event
    def set_edit_username(self, value):
        self.edit_username = value

    @rx.event
    def set_edit_email(self, value):
        self.edit_email = value

    @rx.event
    def update_profile(self):
        """Actualiza el perfil SOLO si es el usuario propio."""
        user_id = self.logged_user_data.get("user_id")
        # Solo puedes actualizar tu propio perfil
        if not user_id or str(user_id) != str(self.profile_data.get("user_id")):
            return rx.redirect("/login", replace=True)

        with rx.session() as session:
            user = session.exec(select(Users).where(Users.user_id == user_id)).first()
            if user:
                user.username = self.edit_username or user.username
                user.email = self.edit_email or user.email
                session.add(user)
                session.commit()
                # Refresca los datos globales y de perfil
                self.load_logged_user()
                self.load_profile()
                return rx.redirect(f"/profile/{user_id}", replace=True)
            
    @rx.event
    def logout(self):
        """Cierra sesión y limpia el token."""
        self.auth_token = ""
        self.logged_user_data = {}
        return rx.redirect("/login", replace=True)

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

    # ==========================
    # --- Estado general de preguntas y formulario ---
    # ==========================
    # Pregunta nueva (formulario)
    title: str = ""
    body: str = ""
    
    # Estado de carga y lista de preguntas
    is_loading: bool = False
    questions: list[Questions] = []

    # ==========================
    # --- Estado de detalle de pregunta seleccionada ---
    # ==========================
    selected_question_id: int | None = None  # Cambiar question_id por selected_question_id
    question: Questions | None = None        # Objeto pregunta seleccionada
    question_username: str = ""       # Agregar campo separado para username
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
    def set_answer_body(self, body: str):
        """Actualiza el cuerpo de la respuesta a publicar."""
        self.answer_body = body

    # ==========================
    # --- Publicar nueva pregunta ---
    # ==========================
    @rx.event
    def publish_question(self, user_id: int):

        print(f"[DEBUG] user_id (argument): {user_id}")

        if user_id is None or str(user_id).lower() in ["none", "null", ""]:
            print(f"[ERROR] user_id inválido: {user_id}. Redirigiendo a login.")
            return rx.redirect("/login", replace=True)

        """
        Guarda una nueva pregunta con sus tags, limpia el formulario y redirige al dashboard.
        """
        with rx.session() as session:
            # 1. Crear la pregunta
            new_question = Questions(
                title=self.title,
                body=self.body,
                user_id=user_id,
            )
            session.add(new_question)
            session.commit()
            print(f"Pregunta publicada: {new_question.title}")

            # 2. Obtiene el ID de la pregunta recién creada
            new_question_id = new_question.question_id

            # 4. Limpiar campos y redirigir
            self.title = ""
            self.body = ""
            return rx.redirect(f"/question/{new_question_id}", replace=True)

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
    # --- Cargar todas las preguntas que hizo el usuario ---
    # ==========================
    @rx.event
    def load_user_questions(self, user_id: int):
        """Carga todas las preguntas que hizo un usuario específico."""
        self.is_loading = True
        with rx.session() as session:
            results = session.exec(
                select(Questions).where(Questions.user_id == user_id)
            ).all()
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

    search_term: str = ""
    @rx.event
    def set_search_term(self, value: str):
        self.search_term = value
        self.search_questions(value)

    # ==========================
    # --- Cargar detalle de pregunta ---
    # ==========================
    @rx.event
    def load_question_detail(self):
        """Carga el detalle de la pregunta cuyo ID viene en la URL."""
        question_id = self.router.page.params.get("question_id")
        if question_id:
            self.load_question(int(question_id))

    # ==========================
    # --- Cargar preguntas ---
    # ==========================
    question_user: dict = {}
    answers_user: list[dict] = []
    
    @rx.event
    def load_question(self, question_id: int):
        self.selected_question_id = question_id
        with rx.session() as session:
            # Carga la pregunta y su usuario
            q = session.exec(select(Questions).where(Questions.question_id == question_id)).first()
            if q:
                self.question = q
                # Usuario que hizo la pregunta
                user = session.exec(select(Users).where(Users.user_id == q.user_id)).first()
                self.question_user = {
                    "user_id": user.user_id,
                    "username": user.username,
                    "email": user.email,
                } if user else {}

            # Carga respuestas y usuarios de cada respuesta
            answers = session.exec(select(Answers).where(Answers.question_id == question_id)).all()
            self.answers = list(answers)
            # Aquí el truco: armar la lista de usuarios de respuestas
            self.answers_user = []
            for answer in answers:
                ans_user = session.exec(select(Users).where(Users.user_id == answer.user_id)).first()
                self.answers_user.append({
                    "user_id": ans_user.user_id if ans_user else None,
                    "username": ans_user.username if ans_user else "Desconocido",
                    "email": ans_user.email if ans_user else "",
                })

    # ==========================
    # --- Publicar respuesta ---
    # ==========================
    @rx.event
    def post_answer(self, user_id: int):
        print("[DEBUG] Entrando a post_answer()")
        print(f"[DEBUG] answer_body: {self.answer_body}")
        print(f"[DEBUG] selected_question_id: {self.selected_question_id}")
        print(f"[DEBUG] user_id (argument): {user_id}")

        # 1. Validación de campos obligatorios
        if not self.answer_body or not self.selected_question_id:
            print("[WARN] Campos vacíos: respuesta o pregunta no seleccionada")
            return

        # 2. Validación robusta del user_id
        if user_id is None or str(user_id).lower() in ["none", "null", ""]:
            print(f"[ERROR] user_id inválido: {user_id}. Redirigiendo a login.")
            return rx.redirect("/login", replace=True)

        # 3. Intenta guardar la respuesta en la base de datos
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
                print("[DEBUG] Respuesta guardada correctamente en la base de datos")
            except Exception as e:
                print(f"[ERROR] Falló la inserción en la base de datos: {e}")
                session.rollback()
                return

        # 4. Limpia el campo y recarga respuestas
        self.answer_body = ""
        print("[DEBUG] answer_body limpiado")

        answers = session.exec(
            select(Answers).where(
                Answers.question_id == self.selected_question_id
            )
        ).all()
        print(f"[DEBUG] Se encontraron {len(answers)} respuestas tras guardar")

        for answer in answers:
            answer.display_created_at = self._format_datetime(answer.created_at)

        self.answers = list(answers)
        print("[DEBUG] self.answers actualizado")

        # 5. Actualiza la lista de usuarios de respuestas
        self.answers_user = []
        for answer in self.answers:
            ans_user = session.exec(select(Users).where(Users.user_id == answer.user_id)).first()
            self.answers_user.append({
                "user_id": ans_user.user_id if ans_user else None,
                "username": ans_user.username if ans_user else "Desconocido",
                "email": ans_user.email if ans_user else "",
            })
        print("[DEBUG] self.answers_user actualizado después de post_answer")