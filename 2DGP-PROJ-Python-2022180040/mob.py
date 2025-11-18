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
    def __init__(self, x, y, hp, speed, w, h, img_path=None, sheet_cols=1, sheet_rows=1):
        self.x = x
        self.y = y
        self.image = None
        self.hp = hp
        self.speed = speed
        self.w = w
        self.h = h

        self.sheet_cols = sheet_cols
        self.sheet_rows = sheet_rows
        self.frame = 0.0

        if img_path:
            try:
                self.image = load_image(img_path)
            except:
                self.image = None

    def update(self):
        dt = game_framework.frame_time
        self.frame += FRAMES_PER_ACTION * ACTION_PER_TIME * dt

    def draw(self):
        ox, oy = play_mode.cam_ox, play_mode.cam_oy

        if self.image and self.sheet_cols > 0 and self.sheet_rows > 0:
            total = self.sheet_cols * self.sheet_rows
            if total <= 0:
                draw_rectangle(self.x - self.w // 2 + ox, self.y - self.h // 2 + oy,
                               self.x + self.w // 2 + ox, self.y + self.h // 2 + oy)
                return

            idx = int(self.frame) % total
            col = idx % self.sheet_cols
            row = idx // self.sheet_cols

            frame_w = self.image.w // self.sheet_cols
            frame_h = self.image.h // self.sheet_rows
            sx = col * frame_w
            sy = row * frame_h

            self.image.clip_draw(sx, sy, frame_w, frame_h,
                                 self.x + ox, self.y + oy, self.w, self.h)
        else:
            draw_rectangle(self.x - self.w // 2 + ox, self.y - self.h // 2 + oy,
                           self.x + self.w // 2 + ox, self.y + self.h // 2 + oy)

    def get_bb(self):
        return (self.x - self.w // 2, self.y - self.h // 2,
                self.x + self.w // 2, self.y + self.h // 2)

    def handle_collision(self, group, other):
        pass


class DeathKnight(Monster):
    def __init__(self, x, y):
        super().__init__(
            x, y,
            hp=300,
            speed=80.0,
            w=140,
            h=160,
            img_path='image_file/mob/boss/Death Knight.png',
            sheet_cols=1,
            sheet_rows=1
        )
        self.spawn_x = x
        self.move_range = 150.0
        self.dir_x = -1.0

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


class Ghoul(Monster):
    def __init__(self, x, y):
        super().__init__(
            x, y,
            hp=40,
            speed=130.0,
            w=72,
            h=80,
            img_path='image_file/mob/07.Ghoul.png',
            sheet_cols=1,
            sheet_rows=1
        )
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
            sheet_cols=1,
            sheet_rows=1
        )

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
            sheet_cols=1,
            sheet_rows=1
        )

    def update(self):
        super().update()

    def draw(self):
        super().draw()

    def get_bb(self):
        return super().get_bb()

    def handle_collision(self, group, other):
        super().handle_collision(group, other)

