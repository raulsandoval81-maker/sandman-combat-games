from game.collision import distance

NEUTRAL = "NEUTRAL"
CONTACT = "CONTACT"
COLLAR_TIE = "COLLAR_TIE"
TOP_BOTTOM = "TOP_BOTTOM"

CONTACT_DISTANCE = 95
BREAK_DISTANCE = 150
GRAPPLE_SPEED_LIMIT = 2
TURN_WINDOW_SECONDS = 10


class GrappleState:
    def __init__(self):
        self.reset()

    def reset(self):
        self.state = NEUTRAL
        self.control = None
        self.message = "Neutral"
        self.green_control = 0
        self.red_control = 0
        self.top_wrestler = None
        self.bottom_wrestler = None
        self.turn_timer = 0

    def update(self, green, red):
        if self.state == TOP_BOTTOM:
            return

        d = distance(green, red)

        if self.state == NEUTRAL and d <= CONTACT_DISTANCE:
            self.state = CONTACT
            self.control = None
            self.message = "Contact made"

        elif self.state in (CONTACT, COLLAR_TIE):
            maintain_tie_distance(green, red)

            if d >= BREAK_DISTANCE:
                self.reset()
                self.message = "Separated"

    def enter_collar_tie(self, wrestler):
        if self.state == CONTACT:
            self.state = COLLAR_TIE
            self.control = wrestler
            self.message = f"{wrestler.upper()} collar tie"

    def start_top_bottom(self, top_wrestler):
        self.state = TOP_BOTTOM
        self.top_wrestler = top_wrestler
        self.bottom_wrestler = "red" if top_wrestler == "green" else "green"
        self.turn_timer = TURN_WINDOW_SECONDS * 60
        self.message = f"{top_wrestler.upper()} on top — turn window!"

    def tick_turn_timer(self):
        if self.state == TOP_BOTTOM and self.turn_timer > 0:
            self.turn_timer -= 1
            if self.turn_timer <= 0:
                self.reset()
                self.message = "Turn window ended"

    def can_turn(self, wrestler):
        return self.state == TOP_BOTTOM and self.top_wrestler == wrestler and self.turn_timer > 0

    def break_grapple(self):
        self.reset()
        self.message = "Break away"

    def is_grappling(self):
        return self.state in (CONTACT, COLLAR_TIE, TOP_BOTTOM)

    def movement_speed(self):
        if self.state in (CONTACT, COLLAR_TIE):
            return GRAPPLE_SPEED_LIMIT
        return None


def maintain_tie_distance(green, red):
    d = distance(green, red)
    if d == 0:
        return

    if d < 70:
        push = (70 - d) * 0.08
    elif d > 105:
        push = -(d - 105) * 0.05
    else:
        return

    dx = (green.x - red.x) / d
    dy = (green.y - red.y) / d

    green.x += dx * push
    green.y += dy * push
    red.x -= dx * push
    red.y -= dy * push
