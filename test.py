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
        if (pygame.sprite.collide_mask(self, cursor) and not self.bug_at_the_spawn_point_flag
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
    if standard_speed > 3 or number >= 0:
        standard_speed += number


coeffs_x = [i / 100 for i in
            range(50, 100)]  # Чтобы баги летели не только под углом 45 градусов, но и хотя бы как-то искривленно
coeffs_y = [i / 100 for i in range(50, 100)]
coefficients_of_colors_bug = {'red': 1.5, 'pink': 1.3, 'yellow': 1, 'cyan': 0.8}  # Коэффициенты багов
divider = 60  # Делитель, на который делится standart_score, при подсчете очков, добавленных за попавшего бага
limit_speed_bugs = {'red': 25, 'pink': 20, 'yellow': 15, 'cyan': 10}  # Это нужно для того, чтобы не было ошибок,
# связанных со слишком большими числами
price_bugs = {'red': 100, 'pink': 75, 'yellow': 50, 'cyan': 25}  # Кол-во очков, которое пойманный баг принесет, после
# умножится на коэфициент, полученный при делении standart_score на divider


class BugColor(Bug):
    def __init__(self, color, pos_x, pos_y):
        super().__init__(color, pos_x, pos_y)
        self.points = None
        coeff_x, coeff_y = choice(coeffs_x), choice(coeffs_y)
        self.flag_of_make_return_caught_bug = False
        self.vx, self.vy = (int(choice([standard_speed * coefficients_of_colors_bug[self.color],
                                        -standard_speed * coefficients_of_colors_bug[self.color]]) * coeff_x),
                            -int(standard_speed * coefficients_of_colors_bug[self.color] * coeff_y))
        if abs(self.vx) > limit_speed_bugs[self.color]:
            num = self.vx // abs(self.vx)  # Определить с каким знаком число
            self.vx = limit_speed_bugs[self.color] * num  # И оставить его на лимите
        if abs(self.vy) > limit_speed_bugs[self.color]:
            num = self.vy // abs(self.vy)  # Определить с каким знаком число
            self.vy = limit_speed_bugs[self.color] * num
        self.add(red_bugs_group)

    def update(self, arg=None):
        if (pygame.sprite.collide_mask(self, cursor) and not self.bug_at_the_spawn_point_flag
                and arg.type == pygame.MOUSEBUTTONDOWN and self.alive_flag and not self.run_away_flag):
            self.points = int(price_bugs[self.color] * (standard_speed / divider))
            add_score(self.points)
        super().update(arg)

    def is_caught_bug(self):
        if not self.alive_flag and not self.flag_of_make_return_caught_bug:
            self.flag_of_make_return_caught_bug = True
            return self.rect.x, self.rect.y, self.points
        return False


class RedBug(BugColor):
    def __init__(self, pos_x, pos_y):
        super().__init__('red', pos_x, pos_y)


class PinkBug(BugColor):
    def __init__(self, pos_x, pos_y):
        super().__init__('pink', pos_x, pos_y)


class CyanBug(BugColor):
    def __init__(self, pos_x, pos_y):
        super().__init__('cyan', pos_x, pos_y)


class YellowBug(BugColor):
    def __init__(self, pos_x, pos_y):
        super().__init__('yellow', pos_x, pos_y)


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
        self.image = load_image('cursor.png')
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, pos):
        self.rect.x = pos[0]
        self.rect.y = pos[1]


class ScoreBug(pygame.sprite.Sprite):
    def __init__(self, x1, y1, score, image):
        super().__init__(score_of_bug_group, all_sprites)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x1
        self.rect.y = y1
        self.score = score
        self.number_time = FPS * 1  # Время, которое отображается self.number_time / FPS секунд

    def update(self):
        if self.number_time <= 0:
            self.kill()
        self.number_time -= 1


all_sprites = pygame.sprite.Group()
bugs_group = pygame.sprite.Group()
horizontal_borders_group = pygame.sprite.Group()
vertical_borders_group = pygame.sprite.Group()
spawner_group = pygame.sprite.Group()
cursor_group = pygame.sprite.Group()
score_of_bug_group = pygame.sprite.Group()

red_bugs_group = pygame.sprite.Group()
pink_bugs_group = pygame.sprite.Group()
cyan_bugs_group = pygame.sprite.Group()
yellow_bugs_group = pygame.sprite.Group()

spawner = Spawner()
cursor = Cursor()

color = (102, 0, 255)
color_score_bug_text = (250, 215, 0)
green = pygame.Color('green')
yellow = pygame.Color('yellow')


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

    length = 5  # Величина, на которую сдигается прямоугольник с двух сторон
    w = h = length * 2  # Ширина и высота прямоугольников
    height_pause = 10
    height_lmb = 150
    height_rmb = 225
    text_lmb_active = 'On'
    text_rmb_active = 'Off'

    font = pygame.font.Font(None, 100)
    font_buttons = pygame.font.Font(None, 50)
    font_score_bug = pygame.font.Font(None, 30)

    text = font.render('Pause menu', True, green)
    text_lmb = font_buttons.render(f'LMB: {text_lmb_active}', True, yellow)
    text_rmb = font_buttons.render(f'RMB: {text_rmb_active}', True, yellow)

    screen_stop_game.blit(text, (WIDTH // 2 - text.get_width() // 2, height_pause))
    screen_stop_game.blit(text_lmb, (WIDTH // 2 - text.get_width() // 4, height_lmb))
    screen_stop_game.blit(text_rmb, (WIDTH // 2 - text.get_width() // 4, height_rmb))

    maxi_width = max(map(lambda z: z.get_width(), [text_lmb, text_rmb])) + w  # Чтобы было красиво,
    # прямоугольники все выравниваются под самый длинный прямоугольник

    rect_of_text_lmb = pygame.Rect(WIDTH // 2 - text.get_width() // 4 - length, height_lmb - length,
                                   maxi_width, text_lmb.get_height() + h)
    rect_of_text_rmb = pygame.Rect(WIDTH // 2 - text.get_width() // 4 - length, height_rmb - length,
                                   maxi_width, text_rmb.get_height() + h)

    pygame.draw.rect(screen_stop_game, yellow, rect_of_text_lmb, 1)
    pygame.draw.rect(screen_stop_game, yellow, rect_of_text_rmb, 1)

    dx, dy = randint(x + 3, screen_game.get_width() - 35), randint(y + 3, screen_game.get_height() - 35)

    bugs = [RedBug, PinkBug, CyanBug, YellowBug]
    choice(bugs)(dx, dy)

    stop_game_flag = False
    flag_set_time_spawnbugevent = True

    pygame.mouse.set_visible(False)  # Погашение системного курсора
    SPAWNBUGEVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(SPAWNBUGEVENT, TIME)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == SPAWNBUGEVENT:
                dx, dy = randint(x + 3, screen_game.get_width() - 35), randint(y + 3, screen_game.get_height() - 35)
                choice(bugs)(dx, dy)
            if event.type == pygame.MOUSEMOTION:
                cursor.update(event.pos)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    stop_game_flag = bool((int(stop_game_flag) + 1) % 2)
        screen_game.fill((0, 0, 0))
        screen_game.blit(screen_fixed_elements, (0, 0))
        for bug in bugs_group:
            now = bug.is_caught_bug()
            if now:  # Либо False, либо кортеж значений координат x, y и кол-во очков, что будет True
                x1, y1, points = now
                text = font_score_bug.render(f"+{points}", True, color_score_bug_text)
                ScoreBug(x1, y1, points, text)
        bugs_group.draw(screen_game)
        score_of_bug_group.draw(screen_game)
        score_of_bug_group.update()
        if pygame.mouse.get_focused():  # Проверка на то, находится ли курсор мыши в экране игры
            cursor_group.draw(screen_game)
        if not stop_game_flag:
            if pygame.mouse.get_visible():
                pygame.mouse.set_visible(False)
            bugs_group.update(event)
            if not flag_set_time_spawnbugevent:
                pygame.time.set_timer(SPAWNBUGEVENT, TIME)
                flag_set_time_spawnbugevent = True
        else:
            if not pygame.mouse.get_visible():
                pygame.mouse.set_visible(True)  # СДЕЛАТЬ ПОСЛЕ СМЕНУ КУРСОРА У ОБЪЕКТА КЛАССА cursor
            screen_game.blit(screen_stop_game, (0, 0))
            if flag_set_time_spawnbugevent:
                pygame.time.set_timer(SPAWNBUGEVENT, 0)
                flag_set_time_spawnbugevent = False
        pygame.display.flip()
        clock.tick(FPS)


start_game()
