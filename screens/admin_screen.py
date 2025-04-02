# screens/admin_screen.py
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.dropdown import DropDown
from kivy.app import App
from kivy.clock import Clock
from database import get_orders, update_order_status, add_user, get_users, delete_user

class AdminScreen(Screen):
    SECRET_PIN = "2005mayexcellent"

    def on_enter(self):
        app = App.get_running_app()
        if not app.current_user or app.current_user[3] != "admin":
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
        if pin == self.SECRET_PIN:
            self.show_admin_dashboard()
        else:
            layout = self.ids.admin_layout.children[0]
            layout.add_widget(Label(text="Incorrect PIN!", size_hint_y=None, height=40, color=(1, 0, 0, 1)))

    def show_admin_dashboard(self):
        layout = self.ids.admin_layout.children[0]
        layout.clear_widgets()

        # Add User Form
        add_box = BoxLayout(orientation="horizontal", size_hint_y=None, height=60)
        self.name_input = TextInput(hint_text="Name", size_hint_x=0.25)
        self.pin_input = TextInput(hint_text="PIN", size_hint_x=0.25, password=True)
        self.dept_input = TextInput(hint_text="Department", size_hint_x=0.25)
        role_dropdown = DropDown()
        for role in ["user", "moderator"]:
            btn = Button(text=role, size_hint_y=None, height=40)
            btn.bind(on_release=lambda btn: self.set_role(btn.text, role_dropdown))
            role_dropdown.add_widget(btn)
        self.role_btn = Button(text="Role", size_hint_x=0.15)
        self.role_btn.bind(on_release=lambda x: role_dropdown.open(self.role_btn))
        add_btn = Button(text="Add User", size_hint_x=0.1, background_color=(0, 0.8, 0, 1))
        add_btn.bind(on_press=lambda x: self.add_new_user())
        add_box.add_widget(self.name_input)
        add_box.add_widget(self.pin_input)
        add_box.add_widget(self.dept_input)
        add_box.add_widget(self.role_btn)
        add_box.add_widget(add_btn)
        layout.add_widget(add_box)
        self.feedback_label = Label(text="", size_hint_y=None, height=40)
        layout.add_widget(self.feedback_label)

        # Users List
        user_layout = self.ids.user_list.children[0]
        user_layout.clear_widgets()
        users = get_users()
        if not users:
            user_layout.add_widget(Label(text="No users", size_hint_y=None, height=40))
        for user_id, name, dept, role in users:
            self.add_user_row(user_layout, user_id, name, dept, role)

        # Orders List
        order_layout = self.ids.order_list.children[0]
        order_layout.clear_widgets()
        orders = get_orders()
        if not orders:
            order_layout.add_widget(Label(text="No orders", size_hint_y=None, height=40))
        for order_id, pamphlet, qty, questions, instructions, status, user_id in orders:
            self.add_order_row(order_layout, order_id, pamphlet, qty, questions, status, user_id)

    def set_role(self, role, dropdown):
        self.role_btn.text = role
        dropdown.dismiss()

    def add_new_user(self):
        name = self.name_input.text
        pin = self.pin_input.text
        dept = self.dept_input.text
        role = self.role_btn.text.lower()
        if role not in ["user", "moderator"]:
            self.show_feedback("Invalid role!", (1, 0, 0, 1))
            return
        if name and pin and dept:
            user_id = add_user(name, pin, dept, role)
            user_layout = self.ids.user_list.children[0]
            self.add_user_row(user_layout, user_id, name, dept, role)
            self.name_input.text = ""
            self.pin_input.text = ""
            self.dept_input.text = ""
            self.role_btn.text = "Role"
            self.show_feedback("User added!", (0, 0.8, 0, 1))
        else:
            self.show_feedback("Fill all fields!", (1, 0, 0, 1))

    def add_user_row(self, layout, user_id, name, dept, role):
        row = BoxLayout(orientation="horizontal", size_hint_y=None, height=50)
        row.add_widget(Label(text=name, size_hint_x=0.3))
        row.add_widget(Label(text=dept, size_hint_x=0.3))
        row.add_widget(Label(text=role.capitalize(), size_hint_x=0.2))
        delete_btn = Button(text="Delete", size_hint_x=0.2, background_color=(1, 0, 0, 1))
        delete_btn.bind(on_press=lambda x: self.delete_user(user_id, row))
        row.add_widget(delete_btn)
        layout.add_widget(row)

    def delete_user(self, user_id, row):
        delete_user(user_id)
        self.ids.user_list.children[0].remove_widget(row)
        self.show_feedback("User deleted!", (0, 0.8, 0, 1))

    def add_order_row(self, layout, order_id, pamphlet, qty, questions, status, user_id):
        row = BoxLayout(orientation="horizontal", size_hint_y=None, height=50)
        row.add_widget(Label(text=f"User {user_id}", size_hint_x=0.2))
        row.add_widget(Label(text=pamphlet, size_hint_x=0.2))
        row.add_widget(Label(text=str(qty), size_hint_x=0.1))
        status_label = Label(text=status.capitalize(), size_hint_x=0.2)
        row.add_widget(status_label)
        action_box = BoxLayout(size_hint_x=0.2)
        if pamphlet != "Online Assignment" and status == "pending":
            btn = Button(text="Mark Arrived", background_color=(1, 0.8, 0, 1))
            btn.bind(on_press=lambda x: self.update_order(order_id, "arrived", status_label, action_box))
            action_box.add_widget(btn)
        elif pamphlet != "Online Assignment" and status == "arrived":
            btn = Button(text="Mark Received", background_color=(0, 0.8, 0, 1))
            btn.bind(on_press=lambda x: self.update_order(order_id, "pamphlet received", status_label, action_box))
            action_box.add_widget(btn)
        row.add_widget(action_box)
        row.add_widget(Label(text=questions[:20] + "..." if questions else "", size_hint_x=0.2))
        layout.add_widget(row)

    def update_order(self, order_id, new_status, status_label, action_box):
        update_order_status(order_id, new_status)
        status_label.text = new_status.capitalize()
        action_box.clear_widgets()
        if new_status == "arrived":
            btn = Button(text="Mark Received", background_color=(0, 0.8, 0, 1))
            btn.bind(on_press=lambda x: self.update_order(order_id, "pamphlet received", status_label, action_box))
            action_box.add_widget(btn)

    def show_feedback(self, message, color):
        self.feedback_label.text = message
        self.feedback_label.color = color
        Clock.schedule_once(lambda dt: self.clear_feedback(), 3)

    def clear_feedback(self):
        self.feedback_label.text = ""