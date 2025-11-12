from pico2d import load_image, get_time, draw_rectangle
from sdl2 import SDL_KEYDOWN, SDL_KEYUP, SDLK_SPACE, SDLK_w, SDLK_a, SDLK_s, SDLK_d, SDLK_LSHIFT, SDLK_j, SDLK_k

import game_framework
import game_world
import play_mode
from state_machine import StateMachine

def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE

time_out = lambda e: e[0] == 'TIMEOUT'

def right_down(e):  return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_d
def right_up(e):    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP   and e[1].key == SDLK_d

def left_down(e):   return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_a
def left_up(e):     return e[0] == 'INPUT' and e[1].type == SDL_KEYUP   and e[1].key == SDLK_a

def up_down(e):     return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_w
def up_up(e):       return e[0] == 'INPUT' and e[1].type == SDL_KEYUP   and e[1].key == SDLK_w

def down_down(e):   return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_s
def down_up(e):     return e[0] == 'INPUT' and e[1].type == SDL_KEYUP   and e[1].key == SDLK_s

def no_input(e): return e[0] == 'NO_INPUT'

def shift_down(e): return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LSHIFT

def attack_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_j

def special_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_k

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
ROLL_DISTANCE = 150.0

ATTACK_TIME = 0.30
ATTACK_COOLDOWN = 0.20

SPECIAL_DURATION = 15.0
SPECIAL_COOLDOWN = 20.0


class Idle:

    def __init__(self, tuar):
        self.tuar = tuar

    def enter(self, e):
        self.tuar.wait_time = get_time()
        self.tuar.dir_x = 0
        self.tuar.dir_y = 0
        self.tuar.image = self.tuar.cur_idle_img

    def exit(self, e):
        pass

    def do(self):
        pass

    def draw(self):
        if self.tuar.attack_active:
            self.tuar.draw_attack()
            return
        if self.tuar.roll_active:
            self.tuar.draw_roll()
            return
        flip = 'h' if self.tuar.face_dir == -1 else ''
        self.tuar.cur_idle_img.composite_draw(
            0, flip,
            self.tuar.x + play_mode.cam_ox,
            self.tuar.y + play_mode.cam_oy,
            100, 100
        )


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


    def exit(self, e):
        if space_down(e):
            pass
        pass

    def do(self):
        if self.tuar.roll_active:
            self.tuar.frame += FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time
            return

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
        if self.tuar.attack_active:
            self.tuar.draw_attack()
            return
        if self.tuar.roll_active:
            self.tuar.draw_roll()
            return
        if not self.tuar.roll_active and not self.tuar.attack_active:
            idx = int(self.tuar.frame) % len(self.tuar.cur_run_images)
            img = self.tuar.cur_run_images[idx]
            flip = 'h' if self.tuar.face_dir == -1 else ''
            img.composite_draw(0, flip,
            self.tuar.x + play_mode.cam_ox,
            self.tuar.y + play_mode.cam_oy,
            100, 100
        )


class Tuar:
    def __init__(self):
        self.x, self.y = 1024 / 2, 720 / 2
        self.frame = 0
        self.face_dir = 1
        self.dir_x = 0
        self.dir_y = 0
        self.hp = 100
        self.max_hp = 100

        self.bb = 100

        self.special_active = False
        self.special_t = 0.0
        self.special_cd = 0.0

        self.base_idle = load_image('image_file/char/tuar01/tuar_01.png')
        self.tf_idle = load_image('image_file/char/tuar04/tuar04_01.png')

        self.base_run = [load_image(f'image_file/char/tuar01/tuar_{i:02d}.png') for i in range(1, 5)]
        self.tf_run = [load_image(f'image_file/char/tuar04/tuar04_{i:02d}.png') for i in range(1, 5)]

        self.base_atk = [load_image(f'image_file/char/tuar01/tuar_{i:02d}.png') for i in range(5, 8)]
        self.tf_atk = [load_image(f'image_file/char/tuar04/tuar04_{i:02d}.png') for i in range(5, 8)]

        self.cur_idle_img = self.base_idle
        self.cur_run_images = self.base_run
        self.cur_attack_imgs = self.base_atk
        self.roll_image = self.base_idle

        self.roll_active = False
        self.roll_t = 0.0
        self.roll_vx, self.roll_vy = 0.0, 0.0
        self.roll_cd = 0.0

        self.attack_active = False
        self.attack_t = 0.0
        self.attack_cd = 0.0

        self.item = None

        self.IDLE = Idle(self)
        self.RUN = Run(self)
        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.IDLE: {
                    space_down: self.IDLE,
                    right_down: self.RUN, left_down: self.RUN,
                    up_down: self.RUN, down_down: self.RUN,
                    right_up: self.IDLE, left_up: self.IDLE,
                    up_up: self.IDLE, down_up: self.IDLE,
                },
                self.RUN: {
                    space_down: self.RUN,
                    right_down: self.RUN, left_down: self.RUN,
                    up_down: self.RUN, down_down: self.RUN,
                    right_up: self.RUN, left_up: self.RUN,
                    up_up: self.RUN, down_up: self.RUN,
                    no_input: self.IDLE,
                }
            }
        )

    def update(self):
        dt = game_framework.frame_time
        if self.special_cd > 0.0:
            self.special_cd = max(0.0, self.special_cd - dt)
        if self.special_active:
            self.special_t += dt
            if self.special_t >= SPECIAL_DURATION:
                self.special_active = False
                self.apply_skin(False)
                self.special_cd = SPECIAL_COOLDOWN

        if self.attack_cd > 0.0:
            self.attack_cd = max(0.0, self.attack_cd - game_framework.frame_time)

        if self.attack_active:
            dt = game_framework.frame_time
            self.attack_t += dt
            if self.attack_t >= ATTACK_TIME:
                self.attack_active = False
                self.attack_cd = ATTACK_COOLDOWN

        if self.roll_cd > 0.0:
            self.roll_cd = max(0.0, self.roll_cd - game_framework.frame_time)

        if self.roll_active:
            dt = game_framework.frame_time
            self.roll_t += dt
            self.x += self.roll_vx * ROLL_DISTANCE * ROLL_SPEED_SCALE * dt
            self.y += self.roll_vy * ROLL_DISTANCE * ROLL_SPEED_SCALE * dt
            if self.roll_t >= ROLL_TIME:
                self.roll_active = False
                self.roll_cd = ROLL_COOLDOWN
        self.state_machine.update()

    def handle_event(self, event):
        if special_down(('INPUT', event)):
            self.try_special()

        if attack_down(('INPUT', event)):
            self.try_attack()
            
        if shift_down(('INPUT', event)):
            self.try_roll()
        self.state_machine.handle_state_event(('INPUT', event))
        pass

    def get_bb(self):
        return self.x - 30, self.y - 50, self.x + 10, self.y + 10

    def handle_collision(self, group, other):
        if group == 'tuar:wall':
            la, ba, ra, ta = self.get_bb()
            lb, bb, rb, tb = other.get_bb()

            pen_x = min(ra - lb, rb - la)
            pen_y = min(ta - bb, tb - ba)

            if pen_x < pen_y:
                if ra - lb < rb - la:
                    self.x -= (ra - lb)
                else:
                    self.x += (rb - la)
            else:
                if ta - bb < tb - ba:
                    self.y -= (ta - bb)
                else:
                    self.y += (tb - ba)
        elif group == 'tuar:door':
            pass

    def draw(self):
        self.state_machine.draw()
        draw_rectangle(*self.get_bb())

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

    def try_attack(self):
        if self.attack_active or self.attack_cd > 0.0:
            return
        if self.roll_active or self.roll_cd > 0.0:
            return
        self.attack_active = True
        self.attack_t = 0.0

    def try_special(self):
        if self.special_active or self.special_cd > 0.0:
            return

        self.special_active = True
        self.special_t = 0.0
        self.apply_skin(True)
        self.special_t = 0.0

    def apply_skin(self, special: bool):
        self.special_active = special
        if special:
            self.cur_idle_img = self.tf_idle
            self.cur_run_images = self.tf_run
            self.cur_attack_imgs = self.tf_atk
            self.roll_image = self.tf_idle
        else:
            self.cur_idle_img = self.base_idle
            self.cur_run_images = self.base_run
            self.cur_attack_imgs = self.base_atk
            self.roll_image = self.base_idle

    def draw_attack(self):
        t = max(0.0, min(1.0, self.attack_t / ATTACK_TIME))
        idx = int(t * len(self.cur_attack_imgs))
        if idx >= len(self.cur_attack_imgs):
            idx = len(self.cur_attack_imgs) - 1
        img = self.cur_attack_imgs[idx]
        flip = 'h' if self.face_dir == -1 else ''
        img.composite_draw(0, flip, self.x, self.y, 100, 100)

    def draw_roll(self):
        img = self.roll_image
        sw, sh = img.w, img.h
        W, H = 100, 100

        feet_x = self.x
        feet_y = self.y - (H * 0.38)

        t = max(0.0, min(1.0, self.roll_t / ROLL_TIME))
        direction = 1.0 if self.face_dir > 0 else -1.0
        angle = -t * 2.0 * PI * direction

        img.clip_composite_draw(0, 0, sw, sh, angle, '', self.x, self.y - 20, W, H)
