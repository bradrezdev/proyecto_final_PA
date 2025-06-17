from project.connect_db import supabase
import reflex as rx

class State(rx.State):
    async def handle_signup(self, form_data: dict):
        username = form_data.get("username")
        email = form_data.get("email")
        password = form_data.get("password")
        confirm_password = form_data.get("confirm_password")

        if not username or not email or not password or not confirm_password:
            return rx.window_alert("Por favor, llena todos los campos.")

        if password != confirm_password:
            return rx.window_alert("Las contraseñas no coinciden.")

        #1. Registrar con Supabase Auth
        result = supabase.auth.sign_up({
            "email": email,
            "password": password
        })

        if result.get("error"):
            return rx.windows_alert(f"Error: {result['error']['message']}")
        
        user_id = result["data"]["user"]["id"]

        # 3. Crear user_profile
        supabase.table("user_profile").insert({
            "user_id": user_id,
            "username": username,
            "total_stars": 0
        }).execute()

        return rx.redirect("/login")