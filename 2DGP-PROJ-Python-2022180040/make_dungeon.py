from pico2d import *

class Grass:
    def __init__(self):
        self.image = load_image('image_file/bag/game_bg++.png')
        self.w , self.h = 1024, 720
        self.x = self.w //2
        self.y = self.h //2
        self.play_x1, self.play_y1 = 130, 120
        self.play_x2, self.play_y2 = 900, 620

    def update(self):
        pass

    def draw(self):
        self.image.draw(self.x, self.y, self.w, self.h)
        draw_rectangle(self.play_x1, self.play_y1, self.play_x2, self.play_y2)
    def get_bb(self):
        return self.play_x1, self.play_y1, self.play_x2, self.play_y2
