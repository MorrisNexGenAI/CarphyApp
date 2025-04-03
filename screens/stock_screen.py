# screens/stock_screen.py
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.app import App
from database import get_all_pamphlets, update_stock

class StockScreen(Screen):
    def on_enter(self):
        self.update_stock_list()

    def update_stock_list(self):
        app = App.get_running_app()
        if not app.current_user or app.current_user[3] not in ["admin", "moderator"]:
            self.manager.current = "home"
            return
        
        layout = self.ids.stock_layout.children[0]  # BoxLayout inside ScrollView
        layout.clear_widgets()
        
        pamphlets = get_all_pamphlets()
        for pamphlet_name, stock, dept, course_name in pamphlets:
            row = BoxLayout(orientation="horizontal", size_hint_y=None, height=50)
            row.add_widget(Label(text=f"{dept} - {course_name}", size_hint_x=0.3))
            row.add_widget(Label(text=pamphlet_name, size_hint_x=0.3))
            stock_input = TextInput(text=str(stock), size_hint_x=0.2, multiline=False)
            update_btn = Button(text="Update", size_hint_x=0.2, background_color=(0, 0.7, 0, 1))
            update_btn.bind(on_press=lambda btn, pn=pamphlet_name, si=stock_input: self.update_stock(pn, si.text))
            row.add_widget(stock_input)
            row.add_widget(update_btn)
            layout.add_widget(row)

    def update_stock(self, pamphlet_name, stock_text):
        try:
            stock = int(stock_text)
            if stock >= 0:
                update_stock(pamphlet_name, stock)
                self.update_stock_list()  # Refresh list
        except ValueError:
            pass  # Ignore invalid input