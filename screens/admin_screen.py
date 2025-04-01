# screens/admin_screen.py
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from database import get_orders, update_order_status, add_user

class AdminScreen(Screen):
    SECRET_PIN = "2005mayexcellent"

    def on_enter(self):
        app = App.get_running_app()
        if not app.current_user or app.current_user[3] not in ["admin", "moderator"]:
            self.verify_admin()
        else:
            self.show_admin_dashboard()

    def verify_admin(self):
        layout = self.ids.admin_layout.children[0]
        layout.clear_widgets()
        pin_input = TextInput(hint_text="Enter Admin PIN", size_hint_y=None, height=50, password=True)
        submit_btn = Button(text="Verify", size_hint=(0.6, 0.25), pos_hint={"center_x": 0.5})
        submit_btn.bind(on_press=lambda x: self.check_pin(pin_input.text))
        layout.add_widget(pin_input)
        layout.add_widget(submit_btn)

    def check_pin(self, pin):
        layout = self.ids.admin_layout.children[0]
        if pin == self.SECRET_PIN:
            self.show_admin_dashboard()
        else:
            layout.add_widget(Label(text="Incorrect PIN!", size_hint_y=None, height=40))

    def show_admin_dashboard(self):
        layout = self.ids.admin_layout.children[0]
        layout.clear_widgets()
        app = App.get_running_app()
        role = app.current_user[3]

        # Admin-only: Add User
        if role == "admin":
            add_user_box = BoxLayout(orientation="horizontal", size_hint_y=None, height=60)
            name_input = TextInput(hint_text="Name", size_hint_x=0.3, height=60)
            pin_input = TextInput(hint_text="PIN", size_hint_x=0.3, height=60)
            dept_input = TextInput(hint_text="Department", size_hint_x=0.3, height=60)
            role_input = TextInput(hint_text="Role (user/moderator)", size_hint_x=0.3, height=60)
            add_btn = Button(text="Add", size_hint_x=0.1)
            add_btn.bind(on_press=lambda x: self.add_new_user(name_input.text, pin_input.text, dept_input.text, role_input.text))
            add_user_box.add_widget(name_input)
            add_user_box.add_widget(pin_input)
            add_user_box.add_widget(dept_input)
            add_user_box.add_widget(role_input)
            add_user_box.add_widget(add_btn)
            layout.add_widget(add_user_box)
            layout.add_widget(Label(text="Added users appear after refresh", size_hint_y=None, height=40))

        # Orders (both Admin and Moderator)
        orders = get_orders()
        for order_id, pamphlet, qty, questions, instructions, status, user_id in orders:
            row = BoxLayout(orientation="horizontal", size_hint_y=None, height=60)
            row.add_widget(Label(text=f"User {user_id}: {pamphlet}", size_hint_x=0.3))
            row.add_widget(Label(text=f"Qty: {qty}", size_hint_x=0.1))
            row.add_widget(Label(text=status.capitalize(), size_hint_x=0.2))
            
            if pamphlet == "Online Assignment":
                row.add_widget(Label(text="Assignment (Read-Only)", size_hint_x=0.2))
            elif status == "pending" and role in ["admin", "moderator"]:
                btn = Button(text="Mark Arrived", size_hint_x=0.2)
                btn.bind(on_press=lambda x, oid=order_id: self.update_status(oid, "arrived"))
                row.add_widget(btn)
            elif status == "arrived" and role == "admin":  # Admin-only
                btn = Button(text="Mark Received", size_hint_x=0.2)
                btn.bind(on_press=lambda x, oid=order_id: self.update_status(oid, "pamphlet received"))
                row.add_widget(btn)
            else:
                row.add_widget(Label(text="", size_hint_x=0.2))
            
            row.add_widget(Label(text=questions[:20] + "..." if questions else "", size_hint_x=0.2))
            layout.add_widget(row)

    def add_new_user(self, name, pin, dept, role):
        layout = self.ids.admin_layout.children[0]
        if role not in ["user", "moderator"]:
            layout.add_widget(Label(text="Invalid role! Use 'user' or 'moderator'", size_hint_y=None, height=40))
        else:
            add_user(name, pin, dept, role)
            self.show_admin_dashboard()

    def update_status(self, order_id, status):
        update_order_status(order_id, status)
        self.show_admin_dashboard()