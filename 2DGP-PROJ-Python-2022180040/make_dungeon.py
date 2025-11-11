from pico2d import *


class Wall:
    def __init__(self, l, b, r, t):
        self.l, self.b, self.r, self.t = l, b, r, t
    def update(self): pass
    def draw(self):
        draw_rectangle(self.l, self.b, self.r, self.t)
    def get_bb(self):
        return (self.l, self.b, self.r, self.t)
    def handle_collision(self, group, other):
        pass
class Door:
    def __init__(self, l, b, r, t):
        self.l, self.b, self.r, self.t = l, b, r, t
    def update(self): pass
    def draw(self):
        draw_rectangle(self.l, self.b, self.r, self.t)
    def get_bb(self):
        return (self.l, self.b, self.r, self.t)
    def handle_collision(self, group, other):
        pass

class Dungeon:
    def __init__(self):
        self.image = load_image('image_file/bag/game_bg++.png')
        self.w , self.h = 1024, 720
        self.x = self.w //2
        self.y = self.h //2
        self.play_x1, self.play_y1 = 130, 100
        self.play_x2, self.play_y2 = 900, 600
        top = (0, self.play_y2, self.w, self.h)
        left = (0, 0, self.play_x1, self.h)
        bottom = (0, 0, self.w, self.play_y1)
        right = (self.play_x2, 0, self.w, self.h)

        self.walls = [
            Wall(*top),
            Wall(*left),
            Wall(*bottom),
            Wall(*right),
        ]

    def update(self):
        pass

    def draw(self):
        self.image.draw(self.x, self.y, self.w, self.h)
        for w in self.walls:
            w.draw()
    def get_bb(self):
        pass
    def handle_collision(self, group, other):
        if group == 'tuar:dungeon':
            pass