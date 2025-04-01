# screens/pamphlet_screen.py
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from database import get_pamphlets, add_order, get_orders, update_order_status

class PamphletScreen(Screen):
    def on_enter(self):
        app = self.manager.get_root()
        if not app.current_user or app.current_user[3] in ["admin", "moderator"]:
            self.manager.current = "home"  # Redirect admin/moderator
            return
        
        home_screen = self.manager.get_screen("home")
        course_screen = self.manager.get_screen("course")
        department = home_screen.selected_department
        course = course_screen.selected_course
        self.update_pamphlet_list(department, course)

    def update_pamphlet_list(self, department, course):
        self.ids.pamphlet_layout.clear_widgets()
        pamphlets = get_pamphlets(department, course)
        for pamphlet_name, stock in pamphlets:
            row = BoxLayout(orientation="horizontal", size_hint_y=None, height=60)
            row.add_widget(Label(text=f"Price: 50 LD", size_hint_x=0.3))
            row.add_widget(Label(text=pamphlet_name, size_hint_x=0.4))
            order_btn = Button(text="Order", size_hint_x=0.3)
            order_btn.bind(on_press=lambda x, p=pamphlet_name: self.order_pamphlet(p))
            row.add_widget(order_btn)
            self.ids.pamphlet_layout.add_widget(row)

    def order_pamphlet(self, pamphlet_name):
        self.ids.pamphlet_layout.clear_widgets()
        confirm_label = Label(text=f"Done! Your order for '{pamphlet_name}' has been placed.", size_hint_y=None, height=50)
        ok_btn = Button(text="OK", size_hint=(0.6, 0.25), pos_hint={"center_x": 0.5})
        cancel_btn = Button(text="Cancel", size_hint=(0.6, 0.25), pos_hint={"center_x": 0.5})
        
        app = self.manager.get_root()
        user_id = app.current_user[4]
        ok_btn.bind(on_press=lambda x: self.confirm_order(user_id, pamphlet_name))
        cancel_btn.bind(on_press=self.cancel_order)
        
        self.ids.pamphlet_layout.add_widget(confirm_label)
        self.ids.pamphlet_layout.add_widget(ok_btn)
        self.ids.pamphlet_layout.add_widget(cancel_btn)

    def cancel_order(self, *args):
        self.manager.current = "course"

    def confirm_order(self, user_id, pamphlet_name):
        add_order(user_id, pamphlet_name, 1)
        self.ids.pamphlet_layout.clear_widgets()
        done_label = Label(text="Done! Press OK to go back.", size_hint_y=None, height=50)
        final_ok_btn = Button(text="OK", size_hint=(0.6, 0.25), pos_hint={"center_x": 0.5})
        final_ok_btn.bind(on_press=lambda x: self.show_pending(pamphlet_name))
        self.ids.pamphlet_layout.add_widget(done_label)
        self.ids.pamphlet_layout.add_widget(final_ok_btn)

    def show_pending(self, pamphlet_name):
        self.ids.pamphlet_layout.clear_widgets()
        pending_label = Label(text=f"Pending: {pamphlet_name}", size_hint_y=None, height=50)
        receive_btn = Button(text="Receive", size_hint=(0.6, 0.25), pos_hint={"center_x": 0.5})
        receive_btn.bind(on_press=lambda x: self.mark_received(pamphlet_name))
        self.ids.pamphlet_layout.add_widget(pending_label)
        self.ids.pamphlet_layout.add_widget(receive_btn)

    def mark_received(self, pamphlet_name):
        app = self.manager.get_root()
        user_id = app.current_user[4]
        orders = get_orders(user_id)
        for order_id, name, qty, _, _, status in orders:
            if name == pamphlet_name and status == "pending":
                update_order_status(order_id, "received")
                break
        self.manager.current = "course"