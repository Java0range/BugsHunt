import pygame as pg
import sys
from Sounds import Sounds

pg.init()
so = Sounds()
sc = pg.display.set_mode((400, 300))
so.play_music()

while 1:
    for i in pg.event.get():
        if i.type == pg.QUIT:
            sys.exit()

        elif i.type == pg.MOUSEBUTTONUP:
            if i.button == 1:
                so.play_game_conflict()

    pg.time.delay(20)
