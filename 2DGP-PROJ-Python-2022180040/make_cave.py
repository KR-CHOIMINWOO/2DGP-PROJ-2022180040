from pico2d import get_canvas_width, get_canvas_height, load_image
import game_framework
import play_mode


class CaveEntrance:
    def __init__(self):
        cw, ch = get_canvas_width(), get_canvas_height()
        self.w, self.h = 80, 180
        self.x = cw - 60
        self.y = ch // 2
        self.image = load_image('image_file/bag/cave.png')
        self.entered = False

    def update(self):
        pass

    def draw(self):
        if self.image:
            self.image.draw(self.x, self.y, self.w, self.h)

    def get_bb(self):
        return (self.x - self.w//2, self.y - self.h//2,
                self.x + self.w//2, self.y + self.h//2)

    def handle_collision(self, group, other):
        if group == 'tuar:cave' and not self.entered:
            self.entered = True
            game_framework.change_mode(play_mode)