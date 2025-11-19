from pico2d import draw_circle
import game_framework
import game_world
import math

BULLET_SPEED_PPS = 500.0
BULLET_RANGE     = 600.0
BULLET_W         = 20
BULLET_H         = 20

DIR_RIGHT, DIR_LEFT, DIR_UP, DIR_DOWN = 'right', 'left', 'up', 'down'


class Bullet:
    def __init__(self, x, y, direction: str, owner=None):
        self.x, self.y = x, y
        self.direction = direction
        self.alive_dist = 0.0
        self.owner = owner

        self.damage = getattr(owner, 'atk', 1) if owner else 1

        if direction == DIR_RIGHT:
            self.vx, self.vy = BULLET_SPEED_PPS, 0.0
        elif direction == DIR_LEFT:
            self.vx, self.vy = -BULLET_SPEED_PPS, 0.0
        elif direction == DIR_UP:
            self.vx, self.vy = 0.0, BULLET_SPEED_PPS
        else:
            self.vx, self.vy = 0.0, -BULLET_SPEED_PPS

        self.hit_targets = set()

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
        self.alive_dist += (dx * dx + dy * dy) ** 0.5

        if self.alive_dist >= BULLET_RANGE:
            if self.is_in_world():
                game_world.remove_object(self)

    def draw(self):
        r = BULLET_W // 2
        draw_circle(self.x, self.y, r,0,255,0,255, filled=True)

    def get_bb(self):
        return (
            self.x - BULLET_W // 2,
            self.y - BULLET_H // 2,
            self.x + BULLET_W // 2,
            self.y + BULLET_H // 2
        )

    def handle_collision(self, group, other):
        if group == 'bullet:tuar':
            if not self.is_in_world():
                return

            if getattr(other, 'roll_active', False):
                return

            if other in self.hit_targets:
                return

            if hasattr(other, 'take_damage'):
                other.take_damage(self.damage)

            self.hit_targets.add(other)

            if self.is_in_world():
                game_world.remove_object(self)

