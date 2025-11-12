from pico2d import load_image


class Bg:
    def __init__(self):
        self.image = load_image('image_file/bag/wait_bg1.png')

    def draw(self):
        self.image.draw(1024 / 3, 720 / 2, 1024, 720)
        self.image.draw(1024 , 720 / 2, 1024, 720)

    def update(self):
        pass
