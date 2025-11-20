from pico2d import load_image, draw_rectangle
import game_framework
import play_mode
import game_world
import math
import random
from mob import Monster

PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 10.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.9
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

class DeathKnight(Monster):
    def __init__(self, x, y):
        super().__init__(
            x, y,
            hp=5,
            speed=RUN_SPEED_PPS * 0.6,
            w=80,
            h=120,
            img_path=None,
            sheet_cols=1
        )

        self.frames = {
            'idle': [],
            'move': [],
            'attack': [],
            'revive': [],
            'teleport': [],
            'special': [],
            'die': []
        }

        idle_paths = [
            f'image_file/mob/boss/Death Knight/Death Knight_{i}.png'
            for i in (1, 2, 3, 4)
        ]

        attack_paths = [
            f'image_file/mob/boss/Death Knight Att/Death Knight Att_{i}.png'
            for i in (1, 2, 3, 4, 5, 6)
        ]

        die_paths = [
            f'image_file/mob/boss/Death Knight Revive/Death Knight Revive_{i}.png'
            for i in (1, 2, 3, 4, 5)
        ]

        revive_paths = [
            f'image_file/mob/boss/Death Knight Revive/Death Knight Revive_{i}.png'
            for i in (6, 7, 8, 9, 10)
        ]

        teleport_paths = [
            f'image_file/mob/boss/Death Knight BackRun/Death Knight BackRun_{i}.png'
            for i in (1, 2, 3, 4, 5)
        ]

        special_paths = [
            f'image_file/mob/boss/Death In/Death In_{i}.png'
            for i in (1, 2, 3)
        ]

        self.frames['idle']     = [self.safe_load(p) for p in idle_paths]
        self.frames['move']     = self.frames['idle']
        self.frames['attack']   = [self.safe_load(p) for p in attack_paths]
        self.frames['die']      = [self.safe_load(p) for p in die_paths]
        self.frames['revive']   = [self.safe_load(p) for p in revive_paths]
        self.frames['teleport'] = [self.safe_load(p) for p in teleport_paths]
        self.frames['special']  = [self.safe_load(p) for p in special_paths]

        self.state = 'idle'
        self.phase = 1
        self.max_hp_phase2 = 300

        self.atk = 20
        self.attack_interval = 1.2
        self.attack_range = 80.0
        self.attack_frame_duration = 0.5

        self.sequence = None

        self.special_orbs = []
        self.special_time = 0.0
        self.special_duration = 3.0
        self.special_radius = 500.0

        self.phase2_mode = 'idle'
        self.phase2_timer = 0.0
        self.phase2_dash_count = 0
        self.phase2_idle_interval = 1.0
        self.phase2_dash_speed = RUN_SPEED_PPS * 5.0
        self.phase2_max_dash = 3
        self.phase2_dash_hit = False

    def safe_load(self, path):
        try:
            return load_image(path)
        except:
            print("image load fail:", path)
            return None

    def start_phase_change(self):
        self.phase = 2
        self.hp = self.max_hp_phase2
        self.sequence = 'phase_change'
        self.state = 'die'
        self.frame = 0.0
        self.attack_cool = 9999.0
        self.attack_frame_time = 0.0
        self.special_orbs = []
        self.special_time = 0.0

    def take_damage(self, amount):
        if self.hp <= 0 and self.phase == 2:
            return
        if self.sequence is not None:
            return

        self.hp -= amount
        print("DeathKnight hit, hp =", self.hp)

        if self.phase == 1 and self.hp <= 0:
            self.start_phase_change()
            return

        if self.phase == 2 and self.hp <= 0:
            if self.is_in_world():
                game_world.remove_object(self)

    def init_special_orbs(self):
        self.special_orbs = []
        imgs = [img for img in self.frames['special'] if img is not None]
        if not imgs:
            return

        base_angles = [0.0, 2 * math.pi / 3.0, 4 * math.pi / 3.0]
        self.special_time = 0.0

        for i, a in enumerate(base_angles):
            self.special_orbs.append({
                'img': imgs[i % len(imgs)],
                'theta': a,
                'radius': self.special_radius
            })

    def try_attack(self):
        if self.sequence is not None:
            return

        if self.phase == 1:
            self.try_attack_phases1()

    def try_attack_phases1(self):
        tuar = getattr(play_mode, 'tuar', None)
        if not tuar:
            return

        dx = tuar.x - self.x
        dy = tuar.y - self.y
        dist2 = dx * dx + dy * dy

        if dist2 > self.attack_range * self.attack_range:
            dist = dist2 ** 0.5
            if dist > 0.0001:
                dir_x = dx / dist
                dir_y = dy / dist
                dt = game_framework.frame_time
                self.x += dir_x * self.speed * dt
                self.y += dir_y * self.speed * dt
            if self.state != 'attack':
                self.state = 'idle'
        else:
            if self.attack_cool <= 0.0:
                tuar.take_damage(self.atk)
                self.attack_cool = self.attack_interval
                self.state = 'attack'
                self.frame = 0.0
                self.attack_frame_time = self.attack_frame_duration

    def update(self):
        dt = game_framework.frame_time

        if self.sequence == 'phase_change':
            if self.state == 'die':
                self.frame += FRAMES_PER_ACTION * ACTION_PER_TIME * dt
                imgs = [img for img in self.frames['die'] if img is not None]
                if not imgs or int(self.frame) >= len(imgs):
                    self.state = 'special'
                    self.frame = 0.0
                    self.init_special_orbs()

            elif self.state == 'special':
                self.special_time += dt
                t = min(1.0, self.special_time / self.special_duration)
                for orb in self.special_orbs:
                    orb['theta'] += 2.0 * math.pi * 2.0 * dt
                    orb['radius'] = self.special_radius * (1.0 - t)
                if self.special_time >= self.special_duration:
                    self.state = 'revive'
                    self.frame = 0.0

            elif self.state == 'revive':
                self.frame += FRAMES_PER_ACTION * ACTION_PER_TIME * dt
                imgs = [img for img in self.frames['revive'] if img is not None]
                if not imgs or int(self.frame) >= len(imgs):
                    self.sequence = None
                    self.state = 'idle'
                    self.frame = 0.0
                    self.attack_cool = 0.5

            return

        if self.phase == 2:
            self.frame += FRAMES_PER_ACTION * ACTION_PER_TIME * dt

            if self.phase2_mode == 'idle':
                self.phase2_timer += dt
                if self.phase2_timer >= self.phase2_idle_interval:
                    self.phase2_timer = 0.0
                    self.phase2_dash_count = 0
                    self.phase2_mode = 'teleport'
                    self.state = 'teleport'
                    self.frame = 0.0
                return

            if self.phase2_mode == 'teleport':
                imgs = [img for img in self.frames['teleport'] if img is not None]
                if not imgs:
                    self.start_phase2_dash()
                    return

                if int(self.frame) >= len(imgs):
                    self.start_phase2_dash()
                return

            if self.phase2_mode == 'dash':
                dungeon = getattr(play_mode, 'dungeon', None)
                bottom_limit = dungeon.play_y1 - 100 if dungeon else self.y - 400

                self.y -= self.phase2_dash_speed * dt

                tuar = getattr(play_mode, 'tuar', None)
                if tuar and not self.phase2_dash_hit and self.check_hit_tuar(tuar):
                    tuar.take_damage(self.atk)
                    self.phase2_dash_hit = True

                if self.y < bottom_limit:
                    self.phase2_dash_count += 1
                    if self.phase2_dash_count >= self.phase2_max_dash:
                        self.phase2_mode = 'idle'
                        self.state = 'idle'
                        self.phase2_timer = 0.0
                    else:
                        self.phase2_mode = 'teleport'
                        self.state = 'teleport'
                        self.frame = 0.0

        super().update()

    def start_phase2_dash(self):
        dungeon = getattr(play_mode, 'dungeon', None)
        if dungeon:
            margin = 60
            x = random.randint(dungeon.play_x1 + margin, dungeon.play_x2 - margin)
            self.x = x
            self.y = dungeon.play_y2 + 150
        self.phase2_mode = 'dash'
        self.state = 'attack'
        self.frame = 0.0
        self.phase2_dash_hit = False

    def check_hit_tuar(self, tuar):
        la, ba, ra, ta = self.get_bb()
        lb, bb, rb, tb = tuar.get_bb()
        if la > rb or ra < lb or ba > tb or ta < bb:
            return False
        if getattr(tuar, 'roll_active', False):
            return False
        return True

    def draw(self):
        ox, oy = play_mode.cam_ox, play_mode.cam_oy

        if self.sequence == 'phase_change' and self.state == 'special' and self.special_orbs:
            for orb in self.special_orbs:
                img = orb['img']
                if img is None:
                    continue
                r = orb['radius']
                x = self.x + math.cos(orb['theta']) * r + ox
                y = self.y + math.sin(orb['theta']) * r + oy
                img.draw(x, y, 64, 64)
            return

        if self.phase == 2 and self.phase2_mode == 'dash':
            imgs = [img for img in self.frames['attack'] if img is not None]
            if imgs:
                last = imgs[-1]
                last.draw(self.x + ox, self.y + oy, self.w, self.h)
                return

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
