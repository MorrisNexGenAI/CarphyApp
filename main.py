# main.py
import os
os.add_dll_directory(r"C:\Users\User\Desktop\Test\CarphyApp\venv\share\angle\bin")

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from screens.signup_screen import SignupScreen
from screens.login_screen import LoginScreen
from screens.home_screen import HomeScreen
from screens.course_screen import CourseScreen
from screens.pamphlet_screen import PamphletScreen
from screens.cart_screen import CartScreen
from screens.admin_screen import AdminScreen
from database import get_user

Builder.load_file("carphy.kv")

class WelcomeScreen(Screen):
    pass

class CarphyApp(App):
    current_user = None  # App-level variable

    def build(self):
        self.sm = ScreenManager()
        self.sm.add_widget(WelcomeScreen(name="welcome"))
        self.sm.add_widget(SignupScreen(name="signup"))
        self.sm.add_widget(LoginScreen(name="login"))
        self.sm.add_widget(HomeScreen(name="home"))
        self.sm.add_widget(CourseScreen(name="course"))
        self.sm.add_widget(PamphletScreen(name="pamphlet"))
        self.sm.add_widget(CartScreen(name="cart"))
        self.sm.add_widget(AdminScreen(name="admin"))

        # Load last logged-in user
        try:
            with open("last_login.txt", "r") as f:
                name, pin = f.read().strip().split(",")
                user = get_user(name, pin)
                if user:
                    self.current_user = user  # (name, pin, dept, role, id)
                    self.sm.current = "home"
                    return self.sm
        except (FileNotFoundError, ValueError):
            pass
        
        self.sm.current = "welcome"
        return self.sm

if __name__ == "__main__":
    CarphyApp().run()