# screens/cart_screen.py
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App  # Add this import
from database import add_order, get_orders, update_order_status

class CartScreen(Screen):
    def on_enter(self):
        app = App.get_running_app()  # Fix here
        if not app.current_user or app.current_user[3] in ["admin", "moderator"]:
            self.manager.current = "home"
            return
        self.update_cart()

    def update_cart(self):
        self.ids.cart_layout.clear_widgets()
        course = self.manager.get_screen("course").selected_course
        self.ids.cart_layout.add_widget(Label(text=f"Assignment for {course} (100 LD/sheet)", size_hint_y=None, height=50))
        self.questions_input = TextInput(hint_text="Enter assignment questions", size_hint_y=None, height=100)
        self.instructions_input = TextInput(hint_text="Enter instructions", size_hint_y=None, height=100)
        submit_btn = Button(text="Submit Assignment", size_hint=(0.6, 0.25), pos_hint={"center_x": 0.5})
        submit_btn.bind(on_press=lambda x: self.submit_assignment())
        self.ids.cart_layout.add_widget(self.questions_input)
        self.ids.cart_layout.add_widget(self.instructions_input)
        self.ids.cart_layout.add_widget(submit_btn)
        self.show_pending_orders()

    def show_pending_orders(self):
        app = App.get_running_app()  # Fix here
        orders = get_orders(app.current_user[4])
        for order_id, pamphlet, qty, questions, instructions, status in orders:
            if pamphlet != "Online Assignment":
                continue
            row = BoxLayout(orientation="horizontal", size_hint_y=None, height=60)
            row.add_widget(Label(text="Assignment", size_hint_x=0.4))
            row.add_widget(Label(text=f"Qty: {qty}", size_hint_x=0.2))
            row.add_widget(Label(text=status.capitalize(), size_hint_x=0.2))
            if status == "arrived":
                btn = Button(text="Receive", size_hint_x=0.2)
                btn.bind(on_press=lambda x, oid=order_id: self.mark_received(oid))
                row.add_widget(btn)
            else:
                row.add_widget(Label(text="", size_hint_x=0.2))
            self.ids.cart_layout.add_widget(row)

    def mark_received(self, order_id):
        update_order_status(order_id, "received")
        self.update_cart()

    def submit_assignment(self):
        app = App.get_running_app()  # Fix here
        user_id = app.current_user[4]
        questions = self.questions_input.text
        instructions = self.instructions_input.text
        if questions or instructions:
            add_order(user_id, "Online Assignment", 1, questions, instructions)
        self.manager.current = "course"