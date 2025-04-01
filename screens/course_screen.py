# screens/course_screen.py
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from database import get_courses

class CourseScreen(Screen):
    def on_enter(self):
        department = self.manager.get_screen("home").selected_department
        self.update_course_list(department)

    def update_course_list(self, department):
        self.ids.course_layout.clear_widgets()
        app = self.manager.get_root()
        if not app.current_user or app.current_user[3] in ["admin", "moderator"]:
            self.ids.course_layout.add_widget(Label(
                text="Restricted for users only. Use Admin Dashboard.",
                size_hint_y=None,
                height=50
            ))
            return

        courses = get_courses(department)
        for course in courses:
            row = BoxLayout(orientation="horizontal", size_hint_y=None, height=60)
            row.add_widget(Label(text=course, size_hint_x=0.5))
            buy_btn = Button(text="Buy Pamphlet", size_hint_x=0.25)
            buy_btn.bind(on_press=lambda x, c=course: self.buy_pamphlet(c))
            row.add_widget(buy_btn)
            assign_btn = Button(text="Do Assignment", size_hint_x=0.25)
            assign_btn.bind(on_press=lambda x, c=course: self.do_assignment(c))
            row.add_widget(assign_btn)
            self.ids.course_layout.add_widget(row)

    def buy_pamphlet(self, course):
        self.selected_course = course
        self.manager.current = "pamphlet"

    def do_assignment(self, course):
        self.selected_course = course
        self.manager.current = "cart"