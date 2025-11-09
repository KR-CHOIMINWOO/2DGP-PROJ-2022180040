from pico2d import load_image, get_time
from sdl2 import SDL_KEYDOWN, SDL_KEYUP, SDLK_SPACE, SDLK_RIGHT, SDLK_LEFT, SDLK_UP, SDLK_DOWN

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
        self.tuar.image.draw(self.tuar.x, self.tuar.y, 150, 150)


class Run:
    def __init__(self, tuar):
        self.tuar = tuar
        self.images = []
        self.frame_time = 0

    def enter(self, e):
        if right_down(e) or left_up(e):
            self.tuar.dir_x = self.tuar.face_dir = 1
        elif left_down(e) or right_up(e):
            self.tuar.dir_x = self.tuar.face_dir = -1

        if up_down(e) or down_up(e):
            self.tuar.dir_y = 1
        elif down_down(e) or up_up(e):
            self.tuar.dir_y = -1

        self.frame_time = get_time()

        if not self.images:
            for i in range(1, 4):
                filename =  f'image_file/char/tuar01/tuar_{i:02d}.png'
                self.images.append(load_image(filename))


    def exit(self, e):
        if space_down(e):
            pass
        pass

    def do(self):
        self.tuar.frame = (self.tuar.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4

        dx, dy = float(self.tuar.dir_x), float(self.tuar.dir_y)

        if dx > 0: self.tuar.face_dir = 1
        if dx < 0: self.tuar.face_dir = -1

        mag = (dx * dx + dy * dy) ** 0.5
        if mag > 0.0:
            nx, ny = dx / mag, dy / mag
            self.tuar.x += nx * RUN_SPEED_PPS * game_framework.frame_time
            self.tuar.y += ny * RUN_SPEED_PPS * game_framework.frame_time

    def draw(self):
        image = self.images[int(self.tuar.frame)]
        flip = 'h' if self.tuar.face_dir == -1 else ''
        image.composite_draw(0, flip, self.tuar.x, self.tuar.y, 150, 150)


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
        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.IDLE: {space_down: self.IDLE,
                            right_down: self.RUN, left_down: self.RUN,
                            up_down: self.RUN, down_down: self.RUN},
                self.RUN: {space_down: self.RUN,
                           right_down: self.RUN, left_down: self.RUN,
                           up_down: self.RUN, down_down: self.RUN,
                           right_up: self.RUN, left_up: self.RUN,
                           up_up: self.RUN, down_up: self.RUN}
            }
        )
        self.item = None

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_state_event(('INPUT', event))
        pass

    def draw(self):
        self.state_machine.draw()
