# screens/profile_screen.py
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App

class ProfileScreen(Screen):
    def on_enter(self):
        self.show_profile()

    def show_profile(self):
        layout = self.ids.profile_layout.children[0]
        layout.clear_widgets()
        
        app = App.get_running_app()
        if not app.current_user:
            self.manager.current = "login"
            return
        
        # Unpack 5 values: name, pin, dept, role, user_id
        name, _, dept, role, user_id = app.current_user
        layout.add_widget(Label(
            text=f"{name}\n[size=18]{dept}[/size]",
            markup=True,
            size_hint_y=None,
            height=80,
            halign="center",
            font_size=24
        ))
        layout.add_widget(Label(
            text=f"Role: {role.capitalize()}",
            size_hint_y=None,
            height=50
        ))
        layout.add_widget(Label(
            text=f"User ID: {user_id}",
            size_hint_y=None,
            height=50
        ))
        
        logout_btn = Button(
            text="Logout",
            size_hint=(0.5, 0.2),
            pos_hint={"center_x": 0.5},
            background_color=(1, 0, 0, 1)
        )
        logout_btn.bind(on_press=self.logout)
        layout.add_widget(logout_btn)

    def logout(self, *args):
        app = App.get_running_app()
        app.current_user = None
        self.manager.current = "login"