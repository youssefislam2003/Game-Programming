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
clk = pg.time.Clock()

SCRIPT_DIR = os.path.dirname(os.path.dirname(__file__))
ASSETS_DIR = os.path.join(SCRIPT_DIR, 'assets')

def loadIMG(name, size):
    path = os.path.join(ASSETS_DIR, name)

    if os.path.exists(path):
        image = pg.image.load(path)
        return pg.transform.scale(image, size)
    else:
        return None
    
def createPlaceholder(size, color):
        surface = pg.Surface(size)
        surface.fill(color)
        return surface 
    
bgIMG = loadIMG('bg.png', (WIN_W, WIN_H)) or createPlaceholder ((WIN_W, WIN_H), (135, 206, 235))
    
birdIMG = [loadIMG('bird.png', (bird_w, bird_h))]
    
if not birdIMG[0]:
    birdIMG = [createPlaceholder((bird_w, bird_h), COLOR_BIRD)]

pipeIMG = loadIMG('bird.png', (80,500)) or createPlaceholder((80, 500), COLOR_PIPE)
pipeImgFlipped = pg.transform.flip(pipeIMG, False, True)

try:
     flapSND= pg.mixer.Sound(os.path.join(ASSETS_DIR, 'flap.wav'))
     bgSND = pg.mixer.Sound(os.path.join(ASSETS_DIR, 'background_music.wav'))
     bgSND.set_volume(0.05)
     crashSND = pg.mixer.Sound(os.path.join(ASSETS_DIR, 'crash.wav'))
     bgSND.play(-1)

except Exception as e:
     flapSND = None
     bgSND = None 
     crashSND = None 

     current_bird = 0
     animation_speed = 0.2
     animation_time = 0

     def _updatee_bird(y, vel):
          vel += gravity
          y += vel
          lg.debug(f"Bird updated -> Y: {y},Velocity: {vel}")
          return y, vel
     
     def _update_bird_animation(dt):
          global animation_time, current_bird_frame
          animation_time += dt
          if animation_time >= animation_speed: animation_time = 0
          current_bird_frame = (current_bird_frame + 1) % len(birdIMG)

def _update_pipes(pipe_list, scr,pipe_speed, gap_size):
     for p in pipe_list:
          p['x'] -= pipe_speed
          if p['x'] < -80:
               p['x'] = WIN_W
               p['h'] = rnd.randint(200, 400)
               scr += 1
               lg.info(f"Score updated: {scr}")
     return pipe_list, scr 

def _draw_all():
     win.blit(bgIMG, (0, 0))

     bird_angle = max(-30, min(bird_velocity* 2, 30))
     rotated_bird = pg.transform.rotate(birdIMG[current_bird_frame], -bird_angle)
     bird_rect = rotated_bird.get_rect(center=(bird_x +bird_w//2, bird_y + bird_h//2))
     win.blit(rotated_bird, bird_rect.topleft)
     


