from pico2d import load_image, draw_rectangle, get_canvas_width, get_canvas_height
import  game_framework
import game_world
import play_mode

class Monster:
    def __init__(self, x, y, hp, speed, w, h, img_path = None):
        self.x = x
        self.y = y
        self.image = None
        self.hp = hp
        self.speed = speed
        self.w = w
        self.h = h
        if img_path:
            try:
                self.image = load_image(img_path)
            except:
                self.image = None
        pass
    def update(self):
        pass
    def draw(self):
        pass
    def get_bb(self):
        pass
    def handle_collision(self, group, other):
        pass

class DeathKnight(Monster):
    def __init__(self):
        pass
    def update(self):
        pass
    def draw(self):
        pass
    def get_bb(self):
        pass
    def handle_collision(self, group, other):
        pass

class Ghoul(Monster):
    def __init__(self):
        pass
    def update(self):
        pass
    def draw(self):
        pass
    def get_bb(self):
        pass
    def handle_collision(self, group, other):
        pass

class Grave(Monster):
    def __init__(self):
        pass
    def update(self):
        pass
    def draw(self):
        pass
    def get_bb(self):
        pass
    def handle_collision(self, group, other):
        pass

class Zombie(Monster):
    def __init__(self):
        pass
    def update(self):
        pass
    def draw(self):
        pass
    def get_bb(self):
        pass
    def handle_collision(self, group, other):
        pass
