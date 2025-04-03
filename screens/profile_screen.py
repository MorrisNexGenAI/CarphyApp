# screens/profile_screen.py
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.app import App
from database import get_orders

class ProfileScreen(Screen):
    def on_enter(self):
        self.update_profile()

    def update_profile(self):
        app = App.get_running_app()
        if not app.current_user:
            self.manager.current = "login"
            return
        
        # Get user details (name, pin, dept, role, id)
        name, _, dept, role, user_id = app.current_user
        
        # Clear existing layout (ScrollView's child)
        layout = self.ids.profile_layout.children[0]  # Get the BoxLayout inside ScrollView
        layout.clear_widgets()
        
        # User Info
        info_box = BoxLayout(orientation="vertical", size_hint_y=None, height=100)
        info_box.add_widget(Label(text=f"Name: {name}", font_size=20, size_hint_y=None, height=30))
        info_box.add_widget(Label(text=f"Department: {dept}", font_size=20, size_hint_y=None, height=30))
        info_box.add_widget(Label(text=f"Role: {role.capitalize()}", font_size=20, size_hint_y=None, height=30))
        layout.add_widget(info_box)
        
        # Order History
        order_list = BoxLayout(orientation="vertical", size_hint_y=None)
        order_list.bind(minimum_height=order_list.setter('height'))
        
        orders = get_orders(user_id)
        if not orders:
            order_list.add_widget(Label(text="No orders yet", size_hint_y=None, height=40))
        else:
            for order in orders:
                order_id, pamphlet_name, qty, questions, instructions, status = order
                order_row = BoxLayout(orientation="horizontal", size_hint_y=None, height=50)
                order_row.add_widget(Label(text=f"Order #{order_id}", size_hint_x=0.2))
                order_row.add_widget(Label(text=pamphlet_name, size_hint_x=0.3))
                order_row.add_widget(Label(text=f"Qty: {qty}", size_hint_x=0.15))
                order_row.add_widget(Label(text=status.capitalize(), size_hint_x=0.25))
                order_list.add_widget(order_row)
        
        layout.add_widget(order_list)