# screens/home_screen.py
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.label import Label  # Added for clarity, though not used here
from database import get_departments

class HomeScreen(Screen):
    def on_enter(self):
        self.update_department_list()

    def update_department_list(self):
        self.ids.dept_layout.clear_widgets()
        departments = get_departments()
        for dept in departments:
            btn = Button(
                text=dept,
                size_hint_y=None,
                height=50,
                on_press=lambda x, d=dept: self.select_department(d)
            )
            self.ids.dept_layout.add_widget(btn)
        
        # Hidden admin button (top-right corner, subtle)
        if hasattr(self.manager, "current_user") and self.manager.current_user[3] in ["admin", "moderator"]:
            admin_btn = Button(
                text="A",
                size_hint=(0.1, 0.1),
                pos_hint={"right": 1, "top": 1},
                background_color=(0.5, 0.5, 0.5, 0.5),  # Subtle gray
                on_press=self.go_to_admin  # Use a method instead of lambda
            )
            self.add_widget(admin_btn)

    def select_department(self, department):
        self.selected_department = department
        self.manager.current = "course"

    def go_to_admin(self, *args):
        self.manager.current = "admin"