from pico2d import *


class Wall:
    def __init__(self, l, b, r, t):
        self.l, self.b, self.r, self.t = l, b, r, t
    def update(self): pass
    def draw(self):
        draw_rectangle(self.l, self.b, self.r, self.t)
    def get_bb(self):
        return (self.l, self.b, self.r, self.t)
    def handle_collision(self, group, other):
        pass
class Door:
    def __init__(self, l, b, r, t, name, on_enter):
        self.l, self.b, self.r, self.t = l, b, r, t
        self.name = name
        self.on_enter = on_enter
    def update(self): pass
    def draw(self):
        draw_rectangle(self.l, self.b, self.r, self.t)
        pass
    def get_bb(self):
        return (self.l, self.b, self.r, self.t)
    def handle_collision(self, group, other):
        if group == 'tuar:door':
            self.on_enter(self.name, other)

class Dungeon:
    def __init__(self):
        self.image = load_image('image_file/bag/game_bg++.png')
        self.w , self.h = 1024, 720
        self.x = self.w //2
        self.y = self.h //2
        self.play_x1, self.play_y1 = 130, 100
        self.play_x2, self.play_y2 = 900, 600

        top = (0, self.play_y2, self.w, self.h)
        left = (0, 0, self.play_x1, self.h)
        bottom = (0, 0, self.w, self.play_y1)
        right = (self.play_x2, 0, self.w, self.h)

        self.walls = [
            Wall(*top),
            Wall(*left),
            Wall(*bottom),
            Wall(*right),
        ]

        self.door_thick = 20  # 감지 폭
        self.door_lines = [
            # name, (ax, ay) ~ (bx, by)
            ('top',    450, 120, 580, 120),
            ('right',  880, 320, 880, 420),
            ('bottom', 450, 580, 580, 580),
            ('left',   150, 320, 150, 420),
        ]
        self.doors = []
        self._build_doors()

        self.room_id = 0

    def update(self):
        pass

    def draw(self):
        self.image.draw(self.x, self.y, self.w, self.h)
        for w in self.walls:
            w.draw()
    def get_bb(self):
        pass
    def handle_collision(self, group, other):
        if group == 'tuar:dungeon':
            pass

    def _build_doors(self):
        pad = self.door_thick // 2
        self.doors.clear()
        for name, ax, ay, bx, by in self.door_lines:
            if ay == by:
                x1, x2 = sorted([ax, bx])
                rect = (x1, ay - pad, x2, ay + pad)
            else:
                y1, y2 = sorted([ay, by])
                rect = (ax - pad, y1, ax + pad, y2)
            l, b, r, t = rect
            self.doors.append(Door(l, b, r, t, name, self._on_door_enter))

    def _on_door_enter(self, door_name, tuar):
        self.room_id += 1

        margin = 80
        cx = (self.play_x1 + self.play_x2) // 2
        cy = (self.play_y1 + self.play_y2) // 2
        if door_name == 'top':
            nx, ny = cx, self.play_y2 - margin
        elif door_name == 'bottom':
            nx, ny = cx, self.play_y1 + margin
        elif door_name == 'left':
            nx, ny = self.play_x2 - margin, cy
        elif door_name == 'right':
            nx, ny = self.play_x1 + margin, cy
        else:
            nx, ny = cx, cy

        tuar.x, tuar.y = nx, ny
        tuar.dir_x = 0
        tuar.dir_y = 0