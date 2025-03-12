from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen

class MainMenu(Screen):
    def __init__(self, **kwargs):
        super(MainMenu, self).__init__(**kwargs)

        layout = BoxLayout(orientation='vertical')
        layout.add_widget(Label(text='Главное меню', font_size=50))

        # Добавляем кнопку для выбора уровня
        button_layout = BoxLayout(size_hint_y=0.2)
        for i in range(1, 4):
            button = Button(text=f'Уровень {i}')
            button.bind(on_press=lambda instance, level=i: self.goto_level(level))
            button_layout.add_widget(button)

        layout.add_widget(button_layout)
        self.add_widget(layout)

    def goto_level(self, level):
        self.manager.current = f'level{level}'

class GameLevel(Screen):
    def __init__(self, level_number, **kwargs):
        super(GameLevel, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(Label(text=f'Уровень {level_number}', font_size=50))

        # Кнопка для возврата в главное меню
        back_button = Button(text='Назад в меню', size_hint_y=0.2)
        back_button.bind(on_press=self.back_to_menu)
        layout.add_widget(back_button)

        self.add_widget(layout)

    def back_to_menu(self, instance):
        self.manager.current = 'main'

class GameApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainMenu(name='main'))
        for i in range(1, 4):
            sm.add_widget(GameLevel(i, name=f'level{i}'))
        return sm

if __name__ == '__main__':
    GameApp().run()