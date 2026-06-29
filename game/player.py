from game.settings import GREEN_START, RED_START

class Player:
    def __init__(self, name, start_pos):
        self.name = name
        self.start_x, self.start_y = start_pos
        self.reset()

    def reset(self):
        self.x = self.start_x
        self.y = self.start_y
        self.score = 0
        self.actions = 0
        self.cooldown = 0
        self.sprawl_timer = 0

    def tick(self):
        if self.cooldown > 0:
            self.cooldown -= 1
        if self.sprawl_timer > 0:
            self.sprawl_timer -= 1

def create_players():
    green = Player("green", GREEN_START)
    red = Player("red", RED_START)
    return green, red
