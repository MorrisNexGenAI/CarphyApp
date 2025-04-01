# screens/signup_screen.py
from kivy.uix.screenmanager import Screen
from database import add_user

class SignupScreen(Screen):
    def submit_signup(self):
        name = self.ids.name_input.text
        pin = self.ids.pin_input.text
        dept = self.ids.dept_input.text
        
        if name and pin and dept:
            if add_user(name, pin, dept):
                self.manager.current = "login"
                self.clear_inputs()
            else:
                self.ids.status_label.text = "User creation failed!"
        else:
            self.ids.status_label.text = "Please fill all fields!"

    def clear_inputs(self):
        self.ids.name_input.text = ""
        self.ids.pin_input.text = ""
        self.ids.dept_input.text = ""
        self.ids.status_label.text = ""