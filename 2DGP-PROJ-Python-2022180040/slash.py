from pico2d import draw_rectangle, load_image
import game_framework
import game_world

SLASH_SPEED_PPS   = 700.0
SLASH_RANGE       = 360.0
SLASH_W           = 50
SLASH_H           = 90
SLASH_IMG_PATH1    = 'image_file/effect/s1_01.png'
SLASH_IMG_PATH2    = 'image_file/effect/s1_02.png'

class Slash:
    def __init__(self, x, y, face_dir):
        self.x = x
        self.y = y
        self.dir = 1 if face_dir >= 0 else -1
        self.vx = self.dir * SLASH_SPEED_PPS
        self.vy = 0.0
        self.alive_dist = 0.0
        try:
            self.image = load_image(SLASH_IMG_PATH1 if self.dir > 0 else SLASH_IMG_PATH2)
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