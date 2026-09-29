from game.collision import distance

NEUTRAL = "NEUTRAL"
CONTACT = "CONTACT"
COLLAR_TIE = "COLLAR_TIE"
SCRAMBLE = "SCRAMBLE"
TOP_BOTTOM = "TOP_BOTTOM"

CONTACT_DISTANCE = 95
BREAK_DISTANCE = 150
GRAPPLE_SPEED_LIMIT = 2
SCRAMBLE_SPEED_LIMIT = 1.25
SCRAMBLE_FRAMES = 20
SNAP_SHOT_FRAMES = 12
SNAP_SETUP_FRAMES = 90
TURN_WINDOW_SECONDS = 10
HAND_FIGHT_THRESHOLD = 3


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
        self.turn_used = False
        self.shot_attacker = None
        self.shot_defender = None
        self.scramble_timer = 0
        self.defender_sprawled = False
        self.pending_resolution = None
        self.snap_setup = None
        self.snap_timer = 0

    def update(self, green, red):
        if self.state == TOP_BOTTOM:
            return

        if self.state == SCRAMBLE:
            self._tick_scramble()
            return

        if self.snap_timer > 0:
            self.snap_timer -= 1
            if self.snap_timer == 0:
                self.snap_setup = None
                self.message = "Snap-down opening closed"

        d = distance(green, red)

        if self.state == NEUTRAL and d <= CONTACT_DISTANCE:
            self.state = CONTACT
            self.control = None
            self.message = "Hand fight range"

        elif self.state in (CONTACT, COLLAR_TIE):
            maintain_tie_distance(green, red)

            if d >= BREAK_DISTANCE:
                self.reset()
                self.message = "Separated"

    def hand_fight(self, wrestler):
        """Build inside-control pressure instead of granting a tie instantly."""
        if self.state not in (CONTACT, COLLAR_TIE):
            return False

        if wrestler not in ("green", "red"):
            return False

        opponent = "red" if wrestler == "green" else "green"
        own_attr = f"{wrestler}_control"
        opponent_attr = f"{opponent}_control"

        own_value = min(HAND_FIGHT_THRESHOLD, getattr(self, own_attr) + 1)
        opponent_value = max(0, getattr(self, opponent_attr) - 1)
        setattr(self, own_attr, own_value)
        setattr(self, opponent_attr, opponent_value)
        if self.snap_setup == opponent:
            self.snap_setup = None
            self.snap_timer = 0

        if own_value >= HAND_FIGHT_THRESHOLD:
            self.state = COLLAR_TIE
            self.control = wrestler
            self.message = f"{wrestler.upper()} wins inside control"
        else:
            if self.state == COLLAR_TIE and self.control == opponent:
                # A successful counter strips the old tie before new control is won.
                self.state = CONTACT
                self.control = None
            self.message = (
                f"{wrestler.upper()} hand fights "
                f"{own_value}/{HAND_FIGHT_THRESHOLD}"
            )
        return True

    def enter_collar_tie(self, wrestler):
        """Backward-compatible alias for the modern hand-fight action."""
        return self.hand_fight(wrestler)

    def control_progress(self, wrestler):
        if wrestler == "green":
            return self.green_control, HAND_FIGHT_THRESHOLD
        if wrestler == "red":
            return self.red_control, HAND_FIGHT_THRESHOLD
        return 0, HAND_FIGHT_THRESHOLD

    def snap_down(self, wrestler):
        """A controlled tie creates a short opening for a quicker shot."""
        if self.state != COLLAR_TIE or self.control != wrestler:
            return False
        self.snap_setup = wrestler
        self.snap_timer = SNAP_SETUP_FRAMES
        self.message = f"{wrestler.upper()} snaps down — shoot now!"
        return True

    def can_shoot(self, wrestler):
        if self.state == CONTACT:
            return True
        if self.state == COLLAR_TIE:
            return self.control in (None, wrestler)
        return False

    def start_shot(self, wrestler):
        if not self.can_shoot(wrestler):
            return False

        setup_shot = self.snap_setup == wrestler and self.snap_timer > 0
        self.state = SCRAMBLE
        self.shot_attacker = wrestler
        self.shot_defender = "red" if wrestler == "green" else "green"
        self.scramble_timer = SNAP_SHOT_FRAMES if setup_shot else SCRAMBLE_FRAMES
        self.snap_setup = None
        self.snap_timer = 0
        self.defender_sprawled = False
        self.pending_resolution = None
        self.control = wrestler
        self.message = (
            f"{wrestler.upper()} shoots off the snap — defend!"
            if setup_shot else f"{wrestler.upper()} attacks — defend!"
        )
        return True

    def attempt_sprawl(self, wrestler):
        if (
            self.state != SCRAMBLE
            or wrestler != self.shot_defender
            or self.scramble_timer <= 0
        ):
            return False

        self.defender_sprawled = True
        self.message = f"{wrestler.upper()} sprawls — scramble!"
        return True

    def _tick_scramble(self):
        if self.scramble_timer <= 0:
            return

        self.scramble_timer -= 1
        if self.scramble_timer > 0:
            return

        attacker = self.shot_attacker
        defender = self.shot_defender

        if self.defender_sprawled:
            self.state = CONTACT
            self.control = defender
            if defender == "green":
                self.green_control = min(HAND_FIGHT_THRESHOLD, self.green_control + 1)
                self.red_control = max(0, self.red_control - 1)
            else:
                self.red_control = min(HAND_FIGHT_THRESHOLD, self.red_control + 1)
                self.green_control = max(0, self.green_control - 1)
            self.message = f"{defender.upper()} stuffs the shot"
            self.pending_resolution = {
                "outcome": "sprawl",
                "attacker": attacker,
                "defender": defender,
            }
            self.shot_attacker = None
            self.shot_defender = None
            self.defender_sprawled = False
            return

        self.pending_resolution = {
            "outcome": "takedown",
            "attacker": attacker,
            "defender": defender,
        }
        self.start_top_bottom(attacker)

    def consume_resolution(self):
        resolution = self.pending_resolution
        self.pending_resolution = None
        return resolution

    def start_top_bottom(self, top_wrestler):
        self.state = TOP_BOTTOM
        self.top_wrestler = top_wrestler
        self.bottom_wrestler = "red" if top_wrestler == "green" else "green"
        self.turn_timer = TURN_WINDOW_SECONDS * 60
        self.turn_used = False
        self.shot_attacker = None
        self.shot_defender = None
        self.scramble_timer = 0
        self.defender_sprawled = False
        self.message = f"{top_wrestler.upper()} secures top control"

    def tick_turn_timer(self):
        if self.state == TOP_BOTTOM and self.turn_timer > 0:
            self.turn_timer -= 1
            if self.turn_timer <= 0:
                self.reset()
                self.message = "Turn window ended"

    def can_turn(self, wrestler):
        return (
            self.state == TOP_BOTTOM
            and self.top_wrestler == wrestler
            and self.turn_timer > 0
            and not self.turn_used
        )

    def record_turn(self, wrestler):
        """Consume the single scoring turn available in this top possession."""
        if not self.can_turn(wrestler):
            return False
        self.turn_used = True
        return True

    def break_grapple(self):
        self.reset()
        self.message = "Break away"

    def is_grappling(self):
        return self.state in (CONTACT, COLLAR_TIE, SCRAMBLE, TOP_BOTTOM)

    def movement_speed(self):
        if self.state in (CONTACT, COLLAR_TIE):
            return GRAPPLE_SPEED_LIMIT
        if self.state == SCRAMBLE:
            return SCRAMBLE_SPEED_LIMIT
        if self.state == TOP_BOTTOM:
            return 0
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
