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
import os
import sys

def resource_path(relative):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative)
    return os.path.join(relative)

path = resource_path('code_lvl_2_file.txt')

# Константы
TILE_SIZE = 20
WIDTH, HEIGHT = TILE_SIZE*47, TILE_SIZE*24
Window.size = (WIDTH+TILE_SIZE, HEIGHT+(TILE_SIZE*3))

# Цвета
WHITE = (1, 1, 1, 1)  # Kivy использует значения от 0 до 1 для цвета
BLACK = (0, 0, 0, 1)
RED = (1, 0, 0, 0.5)  # Цвет бонуса
PLAYING = True

class MainMenu(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.label = Label(text="PacMan", font_size='40sp')
        self.add_widget(self.label)

        self.start_button = Button(text='Старт', size_hint=(1, 0.2))
        self.start_button.bind(on_press=self.start_game)
        self.add_widget(self.start_button)

    def start_game(self, instance):
        app = App.get_running_app()
        app.root.clear_widgets()
        game = Game()
        app.root.add_widget(game)

class GameScreen(BoxLayout):
    def __init__(self, is_winner, restart_callback, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        message = "Вы выиграли!" if is_winner else "Вы проиграли!"
        color = (0, 1, 0, 1) if is_winner else (1, 0, 0, 1)
        # Создаем метку с сообщением
        self.label = Label(text=message, font_size='40sp', color=color)
        self.add_widget(self.label)

        self.restart_button = Button(text='Начать уровень заново', size_hint=(1, 0.2))
        self.restart_button.bind(on_press=restart_callback)
        self.add_widget(self.restart_button)

        self.main_menu_button = Button(text='Главное меню', size_hint=(1, 0.2))
        self.main_menu_button.bind(on_press=self.go_to_main_menu)
        self.add_widget(self.main_menu_button)

    def go_to_main_menu(self, instance):
        app = App.get_running_app()
        app.root.clear_widgets()
        main_menu = MainMenu()
        app.root.add_widget(main_menu)


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

    def __init__(self, pos, **kwargs):
        super(Ghost, self).__init__(**kwargs)
        self.size = (20, 20)  # Размер кружка
        self.pos = pos  # Начальная позиция кружка
        self.speed = 1  # Скорость движения призрака
        with self.canvas:
            Color(1, 0, 1)  # Фиолетовый цвет (RGB)
            self.ellipse = Ellipse(pos=self.pos, size=self.size)

    def move_towards(self, target_pos, walls):
        """Двигает призрака к заданной позиции (target_pos), избегая стен."""
        # Возможные направления движения
        directions = [
            Vector(1, 0),   # Вправо
            Vector(-1, 0),  # Влево
            Vector(0, 1),   # Вверх
            Vector(0, -1)   # Вниз
        ]

        # Вычисляем направление к цели
        target_direction = Vector(target_pos) - Vector(self.pos)
        target_direction = target_direction.normalize()

        # Выбираем направление, которое ближе всего к направлению на цель и не ведет в стену
        best_direction = None
        min_distance = float('inf')

        for direction in directions:
            # Пробуем двигаться в этом направлении
            new_pos = Vector(self.pos) + direction * self.speed
            if not self.collides_with_walls(new_pos, walls):
                # Вычисляем расстояние до цели при движении в этом направлении
                distance = Vector(target_pos).distance(new_pos)
                if distance < min_distance:
                    min_distance = distance
                    best_direction = direction

        # Если найдено допустимое направление, двигаемся
        if best_direction:
            self.pos = Vector(self.pos) + best_direction * self.speed
            self.ellipse.pos = self.pos  # Обновляем визуальное представление

    def collides_with_walls(self, pos, walls):
        """Проверяет, сталкивается ли призрак со стенами."""
        for coord in walls:
            xcoll = False
            ycoll = False
            if pos[0] <= 0 or pos[1] <= 0 or pos[0] >= WIDTH or pos[1] >= HEIGHT:
                xcoll = True
                ycoll = True
            if coord[0] - self.size[0] < pos[0] < coord[0] + TILE_SIZE:
                xcoll = True
            if coord[1] - self.size[1] < pos[1] < coord[1] + TILE_SIZE:
                ycoll = True
            if xcoll == True and ycoll == True:
                return True

        return False

    def check_ghost(self, pacman):
        """Проверяет столкновение с Пак-Маном."""
        xcoll = self.x < pacman.x + pacman.width and self.x + self.width > pacman.x
        ycoll = self.y < pacman.y + pacman.height and self.y + self.height > pacman.y
        return xcoll and ycoll


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
        self.level = load_level(path)
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
        self.level = load_level(path)
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
            self.count+=1
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
    clock_event = None

    def __init__(self, **kwargs):
        super(Game, self).__init__(**kwargs)
        self.level_widget = LevelWidget()  # Создаем уровень
        self.pacman = Pacman()  # Создаем объект Pacman
        self.wall_widget = Wall()
        self.bonus = Bonus()  # Создаем объект бонуса
        self.enemies = [Ghost(pos=(20,440)), Ghost(pos=(920,460))]
        self.add_widget(self.level_widget)  # Добавляем уровень в игру
        self.add_widget(self.wall_widget)
        self.count_bonus = self.bonus.count

        self.bonus_now = len(self.bonus.coordinates) - self.bonus.count
        self.bonus_label = Label(text=f"Бонусов: {self.bonus_now}", size_hint=(1, None), height=80, pos=(40, HEIGHT),
                                 color=(1, 1, 1))
        self.add_widget(self.bonus_label)
        self.add_widget(self.bonus) # Добавляем бонус на уровень
        self.bonus_win_count = len(self.bonus.coordinates)
        self.add_widget(self.pacman)  # Добавляем Пак-Мэна на уровень
        for enemy in self.enemies:
            self.add_widget(enemy)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        clock_event = Clock.schedule_interval(self.update, 1.0 / 60.0)  # Обновляем игру 60 раз в секунду

    def stop_game(self):
        if self.clock_event:
            self.clock_event.cancel()
        self.game_progress = 'off'
    def restart_game(self, instance):
        self.clear_widgets()
        game = Game()  # Создаем новый экземпляр игры
        self.parent.add_widget(game)

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
                self.bonus_label.text = f"Бонусов: {self.bonus.count}. max: {self.bonus_win_count}"
                self.add_widget(self.bonus_label)  # Столкновение с бонусом
            if self.bonus.count == self.bonus_win_count:
                self.end_game(is_winner=True)
            # Двигаем призрака к Пак-Ману, учитывая стены
            for enemy in self.enemies:
                enemy.move_towards(self.pacman.pos, self.wall_widget.coordinates)
            for enemy in self.enemies:
            # Проверяем столкновение с призраком
                if enemy.check_ghost(self.pacman):
                    self.end_game(is_winner=False)

    def end_game(self, is_winner):
        self.stop_game()
        self.remove_widget(self.level_widget)
        self.remove_widget(self.wall_widget)
        self.remove_widget(self.bonus)
        self.remove_widget(self.pacman)
        self.remove_widget(self.bonus_label)
        for enemy in self.enemies:
            self.remove_widget(enemy)
        layout = GameScreen(is_winner=is_winner, restart_callback=self.restart_game, size=(WIDTH + TILE_SIZE, HEIGHT + TILE_SIZE))
        self.add_widget(layout)

# Основной класс приложения
class PacmanApp(App):
    def build(self):
        return MainMenu()


if __name__ == '__main__':
    PacmanApp().run()
    PacmanApp().stop()