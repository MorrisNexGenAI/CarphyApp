# screens/pamphlet_screen.py
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from database import get_pamphlets, add_order, get_orders, update_order_status

class PamphletScreen(Screen):
    def on_enter(self):
        app = App.get_running_app()
        if not app.current_user or app.current_user[3] in ["admin", "moderator"]:
            self.manager.current = "home"
            return
        
        home_screen = self.manager.get_screen("home")
        course_screen = self.manager.get_screen("course")
        department = home_screen.selected_department
        course = course_screen.selected_course
        self.update_pamphlet_list(department, course)

    def update_pamphlet_list(self, department, course):
        layout = self.ids.pamphlet_layout.children[0]
        layout.clear_widgets()
        pamphlets = get_pamphlets(department, course)
        for pamphlet_name, stock in pamphlets:
            row = BoxLayout(orientation="horizontal", size_hint_y=None, height=60)
            row.add_widget(Label(text=f"Price: 50 LD", size_hint_x=0.3))
            row.add_widget(Label(text=pamphlet_name, size_hint_x=0.4))
            order_btn = Button(text="Order", size_hint_x=0.3)
            order_btn.bind(on_press=lambda x, p=pamphlet_name: self.order_pamphlet(p))
            row.add_widget(order_btn)
            layout.add_widget(row)

    def order_pamphlet(self, pamphlet_name):
        layout = self.ids.pamphlet_layout.children[0]
        layout.clear_widgets()
        
        app = App.get_running_app()
        user_id = app.current_user[4]
        role = app.current_user[3]
        add_order(user_id, pamphlet_name, 1)
        
        layout.add_widget(Label(
            text=f"Done! Your order for '{pamphlet_name}' has been placed.",
            size_hint_y=None,
            height=50
        ))
        status_btn = Button(
            text="Pending",
            size_hint=(0.6, 0.25),
            pos_hint={"center_x": 0.5},
            disabled=True,
            background_color=(0.5, 0.5, 0.5, 1)
        )
        layout.add_widget(status_btn)
        
        # Show "Check Receive" only for Users and Admins
        if role in ["user", "admin"]:
            layout.add_widget(Label(
                text="Check the 'Check Receive' button below when you receive your pamphlet.",
                size_hint_y=None,
                height=50,
                font_size=14
            ))
            receive_btn = Button(
                text="Check Receive",
                size_hint=(0.6, 0.25),
                pos_hint={"center_x": 0.5},
                background_color=(0, 0.7, 0, 1)
            )
            receive_btn.bind(on_press=lambda x: self.mark_received(pamphlet_name, status_btn))
            layout.add_widget(receive_btn)

    def mark_received(self, pamphlet_name, status_btn):
        layout = self.ids.pamphlet_layout.children[0]
        app = App.get_running_app()
        user_id = app.current_user[4]
        orders = get_orders(user_id)
        for order_id, name, qty, _, _, status in orders:
            if name == pamphlet_name and status == "pending":
                update_order_status(order_id, "pamphlet received")
                break
        
        # Update UI immediately
        status_btn.text = "Pamphlet Received"
        status_btn.background_color = (0, 1, 0, 1)  # Green for received
        for widget in layout.children[:]:  # Remove instruction and button
            if isinstance(widget, (Label, Button)) and widget != status_btn:
                layout.remove_widget(widget)
        ok_btn = Button(
            text="OK",
            size_hint=(0.6, 0.25),
            pos_hint={"center_x": 0.5},
            on_press=lambda x: self.return_to_course()
        )
        layout.add_widget(ok_btn)

    def return_to_course(self):
        self.manager.current = "course"