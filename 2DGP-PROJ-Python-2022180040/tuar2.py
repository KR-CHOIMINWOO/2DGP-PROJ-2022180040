from pico2d import load_image, get_time
from sdl2 import SDL_KEYDOWN, SDL_KEYUP, SDLK_SPACE, SDLK_RIGHT, SDLK_LEFT, SDLK_UP, SDLK_DOWN, SDLK_LSHIFT

import game_framework
import game_world
from state_machine import StateMachine


def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE

time_out = lambda e: e[0] == 'TIMEOUT'

def right_down(e):  return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT
def right_up(e):    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP   and e[1].key == SDLK_RIGHT

def left_down(e):   return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT
def left_up(e):     return e[0] == 'INPUT' and e[1].type == SDL_KEYUP   and e[1].key == SDLK_LEFT

def up_down(e):     return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_UP
def up_up(e):       return e[0] == 'INPUT' and e[1].type == SDL_KEYUP   and e[1].key == SDLK_UP

def down_down(e):   return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_DOWN
def down_up(e):     return e[0] == 'INPUT' and e[1].type == SDL_KEYUP   and e[1].key == SDLK_DOWN

def no_input(e): return e[0] == 'NO_INPUT'

def shift_down(e): return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LSHIFT

# 용사의 Run Speed 계산

# 용사 Run Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 20.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# 용사 Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

PI = 3.141592
ROLL_TIME = 0.40
ROLL_SPEED_SCALE = 2.5
ROLL_COOLDOWN = 0.20

class Idle:

    def __init__(self, tuar):
        self.tuar = tuar

    def enter(self, e):
        self.tuar.wait_time = get_time()
        self.tuar.dir_x = 0
        self.tuar.dir_y = 0
        # 이미지 하나만 로드
        self.tuar.image = load_image('image_file/char/tuar01/tuar_01.png')

    def exit(self, e):
        pass

    def do(self):
        pass

    def draw(self):
        flip = 'h' if self.tuar.face_dir == -1 else ''
        self.tuar.image.composite_draw(0, flip, self.tuar.x, self.tuar.y, 100, 100)


class Run:
    def __init__(self, tuar):
        self.tuar = tuar
        self.images = []
        self.frame_time = 0
        self.run_images = []

    def enter(self, e):
        if right_down(e) or left_up(e):
            self.tuar.dir_x += 1
        elif left_down(e) or right_up(e):
            self.tuar.dir_x += -1

        if up_down(e) or down_up(e):
            self.tuar.dir_y += 1
        elif down_down(e) or up_up(e):
            self.tuar.dir_y += -1

        if right_down(e): self.tuar.face_dir = 1
        if left_down(e):  self.tuar.face_dir = -1
        self.frame_time = get_time()

        if not self.run_images:
            for i in range(1, 5):
                self.run_images.append(load_image(f'image_file/char/tuar01/tuar_{i:02d}.png'))


    def exit(self, e):
        if space_down(e):
            pass
        pass

    def do(self):
        self.tuar.frame += FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time

        dx, dy = self.tuar.dir_x, self.tuar.dir_y

        if dx > 0:
            self.tuar.face_dir = 1
        elif dx < 0:
            self.tuar.face_dir = -1

        self.tuar.x += dx * RUN_SPEED_PPS * game_framework.frame_time
        self.tuar.y += dy * RUN_SPEED_PPS * game_framework.frame_time

        if self.tuar.dir_x == 0 and self.tuar.dir_y == 0:
            self.tuar.state_machine.handle_state_event(('NO_INPUT', None))
            return

    def draw(self):
        idx = int(self.tuar.frame) % len(self.run_images)
        image = self.run_images[idx]
        flip = 'h' if self.tuar.face_dir == -1 else ''
        image.composite_draw(0, flip, self.tuar.x, self.tuar.y, 100, 100)

# class Roll:
#     def __init__(self, tuar):
#         self.tuar = tuar
#         self.elapsed = 0.0
#         self.vx = 0.0
#         self.vy = 0.0
#
#     def enter(self, e):
#         dx, dy = float(self.tuar.dir_x), float(self.tuar.dir_y)
#         if dx == 0.0 and dy == 0.0:
#             dx, dy = (1.0 if self.tuar.face_dir > 0 else -1.0), 0.0
#
#         mag = (dx*dx + dy*dy) ** 0.5
#         if mag > 0.0:
#             self.vx, self.vy = dx/mag, dy/mag
#         else:
#             self.vx, self.vy = 1.0, 0.0
#
#         self.elapsed = 0.0
#         if not hasattr(self.tuar, 'roll_image'):
#             self.tuar.roll_image = load_image('image_file/char/tuar01/tuar_01.png')
#
#     def exit(self, e):
#         pass
#
#     def do(self):
#         dt = game_framework.frame_time
#         self.elapsed += dt
#
#         self.tuar.x += self.vx * RUN_SPEED_PPS * ROLL_SPEED_SCALE * dt
#         self.tuar.y += self.vy * RUN_SPEED_PPS * ROLL_SPEED_SCALE * dt
#
#         if self.elapsed >= ROLL_TIME:
#             self.tuar.state_machine.handle_state_event(('TIMEOUT', None))
#
#     def draw(self):
#         t = max(0.0, min(1.0, self.elapsed / ROLL_TIME))
#         direction = 1.0 if self.tuar.face_dir > 0 else -1.0
#         angle = -t * 2.0 * PI * direction
#
#         w, h = self.tuar.roll_image.w, self.tuar.roll_image.h
#         self.tuar.roll_image.clip_composite_draw(0, 0, w, h, angle, '',
#                                                  self.tuar.x, self.tuar.y, 100, 100)


class Tuar:
    def __init__(self):
        self.x, self.y = 50, 150
        self.frame = 0
        self.face_dir = 1
        self.dir_x = 0
        self.dir_y = 0
        self.images = [
            load_image('image_file/char/tuar01/tuar_01.png'),
            load_image('image_file/char/tuar01/tuar_02.png'),
            load_image('image_file/char/tuar01/tuar_03.png'),
            load_image('image_file/char/tuar01/tuar_04.png'),
            load_image('image_file/char/tuar01/tuar_05.png'),
            load_image('image_file/char/tuar01/tuar_06.png'),
            load_image('image_file/char/tuar01/tuar_07.png'),
        ]

        self.IDLE = Idle(self)
        self.RUN = Run(self)
        # self.Roll = Roll(self)
        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.IDLE: {
                    space_down: self.IDLE,
                    right_down: self.RUN, left_down: self.RUN,
                    up_down: self.RUN, down_down: self.RUN,
                    right_up: self.IDLE, left_up: self.IDLE,
                    up_up: self.IDLE, down_up: self.IDLE,

                    # shift_down: self.Roll,
                },
                self.RUN: {
                    space_down: self.RUN,
                    right_down: self.RUN, left_down: self.RUN,
                    up_down: self.RUN, down_down: self.RUN,
                    right_up: self.RUN, left_up: self.RUN,
                    up_up: self.RUN, down_up: self.RUN,

                    no_input: self.IDLE,
                    # shift_down: self.Roll,
                },

                # self.Roll: {
                #     space_down: self.Roll,
                #     right_down: self.Roll, left_down: self.Roll,
                #     up_down: self.Roll, down_down: self.Roll,
                #     right_up: self.Roll, left_up: self.Roll,
                #     up_up: self.Roll, down_up: self.Roll,
                #
                #     time_out: self.IDLE,
                # }
            }
        )
        self.roll_active = False
        self.roll_t = 0.0
        self.roll_vx, self.roll_vy = 0.0, 0.0
        self.roll_cd = 0.0
        self.roll_image = load_image('image_file/char/tuar01/tuar_01.png')  # 1번 이미지

        self.item = None

    def update(self):
        if self.roll_cd > 0.0:
            self.roll_cd = max(0.0, self.roll_cd - game_framework.frame_time)

        if self.roll_active:
            dt = game_framework.frame_time
            self.roll_t += dt
            self.x += self.roll_vx * RUN_SPEED_PPS * ROLL_SPEED_SCALE * dt
            self.y += self.roll_vy * RUN_SPEED_PPS * ROLL_SPEED_SCALE * dt
            if self.roll_t >= ROLL_TIME:
                self.roll_active = False
                self.roll_cd = ROLL_COOLDOWN
        self.state_machine.update()

    def handle_event(self, event):
        if shift_down(('INPUT', event)):
            self.try_roll()
        self.state_machine.handle_state_event(('INPUT', event))
        pass

    def draw(self):
        self.state_machine.draw()

    def try_roll(self):
        if self.roll_active or self.roll_cd > 0.0:
            return

        dx, dy = float(self.dir_x), float(self.dir_y)

        if dy == 0.0:
            dy = 0.0

        if dx == 0.0 and dy == 0.0:
            dx, dy = (1.0 if self.face_dir > 0 else -1.0), 0.0

        mag = (dx * dx + dy * dy) ** 0.5
        if mag == 0.0:
            return
        self.roll_vx, self.roll_vy = dx / mag, dy / mag

        self.roll_active = True
        self.roll_t = 0.0
