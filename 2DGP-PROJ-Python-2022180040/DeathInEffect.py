from pico2d import *
import game_framework
import game_world
import play_mode
import random
import math
from mob import Monster

PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 20.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 1.0
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8


DEATH_IN_IMAGES = None

def load_death_in_images():
    global DEATH_IN_IMAGES
    if DEATH_IN_IMAGES is None:
        paths = [
            f'image_file/mob/boss/Death In/Death In_{i}.png'
            for i in (1, 2, 3, 4, 5)
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
    def __init__(self, x, y, damage=20, target='player'):
        self.x = x
        self.y = y
        self.damage = damage
        self.target = target
        self.images = load_death_in_images()
        self.frame = 0.0

        self.warn_time = 0.6
        self.active_time = 0.4
        self.timer = 0.0
        self.phase = 'warn'
        self.hit_done = False

        self.w = 48
        self.h = 48

    def update(self):
        dt = game_framework.frame_time
        self.timer += dt
        self.frame += FRAMES_PER_ACTION * ACTION_PER_TIME * dt

        if self.phase == 'warn':
            if self.timer >= self.warn_time:
                self.phase = 'active'
                self.timer = 0.0
        elif self.phase == 'active':
            if self.target == 'player':
                tuar = getattr(play_mode, 'tuar', None)
                if tuar and not self.hit_done and not getattr(tuar, 'roll_active', False):
                    if self.check_hit_tuar(tuar):
                        tuar.take_damage(self.damage)
                        self.hit_done = True
            elif self.target == 'monster':
                if not self.hit_done:
                    for layer in game_world.world:
                        for obj in layer:
                            if isinstance(obj, Monster):
                                if self.check_hit_tuar(obj):
                                    if hasattr(obj, 'take_damage'):
                                        obj.take_damage(self.damage)
                                    self.hit_done = True
                                    break
                        if self.hit_done:
                            break

            if self.timer >= self.active_time:
                if self in sum(game_world.world, []):
                    game_world.remove_object(self)

    def check_hit_tuar(self, tuar):
        la, ba, ra, ta = self.get_bb()
        lb, bb, rb, tb = tuar.get_bb()
        if la > rb or ra < lb or ba > tb or ta < bb:
            return False
        return True

    def draw(self):
        ox, oy = play_mode.cam_ox, play_mode.cam_oy
        if not self.images:
            draw_rectangle(
                self.x - self.w // 2 + ox,
                self.y - self.h // 2 + oy,
                self.x + self.w // 2 + ox,
                self.y + self.h // 2 + oy
            )
            return

        if self.phase == 'warn':
            img = self.images[0]
        else:
            img = self.images[-1]

        img.draw(self.x + ox, self.y + oy, self.w, self.h)

    def get_bb(self):
        return (
            self.x - self.w // 2,
            self.y - self.h // 2,
            self.x + self.w // 2,
            self.y + self.h // 2
        )

    def handle_collision(self, group, other):
        pass