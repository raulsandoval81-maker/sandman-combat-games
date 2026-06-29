from game.collision import distance

NEUTRAL = "NEUTRAL"
CONTACT = "CONTACT"
COLLAR_TIE = "COLLAR_TIE"

CONTACT_DISTANCE = 95
BREAK_DISTANCE = 150
GRAPPLE_SPEED_LIMIT = 2


class GrappleState:
    def __init__(self):
        self.reset()

    def reset(self):
        self.state = NEUTRAL
        self.control = None
        self.message = "Neutral"

        # Required because ui.py still displays these
        self.green_control = 0
        self.red_control = 0

    def update(self, green, red):
        d = distance(green, red)

        if self.state == NEUTRAL:
            if d <= CONTACT_DISTANCE:
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

    def break_grapple(self):
        self.reset()
        self.message = "Break away"

    def is_grappling(self):
        return self.state in (CONTACT, COLLAR_TIE)

    def movement_speed(self):
        if self.is_grappling():
            return GRAPPLE_SPEED_LIMIT
        return None

    def start_pummel(self):
        self.message = "Pummel parked for later"

    def pummel_green(self):
        self.message = "Pummel parked for later"

    def pummel_red(self):
        self.message = "Pummel parked for later"


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