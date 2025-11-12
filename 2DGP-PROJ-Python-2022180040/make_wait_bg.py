from pico2d import load_image


class Grass:
    def __init__(self):
        self.image = load_image('image_file/bag/wait_bg.png')

    def draw(self):
        self.image.draw(1024 / 2, 40, 1024, 80)

    def update(self):
        pass
