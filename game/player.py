from game.settings import GREEN_START, RED_START


class Player:
    def __init__(self, name, start_pos):
        self.name = name
        self.start_x, self.start_y = start_pos
        self.reset()

    def reset(self):
        self.x = float(self.start_x)
        self.y = float(self.start_y)
        self.vx = 0.0
        self.vy = 0.0
        self.facing_x = 1.0 if self.name == "green" else -1.0
        self.facing_y = 0.0
        self.score = 0
        self.actions = 0
        self.cooldown = 0
        self.sprawl_timer = 0

    def set_move_intent(
        self,
        direction_x,
        direction_y,
        max_speed,
        acceleration=0.85,
        friction=0.72,
    ):
        """Apply smooth stance movement without changing wrestling rules."""
        magnitude = (direction_x * direction_x + direction_y * direction_y) ** 0.5

        if magnitude > 1.0:
            direction_x /= magnitude
            direction_y /= magnitude
            magnitude = 1.0

        if magnitude > 0.01 and max_speed > 0:
            target_vx = direction_x * max_speed
            target_vy = direction_y * max_speed
            self.vx += (target_vx - self.vx) * acceleration
            self.vy += (target_vy - self.vy) * acceleration

            self.facing_x = direction_x
            self.facing_y = direction_y
        else:
            self.vx *= friction
            self.vy *= friction

            if abs(self.vx) < 0.05:
                self.vx = 0.0
            if abs(self.vy) < 0.05:
                self.vy = 0.0

        self.x += self.vx
        self.y += self.vy

    def stop_motion(self):
        self.vx = 0.0
        self.vy = 0.0

    def tick(self):
        if self.cooldown > 0:
            self.cooldown -= 1
        if self.sprawl_timer > 0:
            self.sprawl_timer -= 1


def create_players():
    green = Player("green", GREEN_START)
    red = Player("red", RED_START)
    return green, red
