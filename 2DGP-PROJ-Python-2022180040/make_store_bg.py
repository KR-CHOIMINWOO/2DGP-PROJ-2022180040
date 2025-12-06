from pico2d import load_image


class Bg:
    def __init__(self):
        self.image = load_image('image_file/bag/store_room_in.png')

    def draw(self):
        self.image.draw(1024 / 2 - 20 , 720 / 2 + 60  , 1024, 1024)

    def update(self):
        pass
