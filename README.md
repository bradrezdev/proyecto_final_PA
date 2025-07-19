# Proyecto Final PA

Proyecto Final de Programación Avanzada  
Aplicación web de preguntas y respuestas para estudiantes y programadores, desarrollada con [Reflex](https://reflex.dev/) y [Supabase](https://supabase.com).

---

## 🚀 Características

- Registro y autenticación de usuarios con JWT y bcrypt.
- Publicación de preguntas y respuestas.
- Perfil de usuario editable.
- Búsqueda de preguntas por tema.
- Interfaz responsiva con modo claro/oscuro.

---

## 🛠️ Instalación

1. **Clona el repositorio:**
   ```
   git clone https://github.com/bradrezdev/proyecto_final_PA.git
   cd proyecto_final_PA
   ```

2. **Crea y activa un entorno virtual (opcional pero recomendado):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Mac/Linux
   .\venv\Scripts\activate   # En Windows
   ```

3. **Instala las dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configura las variables de entorno:**
   - Edita el archivo `.env` en la carpeta `project` y coloca tu clave secreta JWT:
     ```
     JWT_SECRET_KEY=tu_clave_secreta
     ```

5. **Inicializa la base de datos:**
   - Configura el motor de base de datos en Reflex (ver `rxconfig.py`).

---

## 🏃‍♂️ Ejecución

```bash
reflex run
```

---

## 📁 Estructura del proyecto

```bash
project/
│   ├── models/         # Modelos de base de datos (Users, Questions, Answers).
│   ├── pages/          # Páginas secundarias (login, signup, profile, question, new_question).
│   ├── state.py        # Lógica y estados globales.
│   ├── theme.py        # Temas de colores.
│   ├── header_layout.py # Header y navegación.
│   ├── project.py      # Landing Page | Página principal.
│   └── .env            # Variables de entorno.
requirements.txt        # Dependencias.
README.md               # Este archivo.
LICENSE                 # Licencia MIT.
rx.config.py            # Conexión con la base de datos.
```

---

## 🧑‍💻 Contribución

1. Haz un fork del repositorio.
2. Crea una rama (`git checkout -b feature/nueva-funcionalidad`).
3. Realiza tus cambios y haz commit.
4. Envía un pull request.

---

## 📚 Tecnologías usadas

- [Reflex](https://reflex.dev/) (frontend y backend)
- [SQLModel](https://sqlmodel.tiangolo.com/) (ORM)
- [bcrypt](https://pypi.org/project/bcrypt/) (hash de contraseñas)
- [PyJWT](https://pyjwt.readthedocs.io/) (autenticación JWT)
- [pytz](https://pypi.org/project/pytz/) (zonas horarias)
- [python-dotenv](https://pypi.org/project/python-dotenv/) (variables de entorno)

---

## 📦 Dependencias

Todas las dependencias necesarias para ejecutar la aplicación están listadas en el archivo [`requirements.txt`](requirements.txt).  
Si agregas nuevas librerías, recuerda actualizar este archivo usando:

```bash
pip freeze > requirements.txt
```

Para instalar las dependencias, simplemente ejecuta:

```bash
pip install -r requirements.txt
```

---

## 📝 Licencia

Este proyecto está bajo la licencia MIT.

---

## 📬 Contacto

¿Dudas o sugerencias?  
Escríbeme a [b.nunez@hotmail.es](b.nunez@hotmail.es).