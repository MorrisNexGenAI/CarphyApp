# screens/moderator_screen.py
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from database import get_orders, update_order_status

class ModeratorScreen(Screen):
    def on_enter(self):
        app = App.get_running_app()
        if not app.current_user or app.current_user[3] != "moderator":
            self.manager.current = "home"
            return
        self.show_moderator_dashboard()

    def show_moderator_dashboard(self):
        layout = self.ids.moderator_layout.children[0]
        layout.clear_widgets()
        
        stock_btn = Button(text="Manage Stock", size_hint_y=None, height=40, background_color=(0, 0.7, 0, 1))
        stock_btn.bind(on_press=self.go_to_stock)  # Bind to method
        layout.add_widget(stock_btn)

        order_layout = self.ids.order_list.children[0]
        order_layout.clear_widgets()
        orders = get_orders()
        if not orders:
            order_layout.add_widget(Label(text="No orders", size_hint_y=None, height=40))
        for order_id, pamphlet, qty, questions, instructions, status, user_id in orders:
            self.add_order_row(order_layout, order_id, pamphlet, qty, questions, status, user_id)

    def go_to_stock(self, instance):  # Added method to handle navigation
        self.manager.current = "stock"

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