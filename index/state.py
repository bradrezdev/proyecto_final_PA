''' state.py '''

class State():
    """The app state."""
    pass

class Login():
    email: str = ""
    password: str = ""

    def setEmail(self, input_email):
        self.email = input_email

    def setPassword(self, input_password):
        self.password = input_password
