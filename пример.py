from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

class MainMenu(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'

        # Заголовок с названием игры
        self.title_label = Label(text='PacMan', font_size='60sp', size_hint=(1, 0.3))
        self.add_widget(self.title_label)

        # Кнопка "Старт"
        self.start_button = Button(text='Старт', size_hint=(1, 0.2))
        self.start_button.bind(on_press=self.start_game)
        self.add_widget(self.start_button)

    def start_game(self, instance):
        # Переход к экрану игры
        App.get_running_app().show_game_screen()

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

        # Кнопка для выхода в главное меню
        self.quit_button = Button(text='Главное меню', size_hint=(1, 0.2))
        self.quit_button.bind(on_press=self.quit_game)
        self.add_widget(self.quit_button)

    def quit_game(self, instance):
        # Переход к главному меню
        App.get_running_app().show_main_menu()

class PacmanApp(App):
    def build(self):
        self.title = 'Главное меню'  # Устанавливаем заголовок окна
        return MainMenu()  # Показываем главное меню при запуске

    def show_game_screen(self):
        # Получаем ввод от пользователя
        user_input = input("True или False:").strip().lower()
        is_winner = user_input == 'true'  # Преобразуем ввод в булевое значение
        self.root.clear_widgets()  # Очищаем текущее содержимое
        self.root.add_widget(GameScreen(is_winner))  # Добавляем экран игры

    def show_main_menu(self):
        # Переход к главному меню
        self.root.clear_widgets()  # Очищаем текущее содержимое
        self.root.add_widget(MainMenu())  # Добавляем главное меню

if __name__ == '__main__':
    PacmanApp().run()