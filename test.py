import pygame
from sys import exit
from os import path
from random import randint, choice

pygame.init()
FPS = 60
SIZE = WIDTH, HEIGHT = 800, 540
TIME = 3000
SCORE = 0
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
standard_speed = 3
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
        self.run_away_flag = False
        self.vx = randint(-5, 5)
        self.vy = randint(1, 5)

        self.rect = pygame.Rect(pos_x, pos_y, self.length, self.length)
        if self.vx >= 0:
            self.image = self.bug_states['right_move']
        elif self.vx < 0:
            self.image = self.bug_states['left_move']

    def cut_image(self):
        x = pos_bugs_in_image[self.color]
        for y in range(count_bug_in_column_image):
            self.lst_cuts.append(bugs_image.subsurface(pygame.Rect(self.length * x, self.length * y,
                                                                   self.length, self.length)))

    def update(self, arg=None):
        if (pygame.sprite.collide_rect(self, cursor) and not self.bug_at_the_spawn_point_flag
                and arg.type == pygame.MOUSEBUTTONDOWN and self.alive_flag and not self.run_away_flag):
            self.alive_flag = False
            change_standart_speed(1)
        if self.count_of_collide_bug <= 0 and not self.run_away_flag:
            self.run_away_flag = True
            change_standart_speed(-1)
        if self.run_away_flag:
            self.image = self.bug_states['run_away']
            self.rect = self.rect.move(0, -5)
            if self.rect.y <= -self.rect.height:
                self.kill()
        elif not self.alive_flag:
            self.image = self.bug_states['dead']
            self.rect = self.rect.move(0, 5)
            if self.rect.y >= HEIGHT:
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


def change_standart_speed(number):
    global standard_speed
    if standard_speed > 2 or number >= 0:
        standard_speed += number


coeff_x = 0.9  # Чтобы баги летели не только под углом 45 градусов, но и хотя бы как-то искривленно
coeff_y = 0.75
coeff_red_bug = 1.5
coeff_pink_bug = 1.3
coeff_yellow_bug = 1
coeff_cyan_bug = 0.8
limit_speed_bugs = {'red': 23, 'pink': 18, 'yellow': 13, 'cyan': 10}  # Это нужно для того, чтобы не было ошибок,
# связанных со слишком большими числами
price_bugs = {'red': 100, 'pink': 75, 'yellow': 50, 'cyan': 25}


class RedBug(Bug):
    def __init__(self, pos_x, pos_y):
        super().__init__('red', pos_x, pos_y)
        self.vx, self.vy = (int(choice([standard_speed * coeff_red_bug, -standard_speed * coeff_red_bug]) * coeff_x),
                            -int(standard_speed * coeff_red_bug * coeff_y))
        if abs(self.vx) > limit_speed_bugs[self.color]:
            num = self.vx // abs(self.vx)  # Определить с каким знаком число
            self.vx = limit_speed_bugs[self.color] * num  # И оставить его на лимите
        if abs(self.vy) > limit_speed_bugs[self.color]:
            num = self.vy // abs(self.vy)  # Определить с каким знаком число
            self.vy = limit_speed_bugs[self.color] * num
        self.add(red_bugs_group)

    def update(self, arg=None):
        if (pygame.sprite.collide_rect(self, cursor) and not self.bug_at_the_spawn_point_flag
                and arg.type == pygame.MOUSEBUTTONDOWN and self.alive_flag and not self.run_away_flag):
            add_score(price_bugs[self.color])
        super().update(arg)


class PinkBug(Bug):
    def __init__(self, pos_x, pos_y):
        super().__init__('pink', pos_x, pos_y)
        self.vx, self.vy = (int(choice([standard_speed * coeff_pink_bug, -standard_speed * coeff_pink_bug]) * coeff_x),
                            -int(standard_speed * coeff_pink_bug * coeff_y))
        if abs(self.vx) > limit_speed_bugs[self.color]:
            num = self.vx // abs(self.vx)
            self.vx = limit_speed_bugs[self.color] * num
        if abs(self.vy) > limit_speed_bugs[self.color]:
            num = self.vy // abs(self.vy)
            self.vy = limit_speed_bugs[self.color] * num
        self.add(pink_bugs_group)

    def update(self, arg=None):
        if (pygame.sprite.collide_rect(self, cursor) and not self.bug_at_the_spawn_point_flag
                and arg.type == pygame.MOUSEBUTTONDOWN and self.alive_flag and not self.run_away_flag):
            add_score(price_bugs[self.color])
        super().update(arg)


class CyanBug(Bug):
    def __init__(self, pos_x, pos_y):
        super().__init__('cyan', pos_x, pos_y)
        self.vx, self.vy = (int(choice([standard_speed * coeff_cyan_bug, -standard_speed * coeff_cyan_bug]) * coeff_x),
                            -int(standard_speed * coeff_cyan_bug * coeff_y))
        if abs(self.vx) > limit_speed_bugs[self.color]:
            num = self.vx // abs(self.vx)
            self.vx = limit_speed_bugs[self.color] * num
        if abs(self.vy) > limit_speed_bugs[self.color]:
            num = self.vy // abs(self.vy)
            self.vy = limit_speed_bugs[self.color] * num
        self.add(cyan_bugs_group)

    def update(self, arg=None):
        if (pygame.sprite.collide_rect(self, cursor) and not self.bug_at_the_spawn_point_flag
                and arg.type == pygame.MOUSEBUTTONDOWN and self.alive_flag and not self.run_away_flag):
            add_score(price_bugs[self.color])
        super().update(arg)


class YellowBug(Bug):
    def __init__(self, pos_x, pos_y):
        super().__init__('yellow', pos_x, pos_y)
        self.vx, self.vy = (int(choice([standard_speed * coeff_yellow_bug,
                                        -standard_speed * coeff_yellow_bug]) * coeff_x),
                            -int(standard_speed * coeff_yellow_bug * coeff_y))
        if abs(self.vx) > limit_speed_bugs[self.color]:
            num = self.vx // abs(self.vx)
            self.vx = limit_speed_bugs[self.color] * num
        if abs(self.vy) > limit_speed_bugs[self.color]:
            num = self.vy // abs(self.vy)
            self.vy = limit_speed_bugs[self.color] * num
        self.add(yellow_bugs_group)

    def update(self, arg=None):
        if (pygame.sprite.collide_rect(self, cursor) and not self.bug_at_the_spawn_point_flag
                and arg.type == pygame.MOUSEBUTTONDOWN and self.alive_flag and not self.run_away_flag):
            add_score(price_bugs[self.color])
        super().update(arg)


def add_score(number):
    global SCORE
    SCORE += number


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

red_bugs_group = pygame.sprite.Group()
pink_bugs_group = pygame.sprite.Group()
cyan_bugs_group = pygame.sprite.Group()
yellow_bugs_group = pygame.sprite.Group()

spawner = Spawner()
cursor = Cursor()

color = (102, 0, 255)
green = pygame.Color('green ')


def terminate():
    pygame.quit()
    exit()


def start_game():
    screen_fixed_elements = pygame.Surface(SIZE)  # Отдельное окно, на котором нарисуются неподвижные объекты 1 раз
    screen_stop_game = pygame.Surface(SIZE)
    screen_stop_game.fill(pygame.Color(color))
    Border(0, 0, WIDTH - 1, 0)
    Border(0, HEIGHT - 1, WIDTH - 1, HEIGHT - 1)
    Border(0, 0, 0, HEIGHT - 1)
    Border(WIDTH - 1, 0, WIDTH - 1, HEIGHT - 1)
    vertical_borders_group.draw(screen_fixed_elements)
    horizontal_borders_group.draw(screen_fixed_elements)
    spawner_group.draw(screen_fixed_elements)

    font = pygame.font.Font(None, 100)
    text = font.render('STOP', True, green)
    screen_stop_game.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))

    dx, dy = randint(x + 3, screen_game.get_width() - 35), randint(y + 3, screen_game.get_height() - 35)

    bugs = [RedBug, PinkBug, CyanBug, YellowBug]
    choice(bugs)(dx, dy)

    stop_game_flag = False
    flag_set_time_spawnbugevent = True

    SPAWNBUGEVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(SPAWNBUGEVENT, TIME)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == SPAWNBUGEVENT:
                dx, dy = randint(x, screen_game.get_width() - 35), randint(y, screen_game.get_height() - 35)
                choice(bugs)(dx, dy)
            if event.type == pygame.MOUSEMOTION:
                cursor.update(event.pos)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    stop_game_flag = bool((int(stop_game_flag) + 1) % 2)
        screen_game.fill((0, 0, 0))
        screen_game.blit(screen_fixed_elements, (0, 0))
        bugs_group.draw(screen_game)
        cursor_group.draw(screen_game)
        if not stop_game_flag:
            bugs_group.update(event)
            if not flag_set_time_spawnbugevent:
                pygame.time.set_timer(SPAWNBUGEVENT, TIME)
                flag_set_time_spawnbugevent = True
        else:
            screen_game.blit(screen_stop_game, (0, 0))
            if flag_set_time_spawnbugevent:
                pygame.time.set_timer(SPAWNBUGEVENT, 0)
                flag_set_time_spawnbugevent = False
        pygame.display.flip()
        clock.tick(FPS)


start_game()
