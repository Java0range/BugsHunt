import pygame
from Score import load_score, save_score
from Sounds import Sounds

# инициализация pygame
pygame.init()
screen = pygame.display.set_mode((800, 540))

# глобальные игровые переменные
running = True
main_menu = True

# инициализация игровых объектов
play_button = pygame.Rect(355, 290, 95, 48)

# фоны
background_image = pygame.image.load('./data/menu_background.png').convert()

# инициализация звуков
sounds = Sounds()

# шрифты
font = pygame.font.SysFont("Times New Roman", 20)

# основной цикл игры
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if main_menu:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.collidepoint(event.pos):
                    sounds.play_start()
                    print("Старт игры!")
                    main_menu = False
    screen.fill((255, 255, 255))
    if main_menu:
        screen.blit(background_image, (0, 0))
        screen.blit(font.render(f"TOP SCORE = {load_score()}", False, pygame.Color("green")), (320, 475))
    if not main_menu:
        screen.fill((255, 255, 255))
    pygame.display.flip()
pygame.quit()