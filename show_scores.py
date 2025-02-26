from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

class GameScreen(BoxLayout):
    def __init__(self, is_winner, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'

        # Определяем сообщение о победе или поражении
        if is_winner:
            message = "Вы победили!"
            color = (0, 1, 0, 1)  # Зеленый
        else:
            message = "Вы проиграли!"
            color = (1, 0, 0, 1)  # Красный

        # Создаем метку с сообщением
        self.label = Label(text=message, font_size='40sp', color=color)
        self.add_widget(self.label)

        # Кнопка для выхода из игры
        self.quit_button = Button(text='Выход', size_hint=(1, 0.2))
        self.quit_button.bind(on_press=self.quit_game)
        self.add_widget(self.quit_button)

    def quit_game(self, instance):
        App.get_running_app().stop()

class PacmanApp(App):
    def build(self):
        # Получаем ввод от пользователя
        user_input = input ("True или False:").strip().lower()
        is_winner = user_input  == 'true'  # Преобразуем ввод в булевое значение
        return GameScreen(is_winner)

if __name__ == '__main__':
    PacmanApp().run()

