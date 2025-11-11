from pico2d import *

class Dungeon:
    def __init__(self):
        self.image = load_image('image_file/bag/game_bg++.png')
        self.w , self.h = 1024, 720
        self.x = self.w //2
        self.y = self.h //2
        self.play_x1, self.play_y1 = 130, 100
        self.play_x2, self.play_y2 = 900, 600
        self.rect1 = (0, self.h, self.w, self.play_y2)
        self.rect2 = (0,0,self.play_x1, self.play_y2)
        self.rect3 = (0,0,self.w, self.play_y1)
        self.rect4 = (self.play_x2,0,self.w, self.h)

    def update(self):
        pass

    def draw(self):
        self.image.draw(self.x, self.y, self.w, self.h)
        draw_rectangle(*self.rect1)
        draw_rectangle(*self.rect2)
        draw_rectangle(*self.rect3)
        draw_rectangle(*self.rect4)
    def get_bb(self):
        return [self.rect1, self.rect2, self.rect3, self.rect4]
        pass
    def handle_collision(self, group, other):
        if group == 'tuar:dungeon':
            pass