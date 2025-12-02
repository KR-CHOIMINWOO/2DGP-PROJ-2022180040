from pico2d import *
import game_framework
import game_world
import play_mode
import random
import math

PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 20.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8


DEATH_IN_IMAGES = None

def load_death_in_images():
    global DEATH_IN_IMAGES
    if DEATH_IN_IMAGES is None:
        paths = [
            f'image_file/mob/boss/Death In/Death In_{i}.png'
            for i in (1, 2, 3)
        ]
        imgs = []
        for p in paths:
            try:
                imgs.append(load_image(p))
            except:
                print("image load fail:", p)
        DEATH_IN_IMAGES = imgs
    return DEATH_IN_IMAGES

class DeathInEffect:
    def __init__(self, x, y, damage=20):
        self.x = x
        self.y = y
        self.damage = damage

        self.images = load_death_in_images()
        self.frame = 0.0

        self.warn_time = 0.6
        self.active_time = 0.4
        self.timer = 0.0
        self.phase = 'warn'
        self.hit_done = False

        self.w = 140
        self.h = 140
