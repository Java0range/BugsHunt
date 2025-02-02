import pygame as pg


class Sounds:
    def __init__(self):
        self.sound_gun = pg.mixer.Sound('../../data/Gunshot.wav')
        self.sound_gun.set_volume(0.4)

        self.sound_fall = pg.mixer.Sound('../../data/medlenno_punch.wav')
        self.sound_fall.set_volume(0.4)

        self.start_game = pg.mixer.Sound('../../data/start_game.mp3')
        self.start_game.set_volume(0.4)

        self.start_conflict = pg.mixer.Sound('../../data/rebound.mp3')
        self.start_conflict.set_volume(0.4)

        self.points_score = pg.mixer.Sound('../../data/points_score.mp3')
        self.points_score.set_volume(0.4)

        self.game_over = pg.mixer.Sound('../../data/game_over.mp3')
        self.game_over.set_volume(0.4)

    def play_shot(self):
        self.sound_gun.play()

    def play_music(self):
        pass

    def play_fall(self):
        self.sound_fall.play()

    def play_start(self):
        self.start_game.play()

    def play_game_over(self):
        self.game_over.play()

    def play_points_score(self):
        self.points_score.play()

    def play_game_conflict(self):
        self.start_conflict.play()
