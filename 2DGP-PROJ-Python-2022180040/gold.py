from pico2d import load_font

class Gold:
    def __init__(self):
        self.amount = 0
        self.font = None

    def reset(self):
        self.amount = 0

    def add(self, value):
        if value > 0:
            self.amount += value

    def can_afford(self, cost):
        return self.amount >= cost

    def pay(self, cost):
        if self.amount >= cost:
            self.amount -= cost
            return True
        return False

    def get(self):
        return self.amount

    def ensure_font(self, size=24, path='ENCR10B.TTF'):
        if self.font is None:
            self.font = load_font(path, size)

    def draw(self, x, y, color=(255, 255, 0)):
        self.ensure_font()
        self.font.draw(x, y, f'GOLD : {self.amount}', color)


gold = Gold()
