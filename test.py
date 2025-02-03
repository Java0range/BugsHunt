import pygame
from sys import exit
from os import path
from random import randint, choice

FPS = 60
SIZE = WIDTH, HEIGHT = 800, 540
screen_game = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()


def load_image(name, colorkey=None):  # Удобная замена функции pygame.image.load()
    fullname = path.join('data', name)
    if not path.isfile(fullname):
        print(f"Файла {name} не существует")
        exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


spawn_area = x, y = 0, 405
count_bug_in_column_image = 4
colors = ['red', 'pink', 'cyan', 'yellow']
pos_bugs_in_image = {'red': 0, 'pink': 1, 'cyan': 2, 'yellow': 3}
bugs_image = load_image('bugs.png')
spawner_image = load_image('game_background.png')


class Bug(pygame.sprite.Sprite):
    def __init__(self, color, pos_x, pos_y):
        super().__init__(bugs_group, all_sprites)
        self.vx = None
        self.vy = None
        self.length = 32.5  # ширина и высота бага
        self.color = color
        self.lst_cuts = []
        self.cut_image()
        self.bug_states = {'run_away': self.lst_cuts[0],
                           'dead': self.lst_cuts[1],
                           'left_move': self.lst_cuts[2],
                           'right_move': self.lst_cuts[3]}

        self.count_of_collide_bug = 3
        self.bug_at_the_spawn_point_flag = True
        self.alive_flag = True
        self.vx = randint(-5, 5)
        self.vy = randint(1, 5)

        self.rect = pygame.Rect(pos_x, pos_y, self.length, self.length)
        if self.vx >= 0:
            self.image = self.bug_states['right_move']
        elif self.vx < 0:
            self.image = self.bug_states['left_move']
        print(self.lst_cuts)

    def cut_image(self):
        x = pos_bugs_in_image[self.color]
        for y in range(count_bug_in_column_image):
            self.lst_cuts.append(bugs_image.subsurface(pygame.Rect(self.length * x, self.length * y,
                                                                   self.length, self.length)))

    def update(self, arg=None):
        if (pygame.sprite.collide_rect(self, cursor) and not self.bug_at_the_spawn_point_flag
                and arg.type == pygame.MOUSEBUTTONDOWN):
            self.alive_flag = False
        if self.count_of_collide_bug <= 0:
            self.image = self.bug_states['run_away']
            self.rect = self.rect.move(0, -5)
            if self.rect.y < -self.rect.height:
                self.kill()
        elif not self.alive_flag:
            self.image = self.bug_states['dead']
            self.rect = self.rect.move(0, 5)
            if self.rect.y == self.rect.height:
                self.kill()
        else:
            self.rect = self.rect.move(self.vx, self.vy)
            if not self.bug_at_the_spawn_point_flag:
                if pygame.sprite.spritecollideany(self, vertical_borders_group):
                    self.vx = -self.vx
                    self.count_of_collide_bug -= 1
                if pygame.sprite.spritecollideany(self, horizontal_borders_group):
                    self.vy = -self.vy
                    self.count_of_collide_bug -= 1
                if pygame.sprite.collide_mask(self, spawner):
                    self.vy = -self.vy
                    self.count_of_collide_bug -= 1
            elif self.bug_at_the_spawn_point_flag:
                if pygame.sprite.spritecollideany(self, vertical_borders_group):
                    self.vx = -self.vx
                if pygame.sprite.spritecollideany(self, horizontal_borders_group):
                    self.vy = -self.vy
                if not pygame.sprite.collide_mask(self, spawner):
                    self.bug_at_the_spawn_point_flag = False
            if self.vx >= 0:
                self.image = self.bug_states['right_move']
            elif self.vx < 0:
                self.image = self.bug_states['left_move']


class Border(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2:
            self.add(vertical_borders_group)
            self.image = pygame.Surface((1, y2 - y1))
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        elif y1 == y2:
            self.add(horizontal_borders_group)
            self.image = pygame.Surface((x2 - x1, 1))
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


class Spawner(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(spawner_group, all_sprites)
        self.image = spawner_image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)


class Cursor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(cursor_group, all_sprites)
        self.image = pygame.Surface((0, 0))
        self.rect = pygame.Rect(0, 0, 1, 1)

    def update(self, pos):
        self.rect.x = pos[0]
        self.rect.y = pos[1]


all_sprites = pygame.sprite.Group()
bugs_group = pygame.sprite.Group()
horizontal_borders_group = pygame.sprite.Group()
vertical_borders_group = pygame.sprite.Group()
spawner_group = pygame.sprite.Group()
cursor_group = pygame.sprite.Group()

spawner = Spawner()
cursor = Cursor()


def terminate():
    pygame.quit()
    exit()


def start_game():
    screen_fixed_elements = pygame.Surface(SIZE)  # Отдельное окно, на котором нарисуются неподвижные объекты 1 раз
    Border(0, 0, WIDTH - 1, 0)
    Border(0, HEIGHT - 1, WIDTH - 1, HEIGHT - 1)
    Border(0, 0, 0, HEIGHT - 1)
    Border(WIDTH - 1, 0, WIDTH - 1, HEIGHT - 1)
    vertical_borders_group.draw(screen_fixed_elements)
    horizontal_borders_group.draw(screen_fixed_elements)
    spawner_group.draw(screen_fixed_elements)

    Bug(choice(colors), randint(x, screen_game.get_width() - 35), randint(y, screen_game.get_height() - 35))

    SPAWNBUGEVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(SPAWNBUGEVENT, 5000)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == SPAWNBUGEVENT:
                Bug(choice(colors), randint(x, screen_game.get_width() - 35), randint(y, screen_game.get_height() - 35))
            if event.type == pygame.MOUSEMOTION:
                cursor.update(event.pos)
        screen_game.fill((0, 0, 0))
        screen_game.blit(screen_fixed_elements, (0, 0))
        bugs_group.draw(screen_game)
        cursor_group.draw(screen_game)
        bugs_group.update(event)
        pygame.display.flip()
        clock.tick(FPS)


start_game()
