from pico2d import get_canvas_width, get_canvas_height, load_image

class StoreUI:
    def __init__(self):
        self.open = False
        self.boss_cleared = False
        self.before_img = load_image('image_file/bag/store_inter01.png')
        self.after_img = load_image('image_file/bag/store_inter02.png')

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
        if img:
            img.draw(cw // 2, ch // 2)
