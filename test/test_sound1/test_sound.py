import pygame as pg
import sys

pg.init()
sc = pg.display.set_mode((400, 300))

sound1 = pg.mixer.Sound('Gunshot.wav')

while 1:
    for i in pg.event.get():
        if i.type == pg.QUIT:
            sys.exit()

        elif i.type == pg.MOUSEBUTTONUP:
            if i.button == 1:
                sound1.play()

    pg.time.delay(20)
