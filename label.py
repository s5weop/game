from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle, Ellipse
from kivy.properties import NumericProperty, ReferenceListProperty
from kivy.vector import Vector
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

# Константы
TILE_SIZE = 20
WIDTH, HEIGHT = TILE_SIZE*47, TILE_SIZE*24
Window.size = (WIDTH+TILE_SIZE, HEIGHT+(TILE_SIZE*3))

# Цвета
WHITE = (1, 1, 1, 1)  # Kivy использует значения от 0 до 1 для цвета
BLACK = (0, 0, 0, 1)
RED = (1, 0, 0, 0.5)  # Цвет бонуса


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


# Класс для Пак-Мэна
class Pacman(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def __init__(self, **kwargs):
        super(Pacman, self).__init__(**kwargs)
        self.size = (20, 20)  # Размер кружка
        self.pos = (20, 20)  # Начальная позиция кружка
        with self.canvas:
            Color(1, 1, 0)  # Желтый цвет (RGB)
            self.ellipse = Ellipse(pos=self.pos, size=self.size)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos
        if hasattr(self, 'ellipse'):
            self.ellipse.pos = self.pos  # Обновляем позицию кружка


class Ghost(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def __init__(self, **kwargs):
        super(Ghost, self).__init__(**kwargs)
        self.size = (20, 20)  # Размер кружка
        self.pos = (40, 440)  # Начальная позиция кружка
        with self.canvas:
            Color(1, 0, 1)  # Желтый цвет (RGB)
            self.ellipse = Ellipse(pos=self.pos, size=self.size)

    def check_ghost(self, pacman):
        xcoll = False
        ycoll = False

        if self.x - pacman.size[0] < pacman.x < self.x + TILE_SIZE:
            xcoll = True
        if self.y - pacman.size[1] < pacman.y < self.y + TILE_SIZE:
            ycoll = True
        if xcoll == True and ycoll == True:
            return True

def load_level(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        level = [line.strip() for line in file.readlines()]
    return level


# Класс для уровня
class LevelWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(size=self.update_canvas)  # Обновляем холст при изменении размера
        self.update_canvas()

    # Функция для обновления холста
    def update_canvas(self, *args):
        self.canvas.clear()  # Очищаем холст
        with self.canvas:
            Color(*WHITE)  # Устанавливаем цвет фона
            Rectangle(pos=(0, 0), size=(WIDTH, HEIGHT))


class Wall(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.level = load_level('code_lvl_0_file.txt')
        self.coordinates = []

        with self.canvas:
            for y, row in enumerate(self.level):
                for x, tile in enumerate(row):
                    if tile == '#':
                        self.coordinates.append([x*TILE_SIZE, y*TILE_SIZE])
                        Color(*BLACK)  # Устанавливаем цвет стен
                        Rectangle(pos=(x * TILE_SIZE, y * TILE_SIZE), size=(TILE_SIZE, TILE_SIZE))
        print(self.coordinates)

    def check_boundaries(self, pacman):
        for coord in self.coordinates:
            xcoll = False
            ycoll = False
            if pacman.x <= 0 or pacman.y <= 0 or pacman.x >= WIDTH or pacman.y >= HEIGHT:
                xcoll = True
                ycoll = True
            if coord[0] - pacman.size[0] < pacman.x < coord[0] + TILE_SIZE:
                xcoll = True
            if coord[1] - pacman.size[1] < pacman.y < coord[1] + TILE_SIZE:
                ycoll = True
            if xcoll == True and ycoll == True:
                if pacman.velocity[0] > 0:
                    pacman.x = coord[0] - pacman.size[0]
                elif pacman.velocity[0] < 0:
                    pacman.x = coord[0] + TILE_SIZE
                if pacman.velocity[1] > 0:
                    pacman.y = coord[1] - pacman.size[1]
                elif pacman.velocity[1] < 0:
                    pacman.y = coord[1] + TILE_SIZE


class Bonus(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.level = load_level('code_lvl_0_file.txt')
        self.coordinates = []
        self.count = 0

        for y, row in enumerate(self.level):
            for x, tile in enumerate(row):
                if tile == '.':
                    self.coordinates.append([x * TILE_SIZE + int(TILE_SIZE / 4), y * TILE_SIZE + int(TILE_SIZE / 4)])
        self.print_bonuses()

    def check_bonus(self, pacman):
        for coord in self.coordinates:
            xcoll = False
            ycoll = False
            if coord[0] - pacman.size[0] < pacman.x < coord[0] + TILE_SIZE/2:
                xcoll = True
            if coord[1] - pacman.size[1] < pacman.y < coord[1] + TILE_SIZE/2:
                ycoll = True
            if xcoll == True and ycoll == True:
                self.del_bonus([coord[0], coord[1]])
                return True

    def del_bonus(self, bonuscoll):
        if bonuscoll in self.coordinates:
            self.coordinates.remove(bonuscoll)
            print('удалено', bonuscoll)
            self.count +=1
        self.print_bonuses()

    def print_bonuses(self):
        self.canvas.clear()
        with self.canvas:
            for coord in self.coordinates:
                Color(*RED)  # Устанавливаем цвет
                self.ellipse = Ellipse(pos=(coord[0], coord[1]), size=(int(TILE_SIZE / 2), int(TILE_SIZE / 2)))


# Класс для игры
class Game(Widget):
    game_progress = 'on'

    def __init__(self, **kwargs):
        super(Game, self).__init__(**kwargs)
        self.level_widget = LevelWidget()  # Создаем уровень
        self.pacman = Pacman()  # Создаем объект Pacman
        self.wall_widget = Wall()
        self.bonus = Bonus()  # Создаем объект бонуса
        self.ghost = Ghost()
        self.count_bonus = self.bonus.count
        
        self.bonus_now = len(self.bonus.coordinates) - self.bonus.count
        self.bonus_label = Label(text=f"Бонусов: {self.bonus_now}", size_hint=(1, None), height=80, pos=(20, HEIGHT), color=(1,1,1))
        self.add_widget(self.bonus_label)

        self.add_widget(self.level_widget)  # Добавляем уровень в игру
        self.add_widget(self.wall_widget)
        self.add_widget(self.bonus) # Добавляем бонус на уровень
        self.bonus_win_count = len(self.bonus.coordinates)
        self.add_widget(self.pacman)  # Добавляем Пак-Мэна на уровень
        self.add_widget(self.ghost)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        Clock.schedule_interval(self.update, 1.0 / 60.0)  # Обновляем игру 60 раз в секунду

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'up':
            self.pacman.velocity = (0, 2)
        elif keycode[1] == 'down':
            self.pacman.velocity = (0, -2)
        elif keycode[1] == 'left':
            self.pacman.velocity = (-2, 0)
        elif keycode[1] == 'right':
            self.pacman.velocity = (2, 0)
        return True  # Указываем, что событие обработано

    def update(self, dt):
        if self.game_progress == 'on':
            self.pacman.move()  # Двигаем Пак-Мэна
            self.wall_widget.check_boundaries(self.pacman)  # Проверяем границы для Пак-Мэна
            if self.bonus.check_bonus(self.pacman):
                self.remove_widget(self.bonus_label)
                self.bonus_now = len(self.bonus.coordinates) - self.bonus.count
                self.bonus_label.text = f"Бонусов: {self.bonus.count}"
                self.add_widget(self.bonus_label)
            if self.bonus.count == self.bonus_win_count:
                self.game_progress = 'win'
            ghostcoll = self.ghost.check_ghost(self.pacman) # Столкновение с врагом
            if ghostcoll:
                self.game_progress = 'lost'
        else:
            if self.game_progress == 'lost':
                self.remove_widget(self.level_widget)
                self.remove_widget(self.wall_widget)
                self.remove_widget(self.bonus)
                self.remove_widget(self.pacman)
                self.remove_widget(self.ghost)
                self.remove_widget(self.bonus_label)
                layout = GameScreen(is_winner=False, size=(WIDTH+TILE_SIZE, HEIGHT+TILE_SIZE))
                self.add_widget(layout)
            else:
                self.remove_widget(self.level_widget)
                self.remove_widget(self.wall_widget)
                self.remove_widget(self.bonus)
                self.remove_widget(self.pacman)
                self.remove_widget(self.ghost)
                self.remove_widget(self.bonus_label)
                layout = GameScreen(is_winner=True, size=(WIDTH+TILE_SIZE, HEIGHT+TILE_SIZE))
                self.add_widget(layout)


# Основной класс приложения
class PacmanApp(App):
    def build(self):
        game = Game()
        return game


if __name__ == '__main__':
    PacmanApp().run()
