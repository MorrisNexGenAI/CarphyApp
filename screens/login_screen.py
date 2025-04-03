# screens/login_screen.py
from kivy.uix.screenmanager import Screen
from kivy.app import App
from database import get_user

class LoginScreen(Screen):
    def on_enter(self):
        # Auto-fill last login if available
        try:
            with open("last_login.txt", "r") as f:
                name, pin = f.read().strip().split(",")
                self.ids.name_input.text = name
                self.ids.pin_input.text = pin
        except FileNotFoundError:
            pass

    def submit_login(self):
        name = self.ids.name_input.text.strip()
        pin = self.ids.pin_input.text.strip()
        
        if not name or not pin:
            self.ids.status_label.text = "Enter name and PIN!"
            self.ids.status_label.color = (1, 0, 0, 1)
            return
        
        user = get_user(name, pin)  # Returns (name, pin, dept, role, id) or None
        if user:
            app = App.get_running_app()
            app.current_user = user  # Store user data (name, pin, dept, role, id)
            with open("last_login.txt", "w") as f:
                f.write(f"{name},{pin}")
            self.manager.current = "home"
            self.ids.name_input.text = ""
            self.ids.pin_input.text = ""
            role = user[3]  # role is at index 3
            self.ids.status_label.text = f"Welcome, {role.capitalize()} {user[0]}!"
            self.ids.status_label.color = (0, 0.8, 0, 1)  # Green for success
        else:
            self.ids.status_label.text = "Invalid name or PIN!"
            self.ids.status_label.color = (1, 0, 0, 1)  # Red for error