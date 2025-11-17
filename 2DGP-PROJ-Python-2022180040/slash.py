from pico2d import draw_rectangle, load_image
import game_framework
import game_world

SLASH_SPEED_PPS   = 700.0
SLASH_RANGE       = 360.0
SLASH_W           = 50
SLASH_H           = 90
SLASH_IMG_PATH    = 'image_file/effect/s1_01.png'

class Slash:
    def __init__(self, x, y, face_dir):
        self.x = x
        self.y = y
        self.dir = 1 if face_dir >= 0 else -1
        self.vx = self.dir * SLASH_SPEED_PPS
        self.vy = 0.0
        self.alive_dist = 0.0
        try:
            self.image = load_image(SLASH_IMG_PATH)
        except:
            self.image = None
        pass
    def update(self):
        dt = game_framework.frame_time
        dx = self.vx * dt
        dy = self.vy * dt
        self.x += dx
        self.y += dy
        self.alive_dist += (dx * dx + dy * dy) ** 0.5 + abs(dy)

        if self.alive_dist >= SLASH_RANGE:
            game_world.remove_object(self)
    def draw(self):
        pass
    def get_bb(self):
        return (self.x - SLASH_W // 2, self.y - SLASH_H // 2,
                self.x + SLASH_W // 2, self.y + SLASH_H // 2)

    def handle_collision(self, group, other):
        pass