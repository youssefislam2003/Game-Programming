import pygame as pg
import random as rnd 
import logging as lg
lg.basicConfig(level=lg.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

pg.init()
pg.mixer.init()

WIN_W, WIN_H = 800, 800
FPS = 60
COLOR_BG, COLOR_BIRD, COLOR_PIPE, COLOR_TEXT, COLOR_BTN = (255, 255, 255), (255, 0, 0), (34, 139, 34), (0, 0, 0), (200, 200, 200)

gravity, bird_velocity = 0.5, 0 
