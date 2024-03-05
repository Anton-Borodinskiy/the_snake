from random import choice, randint, randrange

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
SPEED = 1

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()

# Функция обработки действий пользователя
def handle_keys(game_object):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT

# Тут опишите все классы игры.
class GameObject():
    def __init__(self,position=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2),body_color=None):
        self.position = position
        self.body_color = body_color
    def draw(self):
        pass
class Snake(GameObject):
    # Метод draw класса Snake
    def __init__(self):
        self.positions = [(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)]
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = SNAKE_COLOR

    # Метод обновления направления после нажатия на кнопку
    def update_direction(self):
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None
    def move(self):
        if self.next_direction:
            direction = self.next_direction
        else:
            direction = self.direction
        if RIGHT == direction or LEFT == direction:
            self.positions.insert(0,(self.positions[0][0]+GRID_SIZE if RIGHT == direction else self.positions[0][0]-GRID_SIZE,self.positions[0][1]))
        else:
            self.positions.insert(0,(self.positions[0][0], self.positions[0][1]-GRID_SIZE if UP == direction else self.positions[0][1]+GRID_SIZE))
        self.last = self.positions.pop()
    def draw(self, surface):
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
                (self.last[0], self.last[1]),
                (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)

    @property
    def get_head_position(self):
        return self.positions[0]

class Apple(GameObject):
    # Метод draw класса Apple
    def __init__(self,body_color):
        self.position = self.randomize_position
        self.body_color = body_color

    @property
    def randomize_position(self):
        return (randrange(0,SCREEN_WIDTH-GRID_SIZE,GRID_SIZE), randrange(0,SCREEN_HEIGHT-GRID_SIZE,GRID_SIZE))
    def draw(self, surface):
        rect = pygame.Rect(
            (self.position[0], self.position[1]),
            (GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)

def main():
    # Тут нужно создать экземпляры классов.
    apple = Apple(body_color=APPLE_COLOR)
    snake = Snake()
    apple.draw(screen)
    while True:
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        snake.draw(screen)
        clock.tick(SPEED)
        pygame.display.update()
        if snake.get_head_position == apple.position:
            apple.position = apple.randomize_position
            apple.draw(screen)
    pygame.quit()

if __name__ == '__main__':
    main()








#     # Затирание последнего сегмента



