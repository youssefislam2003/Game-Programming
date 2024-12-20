import pygame as pg
import random as rnd 
import logging as lg
import os
lg.basicConfig(level=lg.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

pg.init()
pg.mixer.init()

WIN_W, WIN_H = 800, 800
FPS = 60
COLOR_BG, COLOR_BIRD, COLOR_PIPE, COLOR_TEXT, COLOR_BTN = (255, 255, 255), (255, 0, 0), (34, 139, 34), (0, 0, 0), (200, 200, 200)

gravity, bird_velocity = 0.5, 0 
bird_x, bird_y = 100, WIN_H // 2
bird_w, bird_h = 80, 80
pipes = [{'x': WIN_W, 'h': rnd.randint(300, 500), 'gap': 300}]
score, high_score, game_over= 0, 0, False

win = pg.display.set_mode((WIN_W, WIN_H))
pg.display.set_caption("Pharonic Flap")

SCRIPT_DIR = os.path.dirname(os.path.dirname(__file__))
ASSETS_DIR = os.path.join(SCRIPT_DIR, 'assets')
