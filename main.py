import pygame
from Score import load_score, save_score
from Sounds import Sounds
from sys import exit
from os import path
from random import randint, choice

# инициализация pygame
pygame.init()
FPS = 60
SIZE = WIDTH, HEIGHT = 800, 540
TIME = 3000
SCORE = 0
COUNT_LIVES = 8
screen_game = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()
text_lmb_active = True
text_rmb_active = False

# глобальные игровые переменные
running = True
main_menu = True
gameover = False

# инициализация игровых объектов
play_button = pygame.Rect(355, 290, 95, 48)
main_menu_button = pygame.Rect(300, 440, 200, 40)


# Удобная замена функции pygame.image.load()
def load_image(name, colorkey=None):
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


# фоны
menu_background_image = load_image('menu_background.png')
gameover_background_image = load_image('gameover_background.jpg')

# изображение жизней
heart_image = load_image('heart.png')

# инициализация звуков
sounds = Sounds()

# шрифты
main_menu_score_font = pygame.font.SysFont("Times New Roman", 20)
game_over_big_font = pygame.font.SysFont("Times New Roman", 26)

spawn_area = x, y = 0, 405
count_bug_in_column_image = 4
standard_speed = 3
colors = ['red', 'pink', 'cyan', 'yellow']
pos_bugs_in_image = {'red': 0, 'pink': 1, 'cyan': 2, 'yellow': 3}
bugs_image = load_image('bugs.png')
spawner_image = load_image('game_background.png')

coeffs_x = [i / 100 for i in
            range(50, 100)]  # Чтобы баги летели не только под углом 45 градусов, но и хотя бы как-то искривленно
coeffs_y = [i / 100 for i in range(50, 100)]
coefficients_of_colors_bug = {'red': 1.5, 'pink': 1.3, 'yellow': 1, 'cyan': 0.8}  # Коэффициенты багов
divider = 60  # Делитель, на который делится standart_score, при подсчете очков, добавленных за попавшего бага
limit_speed_bugs = {'red': 25, 'pink': 20, 'yellow': 15, 'cyan': 10}  # Это нужно для того, чтобы не было ошибок,
# связанных со слишком большими числами
price_bugs = {'red': 100, 'pink': 75, 'yellow': 50, 'cyan': 25}  # Кол-во очков, которое пойманный баг принесет, после


# умножится на коэфициент, полученный при делении standart_score на divider

# классы и функции
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
            sounds.play_shot()
            if arg.button == 1 and text_lmb_active or arg.button == 3 and text_rmb_active:
                self.alive_flag = False
                change_standart_speed(1)
        if self.count_of_collide_bug <= 0 and not self.run_away_flag:
            self.run_away_flag = True
            change_standart_speed(-1)
            change_count_lives(1)
            sounds.play_fall()
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
                    sounds.play_game_conflict()
                    self.vx = -self.vx
                    self.count_of_collide_bug -= 1
                if pygame.sprite.spritecollideany(self, horizontal_borders_group):
                    sounds.play_game_conflict()
                    self.vy = -self.vy
                    self.count_of_collide_bug -= 1
                if pygame.sprite.collide_mask(self, spawner):
                    sounds.play_game_conflict()
                    self.vy = -self.vy
                    self.count_of_collide_bug -= 1
            elif self.bug_at_the_spawn_point_flag:
                if pygame.sprite.spritecollideany(self, vertical_borders_group):
                    sounds.play_game_conflict()
                    self.vx = -self.vx
                if pygame.sprite.spritecollideany(self, horizontal_borders_group):
                    sounds.play_game_conflict()
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


def change_count_lives(number):
    global COUNT_LIVES
    COUNT_LIVES -= number


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
        self.image_cursor = load_image('cursor.png')
        self.image_paused_menu = load_image('paused_menu_cursor.png')
        self.image_paused_menu_2 = load_image('paused_menu_cursor_2.png')
        self.image = self.image_cursor
        self.rect = self.image.get_rect()
        self.flag_lmb = False
        self.flag_rmb = False
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, pos, flag_game_stop, lmb, rmb):
        self.flag_lmb = False
        self.flag_rmb = False
        if not flag_game_stop:
            self.image = self.image_cursor
        else:
            flag_over_loop = False
            for rect in [lmb, rmb]:
                if pygame.sprite.collide_mask(self, rect):
                    if rect.name == 'lmb':
                        self.flag_lmb = True
                    if rect.name == 'rmb':
                        self.flag_rmb = True
                    self.image = self.image_paused_menu_2
                    self.mask = pygame.mask.from_surface(self.image)
                    flag_over_loop = True
            if not flag_over_loop:
                self.image = self.image_paused_menu
                self.mask = pygame.mask.from_surface(self.image)
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


class Rectangle(pygame.sprite.Sprite):
    def __init__(self, x1, y1, image, name):
        super().__init__(rectangles_group, all_sprites)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x1
        self.rect.y = y1
        self.name = name


# объявление логики игры
all_sprites = pygame.sprite.Group()
bugs_group = pygame.sprite.Group()
horizontal_borders_group = pygame.sprite.Group()
vertical_borders_group = pygame.sprite.Group()
spawner_group = pygame.sprite.Group()
cursor_group = pygame.sprite.Group()
score_of_bug_group = pygame.sprite.Group()
rectangles_group = pygame.sprite.Group()

red_bugs_group = pygame.sprite.Group()
pink_bugs_group = pygame.sprite.Group()
cyan_bugs_group = pygame.sprite.Group()
yellow_bugs_group = pygame.sprite.Group()

cursor = Cursor()
spawner = Spawner()

color = (102, 0, 255)
color_score_bug_text = (250, 215, 0)
green = pygame.Color('green')
yellow = pygame.Color('yellow')
dark_green = (0, 71, 49)


def terminate():  # Выход из игры
    pygame.quit()
    exit()


def update_screen_pause_menu(screen, status_lmb, status_rmb):  # обновление экрана
    text_lmb = font_buttons.render(f'LMB: {dictionary_text_activites[status_lmb]}', True, yellow)
    text_rmb = font_buttons.render(f'RMB: {dictionary_text_activites[status_rmb]}', True, yellow)
    maxi_width = max(map(lambda z: z.get_width(), [text_lmb, text_rmb])) + w  # Чтобы было красиво,
    # прямоугольники все выравниваются под самый длинный прямоугольник

    rect_of_text_lmb = Rectangle(WIDTH // 2 - text.get_width() // 4 - length, height_lmb - length,
                                 pygame.Surface((maxi_width, text_lmb.get_height() + h)), 'lmb')
    rect_of_text_rmb = Rectangle(WIDTH // 2 - text.get_width() // 4 - length, height_rmb - length,
                                 pygame.Surface((maxi_width, text_rmb.get_height() + h)), 'rmb')

    pygame.draw.rect(screen, dark_green, rect_of_text_lmb)
    pygame.draw.rect(screen, dark_green, rect_of_text_rmb)

    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, height_pause))
    screen.blit(text_lmb, (WIDTH // 2 - text.get_width() // 4, height_lmb))
    screen.blit(text_rmb, (WIDTH // 2 - text.get_width() // 4, height_rmb))
    return screen


pygame.display.set_caption('BugsHunt')  # Сделать название окна 'BugsHunt'
pygame.display.set_icon(load_image('BugsHunt.ico'))  # Задать иконку для окна игры

font = pygame.font.Font(None, 100)
font_buttons = pygame.font.Font(None, 50)
font_score_bug = pygame.font.Font(None, 30)
text = font.render('Pause menu', True, green)

length = 5  # Величина, на которую сдигается прямоугольник с двух сторон
w = h = length * 2  # Ширина и высота прямоугольников
height_pause = 10
height_lmb = 150
height_rmb = 240
dictionary_text_activites = {True: 'On', False: 'Off'}

screen_fixed_elements = pygame.Surface(SIZE)  # Отдельное окно, на котором нарисуются неподвижные объекты 1 раз
screen_stop_game = load_image('pause_background.png')
Border(0, 0, WIDTH - 1, 0)
Border(0, HEIGHT - 1, WIDTH - 1, HEIGHT - 1)
Border(0, 0, 0, HEIGHT - 1)
Border(WIDTH - 1, 0, WIDTH - 1, HEIGHT - 1)
vertical_borders_group.draw(screen_fixed_elements)
horizontal_borders_group.draw(screen_fixed_elements)
spawner_group.draw(screen_fixed_elements)

text_lmb = font_buttons.render(f'LMB: {dictionary_text_activites[text_lmb_active]}', True, yellow)
text_rmb = font_buttons.render(f'RMB: {dictionary_text_activites[text_rmb_active]}', True, yellow)

maxi_width = max(map(lambda z: z.get_width(), [text_lmb, text_rmb])) + w  # Чтобы было красиво,
# прямоугольники все выравниваются под самый длинный прямоугольник

rect_of_text_lmb = Rectangle(WIDTH // 2 - text.get_width() // 4 - length, height_lmb - length,
                             pygame.Surface((maxi_width, text_lmb.get_height() + h)), 'lmb')
rect_of_text_rmb = Rectangle(WIDTH // 2 - text.get_width() // 4 - length, height_rmb - length,
                             pygame.Surface((maxi_width, text_rmb.get_height() + h)), 'rmb')

pygame.draw.rect(screen_stop_game, dark_green, rect_of_text_lmb)
pygame.draw.rect(screen_stop_game, dark_green, rect_of_text_rmb)

screen_stop_game.blit(text, (WIDTH // 2 - text.get_width() // 2, height_pause))
screen_stop_game.blit(text_lmb, (WIDTH // 2 - text.get_width() // 4, height_lmb))
screen_stop_game.blit(text_rmb, (WIDTH // 2 - text.get_width() // 4, height_rmb))
cursor.functions = {'lmb': text_lmb_active, 'rmb': text_rmb_active}

bugs = [RedBug, PinkBug, CyanBug, YellowBug]

stop_game_flag = False
flag_set_time_spawnbugevent = True
position_mouse = None

SPAWNBUGEVENT = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWNBUGEVENT, TIME)
sounds.play_music()
# основной цикл игры
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        if main_menu:
            pygame.mouse.set_visible(True)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.collidepoint(event.pos):
                    main_menu = False
        if not main_menu and not gameover:
            if position_mouse is None:
                position_mouse = pygame.mouse.get_pos()
            pygame.mouse.set_visible(False)  # Погашение системного курсора
            if event.type == SPAWNBUGEVENT:
                dx, dy = randint(x + 3, screen_game.get_width() - 35), randint(y + 3, screen_game.get_height() - 35)
                choice(bugs)(dx, dy)
            if event.type == pygame.MOUSEMOTION:
                position_mouse = event.pos
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    stop_game_flag = bool((int(stop_game_flag) + 1) % 2)
            if event.type == pygame.MOUSEBUTTONDOWN and stop_game_flag and any([cursor.flag_lmb, cursor.flag_rmb]):
                text_lmb_active = cursor.flag_lmb
                text_rmb_active = cursor.flag_rmb
                screen_stop_game = update_screen_pause_menu(screen_stop_game, cursor.flag_lmb, cursor.flag_rmb)
        if gameover:
            pygame.mouse.set_visible(True)
            standard_speed = 3
            position_mouse = None
            bugs_group = pygame.sprite.Group()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if main_menu_button.collidepoint(event.pos):
                    SCORE = 0
                    COUNT_LIVES = 8
                    main_menu = True
                    gameover = False
    if main_menu:
        screen_game.blit(menu_background_image, (0, 0))
        screen_game.blit(main_menu_score_font.render(f"TOP SCORE: {load_score()}", False, pygame.Color("green")),
                         (340, 475))
    if not main_menu and not gameover:
        screen_game.fill((0, 0, 0))
        screen_game.blit(screen_fixed_elements, (0, 0))
        pygame.draw.rect(screen_game, pygame.Color("black"), (20, 490, 150, 28))
        pygame.draw.rect(screen_game, pygame.Color((0, 255, 42)), (20, 490, 150, 28), 1)
        pygame.draw.rect(screen_game, pygame.Color("black"), (620, 490, 170, 28))
        pygame.draw.rect(screen_game, pygame.Color((0, 255, 42)), (620, 490, 170, 28), 1)
        screen_game.blit(main_menu_score_font.render(f"SCORE: {SCORE}", False, pygame.Color("green")), (22, 490))
        for lives in range(COUNT_LIVES):
            screen_game.blit(heart_image, (625 + 20 * lives, 495))
        for bug in bugs_group:
            now = bug.is_caught_bug()
            if now:  # Либо False, либо кортеж значений координат x, y и кол-во очков, что будет True
                x1, y1, points = now
                text1 = font_score_bug.render(f"+{points}", True, color_score_bug_text)
                ScoreBug(x1, y1, points, text1)
        bugs_group.draw(screen_game)
        score_of_bug_group.draw(screen_game)
        score_of_bug_group.update()
        if not stop_game_flag:
            if pygame.mouse.get_visible():
                pygame.mouse.set_visible(False)
            bugs_group.update(event)
            if not flag_set_time_spawnbugevent:
                pygame.time.set_timer(SPAWNBUGEVENT, TIME)
                flag_set_time_spawnbugevent = True
        else:
            screen_game.blit(screen_stop_game, (0, 0))
            if flag_set_time_spawnbugevent:
                pygame.time.set_timer(SPAWNBUGEVENT, 0)
                flag_set_time_spawnbugevent = False
        if pygame.mouse.get_focused() and position_mouse:  # Проверка на то, находится ли курсор мыши в экране игры
            cursor.update(position_mouse, stop_game_flag, rect_of_text_lmb, rect_of_text_rmb)
            cursor_group.draw(screen_game)
        if COUNT_LIVES <= 0:
            sounds.play_game_over()
            gameover = True
        pygame.display.flip()
        clock.tick(FPS)
    if gameover:
        top_score = load_score()
        screen_game.blit(gameover_background_image, (0, 0))
        screen_game.blit(game_over_big_font.render(f"SCORE: {SCORE}", False, pygame.Color("green")), (300, 300))
        screen_game.blit(game_over_big_font.render(f"TOP SCORE: {load_score()}", False, pygame.Color("green")),
                         (300, 340))
        if SCORE > top_score:
            save_score(SCORE)
    pygame.display.flip()
