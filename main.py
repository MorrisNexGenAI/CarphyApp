# main.py
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder
from screens.welcome_screen import WelcomeScreen
from screens.signup_screen import SignupScreen
from screens.login_screen import LoginScreen
from screens.home_screen import HomeScreen
from screens.course_screen import CourseScreen
from screens.pamphlet_screen import PamphletScreen
from screens.cart_screen import CartScreen
from screens.admin_screen import AdminScreen
from screens.profile_screen import ProfileScreen  # New import

Builder.load_file("carphy.kv")

class CarphyApp(App):
    def build(self):
        self.current_user = None
        sm = ScreenManager()
        sm.add_widget(WelcomeScreen(name="welcome"))
        sm.add_widget(SignupScreen(name="signup"))
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(HomeScreen(name="home"))
        sm.add_widget(CourseScreen(name="course"))
        sm.add_widget(PamphletScreen(name="pamphlet"))
        sm.add_widget(CartScreen(name="cart"))
        sm.add_widget(AdminScreen(name="admin"))
        sm.add_widget(ProfileScreen(name="profile"))  # New screen
        return sm

if __name__ == "__main__":
    CarphyApp().run()