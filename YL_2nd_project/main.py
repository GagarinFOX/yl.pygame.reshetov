import os
import sys

import pygame

pygame.init()
pygame.key.set_repeat(200, 70)

FPS = 50
WIDTH = 600
HEIGHT = 600
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

player = None

# группы спрайтов
all_sprites = pygame.sprite.Group()  # да
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()  # игрок
wall_group = pygame.sprite.Group()  # стена
door_group = pygame.sprite.Group()  # дверь
furniture_group = pygame.sprite.Group()  # препядстве
enemy_group = pygame.sprite.Group()  # противник
STEP = 10


def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname).convert()
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["", "",
                  "",
                  "",
                  "                           ______press space______"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('pink'))
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


tile_images = {
    'wall': load_image('beton.png'),
    'door': load_image('door.png'),
    'window': load_image('betonwindow1.png'),
    'empty': load_image('flor1.png')
}
player_image = load_image('oper02.png')

tile_width = tile_height = 50


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        if tile_type == 'wall' or tile_type == 'window':
            wall_group.add(self)
        elif tile_type == 'door':
            door_group.add(self)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)

    def go(self, direction):
        if direction == 'left':
            self.rect.x -= STEP
            if pygame.sprite.spritecollideany(self, wall_group):
                self.rect.x += STEP
        elif direction == 'right':
            self.rect.x += STEP
            if pygame.sprite.spritecollideany(self, wall_group):
                self.rect.x -= STEP
            if pygame.sprite.spritecollideany(self, door_group):
                screen.fill('purple')
                generate_level(load_level('lvl2.map'))
        elif direction == 'up':
            self.rect.y -= STEP
            if pygame.sprite.spritecollideany(self, wall_group):
                self.rect.y += STEP
        elif direction == 'down':
            self.rect.y += STEP
            if pygame.sprite.spritecollideany(self, wall_group):
                self.rect.y -= STEP


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == 'w':
                Tile('window', x, y)
            elif level[y][x] == 'd':
                Tile('door', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - HEIGHT // 2)


if __name__ == '__main__':
    start_screen()
    player, level_x, level_y = generate_level(load_level('lvl.map'))
    camera = Camera()

    # running = True
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # running =False
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.go('left')
                if event.key == pygame.K_RIGHT:
                    player.go('right')
                if event.key == pygame.K_UP:
                    player.go('up')
                if event.key == pygame.K_DOWN:
                    player.go('down')
        camera.update(player)
        for sprite in all_sprites:
            camera.apply(sprite)

        screen.fill('purple')
        tiles_group.draw(screen)
        player_group.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
