from random import randrange
from typing import Union, Type
import pygame

# Инициализация PyGame:
pygame.init()

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс для игрового объекта"""

    def __init__(self, position: tuple = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2),
                 body_color: Union[None, tuple] = None) -> None:
        self.position = position
        self.body_color = body_color

    def draw(self) -> None:
        """Пустой метод для отрисовки"""
        pass


class Snake(GameObject):
    """Класс для создания змеи"""

    def __init__(self) -> None:
        super().__init__()
        self.reset()
        self.reset_key = False

    # Метод обновления направления после нажатия на кнопку
    def update_direction(self) -> None:
        """Метод обновления направления после нажатия на кнопку"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self) -> None:
        """Метод для перемещения объекта"""
        if self.next_direction:
            direction = self.next_direction
        else:
            direction = self.direction
        if RIGHT == direction or LEFT == direction:
            position_x = (self.positions[0][0] + GRID_SIZE) % SCREEN_WIDTH \
                if RIGHT == direction \
                else (self.positions[0][0] - GRID_SIZE) % SCREEN_WIDTH

            position_y = self.positions[0][1]
            self.positions.insert(0, (position_x, position_y))
        else:
            position_x = self.positions[0][0]
            position_y = (self.positions[0][1] - GRID_SIZE) % SCREEN_HEIGHT \
                if UP == direction \
                else (self.positions[0][1] + GRID_SIZE) % SCREEN_HEIGHT
            self.positions.insert(0, (position_x, position_y))
        if self.positions[0] in self.positions[1:]:
            self.reset()

    def reset(self) -> None:
        """Метод для сброса объекта"""
        self.positions = [(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)]
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = SNAKE_COLOR
        self.last = False
        self.reset_key = True

    def draw(self, surface: Type[pygame.surface.Surface]) -> None:
        """Метод для отрисовки объекта"""
        for position in self.positions[:-1]:
            rect = (
                pygame.Rect((position[0], position[1]), (GRID_SIZE, GRID_SIZE))
            )
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, head_rect)
        pygame.draw.rect(surface, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(
                self.positions.pop(),
                (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)

    @property
    def get_head_position(self) -> tuple:
        """Атрибут для получения координаты головы змеи"""
        return self.positions[0]


class Apple(GameObject):
    """Класс для создания яблока"""

    def __init__(self) -> None:
        super().__init__()
        self.position = self.randomize_position
        self.body_color = APPLE_COLOR

    @property
    def randomize_position(self) -> tuple:
        """Атрибут для генерации случайной позиции яблока"""
        return (randrange(0, SCREEN_WIDTH - GRID_SIZE, GRID_SIZE),
                randrange(0, SCREEN_HEIGHT - GRID_SIZE, GRID_SIZE))

    def draw(self, surface: Type[pygame.surface.Surface]) -> None:
        """Метод для отрисовки объекта"""
        rect = pygame.Rect(
            (self.position[0], self.position[1]),
            (GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)


# Функция обработки действий пользователя
def handle_keys(game_object: Type[Snake]) -> None:
    """Функция для считывания нажатия клавиш"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                raise SystemExit


def main() -> None:
    """Основная функция"""
    snake = Snake()
    apple = Apple()
    apple.draw(screen)
    while True:
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        if snake.get_head_position == apple.position:
            apple.position = apple.randomize_position
            while apple.position in snake.positions:
                apple.position = apple.randomize_position
            apple.draw(screen)
            snake.last = None
        elif snake.reset_key:
            screen.fill(BOARD_BACKGROUND_COLOR)
            apple.draw(screen)
            snake.reset_key = None
        else:
            snake.last = True
        snake.draw(screen)
        clock.tick(SPEED)
        pygame.display.update()
    pygame.quit()


if __name__ == '__main__':
    main()
