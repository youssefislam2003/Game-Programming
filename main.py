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
     
     for pipe in pipes:
          scaled_pipe_top = pg.transform.scale(pipeImgFlipped, (80, pipe['x']))
          win.blit(scaled_pipe_top, (pipe['x'], 0))

          bottom_height = WIN_H - pipe['h'] - pipe['gap']
          scaled_pipe_bottom = pg.tranform.scale(pipeIMG, (80, bottom_height))
          win.blit(scaled_pipe_bottom, (pipe['x'], pipe['h'] + pipe['gap']))
          
txt_font = pg.font.Font(None, 36) 
score_text = txt_font.render(f"Score: {score} High Score: {high_score}", True, COLOR_TEXT)
win.blit(score_text, (10,10))
pg.display.flip()

def _draw_game_over():
     win.blit(bgIMG, (0, 0))
     txt_font = pg.font.Font(None, 72)
     game_over_text = txt_font.render("GAME OVER", True, COLOR_TEXT)
     win.blit(game_over_text, (WIN_W // 2 - game_over_text.get_width() // 2, WIN_H // 3))
     score_text = txt_font.render(f"Score: {score}", True, COLOR_TEXT)
     win.blit(score_text, (WIN_W // 2 - score_text.get_width() // 2, WIN_H // 2))

     btn_font = pg.font.Font(None, 48)
     btn_text = btn_font.render("Restart", True, COLOR_TEXT)
     btn_x, btn_y, btn_w, btn_h = WIN_W // 2 - 100, WIN_H // 2 + 100, 200, 50
     pg.draw.rect(win, COLOR_BTN, (btn_x, btn_y, btn_w, btn_h))
     win.blit(btn_text, (btn_x + btn_w // 2 - btn_text.get_width() // 2, btn_y + btn_h // 2 - btn_text.get_height() // 2))
     pg.display.flip()

     return btn_x, btn_y, btn_w, btn_h

def reset_game(): 
     global bird_y, bird_velocity, pipes, score,game_over, animation_time, current_bird_frame
     bird_y, bird_velocity  = WIN_H // 2, 0
     pipes = [{'x': WIN_W, 'h': rnd.randiant (300,500), 'gap':300}]
     score, game_over = 0, False 
     animation_time, current_bird_frame = 0,0
def calculate_difficulty(score):
     level = min(score, 50)
     gap_size = 300 - (level * 4)
     gap_size= max (gap_size, 100)
     pipe_speed = 5 + ( level * 0.1)
     pipe_speed = min (pipe_speed, 10)
     return gap_size, pipe_speed

def main_game():
     global bird_y, bird_velocity, pipes, score, high_score, game_over
     last_time = pg.time.pygame.time.get_ticks()
     
     while True:
          while not game_over:
               current_time = pg.time.get_ticks()
               dt = (current_time - last_time) / 1000.0
               last_time = current_time

               for ev in pg.event.get():
                    if ev.type == pg.quit
                       lg.info("Game exited by user.")
                       pg.quit()
                       exit()

                    if ev.type == pg.KEYDOWN and ev.key == pg.K_space:
                         bird_velocity = -10
                         lg.debug("Bird flapped.")
                         if flapSND: #Flap Sound
                         flapSND.play()
                         lg.debug("Bird flapped.")

           # Adjust difficulity based on score
           gap_size, pipe_speed = calculate_difficulty(score)

           bird_y, bird_velocity = _update_bird(bird_y,bird_velocity)
           _update_bird_animation(dt)
           pipes, score = _update_pipes(pipes, score, pipe_speed,gap_size)

           # Update pipes with new gap size
            for p in pipes:
               p['gap'] = gap_size

          #Check for collisons
           for p in pipes:
               if(bird_x < p['x'] + 80 and bird_x + bird_w > p['x'] and
               not (p['h'] < bird_y < p['h'] + p['gap'])) or bird_y + bird_h > WIN_H or bird_y < 0:
          if crashSND: #Crash Sound
          crashSND.play()
          game_over = True
          high_score = max(high_score, score)  
          lg.error("Collison detected, Game Over!")

          _draw_all()
          clk.tick(FPS)

          #Game Over Logic
          btn_x, btn_y, btn_w, btn_h = _draw_game_over()
           for ev in pg.event.get():
               if ev.type = pg.Quit:
                    lg.info("Game exited by user.")
                    pg.quit()
                    exit()
               if ev.type == pg.MOUSEBUTTONDOWN:
                    mx, my = pg.mouse.pygame.mouse.get_pos()
               if btn_x <= mx <= btn_x + btn_w and btn_y <



