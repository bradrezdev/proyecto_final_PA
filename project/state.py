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
    """Estado base de la aplicación."""
    pass


# ===========================
# --- Registro de usuario ---
# ===========================
class Signup(rx.State):
    """Maneja el registro de nuevos usuarios."""
    
    # --- Propiedades del estado ---
    username: str = ""
    email: str = ""
    password: str = ""
    confirm_password: str = ""

    # --- Setters ---
    @rx.event
    def setUsername(self, input_username: str):
        self.username = input_username

    @rx.event
    def setEmail(self, input_email: str):
        self.email = input_email

    @rx.event
    def setPassword(self, input_password: str):
        self.password = input_password

    @rx.event
    def setConfirmPassword(self, input_confirm_password: str):
        self.confirm_password = input_confirm_password

    # --- Métodos privados ---
    def _search_user(self) -> Users | None:
        """Busca si existe un usuario con el email proporcionado."""
        with rx.session() as session:
            return session.exec(
                select(Users).where(Users.email == self.email)
            ).first()

    # --- Métodos públicos ---
    @rx.event
    def signup_user(self):
        """Registra un nuevo usuario después de validaciones."""
        # Validaciones
        if self.confirm_password != self.password:
            print("Las contraseñas no coinciden.")
            return
            
        if self._search_user():
            print("El usuario ya existe.")
            return

        # Crear nuevo usuario
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


# ===========================
# --- Autenticación ---
# ===========================
class Login(rx.State):
    """Maneja la autenticación y sesión de usuarios."""
    
    # --- Propiedades del estado ---
    # Formulario de login
    username: str = ""
    email: str = ""
    password: str = ""
    
    # Sesión
    auth_token: str = rx.Cookie(name="auth_token", secure=False, same_site="lax")
    logged_user_data: dict = {}
    is_logged: bool = False
    
    # Perfil de usuario
    profile_data: dict = {}
    edit_username: str = ""
    edit_email: str = ""

    # --- Setters ---
    @rx.event
    def setEmail(self, input_email: str):
        self.email = input_email

    @rx.event
    def setPassword(self, input_password: str):
        self.password = input_password

    @rx.event
    def set_edit_username(self, value: str):
        self.edit_username = value

    @rx.event
    def set_edit_email(self, value: str):
        self.edit_email = value

    # --- Métodos privados ---
    def _create_jwt_token(self, user: Users) -> str:
        """Crea un token JWT para el usuario."""
        load_dotenv()
        jwt_secret_key = os.environ.get("JWT_SECRET_KEY")
        
        login_token = {
            "id": user.user_id,
            "username": user.username,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
        }
        
        token = jwt.encode(login_token, jwt_secret_key, algorithm="HS256")
        
        if isinstance(token, bytes):
            token = token.decode()
            
        return token

    def _decode_jwt_token(self, token: str) -> dict | None:
        """Decodifica un token JWT y retorna el payload."""
        if not token or "." not in token:
            return None

        try:
            return jwt.decode(
                token,
                os.environ["JWT_SECRET_KEY"],
                algorithms=["HS256"],
            )
        except jwt.ExpiredSignatureError:
            self.auth_token = ""
            return None
        except Exception:
            return None

    # --- Métodos de autenticación ---
    @rx.event
    def login_user(self):
        """Autentica al usuario y crea la sesión."""
        try:
            with rx.session() as session:
                user = session.exec(
                    select(Users).where(Users.email == self.email)
                ).first()

                if user and bcrypt.checkpw(self.password.encode(), user.password.encode()):
                    self.auth_token = self._create_jwt_token(user)
                    return rx.redirect("/", replace=True)
                else:
                    print("Correo electrónico no encontrado o contraseña incorrecta.")
                    return rx.redirect("/login", replace=True)

        except Exception as e:
            print(f"Error al iniciar sesión: {e}")
            return rx.redirect("/login", replace=True)

    @rx.event
    def load_logged_user(self):
        """Carga los datos del usuario logueado desde el JWT."""
        payload = self._decode_jwt_token(self.auth_token)
        if not payload:
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

    @rx.event
    def check_login(self):
        """Verifica si el usuario ya está logueado."""
        if self.auth_token:
            # Verificar si el token es válido (no expirado)
            payload = self._decode_jwt_token(self.auth_token)
            if payload:
                self.is_logged = True
            else:
                # Token inválido/expirado, limpiar sesión
                self.auth_token = ""
                self.logged_user_data = {}
                self.is_logged = False
        else:
            self.is_logged = False

    @rx.event
    def logout(self):
        """Cierra la sesión del usuario."""
        self.auth_token = ""
        self.logged_user_data = {}
        self.is_logged = False
        return rx.redirect("/login", replace=True)

    # --- Métodos de perfil ---
    @rx.event
    def load_profile(self):
        """Carga el perfil de usuario según la URL."""
        user_id = self.router.page.params.get("user_id")
        if not user_id:
            self.profile_data = {}
            return

        with rx.session() as session:
            user = session.exec(
                select(Users).where(Users.user_id == int(user_id))
            ).first()
            
            if user:
                self.profile_data = {
                    "user_id": user.user_id,
                    "username": user.username,
                    "email": user.email,
                    "created_at": user.created_at.strftime("%d-%m-%Y"),
                }
                
                # Precargar inputs si es el propio perfil
                logged_id = self.logged_user_data.get("user_id")
                if str(logged_id) == str(user.user_id):
                    self.edit_username = user.username
                    self.edit_email = user.email
            else:
                self.profile_data = {}

    @rx.event
    def update_profile(self):
        """Actualiza el perfil del usuario logueado."""
        user_id = self.logged_user_data.get("user_id")
        
        # Solo se puede actualizar el propio perfil
        if not user_id or str(user_id) != str(self.profile_data.get("user_id")):
            return rx.redirect("/login", replace=True)

        with rx.session() as session:
            user = session.exec(
                select(Users).where(Users.user_id == user_id)
            ).first()
            
            if user:
                user.username = self.edit_username or user.username
                user.email = self.edit_email or user.email
                session.add(user)
                session.commit()
                
                # Refrescar datos
                self.load_logged_user()
                self.load_profile()
                return rx.redirect(f"/profile/{user_id}", replace=True)


# ===========================
# --- Estados de búsqueda ---
# ===========================
class SearchUIState(rx.State):
    """Maneja la interfaz de búsqueda."""
    show_search_box: bool = False

    @rx.event
    def toggle_search_box(self):
        self.show_search_box = not self.show_search_box


class SearchState(rx.State):
    """Maneja la funcionalidad de búsqueda."""
    show_search: bool = False
    search_term: str = ""

    @rx.event
    def toggle_search(self):
        self.show_search = not self.show_search
        if not self.show_search:
            self.search_term = ""


# ===========================
# --- Gestión de preguntas ---
# ===========================
class QuestionsState(rx.State):
    """Maneja todas las operaciones relacionadas con preguntas y respuestas."""

    # --- Propiedades del estado ---
    # Formulario de nueva pregunta
    title: str = ""
    body: str = ""
    
    # Estado general
    is_loading: bool = False
    questions: list[Questions] = []

    # Detalle de pregunta seleccionada
    selected_question_id: int | None = None
    question: Questions | None = None
    question_user: dict = {}
    
    # Respuestas
    answers: list[Answers] = []
    answers_user: list[dict] = []
    answer_body: str = ""
    
    # Búsqueda
    search_term: str = ""

    # --- Métodos utilitarios ---
    def _format_datetime(self, dt):
        """Convierte un datetime a hora local CDMX."""
        import pytz, datetime
        local_tz = pytz.timezone("America/Mexico_City")
        
        if isinstance(dt, str):
            utc_dt = datetime.datetime.fromisoformat(dt)
        else:
            utc_dt = dt
            
        if utc_dt.tzinfo is None:
            utc_dt = utc_dt.replace(tzinfo=pytz.utc)
            
        return utc_dt.astimezone(local_tz)

    def _load_question_users(self, session, answers):
        """Carga los usuarios asociados a las respuestas."""
        self.answers_user = []
        for answer in answers:
            ans_user = session.exec(
                select(Users).where(Users.user_id == answer.user_id)
            ).first()
            self.answers_user.append({
                "user_id": ans_user.user_id if ans_user else None,
                "username": ans_user.username if ans_user else "Desconocido",
                "email": ans_user.email if ans_user else "",
            })

    # --- Setters ---
    @rx.event
    def setTitle(self, input_title: str):
        self.title = input_title

    @rx.event
    def setBody(self, input_body: str):
        self.body = input_body

    @rx.event
    def set_answer_body(self, body: str):
        self.answer_body = body

    @rx.event
    def set_search_term(self, value: str):
        self.search_term = value
        self.search_questions(value)

    # --- Métodos de carga de preguntas ---
    @rx.event
    def load_questions(self):
        """Carga todas las preguntas de la base de datos."""
        self.is_loading = True
        with rx.session() as session:
            results = session.exec(select(Questions)).all()
            
            # Ajustar fechas
            for question in results:
                question.created_at = self._format_datetime(question.created_at)
                
            self.questions = list(results)
            self.is_loading = False

    @rx.event
    def load_user_questions(self, user_id: int):
        """Carga todas las preguntas de un usuario específico."""
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

    @rx.event
    def load_question_detail(self):
        """Carga el detalle de la pregunta desde la URL."""
        question_id = self.router.page.params.get("question_id")
        if question_id:
            self.load_question(int(question_id))

    @rx.event
    def load_question(self, question_id: int):
        """Carga una pregunta específica con sus respuestas."""
        self.selected_question_id = question_id
        
        with rx.session() as session:
            # Cargar pregunta y usuario
            q = session.exec(
                select(Questions).where(Questions.question_id == question_id)
            ).first()
            
            if q:
                self.question = q
                
                # Usuario que hizo la pregunta
                user = session.exec(
                    select(Users).where(Users.user_id == q.user_id)
                ).first()
                self.question_user = {
                    "user_id": user.user_id,
                    "username": user.username,
                    "email": user.email,
                } if user else {}

                # Cargar respuestas
                answers = session.exec(
                    select(Answers).where(Answers.question_id == question_id)
                ).all()
                self.answers = list(answers)
                
                # Cargar usuarios de respuestas
                self._load_question_users(session, answers)

    # --- Métodos de búsqueda ---
    @rx.event
    def search_questions(self, term: str):
        """Busca preguntas que coincidan con el término."""
        with rx.session() as session:
            results = session.exec(select(Questions)).all()
            term_lower = term.lower()
            filtered = []
            
            for question in results:
                if (term_lower in question.title.lower() or 
                    term_lower in question.body.lower()):
                    question.created_at = self._format_datetime(question.created_at)
                    filtered.append(question)
                    
            self.questions = filtered

    # --- Métodos de publicación ---
    @rx.event
    def publish_question(self, user_id: int):
        """Publica una nueva pregunta."""
        # Validaciones
        if user_id is None or str(user_id).lower() in ["none", "null", ""]:
            print(f"[ERROR] user_id inválido: {user_id}")
            return rx.redirect("/login", replace=True)

        with rx.session() as session:
            # Crear la pregunta
            new_question = Questions(
                title=self.title,
                body=self.body,
                user_id=user_id,
            )
            session.add(new_question)
            session.commit()
            
            new_question_id = new_question.question_id
            
            # Limpiar campos
            self.title = ""
            self.body = ""
            
            return rx.redirect(f"/question/{new_question_id}", replace=True)

    @rx.event
    def post_answer(self, user_id: int):
        """Publica una nueva respuesta."""
        # Validaciones
        if not self.answer_body or not self.selected_question_id:
            print("[WARN] Campos vacíos")
            return

        if user_id is None or str(user_id).lower() in ["none", "null", ""]:
            print(f"[ERROR] user_id inválido: {user_id}")
            return rx.redirect("/login", replace=True)

        with rx.session() as session:
            try:
                # Crear respuesta
                new_answer = Answers(
                    body=self.answer_body,
                    question_id=self.selected_question_id,
                    user_id=user_id,
                    created_at=datetime.datetime.now(),
                )
                session.add(new_answer)
                session.commit()
                
                # Limpiar campo
                self.answer_body = ""
                
                # Recargar respuestas
                answers = session.exec(
                    select(Answers).where(
                        Answers.question_id == self.selected_question_id
                    )
                ).all()
                
                # Formatear fechas
                for answer in answers:
                    answer.display_created_at = self._format_datetime(answer.created_at)
                
                self.answers = list(answers)
                
                # Actualizar usuarios de respuestas
                self._load_question_users(session, answers)
                
                print("[DEBUG] Respuesta guardada correctamente")
                
            except Exception as e:
                print(f"[ERROR] Falló la inserción: {e}")
                session.rollback()