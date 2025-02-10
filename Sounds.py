import pygame as pg
import pygame.mixer_music


class Sounds:
    def __init__(self):
        self.sound_gun = pg.mixer.Sound('./data/Gunshot.wav')
        self.sound_gun.set_volume(0.4)

        self.sound_fall = pg.mixer.Sound('./data/medlenno_punch.wav')
        self.sound_fall.set_volume(0.4)

        self.start_conflict = pg.mixer.Sound('./data/rebound.mp3')
        self.start_conflict.set_volume(0.4)

        self.game_over = pg.mixer.Sound('./data/game_over.mp3')
        self.game_over.set_volume(0.6)

        pg.mixer_music.load('./data/Bugs Hunt - Soundtrack (IVJN).wav')
        pg.mixer.music.set_volume(0.3)


    def play_shot(self):
        self.sound_gun.play()

    def play_music(self):
        pg.mixer.music.play(-1)

    def play_fall(self):
        self.sound_fall.play()

    def play_game_over(self):
        self.game_over.play()

    def play_game_conflict(self):
        self.start_conflict.play()