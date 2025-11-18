from pico2d import load_image, draw_rectangle, get_canvas_width, get_canvas_height
import game_framework
import game_world
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
    def __init__(self, x, y, hp, speed, w, h, img_path=None, sheet_cols=1):
        self.x = x
        self.y = y
        self.image = None
        self.hp = hp
        self.speed = speed
        self.w = w
        self.h = h

        self.sheet_cols = sheet_cols
        self.frame = 0.0

        self.state = 'move'
        self.anim = {}
        self.set_anim('move', 0, sheet_cols)
        self.set_anim('attack', 0, sheet_cols)
        self.set_anim('hit', 0, sheet_cols)
        self.set_anim('die', 0, sheet_cols)

        if img_path:
            try:
                self.image = load_image(img_path)
            except:
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

            frame_w = self.image.w // self.sheet_cols
            frame_h = self.image.h
            sx = frame_index * frame_w
            sy = 0

            self.image.clip_draw(sx, sy, frame_w, frame_h,
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
            w=140,
            h=160,
            img_path=None,
            sheet_cols=1
        )
        self.state = 'idle'
        self.images = {}
        self.sheet_cols_map = {}

        self.add_anim_sheet('idle', 'image_file/mob/boss/Death Knight.png', 8)

        self.spawn_x = x
        self.move_range = 150.0
        self.dir_x = -1.0

    def add_anim_sheet(self, state, path, cols):
        try:
            img = load_image(path)
            self.images[state] = img
            self.sheet_cols_map[state] = cols
        except:
            pass

    def update(self):
        super().update()
        dt = game_framework.frame_time
        self.x += self.dir_x * self.speed * dt

        if self.x > self.spawn_x + self.move_range:
            self.dir_x = -1.0
        elif self.x < self.spawn_x - self.move_range:
            self.dir_x = 1.0

    def draw(self):
        ox, oy = play_mode.cam_ox, play_mode.cam_oy
        img = self.images.get(self.state, None)
        cols = self.sheet_cols_map.get(self.state, 0)

        if img and cols > 0:
            idx = int(self.frame) % cols
            frame_w = img.w // cols
            frame_h = img.h
            sx = idx * frame_w
            sy = 0
            img.clip_draw(sx, sy, frame_w, frame_h,
                          self.x + ox, self.y + oy, self.w, self.h)
        else:
            draw_rectangle(
                self.x - self.w // 2 + ox,
                self.y - self.h // 2 + oy,
                self.x + self.w // 2 + ox,
                self.y + self.h // 2 + oy
            )

    def get_bb(self):
        return super().get_bb()

    def handle_collision(self, group, other):
        super().handle_collision(group, other)


class Ghoul(Monster):
    def __init__(self, x, y):
        super().__init__(
            x, y,
            hp=40,
            speed=RUN_SPEED_PPS * 1.1,
            w=72,
            h=80,
            img_path='image_file/mob/07.Ghoul.png',
            sheet_cols=7
        )
        self.set_anim('move', 0, 3)
        self.set_anim('hit', 3, 1)
        self.set_anim('die', 3, 1)
        self.set_anim('attack', 4, 3)

        self.spawn_x = x
        self.move_range = 200.0
        self.dir_x = 1.0

    def update(self):
        super().update()
        dt = game_framework.frame_time
        self.x += self.dir_x * self.speed * dt

        if self.x > self.spawn_x + self.move_range:
            self.dir_x = -1.0
        elif self.x < self.spawn_x - self.move_range:
            self.dir_x = 1.0

    def draw(self):
        super().draw()

    def get_bb(self):
        return super().get_bb()

    def handle_collision(self, group, other):
        super().handle_collision(group, other)


class Grave(Monster):
    def __init__(self, x, y):
        super().__init__(
            x, y,
            hp=80,
            speed=0.0,
            w=82,
            h=80,
            img_path='image_file/mob/07.Grave.png',
            sheet_cols=7
        )
        self.set_anim('move', 0, 3)
        self.set_anim('hit', 3, 1)
        self.set_anim('die', 3, 1)
        self.set_anim('attack', 4, 3)

    def update(self):
        super().update()

    def draw(self):
        super().draw()

    def get_bb(self):
        return super().get_bb()

    def handle_collision(self, group, other):
        super().handle_collision(group, other)


class Zombie(Monster):
    def __init__(self, x, y):
        super().__init__(
            x, y,
            hp=60,
            speed=0.0,
            w=82,
            h=80,
            img_path='image_file/mob/07.Zombie.png',
            sheet_cols=7
        )
        self.set_anim('move', 0, 3)
        self.set_anim('hit', 3, 1)
        self.set_anim('die', 3, 1)
        self.set_anim('attack', 4, 3)

    def update(self):
        super().update()

    def draw(self):
        super().draw()

    def get_bb(self):
        return super().get_bb()

    def handle_collision(self, group, other):
        super().handle_collision(group, other)
