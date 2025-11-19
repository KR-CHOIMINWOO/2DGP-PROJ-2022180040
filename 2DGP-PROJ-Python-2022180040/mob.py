from pico2d import load_image, draw_rectangle
import game_framework
import play_mode
import game_world
import math
from mob_bullet import Bullet, DIR_RIGHT, DIR_LEFT, DIR_UP, DIR_DOWN

PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 20.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8


class Monster:
    def __init__(self, x, y, hp, speed, w, h,
                 img_path=None, sheet_cols=1,
                 frame_w=0, frame_h=0):
        self.x = x
        self.y = y
        self.image = None
        self.hp = hp
        self.speed = speed
        self.w = w
        self.h = h

        self.sheet_cols = sheet_cols
        self.frame = 0.0

        self.frame_w = frame_w
        self.frame_h = frame_h

        self.state = 'move'
        self.anim = {}
        self.set_anim('move', 0, sheet_cols)
        self.set_anim('hit', 0, sheet_cols)
        self.set_anim('die', 0, sheet_cols)
        self.set_anim('attack', 0, sheet_cols)

        self.frames = {
            'move': [],
            'hit': [],
            'die': [],
            'attack': []
        }

        self.atk = 5
        self.attack_cool = 0.0
        self.attack_interval = 1.0
        self.attack_range = 50.0

        self.attack_frame_time = 0.0
        self.attack_frame_duration = 0.4

        if img_path:
            try:
                self.image = load_image(img_path)
            except:
                print("image load fail:", img_path)
                self.image = None

    def set_anim(self, state, start, count):
        self.anim[state] = (start, count)

    def update(self):
        dt = game_framework.frame_time
        self.frame += FRAMES_PER_ACTION * ACTION_PER_TIME * dt

        self.attack_cool = max(0.0, self.attack_cool - dt)

        if self.attack_frame_time > 0.0:
            self.attack_frame_time -= dt
            if self.attack_frame_time <= 0.0 and self.state == 'attack':
                self.state = 'move'

        self.try_attack()


    def try_attack(self):
        pass

    def draw(self):
        ox, oy = play_mode.cam_ox, play_mode.cam_oy

        if self.image and self.sheet_cols > 0:
            start, count = self.anim.get(self.state, (0, self.sheet_cols))
            if count <= 0:
                draw_rectangle(
                    self.x - self.w // 2 + ox,
                    self.y - self.h // 2 + oy,
                    self.x + self.w // 2 + ox,
                    self.y + self.h // 2 + oy
                )
                return

            idx_in_state = int(self.frame) % count
            frame_index = (start + idx_in_state) % self.sheet_cols

            fw = self.frame_w if self.frame_w > 0 else self.image.w // self.sheet_cols
            fh = self.frame_h if self.frame_h > 0 else self.image.h

            sx = frame_index * fw
            sy = 0

            self.image.clip_draw(sx, sy, fw, fh,
                                 self.x + ox, self.y + oy, self.w, self.h)
        else:
            draw_rectangle(
                self.x - self.w // 2 + ox,
                self.y - self.h // 2 + oy,
                self.x + self.w // 2 + ox,
                self.y + self.h // 2 + oy
            )

    def get_bb(self):
        return (
            self.x - self.w // 2,
            self.y - self.h // 2,
            self.x + self.w // 2,
            self.y + self.h // 2
        )

    def is_in_world(self):
        for layer in game_world.world:
            if self in layer:
                return True
        return False

    def take_damage(self, amount):
        if self.hp <= 0:
            return

        self.hp -= amount
        print("Monster hit, hp =", self.hp)

        if self.hp <= 0:
            if self.is_in_world():
                game_world.remove_object(self)

    def handle_collision(self, group, other):
        pass


class DeathKnight(Monster):
    def __init__(self, x, y):
        super().__init__(
            x, y,
            hp=300,
            speed=RUN_SPEED_PPS * 0.7,
            w=80,
            h=120,
            img_path=None,
            sheet_cols=1
        )

        idle_paths = [
            f'image_file/mob/boss/Death Knight/Death Knight_{i}.png'
            for i in (1, 2, 3, 4)
        ]

        self.frames['idle'] = [self.safe_load(p) for p in idle_paths]
        self.state = 'idle'

    def safe_load(self, path):
        try:
            return load_image(path)
        except:
            print("image load fail:", path)
            return None

    def update(self):
        super().update()

    def draw(self):
        ox, oy = play_mode.cam_ox, play_mode.cam_oy
        imgs = self.frames.get(self.state, None)
        imgs = [img for img in imgs if img is not None] if imgs else None

        if imgs and len(imgs) > 0:
            idx = int(self.frame) % len(imgs)
            img = imgs[idx]
            img.draw(self.x + ox, self.y + oy, self.w, self.h)
        else:
            draw_rectangle(
                self.x - self.w // 2 + ox,
                self.y - self.h // 2 + oy,
                self.x + self.w // 2 + ox,
                self.y + self.h // 2 + oy
            )

    def get_bb(self):
        return (
            self.x - 60,
            self.y - 100,
            self.x + 20,
            self.y + 20
        )

    def handle_collision(self, group, other):
        super().handle_collision(group, other)


class Ghoul(Monster):
    def __init__(self, x, y):
        super().__init__(
            x, y,
            hp=40,
            speed=RUN_SPEED_PPS * 1.1,
            w=40,
            h=60,
            img_path=None,
            sheet_cols=1
        )

        move_paths = [
            f'image_file/mob/normal/Ghoul/07.Ghoul_{i}.png' for i in (1, 2, 3)
        ]
        hit_paths = [
            'image_file/mob/normal/Ghoul/07.Ghoul_4.png'
        ]
        die_paths = [
            'image_file/mob/normal/Ghoul/07.Ghoul_4.png'
        ]
        attack_paths = [
            f'image_file/mob/normal/Ghoul/07.Ghoul_{i}.png' for i in (5, 6, 7)
        ]

        self.frames['move'] = [self.safe_load(p) for p in move_paths]
        self.frames['hit'] = [self.safe_load(p) for p in hit_paths]
        self.frames['die'] = [self.safe_load(p) for p in die_paths]
        self.frames['attack'] = [self.safe_load(p) for p in attack_paths]

        self.state = 'move'

        self.atk = 5
        self.attack_interval = 1.0
        self.attack_range = 55.0
        self.attack_frame_duration = 0.4


    def safe_load(self, path):
        try:
            return load_image(path)
        except:
            print("image load fail:", path)
            return None

    def try_attack(self):
        tuar = getattr(play_mode, 'tuar', None)
        if not tuar:
            return

        dx = tuar.x - self.x
        dy = tuar.y - self.y
        dist2 = dx * dx + dy * dy

        if dist2 <= self.attack_range * self.attack_range and self.attack_cool <= 0.0:
            tuar.take_damage(self.atk)
            self.attack_cool = self.attack_interval
            self.state = 'attack'
            self.frame = 0.0
            self.attack_frame_time = self.attack_frame_duration

    def update(self):
        tuar = getattr(play_mode, 'tuar', None)
        dt = game_framework.frame_time

        if tuar:
            dx = tuar.x - self.x
            dy = tuar.y - self.y
            dist2 = dx * dx + dy * dy

            if dist2 > 1e-3:
                dist = math.sqrt(dist2)
                dir_x = dx / dist
                dir_y = dy / dist

                self.x += self.speed * dir_x * dt
                self.y += self.speed * dir_y * dt

        super().update()

    def draw(self):
        ox, oy = play_mode.cam_ox, play_mode.cam_oy
        imgs = self.frames.get(self.state, None)
        imgs = [img for img in imgs if img is not None] if imgs else None

        if imgs and len(imgs) > 0:
            idx = int(self.frame) % len(imgs)
            img = imgs[idx]
            img.draw(self.x + ox, self.y + oy, self.w, self.h)
        else:
            draw_rectangle(
                self.x - self.w // 2 + ox,
                self.y - self.h // 2 + oy,
                self.x + self.w // 2 + ox,
                self.y + self.h // 2 + oy
            )

    def get_bb(self):
        return (
            self.x - 30,
            self.y - 50,
            self.x + 10,
            self.y + 10
        )

    def handle_collision(self, group, other):
        super().handle_collision(group, other)


class Grave(Monster):
    def __init__(self, x, y):
        super().__init__(
            x, y,
            hp=80,
            speed=0.0,
            w=40,
            h=60,
            img_path=None,
            sheet_cols=1
        )

        move_paths = [
            f'image_file/mob/normal/Grave/07.Grave_{i}.png' for i in (1, 2, 3)
        ]
        hit_paths = [
            'image_file/mob/normal/Grave/07.Grave_4.png'
        ]
        die_paths = [
            'image_file/mob/normal/Grave/07.Grave_4.png'
        ]
        attack_paths = [
            f'image_file/mob/normal/Grave/07.Grave_{i}.png' for i in (5, 6, 7)
        ]

        self.frames['move'] = [self.safe_load(p) for p in move_paths]
        self.frames['hit'] = [self.safe_load(p) for p in hit_paths]
        self.frames['die'] = [self.safe_load(p) for p in die_paths]
        self.frames['attack'] = [self.safe_load(p) for p in attack_paths]

        self.state = 'move'

        self.atk = 7
        self.attack_interval = 1.5
        self.attack_range = 60.0
        self.attack_frame_duration = 0.4

    def safe_load(self, path):
        try:
            return load_image(path)
        except:
            print("image load fail:", path)
            return None

    def try_attack(self):
        tuar = getattr(play_mode, 'tuar', None)
        if not tuar:
            return

        dx = tuar.x - self.x
        dy = tuar.y - self.y
        dist2 = dx * dx + dy * dy

        if dist2 <= self.attack_range * self.attack_range and self.attack_cool <= 0.0:
            tuar.take_damage(self.atk)
            self.attack_cool = self.attack_interval
            self.state = 'attack'
            self.frame = 0.0
            self.attack_frame_time = self.attack_frame_duration


    def update(self):
        super().update()

    def draw(self):
        ox, oy = play_mode.cam_ox, play_mode.cam_oy
        imgs = self.frames.get(self.state, None)
        imgs = [img for img in imgs if img is not None] if imgs else None

        if imgs and len(imgs) > 0:
            idx = int(self.frame) % len(imgs)
            img = imgs[idx]
            img.draw(self.x + ox, self.y + oy, self.w, self.h)
        else:
            draw_rectangle(
                self.x - self.w // 2 + ox,
                self.y - self.h // 2 + oy,
                self.x + self.w // 2 + ox,
                self.y + self.h // 2 + oy
            )

    def get_bb(self):
        return (
            self.x - 30,
            self.y - 50,
            self.x + 10,
            self.y + 10
        )

    def handle_collision(self, group, other):
        super().handle_collision(group, other)


class Zombie(Monster):
    def __init__(self, x, y):
        super().__init__(
            x, y,
            hp=60,
            speed=0.0,
            w=40,
            h=60,
            img_path=None,
            sheet_cols=1
        )

        move_paths = [
            f'image_file/mob/normal/Zombi/07.Zombi_{i}.png' for i in (1, 2, 3)
        ]
        hit_paths = [
            'image_file/mob/normal/Zombi/07.Zombi_4.png'
        ]
        die_paths = [
            'image_file/mob/normal/Zombi/07.Zombi_4.png'
        ]
        attack_paths = [
            f'image_file/mob/normal/Zombi/07.Zombi_{i}.png' for i in (5, 6, 7)
        ]

        self.frames['move'] = [self.safe_load(p) for p in move_paths]
        self.frames['hit'] = [self.safe_load(p) for p in hit_paths]
        self.frames['die'] = [self.safe_load(p) for p in die_paths]
        self.frames['attack'] = [self.safe_load(p) for p in attack_paths]

        self.state = 'move'

        self.atk = 4
        self.attack_interval = 2.0
        self.attack_range = 400.0
        self.attack_frame_duration = 0.4

    def safe_load(self, path):
        try:
            return load_image(path)
        except:
            print("image load fail:", path)
            return None

    def update(self):
        super().update()

    def try_attack(self):
        tuar = getattr(play_mode, 'tuar', None)
        if not tuar:
            return

        dx = tuar.x - self.x
        dy = tuar.y - self.y
        dist2 = dx * dx + dy * dy

        if dist2 <= self.attack_range * self.attack_range and self.attack_cool <= 0.0:
            if abs(dx) > abs(dy):
                direction = DIR_RIGHT if dx > 0 else DIR_LEFT
            else:
                direction = DIR_UP if dy > 0 else DIR_DOWN

            b = Bullet(self.x, self.y, direction, owner=self)
            game_world.add_object(b, 2)
            game_world.add_collision_pair('bullet:tuar', b, tuar)

            self.attack_cool = self.attack_interval
            self.state = 'attack'
            self.frame = 0.0
            self.attack_frame_time = self.attack_frame_duration

    def draw(self):
        ox, oy = play_mode.cam_ox, play_mode.cam_oy
        imgs = self.frames.get(self.state, None)
        imgs = [img for img in imgs if img is not None] if imgs else None

        if imgs and len(imgs) > 0:
            idx = int(self.frame) % len(imgs)
            img = imgs[idx]
            img.draw(self.x + ox, self.y + oy, self.w, self.h)
        else:
            draw_rectangle(
                self.x - self.w // 2 + ox,
                self.y - self.h // 2 + oy,
                self.x + self.w // 2 + ox,
                self.y + self.h // 2 + oy
            )

    def get_bb(self):
        return (
            self.x - 30,
            self.y - 50,
            self.x + 10,
            self.y + 10
        )

    def handle_collision(self, group, other):
        super().handle_collision(group, other)
