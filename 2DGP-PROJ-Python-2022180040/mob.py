from pico2d import load_image, draw_rectangle
import game_framework
import play_mode

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
            self.x - 30,
            self.y - 50,
            self.x + 10,
            self.y + 10
        )

    def handle_collision(self, group, other):
        super().handle_collision(group, other)
