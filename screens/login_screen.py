# screens/login_screen.py
from kivy.uix.screenmanager import Screen
from database import get_user

class LoginScreen(Screen):
    def submit_login(self):
        name = self.ids.name_input.text
        pin = self.ids.pin_input.text
        
        user = get_user(name, pin)
        if user:
            with open("last_login.txt", "w") as f:
                f.write(f"{name},{pin}")
            app = self.manager.get_root()  # Get CarphyApp instance
            app.current_user = user  # Set app-level current_user
            self.manager.current = "home"
            self.ids.name_input.text = ""
            self.ids.pin_input.text = ""
            self.ids.status_label.text = f"Welcome back, {user[0]}!"
        else:
            self.ids.status_label.text = "Invalid name or PIN!"