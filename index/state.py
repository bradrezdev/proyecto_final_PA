"""Estado de autenticación para la aplicación"""

import reflex as rx
from supabase_client import get_supabase_client
from typing import Dict, Any, Optional

class AuthState(rx.State):
    """Estado para manejar la autenticación de usuarios"""
    
    # Estado del usuario
    user: Dict[str, Any] = {}
    is_authenticated: bool = False
    loading: bool = False
    error_message: str = ""
    success_message: str = ""
    
    # Datos del formulario de registro
    signup_name: str = ""
    signup_email: str = ""
    signup_password: str = ""
    signup_confirm_password: str = ""
    signup_terms_accepted: bool = False
    
    # Datos del formulario de login
    login_email: str = ""
    login_password: str = ""

    def clear_messages(self):
        """Limpiar mensajes de error y éxito"""
        self.error_message = ""
        self.success_message = ""

    def validate_signup_form(self) -> bool:
        """Validar formulario de registro"""
        self.clear_messages()
        
        if not self.signup_name.strip():
            self.error_message = "El nombre es requerido"
            return False
            
        if not self.signup_email.strip():
            self.error_message = "El correo electrónico es requerido"
            return False
            
        if len(self.signup_password) < 6:
            self.error_message = "La contraseña debe tener al menos 6 caracteres"
            return False
            
        if self.signup_password != self.signup_confirm_password:
            self.error_message = "Las contraseñas no coinciden"
            return False
            
        if not self.signup_terms_accepted:
            self.error_message = "Debes aceptar los términos y condiciones"
            return False
            
        return True

    async def handle_signup(self):
        """Manejar registro de usuario"""
        self.loading = True
        
        if not self.validate_signup_form():
            self.loading = False
            return
        
        try:
            supabase = get_supabase_client()
            
            # Registrar usuario con metadatos
            response = supabase.auth.sign_up({
                "email": self.signup_email,
                "password": self.signup_password,
                "options": {
                    "data": {
                        "username": self.signup_name
                    }
                }
            })
            
            if response.user:
                self.success_message = "¡Cuenta creada exitosamente! Revisa tu correo para confirmar tu cuenta."
                # Limpiar formulario
                self.signup_name = ""
                self.signup_email = ""
                self.signup_password = ""
                self.signup_confirm_password = ""
                self.signup_terms_accepted = False
            else:
                self.error_message = "Error al crear la cuenta"
                
        except Exception as e:
            self.error_message = f"Error: {str(e)}"
            
        finally:
            self.loading = False

    async def handle_login(self):
        """Manejar inicio de sesión"""
        self.loading = True
        self.clear_messages()
        
        try:
            supabase = get_supabase_client()
            
            response = supabase.auth.sign_in_with_password({
                "email": self.login_email,
                "password": self.login_password
            })
            
            if response.user:
                self.user = response.user.model_dump()
                self.is_authenticated = True
                self.success_message = "¡Inicio de sesión exitoso!"
                # Redirigir a dashboard o página principal
                return rx.redirect("/dashboard")
            else:
                self.error_message = "Credenciales incorrectas"
                
        except Exception as e:
            self.error_message = f"Error al iniciar sesión: {str(e)}"
            
        finally:
            self.loading = False

    async def handle_logout(self):
        """Manejar cierre de sesión"""
        try:
            supabase = get_supabase_client()
            supabase.auth.sign_out()
            
            # Limpiar estado
            self.user = {}
            self.is_authenticated = False
            self.clear_messages()
            
            return rx.redirect("/login")
            
        except Exception as e:
            self.error_message = f"Error al cerrar sesión: {str(e)}"

    def check_auth_status(self):
        """Verificar estado de autenticación al cargar la página"""
        try:
            supabase = get_supabase_client()
            session = supabase.auth.get_session()
            
            if session and session.user:
                self.user = session.user.model_dump()
                self.is_authenticated = True
            else:
                self.user = {}
                self.is_authenticated = False
                
        except Exception:
            self.user = {}
            self.is_authenticated = False