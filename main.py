import pygame
import sys
from os import path
from random import randrange

WIDTH, HEIGHT = 500, 500
FPS = 50
TILES = []  # здесь хранятся все клетки в формате: экземпляр класса,
# тип(0 - пустая клетка, 1 - стена, 2 - тело змеи, 3 - яблоко), координаты


def generate_level(level):
    new_player, apple, x, y = None, None, None, None
    global TILES
    a = None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                a = Tile('empty', x, y), 0, x, y
            elif level[y][x] == '#':
                a = Tile('wall', x, y), 1
            elif level[y][x] == '@':
                a = Tile('empty', x, y), 0, x, y
                new_player = Player(x, y)
            TILES.append(a)
    apple = Apple(level, x, y)
    # вернем игрока и первое яблоко, а также размер поля в клетках
    return new_player, apple, x, y


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.pos = pos_x, pos_y
        self.body_parts = [] # координаты частей тела
        self.body_len = 1 # длина тела

    def move(self, x, y):
        self.body_parts.append(self.pos)
        self.pos = (x, y)
        self.rect = self.image.get_rect().move(
            tile_width * self.pos[0] % 500, tile_height * self.pos[1] % 500)
        while len(self.body_parts) > self.body_len:  # обновляем координаты тела змеи
            pos = self.body_parts.pop(0)
            delete(pos[0], pos[1])
            a = [Tile('empty', pos[0], pos[1]), 0, pos[0], pos[1]]
            TILES.append(a)
        for i in self.body_parts:  # строим змею
            delete(i[0], i[1])
            a = [Tile('body', i[0], i[1]), 2, i[0], i[1]]
            TILES.append(a)

    def loss(self):  # проигрыш
        end_screen(self.body_len)


class Apple:
    def __init__(self, level, width, height):
        self.level = level
        self.width = width
        self.height = height
        self.used = []

    def generate(self):  # генерация нового яблока
        new = True
        while new:
            yx = randrange(0, self.height), randrange(0, self.width)
            if yx not in self.used:
                if self.level[yx[0]][yx[1]] == '.':
                    for i in TILES:
                        if i[1] == 0:
                            if i[2] == yx[1] and i[3] == yx[0]:
                                self.used.append(yx)
                                delete(yx[1], yx[0])
                                a = [Tile('apple', yx[1], yx[0]), 3, yx[1], yx[0]]
                                TILES.append(a)
                                new = False
        self.used = []


def delete(x, y):  # чистит клетку
    global TILES
    for i in TILES:
        if i[1] != 1:
            if i[2] == x and i[3] == y:
                i[0].kill()


def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def load_image(name, colorkey=None):
    fullname = path.join('data', name)
    # если файл не существует, то выходим
    if not path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()

    image = pygame.image.load(fullname)

    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def terminate():  # завершение работы
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["SSSLITHER", "",
                  "Правила:",
                  "Избегай препятствия на своём пути",
                  "и собери как можно больше яблок"]

    fon = pygame.transform.scale(load_image('fon.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('yellow'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


def end_screen(score):
    intro_text = ["GAME OVER", "", "",
                  f"        X {score - 1}"]

    fon = pygame.transform.scale(load_image('fon.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('yellow'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 180
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                terminate()
        pygame.display.flip()
        clock.tick(FPS)


# main
pygame.init()
size = WIDTH, HEIGHT
screen = pygame.display.set_mode(size)
pygame.display.set_caption('ssslither')
clock = pygame.time.Clock()
start_screen()
# возврат из заставки
# группы спрайтов
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
# задали изображение спрайтов
tile_images = {
    'apple': load_image('apple.png'),
    'wall': load_image('wall.png'),
    'body': load_image('hero.png'),
    'empty': load_image('bg.png')
}
player_image = load_image('head.png')
tile_width = tile_height = 50
level_map = load_level("map.map")
player, apple, level_x, level_y = generate_level(level_map)
apple.generate()
all_sprites.draw(screen)
pygame.display.flip()
# игровой цикл

AUTOMOVE = pygame.USEREVENT + 1  # event автоматического хода
running = True
frame = 0  # счётчик до следующего хода
new_apple = 0  # счётчик до нового яблока
last_move = None  # последнее направление (0-3 по часовой стрелке)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN or event.type == AUTOMOVE:
            if event.type == AUTOMOVE:
                event.key = None
            frame = 0
            new_apple += 1
            if new_apple == 10:
                apple.generate()
                new_apple = 0
            if event.key == pygame.K_UP or (last_move == 0 and event.type == AUTOMOVE):
                player.body_parts.append(player.pos)
                player.move(player.pos[0], (player.pos[1] - 1) % level_y)
                last_move = 0
                if any(player.rect.colliderect(x.rect) and x.image == tile_images["wall"] for x in tiles_group)\
                        or any(player.rect.colliderect(x.rect) and x.image == tile_images["body"] for x in tiles_group):
                    player.loss()
                elif any(player.rect.colliderect(x.rect) and x.image == tile_images["apple"] for x in tiles_group):
                    player.body_len += 1
                    player.body_parts.append(player.pos)
                    delete(player.pos[0], player.pos[1])
                    a = [Tile('empty', player.pos[0], player.pos[1]), 0, player.pos[0], player.pos[1]]
                    TILES.append(a)
                    apple.generate()
            elif event.key == pygame.K_DOWN or (last_move == 1 and event.type == AUTOMOVE):
                player.body_parts.append(player.pos)
                player.move(player.pos[0], (player.pos[1] + 1) % level_y)
                last_move = 1
                if any(player.rect.colliderect(x.rect) and x.image == tile_images["wall"] for x in tiles_group) \
                        or any(player.rect.colliderect(x.rect) and x.image == tile_images["body"] for x in tiles_group):
                    player.loss()
                elif any(player.rect.colliderect(x.rect) and x.image == tile_images["apple"] for x in tiles_group):
                    player.body_len += 1
                    player.body_parts.append(player.pos)
                    delete(player.pos[0], player.pos[1])
                    a = [Tile('empty', player.pos[0], player.pos[1]), 0, player.pos[0], player.pos[1]]
                    TILES.append(a)
                    apple.generate()
            elif event.key == pygame.K_LEFT or (last_move == 2 and event.type == AUTOMOVE):
                player.body_parts.append(player.pos)
                player.move((player.pos[0] - 1) % level_x, player.pos[1])
                last_move = 2
                if any(player.rect.colliderect(x.rect) and x.image == tile_images["wall"] for x in tiles_group) \
                        or any(player.rect.colliderect(x.rect) and x.image == tile_images["body"] for x in tiles_group):
                    player.loss()
                elif any(player.rect.colliderect(x.rect) and x.image == tile_images["apple"] for x in tiles_group):
                    player.body_len += 1
                    player.body_parts.append(player.pos)
                    delete(player.pos[0], player.pos[1])
                    a = [Tile('empty', player.pos[0], player.pos[1]), 0, player.pos[0], player.pos[1]]
                    TILES.append(a)
                    apple.generate()
            elif event.key == pygame.K_RIGHT or (last_move == 3 and event.type == AUTOMOVE):
                player.body_parts.append(player.pos)
                player.move((player.pos[0] + 1) % level_x, player.pos[1])
                last_move = 3
                if any(player.rect.colliderect(x.rect) and x.image == tile_images["wall"] for x in tiles_group) \
                        or any(player.rect.colliderect(x.rect) and x.image == tile_images["body"] for x in tiles_group):
                    player.loss()
                elif any(player.rect.colliderect(x.rect) and x.image == tile_images["apple"] for x in tiles_group):
                    player.body_len += 1
                    player.body_parts.append(player.pos)
                    delete(player.pos[0], player.pos[1])
                    a = [Tile('empty', player.pos[0], player.pos[1]), 0, player.pos[0], player.pos[1]]
                    TILES.append(a)
                    apple.generate()
    screen.fill(pygame.Color(64, 64, 64))
    all_sprites.draw(screen)
    player_group.draw(screen)
    frame += 1
    if frame == 40:
        pygame.event.post(pygame.event.Event(AUTOMOVE))  # совершает ход раз в 40 кадров
    clock.tick(FPS)
    pygame.display.flip()
pygame.quit()
