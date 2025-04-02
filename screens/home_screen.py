# screens/home_screen.py
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.app import App
from database import get_departments

class HomeScreen(Screen):
    def on_enter(self):
        self.update_department_list()

    def update_department_list(self):
        layout = self.ids.dept_layout.children[0]
        layout.clear_widgets()
        departments = get_departments()
        for dept in departments:
            btn = Button(
                text=dept,
                size_hint_y=None,
                height=50,
                on_press=lambda x, d=dept: self.select_department(d)
            )
            layout.add_widget(btn)
        
        app = App.get_running_app()
        if app.current_user:
            # Admin/Moderator button
            if app.current_user[3] in ["admin", "moderator"]:
                admin_btn = Button(
                    text="A",
                    size_hint=(0.1, 0.1),
                    pos_hint={"right": 1, "top": 1},
                    background_color=(0.5, 0.5, 0.5, 0.5),
                    on_press=self.go_to_admin_or_moderator  # Updated binding
                )
                self.add_widget(admin_btn)
            
            # Profile button
            profile_btn = Button(
                text="P",
                size_hint=(0.1, 0.1),
                pos_hint={"right": 0.85, "top": 1},  # Slightly left of "A"
                background_color=(0.5, 0.5, 0.5, 0.5),
                on_press=self.go_to_profile
            )
            self.add_widget(profile_btn)

    def select_department(self, department):
        self.selected_department = department
        self.manager.current = "course"

    def go_to_admin_or_moderator(self, instance):  # New method
        app = App.get_running_app()
        role = app.current_user[3]  # Role at index 3
        if role == "admin":
            self.manager.current = "admin"
        elif role == "moderator":
            self.manager.current = "moderator"

    def go_to_profile(self, *args):
        self.manager.current = "profile"