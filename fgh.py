from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.graphics import Color, Ellipse
from kivy.properties import NumericProperty, ReferenceListProperty
from kivy.vector import Vector

class Pacman(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def __init__(self, **kwargs):
        super(Pacman, self).__init__(**kwargs)
        self.size = (50, 50)  # Размер кружка
        self.pos = (100, 100)  # Начальная позиция кружка
        with self.canvas:
            Color(1, 1, 0)  # Желтый цвет (RGB)
            self.ellipse = Ellipse(pos=self.pos, size=self.size)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos
        if hasattr(self, 'ellipse'):  # Проверяем, существует ли атрибут ellipse
            self.ellipse.pos = self.pos  # Обновляем позицию кружка
        else:
            print("Ошибка: атрибут 'ellipse' не найден!")

class Game(Widget):
    def __init__(self, **kwargs):
        super(Game, self).__init__(**kwargs)
        self.pacman = Pacman()  # Создаем объект Pacman
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self.add_widget(self.pacman)
        Clock.schedule_interval(self.update, 1.0 / 60.0)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'up':
            self.pacman.velocity = (0, 3)
        elif keycode[1] == 'down':
            self.pacman.velocity = (0, -3)
        elif keycode[1] == 'left':
            self.pacman.velocity = (-3, 0)
        elif keycode[1] == 'right':
            self.pacman.velocity = (3, 0)
        return True

    def update(self, dt):
        self.pacman.move()

class PacmanApp(App):
    def build(self):
        game = Game()
        Window.size = (800, 600)  # Установите размер окна
        return game

if __name__ == '__main__':
    PacmanApp().run()
