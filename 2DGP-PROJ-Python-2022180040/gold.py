class Gold:
    def __init__(self):
        self.amount = 0

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


gold = Gold()