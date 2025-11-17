from pico2d import draw_rectangle, load_image
import game_framework
import game_world
import math

SLASH_SPEED_PPS   = 700.0
SLASH_RANGE       = 360.0
SLASH_W           = 50
SLASH_H           = 90
SLASH_IMG_PATH    = 'image_file/effect/s1_01.png'

DIR_RIGHT, DIR_LEFT, DIR_UP, DIR_DOWN = 'right', 'left', 'up', 'down'

class Slash:
    def __init__(self, x, y, direction: str):
        self.x, self.y = x, y
        self.direction = direction
        self.alive_dist = 0.0

        if direction == DIR_RIGHT:
            self.vx, self.vy = SLASH_SPEED_PPS, 0.0
            self.angle = 0.0
            self.flip = ''
        elif direction == DIR_LEFT:
            self.vx, self.vy = -SLASH_SPEED_PPS, 0.0
            self.angle = 0.0
            self.flip = 'h'
        elif direction == DIR_UP:
            self.vx, self.vy = 0.0, SLASH_SPEED_PPS
            self.angle = math.pi / 2
            self.flip = ''
        else:
            self.vx, self.vy = 0.0, -SLASH_SPEED_PPS
            self.angle = -math.pi / 2  #
            self.flip = ''

        try:
            self.image = load_image(SLASH_IMG_PATH)
        except:
            self.image = None
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
        if self.image:
            flip = 'h' if self.dir < 0 else ''
            self.image.composite_draw(0, flip, self.x, self.y, SLASH_W*1.2, SLASH_H*1.1)
        else:
            draw_rectangle(self.x - SLASH_W//2, self.y - SLASH_H//2,
                           self.x + SLASH_W//2, self.y + SLASH_H//2)
    def get_bb(self):
        return (self.x - SLASH_W // 2, self.y - SLASH_H // 2,
                self.x + SLASH_W // 2, self.y + SLASH_H // 2)

    def handle_collision(self, group, other):
        pass