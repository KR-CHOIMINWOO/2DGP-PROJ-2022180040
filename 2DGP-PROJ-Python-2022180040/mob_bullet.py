from pico2d import draw_rectangle, load_image
import game_framework
import game_world
import math

Bullet_SPEED_PPS   = 700.0
Bullet_RANGE       = 360.0
Bullet_W           = 20
Bullet_H           = 20

DIR_RIGHT, DIR_LEFT, DIR_UP, DIR_DOWN = 'right', 'left', 'up', 'down'

class Bullet:
    def __init__(self, x, y, direction: str, owner=None):
        self.x, self.y = x, y
        self.direction = direction
        self.alive_dist = 0.0

        base_atk = getattr(owner, 'atk', 1) if owner else 1
        mult = 2 if getattr(owner, 'special_active', False) else 1
        self.damage = base_atk * mult

        self.hit_targets = set()

        if direction == DIR_RIGHT:
            self.vx, self.vy = Bullet_SPEED_PPS, 0.0
            self.angle = 0.0
            self.flip = ''
        elif direction == DIR_LEFT:
            self.vx, self.vy = -Bullet_SPEED_PPS, 0.0
            self.angle = 0.0
            self.flip = 'h'
        elif direction == DIR_UP:
            self.vx, self.vy = 0.0, Bullet_SPEED_PPS
            self.angle = math.pi / 2
            self.flip = ''
        else:
            self.vx, self.vy = 0.0, -Bullet_SPEED_PPS
            self.angle = -math.pi / 2
            self.flip = ''

    def is_in_world(self):
        for layer in game_world.world:
            if self in layer:
                return True
        return False

    def update(self):
        dt = game_framework.frame_time
        dx = self.vx * dt
        dy = self.vy * dt
        self.x += dx
        self.y += dy
        self.alive_dist += (dx * dx + dy * dy) ** 0.5 + abs(dy)
        if self.alive_dist >= Bullet_RANGE:
            if self.is_in_world():
                game_world.remove_object(self)

    def draw(self):
        if self.image:
            self.image.composite_draw(self.angle, self.flip,
                                      self.x, self.y,
                                      Bullet_W * 1.2, Bullet_H * 1.1)
        else:
            draw_rectangle(self.x - Bullet_W // 2, self.y - Bullet_H // 2,
                           self.x + Bullet_W // 2, self.y + Bullet_H // 2)

    def get_bb(self):
        return (self.x - Bullet_W // 2, self.y - Bullet_H // 2,
                self.x + Bullet_W // 2, self.y + Bullet_H // 2)

    def handle_collision(self, group, other):
        if group == 'slash:monster':
            if other in self.hit_targets:
                return

            alive = getattr(other, 'hp', 1) > 0
            in_world = getattr(other, 'is_in_world', lambda: True)()

            if alive and in_world and hasattr(other, 'take_damage'):
                other.take_damage(self.damage)
                self.hit_targets.add(other)
                if self.is_in_world():
                    game_world.remove_object(self)