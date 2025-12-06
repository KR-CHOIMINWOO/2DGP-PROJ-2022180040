from pico2d import get_canvas_width, get_canvas_height, load_image, draw_rectangle
import game_framework
import play_mode

class witch:
    def __init__(self):
        cw, ch = get_canvas_width(), get_canvas_height()
        self.w, self.h = 180, 180
        self.x = 150
        self.y = 160
        self.image = load_image('image_file/char/witch/witch01.png')
        self.entered = False
        self.overlap = False
        self._player = None

    def update(self):
        self.overlap = False

    def draw(self):
        if self.image:
            self.image.draw(self.x, self.y, self.w, self.h)
        draw_rectangle(* self.get_bb())

    def get_bb(self):
        return (self.x - self.w//2, self.y - self.h//2,
                self.x + self.w//2, self.y + self.h//2)

    def handle_collision(self, group, other):
         if group == 'tuar:store':
             self.overlap = True
             self._player = other

    def try_enter(self):
        if not self.entered:
            self.entered = True