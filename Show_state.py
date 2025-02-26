from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup

class BonusApp(App):
    def build(self):
        self.layout = FloatLayout()

        # Метка и поле ввода для количества бонусов
        self.label = Label(text="Введите количество бонусов:", size_hint=(0.5, 0.1), pos_hint={'center_x': 0.5, 'top': 0.8})
        self.layout.add_widget(self.label)

        self.entry = TextInput(hint_text='Количество бонусов', size_hint=(0.5, 0.1), pos_hint={'center_x': 0.5, 'top': 0.7})
        self.layout.add_widget(self.entry)

        # Кнопка для подтверждения ввода и открытия окна с бонусами
        self.button = Button(text="Показать бонусы", size_hint=(0.5, 0.1), pos_hint={'center_x': 0.5, 'top': 0.5})
        self.button.bind(on_press=self.show_bonus_window)
        self.layout.add_widget(self.button)

        return self.layout

    def show_bonus_window(self, instance):
        # Получаем количество бонусов из поля ввода
        bonus_count = self.entry.text

        # Создаем новое окно для отображения бонусов
        bonus_window = Popup(title="Бонусы", content=Label(text=f"Количество бонусов: {bonus_count}", font_size=16), size_hint=(0.5, 0.5))
        bonus_window.open()

if __name__ == "__main__":
    BonusApp().run()
