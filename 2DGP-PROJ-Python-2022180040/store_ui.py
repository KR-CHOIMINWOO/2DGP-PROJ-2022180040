from pico2d import get_canvas_width, get_canvas_height, load_image, draw_rectangle
from gold import gold


class StoreUI:
    def __init__(self):
        self.open = False
        self.boss_cleared = False
        self.before_img = load_image('image_file/bag/store_inter01.png')
        self.after_img = load_image('image_file/bag/store_inter02.png')

        self.draw_x = 0
        self.draw_y = 0
        self.draw_w = 0
        self.draw_h = 0

        self.upgrade_rects = [
            (0.60, 0.65, 0.83, 0.72),
            (0.60, 0.50, 0.83, 0.57),
            (0.60, 0.37, 0.83, 0.44),
            (0.60, 0.23, 0.83, 0.30),
        ]

        self.special_rects = [
            (0.80, 0.50, 0.97, 0.72),
            (0.80, 0.22, 0.97, 0.44),
        ]

        self.upgrade_items = [
            {'cost': 50, 'hp_up': 20, 'bought': False},
            {'cost': 80, 'atk_up': 1, 'bought': False},
            {'cost': 80, 'aspd_up': 1, 'bought': False},
            {'cost': 80, 'skillspd_up': 1, 'bought': False},
        ]

        self.special_items = [
            {'cost': 150, 'bought': False},
            {'cost': 200, 'bought': False},
        ]

    def sync_boss_state(self):
        try:
            import play_mode
            self.boss_cleared = getattr(play_mode, 'boss_cleared', False)
        except:
            self.boss_cleared = False

    def toggle(self):
        if self.open:
            self.open = False
        else:
            self.sync_boss_state()
            self.open = True

    def draw(self):
        if not self.open:
            return
        cw, ch = get_canvas_width(), get_canvas_height()
        img = self.after_img if self.boss_cleared else self.before_img
        if not img:
            return
        iw, ih = img.w, img.h
        s = min(cw / iw, ch / ih)
        self.draw_w = int(iw * s)
        self.draw_h = int(ih * s)
        self.draw_x = cw // 2
        self.draw_y = ch // 2
        img.draw(self.draw_x, self.draw_y, self.draw_w, self.draw_h)

        left = self.draw_x - self.draw_w // 2
        bottom = self.draw_y - self.draw_h // 2
        for idx, (u1, b, u2, t) in enumerate(self.upgrade_rects):
            l = left + u1 * self.draw_w
            r = left + u2 * self.draw_w
            bb = bottom + b * self.draw_h
            tt = bottom + t * self.draw_h
            draw_rectangle(l, bb, r, tt)

        if self.boss_cleared:
            for idx, (u1, b, u2, t) in enumerate(self.special_rects):
                l = left + u1 * self.draw_w
                r = left + u2 * self.draw_w
                bb = bottom + b * self.draw_h
                tt = bottom + t * self.draw_h
                draw_rectangle(l, bb, r, tt)

    def screen_to_uv(self, sx, sy):
        if self.draw_w <= 0 or self.draw_h <= 0:
            return None
        left = self.draw_x - self.draw_w // 2
        bottom = self.draw_y - self.draw_h // 2
        if not (left <= sx <= left + self.draw_w and bottom <= sy <= bottom + self.draw_h):
            return None
        u = (sx - left) / self.draw_w
        v = (sy - bottom) / self.draw_h
        return u, v

    def handle_click(self, sx, sy):
        if not self.open:
            return

        print('StoreUI.handle_click screen:', sx, sy)

        ch = get_canvas_height()
        sy = ch - sy - 1
        print('StoreUI.handle_click flipped y:', sy)

        uv = self.screen_to_uv(sx, sy)
        if uv is None:
            print('StoreUI: click outside ui area')
            return
        u, v = uv
        print('StoreUI.handle_click uv:', u, v)

        for i, (u1, b, u2, t) in enumerate(self.upgrade_rects):
            if u1 <= u <= u2 and b <= v <= t:
                print('StoreUI: upgrade button', i, 'clicked')
                self.buy_upgrade(i)
                return

        if not self.boss_cleared:
            print('StoreUI: boss not cleared, special buttons locked')
            return

        for i, (u1, b, u2, t) in enumerate(self.special_rects):
            if u1 <= u <= u2 and b <= v <= t:
                print('StoreUI: special button', i, 'clicked')
                self.buy_special(i)
                return

    def buy_upgrade(self, idx):
        if idx < 0 or idx >= len(self.upgrade_items):
            return
        item = self.upgrade_items[idx]

        if not gold.pay(item['cost']):
            return

        try:
            import play_mode
            tuar = getattr(play_mode, 'tuar', None)
            if not tuar:
                return
            if idx == 0 and hasattr(tuar, 'max_hp') and hasattr(tuar, 'hp'):
                tuar.max_hp += item['hp_up']
                tuar.hp = tuar.max_hp
            elif idx == 1 and hasattr(tuar, 'atk'):
                tuar.atk += item['atk_up']
            elif idx == 2 and hasattr(tuar, 'atk_speed_level'):
                tuar.atk_speed_level += item['aspd_up']
            elif idx == 3 and hasattr(tuar, 'skill_speed_level'):
                tuar.skill_speed_level += item['skillspd_up']
        except:
            pass

    def buy_special(self, idx):
        if idx < 0 or idx >= len(self.special_items):
            return
        item = self.special_items[idx]
        if item['bought']:
            return
        if not gold.pay(item['cost']):
            return
        item['bought'] = True
        try:
            import play_mode
            if idx == 0:
                setattr(play_mode, 'awakening_unlocked', True)
            elif idx == 1:
                setattr(play_mode, 'death_hand_unlocked', True)
        except:
            pass

