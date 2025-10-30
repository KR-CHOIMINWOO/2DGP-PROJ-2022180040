from pico2d import load_image, get_time
from sdl2 import SDL_KEYDOWN, SDLK_SPACE, SDLK_RIGHT, SDL_KEYUP, SDLK_LEFT

import game_world
from state_machine import StateMachine


def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE

time_out = lambda e: e[0] == 'TIMEOUT'

def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT


def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT


def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT


def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT

class Idle:

    def __init__(self, tuar):
        self.tuar = tuar

    def enter(self, e):
        self.tuar.wait_time = get_time()
        self.tuar.dir = 0
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
            self.tuar.dir = self.tuar.face_dir = 1
        elif left_down(e) or right_up(e):
            self.tuar.dir = self.tuar.face_dir = -1

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
        current_time = get_time()
        elapsed = current_time - self.frame_time

        if elapsed > 0.1:
            self.tuar.frame = (self.tuar.frame + 1) % len(self.images)
            self.frame_time = current_time

        self.tuar.x += self.tuar.dir * 1

    def draw(self):
        image = self.images[self.tuar.frame]

        flip = 'h' if self.tuar.face_dir == -1 else ''
        image.composite_draw(0, flip, self.tuar.x, self.tuar.y, 150, 150)


class Tuar:
    def __init__(self):
        self.x, self.y = 50, 150
        self.frame = 0
        self.face_dir = 1
        self.dir = 0
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
                self.IDLE : {space_down: self.IDLE, right_down: self.RUN, left_down: self.RUN, right_up: self.RUN, left_up: self.RUN},
                self.RUN : {space_down: self.RUN, right_up: self.IDLE, left_up: self.IDLE, right_down: self.IDLE, left_down: self.IDLE}
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
