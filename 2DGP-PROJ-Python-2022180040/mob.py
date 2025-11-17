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
    def update(self):
        pass
    def draw(self):
        ox, oy = play_mode.cam_ox, play_mode.cam_oy
        if self.image:
            self.image.draw(self.x + ox, self.y + oy, self.w, self.h)
        else:
            draw_rectangle(self.x - self.w//2 + ox, self.y - self.h//2 + oy,
                           self.x + self.w//2 + ox, self.y + self.h//2 + oy)
    def get_bb(self):
        return (self.x - self.w//2 , self.y - self.h//2 ,
                           self.x + self.w//2 , self.y + self.h//2 )
    def handle_collision(self, group, other):
        pass

class DeathKnight(Monster):
    def __init__(self, x, y):
        super().__init__(
            x,y, hp = 300, speed = 80.0, w = 140, h = 160, img_path = 'image_file/mob/boss/Death Knight.png'
        )
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
    def __init__(self, x, y):
        super().__init__(
            x, y,
            hp=40,
            speed=130.0,
            w=72,
            h=80,
            img_path='image_file/mob/07.Ghoul.png',
        )
    def update(self):
        pass
    def draw(self):
        pass
    def get_bb(self):
        pass
    def handle_collision(self, group, other):
        pass

class Grave(Monster):
    def __init__(self, x, y):
        super().__init__(
            x, y,
            hp=80,
            speed=0.0,
            w=82,
            h=80,
            img_path='image_file/mob/07.Grave.png',
        )
    def update(self):
        pass
    def draw(self):
        pass
    def get_bb(self):
        pass
    def handle_collision(self, group, other):
        pass

class Zombie(Monster):
    def __init__(self, x, y):
        super().__init__(
            x, y,
            hp=60,
            speed=0.0,
            w=82,
            h=80,
            img_path='image_file/mob/07.Zombie.png',
        )
    def update(self):
        pass
    def draw(self):
        pass
    def get_bb(self):
        pass
    def handle_collision(self, group, other):
        pass
